from typing import Literal, Union

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

Formato = Literal["json", "pandas", "url"]

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

Output = Union[DataFrame, str, dict, list[dict]]
