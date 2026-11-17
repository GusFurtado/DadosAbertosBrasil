# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from typing import Any, Literal, overload

from pydantic import PositiveInt
from typing_extensions import deprecated

from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

class Frente(Objeto):
    modelo = m.FrenteDetalhes
    chave_obrigatoria = "titulo"

    @property
    @deprecated("Renomeado para `id_situacao`.")
    def id_sitacao(self) -> Any: ...
    cod: int
    verify: bool | None

    def __init__(self, cod: int, verificar_certificado: bool | None = None) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @overload
    def membros(self, url: bool = True, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def membros(self, url: bool = True, index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def membros(
        self, url: bool = True, index: bool = False, *, formato: Literal["pydantic"]
    ) -> list[m.MembroFrente]: ...
    @overload
    def membros(self, url: bool = True, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def membros(self, url: bool = True, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def membros(self, url: bool = True, index: bool = False, *, formato: Literal["url"]) -> str: ...

@overload
def lista_frentes(
    legislatura: PositiveInt | None = None,
    pagina: PositiveInt = 1,
    url: bool = True,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_frentes(
    legislatura: PositiveInt | None = None,
    pagina: PositiveInt = 1,
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_frentes(
    legislatura: PositiveInt | None = None,
    pagina: PositiveInt = 1,
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Frente]: ...
@overload
def lista_frentes(
    legislatura: PositiveInt | None = None,
    pagina: PositiveInt = 1,
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_frentes(
    legislatura: PositiveInt | None = None,
    pagina: PositiveInt = 1,
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_frentes(
    legislatura: PositiveInt | None = None,
    pagina: PositiveInt = 1,
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
