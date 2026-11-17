# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, overload

from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

@overload
def cambio(
    moedas: list[str] | str = ...,
    inicio: date = ...,
    fim: date | None = ...,
    cotacao: Literal["compra", "venda"] = "compra",
    boletim: Literal["abertura", "fechamento", "intermediário"] = "fechamento",
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def cambio(
    moedas: list[str] | str = ...,
    inicio: date = ...,
    fim: date | None = ...,
    cotacao: Literal["compra", "venda"] = "compra",
    boletim: Literal["abertura", "fechamento", "intermediário"] = "fechamento",
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def cambio(
    moedas: list[str] | str = ...,
    inicio: date = ...,
    fim: date | None = ...,
    cotacao: Literal["compra", "venda"] = "compra",
    boletim: Literal["abertura", "fechamento", "intermediário"] = "fechamento",
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Cotacao]: ...
@overload
def cambio(
    moedas: list[str] | str = ...,
    inicio: date = ...,
    fim: date | None = ...,
    cotacao: Literal["compra", "venda"] = "compra",
    boletim: Literal["abertura", "fechamento", "intermediário"] = "fechamento",
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def cambio(
    moedas: list[str] | str = ...,
    inicio: date = ...,
    fim: date | None = ...,
    cotacao: Literal["compra", "venda"] = "compra",
    boletim: Literal["abertura", "fechamento", "intermediário"] = "fechamento",
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def cambio(
    moedas: list[str] | str = ...,
    inicio: date = ...,
    fim: date | None = ...,
    cotacao: Literal["compra", "venda"] = "compra",
    boletim: Literal["abertura", "fechamento", "intermediário"] = "fechamento",
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
