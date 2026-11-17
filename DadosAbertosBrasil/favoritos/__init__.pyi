# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from datetime import date
from typing import Any, Literal, NoReturn, overload

from pydantic import PositiveInt
from typing_extensions import deprecated

from ..bacen.modelos import ValorSerie
from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

def bandeira(uf: str, tamanho: PositiveInt = 100) -> str: ...
def brasao(uf: str, tamanho: PositiveInt = 100) -> str: ...
@overload
def catalogo(formato: Literal["bruto"] | None = None) -> Any: ...
@overload
def catalogo(*, formato: Literal["json"]) -> list[dict[str, Any]]: ...
@overload
def catalogo(*, formato: Literal["pydantic"]) -> list[m.Catalogo]: ...
@overload
def catalogo(*, formato: Literal["pandas"]) -> DataFramePandas: ...
@overload
def catalogo(*, formato: Literal["polars"]) -> DataFramePolars: ...
@overload
def catalogo(*, formato: Literal["url"]) -> str: ...
@overload
def codigos_municipios(formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None) -> Any: ...
@overload
def codigos_municipios(
    *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def codigos_municipios(
    *, formato: Literal["pydantic"], verificar_certificado: bool | None = None
) -> list[m.CodigoMunicipio]: ...
@overload
def codigos_municipios(*, formato: Literal["pandas"], verificar_certificado: bool | None = None) -> DataFramePandas: ...
@overload
def codigos_municipios(*, formato: Literal["polars"], verificar_certificado: bool | None = None) -> DataFramePolars: ...
@overload
def codigos_municipios(*, formato: Literal["url"], verificar_certificado: bool | None = None) -> str: ...
@overload
def ipca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def ipca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def ipca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[ValorSerie]: ...
@overload
def ipca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def ipca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def ipca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@deprecated("Removida no 3.0: levanta `DABFuncaoRemovidaError`.")
def perfil_eleitorado(*args, **kwargs) -> NoReturn: ...
@overload
def pib(
    periodo: Literal["anual", "trimestral"] = "anual",
    tipo: Literal["nominal", "real"] = "real",
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def pib(
    periodo: Literal["anual", "trimestral"] = "anual",
    tipo: Literal["nominal", "real"] = "real",
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def pib(
    periodo: Literal["anual", "trimestral"] = "anual",
    tipo: Literal["nominal", "real"] = "real",
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.ValorIpea]: ...
@overload
def pib(
    periodo: Literal["anual", "trimestral"] = "anual",
    tipo: Literal["nominal", "real"] = "real",
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def pib(
    periodo: Literal["anual", "trimestral"] = "anual",
    tipo: Literal["nominal", "real"] = "real",
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def pib(
    periodo: Literal["anual", "trimestral"] = "anual",
    tipo: Literal["nominal", "real"] = "real",
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def rentabilidade_poupanca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def rentabilidade_poupanca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def rentabilidade_poupanca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[ValorSerie]: ...
@overload
def rentabilidade_poupanca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def rentabilidade_poupanca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def rentabilidade_poupanca(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def reservas_internacionais(
    periodo: Literal["diario", "mensal"] = "mensal",
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def reservas_internacionais(
    periodo: Literal["diario", "mensal"] = "mensal",
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def reservas_internacionais(
    periodo: Literal["diario", "mensal"] = "mensal",
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[ValorSerie]: ...
@overload
def reservas_internacionais(
    periodo: Literal["diario", "mensal"] = "mensal",
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def reservas_internacionais(
    periodo: Literal["diario", "mensal"] = "mensal",
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def reservas_internacionais(
    periodo: Literal["diario", "mensal"] = "mensal",
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def risco_brasil(
    index: bool = False, formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None
) -> Any: ...
@overload
def risco_brasil(
    index: bool = False, *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def risco_brasil(
    index: bool = False, *, formato: Literal["pydantic"], verificar_certificado: bool | None = None
) -> list[m.ValorIpea]: ...
@overload
def risco_brasil(
    index: bool = False, *, formato: Literal["pandas"], verificar_certificado: bool | None = None
) -> DataFramePandas: ...
@overload
def risco_brasil(
    index: bool = False, *, formato: Literal["polars"], verificar_certificado: bool | None = None
) -> DataFramePolars: ...
@overload
def risco_brasil(index: bool = False, *, formato: Literal["url"], verificar_certificado: bool | None = None) -> str: ...
@overload
def salario_minimo(
    tipo: Literal["nominal", "ppc", "real"] = "nominal",
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def salario_minimo(
    tipo: Literal["nominal", "ppc", "real"] = "nominal",
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def salario_minimo(
    tipo: Literal["nominal", "ppc", "real"] = "nominal",
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.ValorIpea]: ...
@overload
def salario_minimo(
    tipo: Literal["nominal", "ppc", "real"] = "nominal",
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def salario_minimo(
    tipo: Literal["nominal", "ppc", "real"] = "nominal",
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def salario_minimo(
    tipo: Literal["nominal", "ppc", "real"] = "nominal",
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def selic(
    periodo: Literal["diario", "mensal", "meta"] = "meta",
    anualizado: bool = True,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def selic(
    periodo: Literal["diario", "mensal", "meta"] = "meta",
    anualizado: bool = True,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def selic(
    periodo: Literal["diario", "mensal", "meta"] = "meta",
    anualizado: bool = True,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[ValorSerie]: ...
@overload
def selic(
    periodo: Literal["diario", "mensal", "meta"] = "meta",
    anualizado: bool = True,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def selic(
    periodo: Literal["diario", "mensal", "meta"] = "meta",
    anualizado: bool = True,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def selic(
    periodo: Literal["diario", "mensal", "meta"] = "meta",
    anualizado: bool = True,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def taxa_referencial(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def taxa_referencial(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def taxa_referencial(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[ValorSerie]: ...
@overload
def taxa_referencial(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def taxa_referencial(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def taxa_referencial(
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
