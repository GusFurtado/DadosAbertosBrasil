# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from typing import Any, Literal, overload

from pydantic import PositiveInt

from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

@overload
def nomes(
    nomes: list[str] | str,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def nomes(
    nomes: list[str] | str,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def nomes(
    nomes: list[str] | str,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.FrequenciaNomes]: ...
@overload
def nomes(
    nomes: list[str] | str,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def nomes(
    nomes: list[str] | str,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def nomes(
    nomes: list[str] | str,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def nomes_uf(nome: str, formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None) -> Any: ...
@overload
def nomes_uf(
    nome: str, *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def nomes_uf(
    nome: str, *, formato: Literal["pydantic"], verificar_certificado: bool | None = None
) -> list[m.NomeUF]: ...
@overload
def nomes_uf(
    nome: str, *, formato: Literal["pandas"], verificar_certificado: bool | None = None
) -> DataFramePandas: ...
@overload
def nomes_uf(
    nome: str, *, formato: Literal["polars"], verificar_certificado: bool | None = None
) -> DataFramePolars: ...
@overload
def nomes_uf(nome: str, *, formato: Literal["url"], verificar_certificado: bool | None = None) -> str: ...
@overload
def nomes_ranking(
    decada: PositiveInt | None = None,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def nomes_ranking(
    decada: PositiveInt | None = None,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def nomes_ranking(
    decada: PositiveInt | None = None,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.RankingNome]: ...
@overload
def nomes_ranking(
    decada: PositiveInt | None = None,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def nomes_ranking(
    decada: PositiveInt | None = None,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def nomes_ranking(
    decada: PositiveInt | None = None,
    sexo: Literal["f", "m"] | None = None,
    localidade: PositiveInt | None = None,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
