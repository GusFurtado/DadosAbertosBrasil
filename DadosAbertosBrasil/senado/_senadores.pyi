# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

class Senador(Objeto):
    modelo = m.SenadorDetalhes
    chave_obrigatoria = "IdentificacaoParlamentar"
    telefones: list[str]
    cod: int
    verify: bool | None

    def __init__(self, cod: int, verificar_certificado: bool | None = None) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Aparte]: ...
    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...
    @overload
    def autorias(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        primeiro_autor: bool | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def autorias(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        primeiro_autor: bool | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def autorias(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        primeiro_autor: bool | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Autoria]: ...
    @overload
    def autorias(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        primeiro_autor: bool | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def autorias(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        primeiro_autor: bool | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def autorias(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        primeiro_autor: bool | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...
    @overload
    def cargos(
        self, comissao: str | None = None, ativos: bool | None = None, formato: Literal["bruto"] | None = None
    ) -> Any: ...
    @overload
    def cargos(
        self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["json"]
    ) -> list[dict[str, Any]]: ...
    @overload
    def cargos(
        self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["pydantic"]
    ) -> list[m.Cargo]: ...
    @overload
    def cargos(
        self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["pandas"]
    ) -> DataFramePandas: ...
    @overload
    def cargos(
        self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["polars"]
    ) -> DataFramePolars: ...
    @overload
    def cargos(self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["url"]) -> str: ...
    @overload
    def comissoes(
        self, comissao: str | None = None, ativos: bool | None = None, formato: Literal["bruto"] | None = None
    ) -> Any: ...
    @overload
    def comissoes(
        self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["json"]
    ) -> list[dict[str, Any]]: ...
    @overload
    def comissoes(
        self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["pydantic"]
    ) -> list[m.MembroComissao]: ...
    @overload
    def comissoes(
        self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["pandas"]
    ) -> DataFramePandas: ...
    @overload
    def comissoes(
        self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["polars"]
    ) -> DataFramePolars: ...
    @overload
    def comissoes(self, comissao: str | None = None, ativos: bool | None = None, *, formato: Literal["url"]) -> str: ...
    @overload
    def cursos(self, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def cursos(self, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def cursos(self, *, formato: Literal["pydantic"]) -> list[m.Curso]: ...
    @overload
    def cursos(self, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def cursos(self, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def cursos(self, *, formato: Literal["url"]) -> str: ...
    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Discurso]: ...
    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...
    @overload
    def filiacoes(self, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def filiacoes(self, index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def filiacoes(self, index: bool = False, *, formato: Literal["pydantic"]) -> list[m.Filiacao]: ...
    @overload
    def filiacoes(self, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def filiacoes(self, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def filiacoes(self, index: bool = False, *, formato: Literal["url"]) -> str: ...
    def historico(self) -> dict: ...
    @overload
    def mandatos(self, index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def mandatos(self, index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def mandatos(self, index: bool = False, *, formato: Literal["pydantic"]) -> list[m.Mandato]: ...
    @overload
    def mandatos(self, index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def mandatos(self, index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def mandatos(self, index: bool = False, *, formato: Literal["url"]) -> str: ...
    @overload
    def liderancas(self, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def liderancas(self, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def liderancas(self, *, formato: Literal["pydantic"]) -> list[m.Lideranca]: ...
    @overload
    def liderancas(self, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def liderancas(self, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def liderancas(self, *, formato: Literal["url"]) -> str: ...
    @overload
    def licencas(
        self, inicio: date | None = None, index: bool = False, formato: Literal["bruto"] | None = None
    ) -> Any: ...
    @overload
    def licencas(
        self, inicio: date | None = None, index: bool = False, *, formato: Literal["json"]
    ) -> list[dict[str, Any]]: ...
    @overload
    def licencas(
        self, inicio: date | None = None, index: bool = False, *, formato: Literal["pydantic"]
    ) -> list[m.Licenca]: ...
    @overload
    def licencas(
        self, inicio: date | None = None, index: bool = False, *, formato: Literal["pandas"]
    ) -> DataFramePandas: ...
    @overload
    def licencas(
        self, inicio: date | None = None, index: bool = False, *, formato: Literal["polars"]
    ) -> DataFramePolars: ...
    @overload
    def licencas(self, inicio: date | None = None, index: bool = False, *, formato: Literal["url"]) -> str: ...
    @overload
    def profissoes(self, formato: Literal["bruto"] | None = None) -> Any: ...
    @overload
    def profissoes(self, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
    @overload
    def profissoes(self, *, formato: Literal["pydantic"]) -> list[m.Profissao]: ...
    @overload
    def profissoes(self, *, formato: Literal["pandas"]) -> DataFramePandas: ...
    @overload
    def profissoes(self, *, formato: Literal["polars"]) -> DataFramePolars: ...
    @overload
    def profissoes(self, *, formato: Literal["url"]) -> str: ...
    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = None,
        comissao: str | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = None,
        comissao: str | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = None,
        comissao: str | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Relatoria]: ...
    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = None,
        comissao: str | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = None,
        comissao: str | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = None,
        comissao: str | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        *,
        formato: Literal["url"],
    ) -> str: ...
    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        formato: Literal["bruto"] | None = None,
    ) -> Any: ...
    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...
    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Voto]: ...
    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...
    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...
    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        *,
        formato: Literal["url"],
    ) -> str: ...

@overload
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
    uf: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    partido: str | None = None,
    contendo: str | None = None,
    excluindo: str | None = None,
    url: bool = True,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
    uf: str | None = None,
    sexo: Literal["f", "m"] | None = None,
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
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
    uf: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    partido: str | None = None,
    contendo: str | None = None,
    excluindo: str | None = None,
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Senador]: ...
@overload
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
    uf: str | None = None,
    sexo: Literal["f", "m"] | None = None,
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
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
    uf: str | None = None,
    sexo: Literal["f", "m"] | None = None,
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
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
    uf: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    partido: str | None = None,
    contendo: str | None = None,
    excluindo: str | None = None,
    url: bool = True,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
