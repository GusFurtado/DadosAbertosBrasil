# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

class Partido(Objeto):
    modelo = m.PartidoDetalhes
    chave_obrigatoria = "status"
    cod: int
    verify: bool | None

    def __init__(self, cod: int, verificar_certificado: bool | None = None) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @overload
    def membros(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        legislatura: PositiveInt | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        ordenar_por: str | None = None,
        asc: bool = True,
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def membros(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        legislatura: PositiveInt | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        ordenar_por: str | None = None,
        asc: bool = True,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def membros(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        legislatura: PositiveInt | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        ordenar_por: str | None = None,
        asc: bool = True,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Deputado]: ...
    @overload
    def membros(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        legislatura: PositiveInt | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        ordenar_por: str | None = None,
        asc: bool = True,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def membros(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        legislatura: PositiveInt | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        ordenar_por: str | None = None,
        asc: bool = True,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def membros(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        legislatura: PositiveInt | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        ordenar_por: str | None = None,
        asc: bool = True,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...

@overload
def lista_partidos(
    legislatura: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "sigla",
    url: bool = True,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_partidos(
    legislatura: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "sigla",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_partidos(
    legislatura: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "sigla",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Partido]: ...
@overload
def lista_partidos(
    legislatura: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "sigla",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_partidos(
    legislatura: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "sigla",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_partidos(
    legislatura: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "sigla",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
