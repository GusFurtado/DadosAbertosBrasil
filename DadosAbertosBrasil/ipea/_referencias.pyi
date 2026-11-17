# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

@overload
def lista_temas(
    cod: PositiveInt | None = None,
    pai: PositiveInt | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_temas(
    cod: PositiveInt | None = None,
    pai: PositiveInt | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_temas(
    cod: PositiveInt | None = None,
    pai: PositiveInt | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Tema]: ...
@overload
def lista_temas(
    cod: PositiveInt | None = None,
    pai: PositiveInt | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_temas(
    cod: PositiveInt | None = None,
    pai: PositiveInt | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_temas(
    cod: PositiveInt | None = None,
    pai: PositiveInt | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def lista_paises(
    cod: str | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_paises(
    cod: str | None = None, index: bool = False, *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def lista_paises(
    cod: str | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Pais]: ...
@overload
def lista_paises(
    cod: str | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_paises(
    cod: str | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_paises(
    cod: str | None = None, index: bool = False, *, formato: Literal["url"], verificar_certificado: bool | None = None
) -> str: ...
@overload
def lista_territorios(
    capital: bool | None = None,
    amc: bool | None = None,
    cod: int | None = None,
    nivel: str | None = None,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_territorios(
    capital: bool | None = None,
    amc: bool | None = None,
    cod: int | None = None,
    nivel: str | None = None,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_territorios(
    capital: bool | None = None,
    amc: bool | None = None,
    cod: int | None = None,
    nivel: str | None = None,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Territorio]: ...
@overload
def lista_territorios(
    capital: bool | None = None,
    amc: bool | None = None,
    cod: int | None = None,
    nivel: str | None = None,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_territorios(
    capital: bool | None = None,
    amc: bool | None = None,
    cod: int | None = None,
    nivel: str | None = None,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_territorios(
    capital: bool | None = None,
    amc: bool | None = None,
    cod: int | None = None,
    nivel: str | None = None,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
def lista_niveis() -> list[str]: ...
