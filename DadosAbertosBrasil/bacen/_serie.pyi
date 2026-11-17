# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.ValorSerie]: ...
@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
