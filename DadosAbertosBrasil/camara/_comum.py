"""Partes comuns das consultas à API da Câmara dos Deputados."""

from datetime import date
from typing import Any

from pydantic import Field, PositiveInt, computed_field

from ..utils.modelos import Params, Registro
from ..utils.requisicao import Requisicao
from ..utils.saida import consultar


class ParamsCamara(Params):
    """Datas em ISO-8601 e booleanos como `true`/`false`."""


class Paginacao(ParamsCamara):
    pagina: PositiveInt = 1
    itens: PositiveInt | None = None


class Ordenacao(Paginacao):
    asc: bool = Field(True, exclude=True)
    ordenar_por: str | None = Field(None, serialization_alias="ordenarPor")

    @computed_field
    @property
    def ordem(self) -> str:
        return "asc" if self.asc else "desc"


class Periodo(ParamsCamara):
    inicio: date | None = Field(None, serialization_alias="dataInicio")
    fim: date | None = Field(None, serialization_alias="dataFim")


def requisicao(
    path: list,
    params: Params | None = None,
    verificar_certificado: bool | None = None,
    cacheavel: bool = False,
) -> Requisicao:
    return Requisicao(
        endpoint="camara",
        path=path,
        params=params.para_api() if params is not None else None,
        chaves=["dados"],
        verificar_certificado=verificar_certificado,
        cacheavel=cacheavel,
    )


def consultar_camara(
    path: list,
    params: Params | None,
    modelo: type[Registro],
    formato: str | None,
    *,
    url: bool = True,
    index: bool = False,
    index_col: str | None = "codigo",
    verificar_certificado: bool | None = None,
    cacheavel: bool = False,
) -> Any:
    return consultar(
        requisicao(path, params, verificar_certificado, cacheavel),
        modelo,
        formato,
        url=url,
        index=index,
        index_col=index_col,
    )
