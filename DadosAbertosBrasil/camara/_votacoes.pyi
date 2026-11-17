# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, overload

from pydantic import PositiveInt
from typing_extensions import deprecated

from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

class Votacao(Objeto):
    modelo = m.VotacaoDetalhes
    chave_obrigatoria = "descricao"

    @property
    @deprecated("Renomeado para `data_registro`.")
    def data_regitro(self) -> Any: ...
    cod: str
    verify: bool | None

    def __init__(self, cod: str, verificar_certificado: bool | None = None) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @overload
    def orientacoes(self, url: bool = True, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def orientacoes(
        self, url: bool = True, index: bool = False, *, formato: Literal["json"]
    ) -> list[dict[str, Any]]: ...
    @overload
    def orientacoes(
        self, url: bool = True, index: bool = False, *, formato: Literal["pydantic"]
    ) -> list[m.Orientacao]: ...
    @overload
    def orientacoes(self, url: bool = True, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def orientacoes(self, url: bool = True, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def orientacoes(self, url: bool = True, index: bool = False, *, formato: Literal["url"]) -> str: ...
    @overload
    def votos(self, url: bool = True, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def votos(self, url: bool = True, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def votos(self, url: bool = True, *, formato: Literal["pydantic"]) -> list[m.Voto]: ...
    @overload
    def votos(self, url: bool = True, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def votos(self, url: bool = True, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def votos(self, url: bool = True, *, formato: Literal["url"]) -> str: ...

@overload
def lista_votacoes(
    proposicao: int | None = None,
    evento: int | None = None,
    orgao: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = False,
    ordenar_por: str = "dataHoraRegistro",
    url: bool = True,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_votacoes(
    proposicao: int | None = None,
    evento: int | None = None,
    orgao: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = False,
    ordenar_por: str = "dataHoraRegistro",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_votacoes(
    proposicao: int | None = None,
    evento: int | None = None,
    orgao: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = False,
    ordenar_por: str = "dataHoraRegistro",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Votacao]: ...
@overload
def lista_votacoes(
    proposicao: int | None = None,
    evento: int | None = None,
    orgao: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = False,
    ordenar_por: str = "dataHoraRegistro",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_votacoes(
    proposicao: int | None = None,
    evento: int | None = None,
    orgao: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = False,
    ordenar_por: str = "dataHoraRegistro",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_votacoes(
    proposicao: int | None = None,
    evento: int | None = None,
    orgao: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = False,
    ordenar_por: str = "dataHoraRegistro",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
