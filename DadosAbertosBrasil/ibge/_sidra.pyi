# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from typing import Any, Literal, overload

from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

@overload
def lista_tabelas(
    contendo: str | None = None,
    excluindo: str | None = None,
    assunto: int | str | None = None,
    classificacao: int | str | None = None,
    periodo: dict | str | None = None,
    periodicidade: int | str | None = None,
    nivel: int | str | None = None,
    pesquisa: str | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def lista_tabelas(
    contendo: str | None = None,
    excluindo: str | None = None,
    assunto: int | str | None = None,
    classificacao: int | str | None = None,
    periodo: dict | str | None = None,
    periodicidade: int | str | None = None,
    nivel: int | str | None = None,
    pesquisa: str | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def lista_tabelas(
    contendo: str | None = None,
    excluindo: str | None = None,
    assunto: int | str | None = None,
    classificacao: int | str | None = None,
    periodo: dict | str | None = None,
    periodicidade: int | str | None = None,
    nivel: int | str | None = None,
    pesquisa: str | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.Tabela]: ...
@overload
def lista_tabelas(
    contendo: str | None = None,
    excluindo: str | None = None,
    assunto: int | str | None = None,
    classificacao: int | str | None = None,
    periodo: dict | str | None = None,
    periodicidade: int | str | None = None,
    nivel: int | str | None = None,
    pesquisa: str | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def lista_tabelas(
    contendo: str | None = None,
    excluindo: str | None = None,
    assunto: int | str | None = None,
    classificacao: int | str | None = None,
    periodo: dict | str | None = None,
    periodicidade: int | str | None = None,
    nivel: int | str | None = None,
    pesquisa: str | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def lista_tabelas(
    contendo: str | None = None,
    excluindo: str | None = None,
    assunto: int | str | None = None,
    classificacao: int | str | None = None,
    periodo: dict | str | None = None,
    periodicidade: int | str | None = None,
    nivel: int | str | None = None,
    pesquisa: str | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def lista_pesquisas(index: bool = False, formato: Literal["bruto"] | None = None) -> Any: ...
@overload
def lista_pesquisas(index: bool = False, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...
@overload
def lista_pesquisas(index: bool = False, *, formato: Literal["pydantic"]) -> list[m.Pesquisa]: ...
@overload
def lista_pesquisas(index: bool = False, *, formato: Literal["pandas"]) -> DataFramePandas: ...
@overload
def lista_pesquisas(index: bool = False, *, formato: Literal["polars"]) -> DataFramePolars: ...
@overload
def lista_pesquisas(index: bool = False, *, formato: Literal["url"]) -> str: ...

class Metadados:
    dados: dict[str, Any]
    cod: int
    nome: str
    assunto: str
    periodos: dict[str, Any]
    localidades: dict[str, Any]
    variaveis: list[dict[str, Any]]
    classificacoes: list[dict[str, Any]]

    def __init__(self, tabela: int) -> None: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...

@overload
def sidra(
    tabela: int,
    periodos: list | int | str = "last",
    variaveis: list | int | str = "allxp",
    localidades: dict = ...,
    classificacoes: dict | None = None,
    ufs_extintas: bool = False,
    decimais: int | None = None,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def sidra(
    tabela: int,
    periodos: list | int | str = "last",
    variaveis: list | int | str = "allxp",
    localidades: dict = ...,
    classificacoes: dict | None = None,
    ufs_extintas: bool = False,
    decimais: int | None = None,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def sidra(
    tabela: int,
    periodos: list | int | str = "last",
    variaveis: list | int | str = "allxp",
    localidades: dict = ...,
    classificacoes: dict | None = None,
    ufs_extintas: bool = False,
    decimais: int | None = None,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.ValorSidra]: ...
@overload
def sidra(
    tabela: int,
    periodos: list | int | str = "last",
    variaveis: list | int | str = "allxp",
    localidades: dict = ...,
    classificacoes: dict | None = None,
    ufs_extintas: bool = False,
    decimais: int | None = None,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def sidra(
    tabela: int,
    periodos: list | int | str = "last",
    variaveis: list | int | str = "allxp",
    localidades: dict = ...,
    classificacoes: dict | None = None,
    ufs_extintas: bool = False,
    decimais: int | None = None,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def sidra(
    tabela: int,
    periodos: list | int | str = "last",
    variaveis: list | int | str = "allxp",
    localidades: dict = ...,
    classificacoes: dict | None = None,
    ufs_extintas: bool = False,
    decimais: int | None = None,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.ReferenciaSidra]: ...
@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
