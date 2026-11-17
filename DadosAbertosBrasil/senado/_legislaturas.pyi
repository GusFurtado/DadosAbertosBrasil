# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.
from typing import Any, Literal, overload

from typing_extensions import deprecated

from ..utils.typing import DataFramePandas, DataFramePolars
from . import modelos as m

@overload
def lista_legislaturas(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
def lista_legislaturas(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
def lista_legislaturas(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
def lista_legislaturas(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
def lista_legislaturas(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
def lista_legislaturas(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
@overload
@deprecated("Renomeada para `senado.lista_legislaturas`.")
def lista_legislatura(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
@deprecated("Renomeada para `senado.lista_legislaturas`.")
def lista_legislatura(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
@deprecated("Renomeada para `senado.lista_legislaturas`.")
def lista_legislatura(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
@deprecated("Renomeada para `senado.lista_legislaturas`.")
def lista_legislatura(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
@deprecated("Renomeada para `senado.lista_legislaturas`.")
def lista_legislatura(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
@deprecated("Renomeada para `senado.lista_legislaturas`.")
def lista_legislatura(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
