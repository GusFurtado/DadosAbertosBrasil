from typing import Any, Literal, overload

from pydantic import validate_call

from ..utils.typing import DataFramePandas, DataFramePolars, Formato, Saida
from . import modelos as m
from ._comum import consultar_senado


@overload
def lista_blocos(
    index: bool = ..., formato: Literal["bruto"] | None = ..., verificar_certificado: bool | None = ...
) -> Any: ...


@overload
def lista_blocos(
    index: bool = ..., *, formato: Literal["json"], verificar_certificado: bool | None = ...
) -> list[dict[str, Any]]: ...


@overload
def lista_blocos(
    index: bool = ..., *, formato: Literal["pydantic"], verificar_certificado: bool | None = ...
) -> list[m.Bloco]: ...


@overload
def lista_blocos(
    index: bool = ..., *, formato: Literal["pandas"], verificar_certificado: bool | None = ...
) -> DataFramePandas: ...


@overload
def lista_blocos(
    index: bool = ..., *, formato: Literal["polars"], verificar_certificado: bool | None = ...
) -> DataFramePolars: ...


@overload
def lista_blocos(index: bool = ..., *, formato: Literal["url"], verificar_certificado: bool | None = ...) -> str: ...


@validate_call
def lista_blocos(
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Obtém a lista e a composição dos Blocos Parlamentares no
    Congresso Nacional.

    Parameters
    ----------
    index : bool, default=False
        Se True, define a coluna `codigo` como index do DataFrame.
        Só se aplica ao formato 'pandas'; com 'polars', é ignorado com aviso.

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": JSON original da API, como veio;
        - "pydantic": lista de modelos Pydantic, um por registro;
        - "pandas": DataFrame pandas;
        - "polars": DataFrame polars;
        - "url": endereço da consulta.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
        Lista de Blocos Parlamentares no Congresso Nacional.

    """

    return consultar_senado(
        ["blocoParlamentar", "lista"],
        ["ListaBlocoParlamentar", "Blocos", "Bloco"],
        None,
        m.Bloco,
        formato,
        index=index,
        verificar_certificado=verificar_certificado,
    )
