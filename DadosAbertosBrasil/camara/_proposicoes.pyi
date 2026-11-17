# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

class Proposicao(Objeto):
    modelo = m.ProposicaoDetalhes
    chave_obrigatoria = "statusProposicao"
    cod: int
    verify: bool | None

    def __init__(self, cod: int, verificar_certificado: bool | None = None) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @overload
    def autores(self, url: bool = True, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def autores(self, url: bool = True, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def autores(self, url: bool = True, *, formato: Literal["pydantic"]) -> list[m.Autor]: ...
    @overload
    def autores(self, url: bool = True, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def autores(self, url: bool = True, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def autores(self, url: bool = True, *, formato: Literal["url"]) -> str: ...
    @overload
    def relacionadas(self, url: bool = True, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def relacionadas(
        self, url: bool = True, index: bool = False, *, formato: Literal["json"]
    ) -> list[dict[str, Any]]: ...
    @overload
    def relacionadas(
        self, url: bool = True, index: bool = False, *, formato: Literal["pydantic"]
    ) -> list[m.ProposicaoRelacionada]: ...
    @overload
    def relacionadas(self, url: bool = True, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def relacionadas(self, url: bool = True, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def relacionadas(self, url: bool = True, index: bool = False, *, formato: Literal["url"]) -> str: ...
    @overload
    def temas(self, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def temas(self, index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def temas(self, index: bool = False, *, formato: Literal["pydantic"]) -> list[m.Tema]: ...
    @overload
    def temas(self, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def temas(self, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def temas(self, index: bool = False, *, formato: Literal["url"]) -> str: ...
    @overload
    def tramitacoes(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def tramitacoes(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def tramitacoes(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Tramitacao]: ...
    @overload
    def tramitacoes(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def tramitacoes(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def tramitacoes(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...
    @overload
    def votacoes(
        self,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def votacoes(
        self,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def votacoes(
        self,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Votacao]: ...
    @overload
    def votacoes(
        self,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def votacoes(
        self,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def votacoes(
        self,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...

@overload
def lista_proposicoes(
    tipo: str | None = None,
    numero: int | None = None,
    ano: PositiveInt | None = None,
    autor_cod: int | None = None,
    autor_nome: str | None = None,
    partido_sigla: str | None = None,
    partido_cod: PositiveInt | None = None,
    autor_uf: str | None = None,
    keyword: str | None = None,
    tramitacao_senado: bool | None = None,
    apresentacao_inicio: date | None = None,
    apresentacao_fim: date | None = None,
    situacao: int | None = None,
    tema: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: int | None = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_proposicoes(
    tipo: str | None = None,
    numero: int | None = None,
    ano: PositiveInt | None = None,
    autor_cod: int | None = None,
    autor_nome: str | None = None,
    partido_sigla: str | None = None,
    partido_cod: PositiveInt | None = None,
    autor_uf: str | None = None,
    keyword: str | None = None,
    tramitacao_senado: bool | None = None,
    apresentacao_inicio: date | None = None,
    apresentacao_fim: date | None = None,
    situacao: int | None = None,
    tema: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: int | None = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_proposicoes(
    tipo: str | None = None,
    numero: int | None = None,
    ano: PositiveInt | None = None,
    autor_cod: int | None = None,
    autor_nome: str | None = None,
    partido_sigla: str | None = None,
    partido_cod: PositiveInt | None = None,
    autor_uf: str | None = None,
    keyword: str | None = None,
    tramitacao_senado: bool | None = None,
    apresentacao_inicio: date | None = None,
    apresentacao_fim: date | None = None,
    situacao: int | None = None,
    tema: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: int | None = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Proposicao]: ...
@overload
def lista_proposicoes(
    tipo: str | None = None,
    numero: int | None = None,
    ano: PositiveInt | None = None,
    autor_cod: int | None = None,
    autor_nome: str | None = None,
    partido_sigla: str | None = None,
    partido_cod: PositiveInt | None = None,
    autor_uf: str | None = None,
    keyword: str | None = None,
    tramitacao_senado: bool | None = None,
    apresentacao_inicio: date | None = None,
    apresentacao_fim: date | None = None,
    situacao: int | None = None,
    tema: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: int | None = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_proposicoes(
    tipo: str | None = None,
    numero: int | None = None,
    ano: PositiveInt | None = None,
    autor_cod: int | None = None,
    autor_nome: str | None = None,
    partido_sigla: str | None = None,
    partido_cod: PositiveInt | None = None,
    autor_uf: str | None = None,
    keyword: str | None = None,
    tramitacao_senado: bool | None = None,
    apresentacao_inicio: date | None = None,
    apresentacao_fim: date | None = None,
    situacao: int | None = None,
    tema: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: int | None = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_proposicoes(
    tipo: str | None = None,
    numero: int | None = None,
    ano: PositiveInt | None = None,
    autor_cod: int | None = None,
    autor_nome: str | None = None,
    partido_sigla: str | None = None,
    partido_cod: PositiveInt | None = None,
    autor_uf: str | None = None,
    keyword: str | None = None,
    tramitacao_senado: bool | None = None,
    apresentacao_inicio: date | None = None,
    apresentacao_fim: date | None = None,
    situacao: int | None = None,
    tema: int | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: int | None = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
