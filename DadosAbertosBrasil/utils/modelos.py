"""Modelos Pydantic de entrada e saída das APIs.

Entrada estrita, saída tolerante:

- `Params`: traduz os argumentos das funções (nomes em português) para os
  parâmetros da API. Valores inválidos levantam erro, porque o erro é do
  usuário.
- `Registro`: lê um registro da resposta da API, com os nomes da API como
  aliases e os nomes do pacote como campos. Campos novos na API são
  ignorados, e um valor que não valida gera `DABValidacaoWarning` e é mantido
  como veio, porque o erro quase sempre é uma mudança na API.

"""

import types
import typing
import warnings
from datetime import date, datetime, time
from functools import cache
from typing import Annotated, Any, ClassVar, Union

from pydantic import AfterValidator, BaseModel, BeforeValidator, ConfigDict, TypeAdapter, ValidationError

from . import parse
from .errors import DABError, DABValidacaoWarning


class _MarcaUrl:
    """Marca os campos com URI, URL ou e-mail, removidos com `url=False`."""

    def __repr__(self) -> str:
        return "URL"


MARCA_URL = _MarcaUrl()


# Validadores tolerantes ------------------------------------------------------


def _vazio(valor: Any) -> bool:
    return valor is None or (isinstance(valor, str) and valor.strip() == "")


def _para_bool(valor: Any) -> Any:
    if _vazio(valor):
        return None
    if isinstance(valor, bool):
        return valor
    if isinstance(valor, (int, float)):
        return bool(valor)
    if isinstance(valor, str):
        texto = valor.strip().lower()
        if texto in {"s", "sim", "true", "t", "1", "y", "yes"}:
            return True
        if texto in {"n", "não", "nao", "false", "f", "0", "no"}:
            return False
    return valor


_FORMATOS_DATA = ("%Y-%m-%d", "%d/%m/%Y", "%Y%m%d", "%m-%d-%Y", "%d-%m-%Y", "%Y/%m/%d")
_FORMATOS_DATAHORA = (
    "%d/%m/%Y %H:%M:%S",
    "%d/%m/%Y %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
)


def _para_data(valor: Any) -> Any:
    if _vazio(valor):
        return None
    if isinstance(valor, datetime):
        return valor.date()
    if isinstance(valor, date):
        return valor
    if isinstance(valor, str):
        texto = valor.strip()
        try:
            return datetime.fromisoformat(texto.replace("Z", "+00:00")).date()
        except ValueError:
            pass
        for formato in _FORMATOS_DATA:
            try:
                return datetime.strptime(texto, formato).date()
            except ValueError:
                continue
        datahora = _para_datahora(texto)
        if isinstance(datahora, datetime):
            return datahora.date()
    return valor


def _para_datahora(valor: Any) -> Any:
    if _vazio(valor):
        return None
    if isinstance(valor, datetime):
        return valor
    if isinstance(valor, date):
        return datetime.combine(valor, time())
    if isinstance(valor, str):
        texto = valor.strip()
        try:
            return datetime.fromisoformat(texto.replace("Z", "+00:00"))
        except ValueError:
            pass
        for formato in _FORMATOS_DATAHORA + _FORMATOS_DATA:
            try:
                return datetime.strptime(texto, formato)
            except ValueError:
                continue
    return valor


def _para_numero(valor: Any) -> Any:
    if _vazio(valor):
        return None
    if isinstance(valor, str):
        texto = valor.strip()
        # Decimal com vírgula, sem separador de milhar ("1,5").
        if "," in texto and "." not in texto:
            texto = texto.replace(",", ".")
        return texto
    return valor


def _para_inteiro(valor: Any) -> Any:
    valor = _para_numero(valor)
    if isinstance(valor, str):
        try:
            numero = float(valor)
        except ValueError:
            return valor
        return int(numero) if numero.is_integer() else valor
    return valor


def _para_texto(valor: Any) -> Any:
    if valor is None:
        return None
    if isinstance(valor, (int, float)) and not isinstance(valor, bool):
        return str(valor)
    return valor


Bool = Annotated[bool | None, BeforeValidator(_para_bool)]
"""Booleano a partir de `"S"`/`"N"`, `"Sim"`/`"Não"`, `"true"`/`"false"` etc."""

Data = Annotated[date | None, BeforeValidator(_para_data)]
"""Data a partir de ISO-8601, `"DD/MM/AAAA"` ou `"AAAAMMDD"`."""

DataHora = Annotated[datetime | None, BeforeValidator(_para_datahora)]
"""Data e hora a partir de ISO-8601 ou `"DD/MM/AAAA HH:MM:SS"`."""

Inteiro = Annotated[int | None, BeforeValidator(_para_inteiro)]
"""Inteiro; texto vazio vira `None`."""

Real = Annotated[float | None, BeforeValidator(_para_numero)]
"""Número real; aceita vírgula decimal; texto vazio vira `None`."""

Texto = Annotated[str | None, BeforeValidator(_para_texto)]
"""Texto; números viram texto."""

Url = Annotated[str | None, MARCA_URL]
"""URI, URL ou e-mail. Removido das tabelas quando `url=False`."""


# Saída -----------------------------------------------------------------------


class Registro(BaseModel):
    """Base dos modelos de saída: um registro (linha) de uma resposta.

    Os campos têm os nomes do pacote, e os aliases de validação apontam para
    os nomes da API, inclusive dentro de objetos aninhados (`AliasPath`).
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    tolerante: ClassVar[bool] = True
    """Se False, um valor inválido levanta erro em vez de aviso."""

    @classmethod
    def colunas_url(cls) -> list[str]:
        """Campos marcados como URI, URL ou e-mail."""
        return [nome for nome, campo in cls.model_fields.items() if MARCA_URL in campo.metadata]


@cache
def _adaptador(modelo: type[Registro]) -> TypeAdapter:
    return TypeAdapter(list[modelo])


def validar(modelo: type[Registro], dados: Any) -> list[Registro]:
    """Valida os registros brutos com `modelo`.

    Um registro inválido não interrompe a consulta quando o modelo é
    tolerante: gera `DABValidacaoWarning` e mantém o valor bruto do campo.
    """
    if dados is None:
        return []
    if isinstance(dados, dict):
        dados = [dados]
    try:
        return _adaptador(modelo).validate_python(dados)
    except ValidationError:
        if not modelo.tolerante:
            raise
    avisados: set[str] = set()
    return [_validar_tolerante(modelo, bruto, avisados) for bruto in dados]


def _validar_tolerante(modelo: type[Registro], bruto: Any, avisados: set[str]) -> Registro:
    try:
        return modelo.model_validate(bruto)
    except ValidationError:
        pass
    registro = modelo.model_construct()
    validador = modelo.__pydantic_validator__
    for nome, campo in modelo.model_fields.items():
        valor = valor_bruto(bruto, nome, campo.validation_alias)
        if valor is _AUSENTE:
            continue
        try:
            validador.validate_assignment(registro, nome, valor)
        except ValidationError:
            registro.__dict__[nome] = valor
            if nome not in avisados:
                avisados.add(nome)
                warnings.warn(
                    f"Valor inesperado em `{modelo.__name__}.{nome}`: {valor!r}. "
                    "A API pode ter mudado; o valor foi mantido como veio.",
                    DABValidacaoWarning,
                    stacklevel=4,
                )
    return registro


_AUSENTE = object()


def valor_bruto(bruto: Any, nome: str, alias: Any) -> Any:
    """Valor de um campo no registro bruto, seguindo o alias de validação."""
    from pydantic import AliasChoices, AliasPath

    if not isinstance(bruto, dict):
        return _AUSENTE
    if alias is None:
        return bruto.get(nome, _AUSENTE)
    if isinstance(alias, str):
        return bruto.get(alias, bruto.get(nome, _AUSENTE))
    if isinstance(alias, AliasPath):
        valor = bruto
        for chave in alias.path:
            try:
                valor = valor[chave]
            except (KeyError, IndexError, TypeError):
                return _AUSENTE
        return valor
    if isinstance(alias, AliasChoices):
        for escolha in alias.choices:
            valor = valor_bruto(bruto, nome, escolha)
            if valor is not _AUSENTE:
                return valor
    return _AUSENTE


def tipo_base(anotacao: Any) -> Any:
    """Tipo principal de um campo, sem `Annotated` e sem `None`."""
    while typing.get_origin(anotacao) is Annotated:
        anotacao = typing.get_args(anotacao)[0]
    origem = typing.get_origin(anotacao)
    if origem in (Union, types.UnionType):
        argumentos = [a for a in typing.get_args(anotacao) if a is not type(None)]
        if len(argumentos) == 1:
            return tipo_base(argumentos[0])
        return Any
    return origem or anotacao


# Entrada ---------------------------------------------------------------------


def _uf(valor: str | None) -> str | None:
    return None if valor is None else parse.uf(valor)


SiglaUF = Annotated[str | None, AfterValidator(_uf)]
"""UF por nome, sigla ou código IBGE; vira a sigla. UF inválida levanta `DABUFError`."""

Maiusculo = Annotated[str | None, AfterValidator(lambda v: None if v is None else v.upper())]


class Params(BaseModel):
    """Base dos modelos de entrada: argumentos → parâmetros da API.

    Use `serialization_alias` para o nome do parâmetro na API e
    `Field(exclude=True)` para argumentos que não vão para a query string
    (filtros aplicados pelo pacote, partes do caminho etc.).
    """

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    formato_data: ClassVar[str] = "%Y-%m-%d"
    verdadeiro: ClassVar[str] = "true"
    falso: ClassVar[str] = "false"

    @classmethod
    def de_locais(cls, locais: dict[str, Any]):
        """Monta o modelo com os argumentos de uma função (`locals()`).

        Erros do pacote (como `DABUFError`) levantados pelos validadores
        chegam ao usuário como vieram, sem o `ValidationError` em volta.
        """
        try:
            return cls(**{nome: locais[nome] for nome in cls.model_fields if nome in locais})
        except ValidationError as erro:
            for detalhe in erro.errors():
                original = detalhe.get("ctx", {}).get("error")
                if isinstance(original, DABError):
                    raise original from erro
            raise

    def para_api(self) -> dict[str, Any]:
        """Parâmetros da query string, com os nomes e formatos da API."""
        dados = self.model_dump(by_alias=True, exclude_none=True)
        return {chave: self._converter(valor) for chave, valor in dados.items()}

    def _converter(self, valor: Any) -> Any:
        if isinstance(valor, bool):
            return self.verdadeiro if valor else self.falso
        if isinstance(valor, (date, datetime)):
            return valor.strftime(self.formato_data)
        if isinstance(valor, (list, tuple, set)):
            return [self._converter(v) for v in valor]
        return valor


def com_params(modelo: type[Params]):
    """Registra o modelo de entrada de uma função pública.

    Usado pelo teste que confere se a assinatura da função e os campos do
    modelo têm os mesmos argumentos.
    """

    def decorador(funcao):
        funcao.__dab_params__ = modelo
        return funcao

    return decorador
