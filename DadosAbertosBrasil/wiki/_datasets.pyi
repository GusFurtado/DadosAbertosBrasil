# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from typing import Any, Literal, overload

from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

Dataset = Literal["governadores", "prefeitos_capitais", "ministros", "tribunais", "partidos", "ufs", "municipios"]

def metadados(dataset: Dataset, verificar_certificado: bool | None = None) -> dict: ...
@overload
def governadores(
    uf: str | None = None, formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None
) -> Any: ...
@overload
def governadores(
    uf: str | None = None, *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def governadores(
    uf: str | None = None, *, formato: Literal["pydantic"], verificar_certificado: bool | None = None
) -> list[m.Governador]: ...
@overload
def governadores(
    uf: str | None = None, *, formato: Literal["pandas"], verificar_certificado: bool | None = None
) -> DataFramePandas: ...
@overload
def governadores(
    uf: str | None = None, *, formato: Literal["polars"], verificar_certificado: bool | None = None
) -> DataFramePolars: ...
@overload
def governadores(
    uf: str | None = None, *, formato: Literal["url"], verificar_certificado: bool | None = None
) -> str: ...
@overload
def prefeitos_capitais(
    uf: str | None = None, formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None
) -> Any: ...
@overload
def prefeitos_capitais(
    uf: str | None = None, *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def prefeitos_capitais(
    uf: str | None = None, *, formato: Literal["pydantic"], verificar_certificado: bool | None = None
) -> list[m.PrefeitoCapital]: ...
@overload
def prefeitos_capitais(
    uf: str | None = None, *, formato: Literal["pandas"], verificar_certificado: bool | None = None
) -> DataFramePandas: ...
@overload
def prefeitos_capitais(
    uf: str | None = None, *, formato: Literal["polars"], verificar_certificado: bool | None = None
) -> DataFramePolars: ...
@overload
def prefeitos_capitais(
    uf: str | None = None, *, formato: Literal["url"], verificar_certificado: bool | None = None
) -> str: ...
@overload
def ministros(
    em_exercicio: bool | None = None, formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None
) -> Any: ...
@overload
def ministros(
    em_exercicio: bool | None = None, *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def ministros(
    em_exercicio: bool | None = None, *, formato: Literal["pydantic"], verificar_certificado: bool | None = None
) -> list[m.Ministro]: ...
@overload
def ministros(
    em_exercicio: bool | None = None, *, formato: Literal["pandas"], verificar_certificado: bool | None = None
) -> DataFramePandas: ...
@overload
def ministros(
    em_exercicio: bool | None = None, *, formato: Literal["polars"], verificar_certificado: bool | None = None
) -> DataFramePolars: ...
@overload
def ministros(
    em_exercicio: bool | None = None, *, formato: Literal["url"], verificar_certificado: bool | None = None
) -> str: ...
@overload
def tribunais(
    tribunal: Literal["STF", "STJ", "TST", "STM", "TCU"] | None = None,
    formato: Literal["bruto"] | None = None,
    verificar_certificado: bool | None = None,
) -> Any: ...
@overload
def tribunais(
    tribunal: Literal["STF", "STJ", "TST", "STM", "TCU"] | None = None,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = None,
) -> list[dict[str, Any]]: ...
@overload
def tribunais(
    tribunal: Literal["STF", "STJ", "TST", "STM", "TCU"] | None = None,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = None,
) -> list[m.MinistroTribunal]: ...
@overload
def tribunais(
    tribunal: Literal["STF", "STJ", "TST", "STM", "TCU"] | None = None,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = None,
) -> DataFramePandas: ...
@overload
def tribunais(
    tribunal: Literal["STF", "STJ", "TST", "STM", "TCU"] | None = None,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = None,
) -> DataFramePolars: ...
@overload
def tribunais(
    tribunal: Literal["STF", "STJ", "TST", "STM", "TCU"] | None = None,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = None,
) -> str: ...
@overload
def partidos(
    ativos: bool | None = None, formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None
) -> Any: ...
@overload
def partidos(
    ativos: bool | None = None, *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def partidos(
    ativos: bool | None = None, *, formato: Literal["pydantic"], verificar_certificado: bool | None = None
) -> list[m.Partido]: ...
@overload
def partidos(
    ativos: bool | None = None, *, formato: Literal["pandas"], verificar_certificado: bool | None = None
) -> DataFramePandas: ...
@overload
def partidos(
    ativos: bool | None = None, *, formato: Literal["polars"], verificar_certificado: bool | None = None
) -> DataFramePolars: ...
@overload
def partidos(
    ativos: bool | None = None, *, formato: Literal["url"], verificar_certificado: bool | None = None
) -> str: ...
@overload
def ufs(formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None) -> Any: ...
@overload
def ufs(*, formato: Literal["json"], verificar_certificado: bool | None = None) -> list[dict[str, Any]]: ...
@overload
def ufs(*, formato: Literal["pydantic"], verificar_certificado: bool | None = None) -> list[m.UF]: ...
@overload
def ufs(*, formato: Literal["pandas"], verificar_certificado: bool | None = None) -> DataFramePandas: ...
@overload
def ufs(*, formato: Literal["polars"], verificar_certificado: bool | None = None) -> DataFramePolars: ...
@overload
def ufs(*, formato: Literal["url"], verificar_certificado: bool | None = None) -> str: ...
@overload
def municipios(
    uf: str | None = None, formato: Literal["bruto"] | None = None, verificar_certificado: bool | None = None
) -> Any: ...
@overload
def municipios(
    uf: str | None = None, *, formato: Literal["json"], verificar_certificado: bool | None = None
) -> list[dict[str, Any]]: ...
@overload
def municipios(
    uf: str | None = None, *, formato: Literal["pydantic"], verificar_certificado: bool | None = None
) -> list[m.Municipio]: ...
@overload
def municipios(
    uf: str | None = None, *, formato: Literal["pandas"], verificar_certificado: bool | None = None
) -> DataFramePandas: ...
@overload
def municipios(
    uf: str | None = None, *, formato: Literal["polars"], verificar_certificado: bool | None = None
) -> DataFramePolars: ...
@overload
def municipios(uf: str | None = None, *, formato: Literal["url"], verificar_certificado: bool | None = None) -> str: ...
