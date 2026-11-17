# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

class Evento(Objeto):
    modelo = m.EventoDetalhes
    chave_obrigatoria = "localCamara"
    cod: int
    verify: bool | None

    def __init__(self, cod: int, verificar_certificado: bool | None = None) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @overload
    def deputados(self, url: bool = True, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def deputados(self, url: bool = True, index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def deputados(self, url: bool = True, index: bool = False, *, formato: Literal["pydantic"]) -> list[m.Deputado]: ...
    @overload
    def deputados(self, url: bool = True, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def deputados(self, url: bool = True, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def deputados(self, url: bool = True, index: bool = False, *, formato: Literal["url"]) -> str: ...
    @overload
    def orgaos(self, url: bool = True, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def orgaos(self, url: bool = True, index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def orgaos(self, url: bool = True, index: bool = False, *, formato: Literal["pydantic"]) -> list[m.Orgao]: ...
    @overload
    def orgaos(self, url: bool = True, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def orgaos(self, url: bool = True, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def orgaos(self, url: bool = True, index: bool = False, *, formato: Literal["url"]) -> str: ...
    @overload
    def pauta(self, url: bool = True, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def pauta(self, url: bool = True, index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def pauta(self, url: bool = True, index: bool = False, *, formato: Literal["pydantic"]) -> list[m.ItemPauta]: ...
    @overload
    def pauta(self, url: bool = True, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def pauta(self, url: bool = True, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def pauta(self, url: bool = True, index: bool = False, *, formato: Literal["url"]) -> str: ...
    @overload
    def votacoes(self, url: bool = True, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def votacoes(self, url: bool = True, index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def votacoes(
        self, url: bool = True, index: bool = False, *, formato: Literal["pydantic"]
    ) -> list[m.VotacaoEvento]: ...
    @overload
    def votacoes(self, url: bool = True, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def votacoes(self, url: bool = True, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def votacoes(self, url: bool = True, index: bool = False, *, formato: Literal["url"]) -> str: ...

@overload
def lista_eventos(
    tipo_evento: PositiveInt | None = None,
    situacao: PositiveInt | None = None,
    tipo_orgao: PositiveInt | None = None,
    orgao: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    hora_inicio: str | None = None,
    hora_fim: str | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "dataHoraInicio",
    url: bool = True,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_eventos(
    tipo_evento: PositiveInt | None = None,
    situacao: PositiveInt | None = None,
    tipo_orgao: PositiveInt | None = None,
    orgao: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    hora_inicio: str | None = None,
    hora_fim: str | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "dataHoraInicio",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_eventos(
    tipo_evento: PositiveInt | None = None,
    situacao: PositiveInt | None = None,
    tipo_orgao: PositiveInt | None = None,
    orgao: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    hora_inicio: str | None = None,
    hora_fim: str | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "dataHoraInicio",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Evento]: ...
@overload
def lista_eventos(
    tipo_evento: PositiveInt | None = None,
    situacao: PositiveInt | None = None,
    tipo_orgao: PositiveInt | None = None,
    orgao: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    hora_inicio: str | None = None,
    hora_fim: str | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "dataHoraInicio",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_eventos(
    tipo_evento: PositiveInt | None = None,
    situacao: PositiveInt | None = None,
    tipo_orgao: PositiveInt | None = None,
    orgao: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    hora_inicio: str | None = None,
    hora_fim: str | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "dataHoraInicio",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_eventos(
    tipo_evento: PositiveInt | None = None,
    situacao: PositiveInt | None = None,
    tipo_orgao: PositiveInt | None = None,
    orgao: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    hora_inicio: str | None = None,
    hora_fim: str | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "dataHoraInicio",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
