# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from typing import Any, Literal, NoReturn, overload

from pydantic import PositiveInt
from typing_extensions import deprecated

from ..utils.typing import DataFramePandas, DataFramePolars, NivelTerritorial
from . import modelos as m

def populacao(
    projecao: Literal["populacao", "nascimento", "obito", "incremento"] | None = None,
    localidade: PositiveInt | None = None,
) -> dict | int: ...
@overload
def localidades(
    nivel: NivelTerritorial = "distritos",
    divisoes: NivelTerritorial | None = None,
    localidade: PositiveInt | str | list[PositiveInt | str] | None = None,
    ordenar_por: str | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def localidades(
    nivel: NivelTerritorial = "distritos",
    divisoes: NivelTerritorial | None = None,
    localidade: PositiveInt | str | list[PositiveInt | str] | None = None,
    ordenar_por: str | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def localidades(
    nivel: NivelTerritorial = "distritos",
    divisoes: NivelTerritorial | None = None,
    localidade: PositiveInt | str | list[PositiveInt | str] | None = None,
    ordenar_por: str | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Localidade]: ...
@overload
def localidades(
    nivel: NivelTerritorial = "distritos",
    divisoes: NivelTerritorial | None = None,
    localidade: PositiveInt | str | list[PositiveInt | str] | None = None,
    ordenar_por: str | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def localidades(
    nivel: NivelTerritorial = "distritos",
    divisoes: NivelTerritorial | None = None,
    localidade: PositiveInt | str | list[PositiveInt | str] | None = None,
    ordenar_por: str | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def localidades(
    nivel: NivelTerritorial = "distritos",
    divisoes: NivelTerritorial | None = None,
    localidade: PositiveInt | str | list[PositiveInt | str] | None = None,
    ordenar_por: str | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...

TipoMalha = Literal["geojson", "topojson", "svg"]

def malha(
    localidade: PositiveInt | str,
    nivel: str = "estados",
    divisoes: str | None = None,
    periodo: PositiveInt = 2020,
    tipo: TipoMalha = "geojson",
    qualidade: Literal["minima", "intermediaria", "maxima"] = "minima",
    formato: Literal["bruto", "url", "svg", "json", "geojson"] = "bruto",
    verificar_certificado: bool | None = None,
) -> dict[str, Any] | str: ...
@deprecated("Removida no 3.0: levanta `DABFuncaoRemovidaError`.")
def coordenadas(*args, **kwargs) -> NoReturn: ...
