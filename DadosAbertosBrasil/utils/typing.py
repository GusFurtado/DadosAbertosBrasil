from typing import TYPE_CHECKING, Any, Literal, TypeAlias, Union

Expectativa = Literal[
    "mensal",
    "selic",
    "trimestral",
    "anual",
    "inflacao",
    "top5mensal",
    "top5anual",
]

Formato = Literal["json", "bruto", "pydantic", "pandas", "polars", "url"]
"""Formatos de retorno das funções com dados tabulares.

- "json": lista de registros normalizados (`list[dict]`), com os mesmos nomes e
  tipos das colunas dos DataFrames;
- "bruto": JSON original da API, como veio;
- "pydantic": lista de modelos Pydantic (`list[Registro]`);
- "pandas": `pandas.DataFrame`;
- "polars": `polars.DataFrame`;
- "url": endereço da consulta.
"""

NivelTerritorial = Literal[
    "distritos",
    "estados",
    "mesorregioes",
    "microrregioes",
    "municipios",
    "regioes-imediatas",
    "regioes-intermediarias",
    "regioes",
    "paises",
]

if TYPE_CHECKING:
    import pandas as pd
    import polars as pl

    from .modelos import Registro

    DataFramePandas: TypeAlias = pd.DataFrame
    DataFramePolars: TypeAlias = pl.DataFrame
    Saida = Union[list[dict[str, Any]], list[Registro], "pd.DataFrame", "pl.DataFrame", str, dict, list]
else:
    # pandas e polars são opcionais: fora do type checking, os tipos não podem referenciá-los.
    DataFramePandas = Any
    DataFramePolars = Any
    Saida = Any

Output = Saida
