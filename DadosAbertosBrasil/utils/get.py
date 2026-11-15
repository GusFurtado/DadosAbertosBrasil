"""Conversão de DataFrames pandas usada só pelas funções descontinuadas.

Sai junto com `favoritos.perfil_eleitorado` e `ibge.coordenadas` (#44).
"""

import warnings
from typing import TYPE_CHECKING

import pandas as pd

from .typing import Output

if TYPE_CHECKING:
    import polars as pl


def _importar_polars():
    try:
        import polars as pl
    except ImportError as erro:
        raise ImportError(
            "O formato 'polars' requer a biblioteca polars. "
            "Instale com `pip install DadosAbertosBrasil[polars]`."
        ) from erro
    return pl


def _avisar_index_polars() -> None:
    warnings.warn(
        "Os argumentos `index` e `index_col` são ignorados quando o "
        "formato é 'polars', pois polars não possui index.",
        UserWarning,
        stacklevel=3,
    )


def _pandas_para_polars(df: pd.DataFrame) -> "pl.DataFrame":
    # pl.from_pandas exige pyarrow para colunas `object` e de extensão (como o
    # `str` padrão do pandas 3); essas passam por listas Python.
    pl = _importar_polars()
    colunas = []
    for nome, serie in df.items():
        nome = str(nome)
        if serie.dtype == object or pd.api.types.is_extension_array_dtype(serie.dtype):
            valores = [None if pd.isna(v) is True else v for v in serie]
            colunas.append(pl.Series(nome, valores, strict=False))
        else:
            colunas.append(pl.from_pandas(serie.rename(nome)))
    return pl.DataFrame(colunas)


def converter(
    df: pd.DataFrame,
    formato: str,
    index: bool = False,
    index_col: str | None = None,
) -> Output:
    """Entrega um DataFrame pandas já formatado no `formato` resolvido.

    Em pandas, define `index_col` como index se `index` for True. Em polars,
    um index nomeado vira coluna e `index` é ignorado com aviso.
    """
    if formato == "polars":
        if index:
            _avisar_index_polars()
        if any(nome is not None for nome in df.index.names):
            df = df.reset_index()
        return _pandas_para_polars(df)
    if index and index_col is not None and not df.empty:
        df = df.set_index(index_col)
    return df
