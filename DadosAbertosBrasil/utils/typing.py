from typing import TYPE_CHECKING, Literal, Union

from pandas import DataFrame


Expectativa = Literal[
    "mensal",
    "selic",
    "trimestral",
    "anual",
    "inflacao",
    "top5mensal",
    "top5anual",
    "instituicoes",
]

Formato = Literal["json", "pandas", "polars", "url"]

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
    import polars as pl

    Output = Union[DataFrame, pl.DataFrame, str, dict, list[dict]]
else:
    # polars é opcional: fora do type checking, o tipo não pode referenciá-lo.
    Output = Union[DataFrame, str, dict, list[dict]]
