# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

class Deputado(Objeto):
    modelo = m.DeputadoDetalhes
    chave_obrigatoria = "ultimoStatus"
    cod: int
    verify: bool | None

    def __init__(self, cod: int, verificar_certificado: bool | None = None) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @overload
    def despesas(
        self,
        legislatura: PositiveInt | None = None,
        ano: PositiveInt | None = None,
        mes: PositiveInt | None = None,
        fornecedor: int | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "ano",
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def despesas(
        self,
        legislatura: PositiveInt | None = None,
        ano: PositiveInt | None = None,
        mes: PositiveInt | None = None,
        fornecedor: int | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "ano",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def despesas(
        self,
        legislatura: PositiveInt | None = None,
        ano: PositiveInt | None = None,
        mes: PositiveInt | None = None,
        fornecedor: int | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "ano",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Despesa]: ...
    @overload
    def despesas(
        self,
        legislatura: PositiveInt | None = None,
        ano: PositiveInt | None = None,
        mes: PositiveInt | None = None,
        fornecedor: int | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "ano",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def despesas(
        self,
        legislatura: PositiveInt | None = None,
        ano: PositiveInt | None = None,
        mes: PositiveInt | None = None,
        fornecedor: int | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "ano",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def despesas(
        self,
        legislatura: PositiveInt | None = None,
        ano: PositiveInt | None = None,
        mes: PositiveInt | None = None,
        fornecedor: int | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "ano",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...
    @overload
    def discursos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def discursos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def discursos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Discurso]: ...
    @overload
    def discursos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def discursos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def discursos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        *,
        formato: Literal["url"],
    ) -> str: ...
    @overload
    def eventos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def eventos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def eventos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.EventoDeputado]: ...
    @overload
    def eventos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def eventos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def eventos(
        self,
        legislatura: PositiveInt | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...
    @overload
    def frentes(self, url: bool = True, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def frentes(self, url: bool = True, index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def frentes(self, url: bool = True, index: bool = False, *, formato: Literal["pydantic"]) -> list[m.Frente]: ...
    @overload
    def frentes(self, url: bool = True, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def frentes(self, url: bool = True, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def frentes(self, url: bool = True, index: bool = False, *, formato: Literal["url"]) -> str: ...
    @overload
    def ocupacoes(self, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def ocupacoes(self, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def ocupacoes(self, *, formato: Literal["pydantic"]) -> list[m.Ocupacao]: ...
    @overload
    def ocupacoes(self, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def ocupacoes(self, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def ocupacoes(self, *, formato: Literal["url"]) -> str: ...
    @overload
    def orgaos(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataInicio",
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def orgaos(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def orgaos(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.OrgaoDeputado]: ...
    @overload
    def orgaos(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def orgaos(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def orgaos(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        asc: bool = True,
        ordenar_por: str = "dataInicio",
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...
    @overload
    def profissoes(self, url: bool = True, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def profissoes(
        self, url: bool = True, index: bool = False, *, formato: Literal["json"]
    ) -> list[dict[str, Any]]: ...
    @overload
    def profissoes(
        self, url: bool = True, index: bool = False, *, formato: Literal["pydantic"]
    ) -> list[m.Profissao]: ...
    @overload
    def profissoes(self, url: bool = True, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def profissoes(self, url: bool = True, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def profissoes(self, url: bool = True, index: bool = False, *, formato: Literal["url"]) -> str: ...

@overload
def lista_deputados(
    nome: str | None = None,
    legislatura: PositiveInt | None = None,
    uf: str | None = None,
    partido: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_deputados(
    nome: str | None = None,
    legislatura: PositiveInt | None = None,
    uf: str | None = None,
    partido: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_deputados(
    nome: str | None = None,
    legislatura: PositiveInt | None = None,
    uf: str | None = None,
    partido: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Deputado]: ...
@overload
def lista_deputados(
    nome: str | None = None,
    legislatura: PositiveInt | None = None,
    uf: str | None = None,
    partido: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_deputados(
    nome: str | None = None,
    legislatura: PositiveInt | None = None,
    uf: str | None = None,
    partido: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_deputados(
    nome: str | None = None,
    legislatura: PositiveInt | None = None,
    uf: str | None = None,
    partido: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
