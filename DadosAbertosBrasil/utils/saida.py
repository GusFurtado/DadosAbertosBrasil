"""Entrega dos dados no formato pedido.

```
kwargs → Params → Requisicao → JSON bruto ─┬→ "bruto" / "url"
                                           └→ list[Registro] ─┬→ "pydantic"
                                                              ├→ "json" (model_dump)
                                                              ├→ "pandas"
                                                              └→ "polars"
```

Os dois backends de DataFrame são montados a partir dos mesmos registros,
com os tipos das colunas tirados do modelo, e nenhum depende do outro.

"""

import warnings
from collections.abc import Callable, Iterable
from datetime import date, datetime
from typing import Any, get_args

from .._config import config
from .errors import DABInputError
from .modelos import Registro, tipo_base, validar
from .requisicao import Requisicao
from .typing import Formato

FORMATOS = get_args(Formato)


def importar_pandas():
    try:
        import pandas as pd
    except ImportError as erro:
        raise ImportError(
            "O formato 'pandas' requer a biblioteca pandas. "
            "Instale com `pip install DadosAbertosBrasil[pandas]`."
        ) from erro
    return pd


def importar_polars():
    try:
        import polars as pl
    except ImportError as erro:
        raise ImportError(
            "O formato 'polars' requer a biblioteca polars. "
            "Instale com `pip install DadosAbertosBrasil[polars]`."
        ) from erro
    return pl


def resolver_formato(formato: str | None) -> str:
    """Formato pedido, ou o de `config.formato`, validado."""
    formato = config.resolver_formato(formato)
    if formato not in FORMATOS:
        raise DABInputError(f"Formato inválido: {formato!r}. Use um de {', '.join(map(repr, FORMATOS))}.")
    return formato


def consultar(
    requisicao: Requisicao,
    modelo: type[Registro],
    formato: str | None,
    *,
    url: bool = True,
    index: bool = False,
    index_col: str | None = "codigo",
    preparar: Callable[[Any], Any] | None = None,
    filtro: Callable[[Registro], bool] | None = None,
    metadados: dict | None = None,
) -> Any:
    """Faz a consulta e entrega os dados no formato pedido.

    Parameters
    ----------
    requisicao : Requisicao
        Consulta à API.
    modelo : type[Registro]
        Modelo de saída de cada registro.
    formato : str, optional
        Formato pedido pelo usuário; se None, usa `config.formato`.
    url : bool, default=True
        Se False, remove os campos marcados como URL do modelo.
    index : bool, default=False
        Em pandas, define `index_col` como index.
    preparar : callable, optional
        Transforma o JSON (já desembrulhado) antes da validação, por exemplo
        para achatar listas aninhadas.
    filtro : callable, optional
        Mantém só os registros para os quais retorna True.
    metadados : dict, optional
        Vão para `DataFrame.attrs` em pandas.

    """
    formato = resolver_formato(formato)
    if formato == "url":
        return requisicao.url

    bruto = requisicao.bruto()
    if formato == "bruto":
        return bruto

    dados = requisicao.desembrulhar(bruto)
    if preparar is not None:
        dados = preparar(dados)
    registros = validar(modelo, dados)
    if filtro is not None:
        registros = [r for r in registros if filtro(r)]
    return tabela(
        registros,
        modelo,
        formato,
        url=url,
        index=index,
        index_col=index_col,
        metadados=metadados,
    )


def tabela(
    registros: Iterable[Registro],
    modelo: type[Registro],
    formato: str,
    *,
    url: bool = True,
    index: bool = False,
    index_col: str | None = "codigo",
    metadados: dict | None = None,
) -> Any:
    """Converte registros já validados para `formato`."""
    registros = list(registros)
    match formato:
        case "pydantic":
            return registros
        case "json":
            excluir = None if url else set(modelo.colunas_url())
            return [r.model_dump(exclude=excluir) for r in registros]
        case "pandas":
            return para_pandas(registros, modelo, url=url, index=index, index_col=index_col, metadados=metadados)
        case "polars":
            return para_polars(registros, modelo, url=url, index=index)
    raise DABInputError(f"Formato {formato!r} não se aplica a esta função.")


def colunas(modelo: type[Registro], url: bool = True) -> list[str]:
    """Colunas da tabela, na ordem dos campos do modelo."""
    remover = set() if url else set(modelo.colunas_url())
    return [nome for nome in modelo.model_fields if nome not in remover]


def _linhas(registros: list[Registro], nomes: list[str]) -> list[dict]:
    return [{nome: r.__dict__.get(nome) for nome in nomes} for r in registros]


def para_pandas(
    registros: list[Registro],
    modelo: type[Registro],
    *,
    url: bool = True,
    index: bool = False,
    index_col: str | None = "codigo",
    metadados: dict | None = None,
):
    """DataFrame pandas com os tipos das colunas tirados do modelo.

    Inteiros e booleanos usam os tipos com suporte a valores ausentes
    (`Int64` e `boolean`); datas viram `datetime64`.
    """
    pd = importar_pandas()
    nomes = colunas(modelo, url)
    df = pd.DataFrame.from_records(_linhas(registros, nomes), columns=nomes)
    for nome in nomes:
        tipo = tipo_base(modelo.model_fields[nome].annotation)
        try:
            if tipo is bool:
                df[nome] = df[nome].astype("boolean")
            elif tipo is int:
                df[nome] = df[nome].astype("Int64")
            elif tipo is float:
                df[nome] = df[nome].astype("float64")
            elif tipo in (date, datetime):
                df[nome] = pd.to_datetime(df[nome])
        except (TypeError, ValueError):
            # Valor bruto mantido por `validar`: a coluna fica como veio.
            continue
    if index and index_col is not None and not df.empty:
        df = df.set_index(index_col)
    if metadados:
        df.attrs.update(metadados)
    return df


def _tipo_polars(pl, tipo: Any):
    return {
        bool: pl.Boolean,
        int: pl.Int64,
        float: pl.Float64,
        str: pl.String,
        date: pl.Date,
        datetime: pl.Datetime,
    }.get(tipo)


def para_polars(
    registros: list[Registro],
    modelo: type[Registro],
    *,
    url: bool = True,
    index: bool = False,
):
    """DataFrame polars com os tipos das colunas tirados do modelo."""
    pl = importar_polars()
    if index:
        warnings.warn(
            "O argumento `index` é ignorado quando o formato é 'polars', pois polars não possui index.",
            UserWarning,
            stacklevel=4,
        )
    nomes = colunas(modelo, url)
    tipos = {nome: _tipo_polars(pl, tipo_base(modelo.model_fields[nome].annotation)) for nome in nomes}
    linhas = _linhas(registros, nomes)
    if not linhas:
        return pl.DataFrame(schema={nome: tipo or pl.Null for nome, tipo in tipos.items()})
    conhecidos = {nome: tipo for nome, tipo in tipos.items() if tipo is not None}
    try:
        df = pl.from_dicts(linhas, schema_overrides=conhecidos, infer_schema_length=None, strict=False)
    except (TypeError, ValueError, pl.exceptions.PolarsError):
        df = pl.from_dicts(linhas, infer_schema_length=None, strict=False)
    return df.select(nomes)
