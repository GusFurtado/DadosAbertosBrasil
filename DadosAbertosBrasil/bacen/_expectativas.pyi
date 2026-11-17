# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.modelos import Registro
from ..utils.typing import DataFramePandas, DataFramePolars, Expectativa

@overload
def expectativas(
    expectativa: Expectativa,
    indicador: str | None = None,
    top: PositiveInt | None = None,
    ordenar_por: str = "Data",
    asc: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def expectativas(
    expectativa: Expectativa,
    indicador: str | None = None,
    top: PositiveInt | None = None,
    ordenar_por: str = "Data",
    asc: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def expectativas(
    expectativa: Expectativa,
    indicador: str | None = None,
    top: PositiveInt | None = None,
    ordenar_por: str = "Data",
    asc: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[Registro]: ...
@overload
def expectativas(
    expectativa: Expectativa,
    indicador: str | None = None,
    top: PositiveInt | None = None,
    ordenar_por: str = "Data",
    asc: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def expectativas(
    expectativa: Expectativa,
    indicador: str | None = None,
    top: PositiveInt | None = None,
    ordenar_por: str = "Data",
    asc: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def expectativas(
    expectativa: Expectativa,
    indicador: str | None = None,
    top: PositiveInt | None = None,
    ordenar_por: str = "Data",
    asc: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
