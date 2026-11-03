"""Partes comuns das consultas à API do Senado Federal."""

import re
from collections.abc import Callable
from typing import Any

from ..utils.modelos import Params, Registro
from ..utils.requisicao import Requisicao
from ..utils.saida import consultar


class ParamsSenado(Params):
    """Datas no formato `AAAAMMDD` e booleanos como `S`/`N`."""

    formato_data = "%Y%m%d"
    verdadeiro = "S"
    falso = "N"


def requisicao(
    path: list,
    chaves: list[str],
    params: Params | None = None,
    verificar_certificado: bool | None = None,
    cacheavel: bool = False,
) -> Requisicao:
    return Requisicao(
        endpoint="senado",
        path=path,
        params=params.para_api() if params is not None else None,
        chaves=chaves,
        verificar_certificado=verificar_certificado,
        cacheavel=cacheavel,
    )


def consultar_senado(
    path: list,
    chaves: list[str],
    params: Params | None,
    modelo: type[Registro],
    formato: str | None,
    *,
    url: bool = True,
    index: bool = False,
    index_col: str | None = "codigo",
    filtro: Callable[[Registro], bool] | None = None,
    verificar_certificado: bool | None = None,
    cacheavel: bool = False,
) -> Any:
    return consultar(
        requisicao(path, chaves, params, verificar_certificado, cacheavel),
        modelo,
        formato,
        url=url,
        index=index,
        index_col=index_col,
        filtro=filtro,
    )


_SEXOS = {"f": "Feminino", "m": "Masculino"}


def filtro_parlamentares(
    sexo: str | None = None,
    partido: str | None = None,
    uf: str | None = None,
    contendo: str | None = None,
    excluindo: str | None = None,
) -> Callable[[Registro], bool] | None:
    """Filtro de senadores por sexo, partido, UF e trecho (regex) do nome."""
    if not any((sexo, partido, uf, contendo, excluindo)):
        return None

    def contem(registro: Registro, padrao: str) -> bool:
        return any(
            isinstance(nome, str) and re.search(padrao, nome)
            for nome in (registro.nome_parlamentar, registro.nome_completo)
        )

    def filtro(registro: Registro) -> bool:
        if sexo is not None and registro.sexo != _SEXOS[sexo]:
            return False
        if partido is not None and registro.partido != partido.upper():
            return False
        if uf is not None and registro.uf != uf:
            return False
        if contendo is not None and not contem(registro, contendo):
            return False
        return excluindo is None or not contem(registro, excluindo)

    return filtro
