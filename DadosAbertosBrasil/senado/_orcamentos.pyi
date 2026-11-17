# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

@overload
def lista_orcamentos(
    autor: str | None = None,
    tipo: str | None = None,
    ano_execucao: PositiveInt | None = None,
    ano_materia: PositiveInt | None = None,
    url: bool = True,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_orcamentos(
    autor: str | None = None,
    tipo: str | None = None,
    ano_execucao: PositiveInt | None = None,
    ano_materia: PositiveInt | None = None,
    url: bool = True,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_orcamentos(
    autor: str | None = None,
    tipo: str | None = None,
    ano_execucao: PositiveInt | None = None,
    ano_materia: PositiveInt | None = None,
    url: bool = True,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.LoteEmendas]: ...
@overload
def lista_orcamentos(
    autor: str | None = None,
    tipo: str | None = None,
    ano_execucao: PositiveInt | None = None,
    ano_materia: PositiveInt | None = None,
    url: bool = True,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_orcamentos(
    autor: str | None = None,
    tipo: str | None = None,
    ano_execucao: PositiveInt | None = None,
    ano_materia: PositiveInt | None = None,
    url: bool = True,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_orcamentos(
    autor: str | None = None,
    tipo: str | None = None,
    ano_execucao: PositiveInt | None = None,
    ano_materia: PositiveInt | None = None,
    url: bool = True,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
