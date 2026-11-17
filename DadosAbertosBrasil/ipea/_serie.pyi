# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import datetime
from typing import Any, Literal, overload

from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

class Serie:
    valores: Any
    dados: Any
    cod: str
    registro: m.Metadados
    base: str | None
    fonte_nome: str | None
    fonte_sigla: str | None
    fonte_url: str | None
    multiplicador: str | None
    periodo: str | None
    ultima_atualizacao: datetime | None
    comentario: str | None
    nome: str | None
    unidade: str | None
    ativo: bool | None
    tema: int | None
    pais: str | None
    numerica: bool | None
    metadados: Any

    def __init__(
        self,
        cod: str,
        index: bool = False,
        verificar_certificado: bool | None = None,
        formato: Literal["json", "pydantic", "pandas", "polars"] | None = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...

@overload
def lista_series(
    contendo: str | None = None,
    excluindo: str | list[str] | None = None,
    fonte: str | None = None,
    ativo: bool | None = None,
    numerica: bool | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_series(
    contendo: str | None = None,
    excluindo: str | list[str] | None = None,
    fonte: str | None = None,
    ativo: bool | None = None,
    numerica: bool | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_series(
    contendo: str | None = None,
    excluindo: str | list[str] | None = None,
    fonte: str | None = None,
    ativo: bool | None = None,
    numerica: bool | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Metadados]: ...
@overload
def lista_series(
    contendo: str | None = None,
    excluindo: str | list[str] | None = None,
    fonte: str | None = None,
    ativo: bool | None = None,
    numerica: bool | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_series(
    contendo: str | None = None,
    excluindo: str | list[str] | None = None,
    fonte: str | None = None,
    ativo: bool | None = None,
    numerica: bool | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_series(
    contendo: str | None = None,
    excluindo: str | list[str] | None = None,
    fonte: str | None = None,
    ativo: bool | None = None,
    numerica: bool | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def serie(
    cod: str, index: bool = False, formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None
) -> Any: ...
@overload
def serie(
    cod: str, index: bool = False, *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def serie(
    cod: str, index: bool = False, *, formato: Literal["pydantic"], verificar_certificado: bool | None = None
) -> list[m.ValorSerie]: ...
@overload
def serie(
    cod: str, index: bool = False, *, formato: Literal["pandas"], verificar_certificado: bool | None = None
) -> DataFramePandas: ...
@overload
def serie(
    cod: str, index: bool = False, *, formato: Literal["polars"], verificar_certificado: bool | None = None
) -> DataFramePolars: ...
@overload
def serie(
    cod: str, index: bool = False, *, formato: Literal["url"], verificar_certificado: bool | None = None
) -> str: ...
