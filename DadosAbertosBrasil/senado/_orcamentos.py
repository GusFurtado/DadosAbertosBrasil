import re
from typing import Any, Literal, overload

from pydantic import Field, PositiveInt, validate_call

from ..utils.modelos import com_params
from ..utils.typing import DataFramePandas, DataFramePolars, Formato, Saida
from . import modelos as m
from ._comum import ParamsSenado, consultar_senado


class _ParamsOrcamentos(ParamsSenado):
    autor: str | None = Field(None, exclude=True)
    tipo: str | None = Field(None, exclude=True)
    ano_execucao: int | None = Field(None, exclude=True)
    ano_materia: int | None = Field(None, exclude=True)


@overload
def lista_orcamentos(
    autor: str | None = ...,
    tipo: str | None = ...,
    ano_execucao: PositiveInt | None = ...,
    ano_materia: PositiveInt | None = ...,
    url: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def lista_orcamentos(
    autor: str | None = ...,
    tipo: str | None = ...,
    ano_execucao: PositiveInt | None = ...,
    ano_materia: PositiveInt | None = ...,
    url: bool = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def lista_orcamentos(
    autor: str | None = ...,
    tipo: str | None = ...,
    ano_execucao: PositiveInt | None = ...,
    ano_materia: PositiveInt | None = ...,
    url: bool = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.LoteEmendas]: ...


@overload
def lista_orcamentos(
    autor: str | None = ...,
    tipo: str | None = ...,
    ano_execucao: PositiveInt | None = ...,
    ano_materia: PositiveInt | None = ...,
    url: bool = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def lista_orcamentos(
    autor: str | None = ...,
    tipo: str | None = ...,
    ano_execucao: PositiveInt | None = ...,
    ano_materia: PositiveInt | None = ...,
    url: bool = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def lista_orcamentos(
    autor: str | None = ...,
    tipo: str | None = ...,
    ano_execucao: PositiveInt | None = ...,
    ano_materia: PositiveInt | None = ...,
    url: bool = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsOrcamentos)
def lista_orcamentos(
    autor: str | None = None,
    tipo: str | None = None,
    ano_execucao: PositiveInt | None = None,
    ano_materia: PositiveInt | None = None,
    url: bool = True,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Obtém a lista dos lotes de emendas orçamentárias.

    Parameters
    ----------
    autor : str, optional
        Texto contendo nome do autor.

    tipo : str, optional
        Tipo de orçamento.

    ano_execucao : int, optional
        Ano que o orçamento foi executado.

    ano_materia : int, optional
        Ano da matéria.

    url : bool, default=True
        Se False, remove as colunas contendo URI, URL e e-mails.
        Vale para os formatos 'json', 'pandas' e 'polars'.

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": JSON original da API, como veio;
        - "pydantic": lista de modelos Pydantic, um por registro;
        - "pandas": DataFrame pandas;
        - "polars": DataFrame polars;
        - "url": endereço da consulta.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
        Lista dos lotes de emendas orçamentárias.

    Examples
    --------
    Buscar o orçamento da Lei de Diretrizes Orçamentárias de 2020.

    >>> senado.orcamento(tipo='LDO', ano_execucao=2020)
              autor_nome  ativo                       autor_email  autor_codigo \
    0          Abou Anni   True        dep.abouanni@camara.leg.br          3896
    1       Acir Gurgacz   True               acir@senador.leg.br          2633
    2    Adriana Ventura   True  dep.adrianaventura@camara.leg.br          3899
    ..               ...    ...                               ...           ...

    Pesquisar por emendas da deputada Adriana Ventura

    >>> senado.orcamento(autor='Adriana')
            autor_nome  ativo                       autor_email  autor_codigo \
    0  Adriana Ventura   True  dep.adrianaventura@camara.leg.br          3899

    """

    def filtro(lote: m.LoteEmendas) -> bool:
        if autor is not None and not (isinstance(lote.autor_nome, str) and re.search(autor, lote.autor_nome)):
            return False
        if tipo is not None and lote.tipo_sigla != tipo:
            return False
        if ano_execucao is not None and lote.ano_execucao != ano_execucao:
            return False
        return ano_materia is None or lote.materia_ano == ano_materia

    return consultar_senado(
        ["orcamento", "lista"],
        ["ListaLoteEmendas", "LotesEmendasOrcamento", "LoteEmendasOrcamento"],
        _ParamsOrcamentos.de_locais(locals()),
        m.LoteEmendas,
        formato,
        url=url,
        filtro=filtro,
        verificar_certificado=verificar_certificado,
    )
