# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, overload

from .. import ibge, wiki
from ..camara.modelos import Deputado
from ..senado.modelos import Senador
from ..utils.typing import DataFramePandas, DataFramePolars
from ._governador import Governador

class UF:
    sigla: str
    verify: bool | None
    registro: wiki.modelos.UF | None

    def __init__(self, uf: str, verificar_certificado: bool | None = None) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    def bandeira(self, tamanho: int = 100) -> str: ...
    def brasao(self, tamanho: int = 100) -> str: ...
    @property
    def densidade(self) -> float: ...
    @overload
    def deputados(
        self,
        nome: str | None = None,
        legislatura: int | None = None,
        partido: str | None = None,
        sexo: str | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: int = 1,
        itens: int | None = None,
        asc: bool = True,
        ordenar_por: str = "nome",
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
        verificar_certificado: bool | None = None,
    ) -> Any: ...
    @overload
    def deputados(
        self,
        nome: str | None = None,
        legislatura: int | None = None,
        partido: str | None = None,
        sexo: str | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: int = 1,
        itens: int | None = None,
        asc: bool = True,
        ordenar_por: str = "nome",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
        verificar_certificado: bool | None = None,
    ) -> list[dict[str, Any]]: ...
    @overload
    def deputados(
        self,
        nome: str | None = None,
        legislatura: int | None = None,
        partido: str | None = None,
        sexo: str | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: int = 1,
        itens: int | None = None,
        asc: bool = True,
        ordenar_por: str = "nome",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
        verificar_certificado: bool | None = None,
    ) -> list[Deputado]: ...
    @overload
    def deputados(
        self,
        nome: str | None = None,
        legislatura: int | None = None,
        partido: str | None = None,
        sexo: str | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: int = 1,
        itens: int | None = None,
        asc: bool = True,
        ordenar_por: str = "nome",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
        verificar_certificado: bool | None = None,
    ) -> DataFramePandas: ...
    @overload
    def deputados(
        self,
        nome: str | None = None,
        legislatura: int | None = None,
        partido: str | None = None,
        sexo: str | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: int = 1,
        itens: int | None = None,
        asc: bool = True,
        ordenar_por: str = "nome",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
        verificar_certificado: bool | None = None,
    ) -> DataFramePolars: ...
    @overload
    def deputados(
        self,
        nome: str | None = None,
        legislatura: int | None = None,
        partido: str | None = None,
        sexo: str | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: int = 1,
        itens: int | None = None,
        asc: bool = True,
        ordenar_por: str = "nome",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
        verificar_certificado: bool | None = None,
    ) -> str: ...
    @property
    def galeria(self) -> ibge.Galeria: ...
    @property
    def governador(self) -> Governador: ...
    @property
    def historia(self) -> ibge.Historia: ...
    def malha(
        self,
        nivel: str = "estados",
        divisoes: str | None = None,
        periodo: int = 2020,
        tipo: Literal["geojson", "topojson", "svg"] = "geojson",
        qualidade: Literal["minima", "intermediaria", "maxima"] = "minima",
        formato: Literal["bruto", "url", "svg", "json", "geojson"] = "bruto",
    ) -> dict[str, Any] | str: ...
    @property
    def municipios(self) -> int | str: ...
    @property
    def populacao(self) -> int: ...
    @property
    def prefeito(self) -> wiki.modelos.PrefeitoCapital: ...
    @overload
    def senadores(
        self,
        tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
        sexo: str | None = None,
        partido: str | None = None,
        contendo: str | None = None,
        excluindo: str | None = None,
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
        verificar_certificado: bool | None = None,
    ) -> Any: ...
    @overload
    def senadores(
        self,
        tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
        sexo: str | None = None,
        partido: str | None = None,
        contendo: str | None = None,
        excluindo: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
        verificar_certificado: bool | None = None,
    ) -> list[dict[str, Any]]: ...
    @overload
    def senadores(
        self,
        tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
        sexo: str | None = None,
        partido: str | None = None,
        contendo: str | None = None,
        excluindo: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
        verificar_certificado: bool | None = None,
    ) -> list[Senador]: ...
    @overload
    def senadores(
        self,
        tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
        sexo: str | None = None,
        partido: str | None = None,
        contendo: str | None = None,
        excluindo: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
        verificar_certificado: bool | None = None,
    ) -> DataFramePandas: ...
    @overload
    def senadores(
        self,
        tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
        sexo: str | None = None,
        partido: str | None = None,
        contendo: str | None = None,
        excluindo: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
        verificar_certificado: bool | None = None,
    ) -> DataFramePolars: ...
    @overload
    def senadores(
        self,
        tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
        sexo: str | None = None,
        partido: str | None = None,
        contendo: str | None = None,
        excluindo: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
        verificar_certificado: bool | None = None,
    ) -> str: ...
