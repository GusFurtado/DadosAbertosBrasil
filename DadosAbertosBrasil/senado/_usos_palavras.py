import functools
from typing import Any, Literal, overload

from pydantic import Field, validate_call

from ..utils.errors import descontinuado
from ..utils.modelos import com_params
from ..utils.typing import DataFramePandas, DataFramePolars, Formato, Saida
from . import modelos as m
from ._comum import ParamsSenado, consultar_senado


class _ParamsTiposUsoPalavra(ParamsSenado):
    ativos: bool = Field(False, serialization_alias="indAtivos")


@overload
def lista_tipos_uso_palavra(
    ativos: bool = ...,
    index: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def lista_tipos_uso_palavra(
    ativos: bool = ..., index: bool = ..., *, formato: Literal["json"], verificar_certificado: bool | None = ...
) -> list[dict[str, Any]]: ...


@overload
def lista_tipos_uso_palavra(
    ativos: bool = ..., index: bool = ..., *, formato: Literal["pydantic"], verificar_certificado: bool | None = ...
) -> list[m.TipoUsoPalavra]: ...


@overload
def lista_tipos_uso_palavra(
    ativos: bool = ..., index: bool = ..., *, formato: Literal["pandas"], verificar_certificado: bool | None = ...
) -> DataFramePandas: ...


@overload
def lista_tipos_uso_palavra(
    ativos: bool = ..., index: bool = ..., *, formato: Literal["polars"], verificar_certificado: bool | None = ...
) -> DataFramePolars: ...


@overload
def lista_tipos_uso_palavra(
    ativos: bool = ..., index: bool = ..., *, formato: Literal["url"], verificar_certificado: bool | None = ...
) -> str: ...


@validate_call
@com_params(_ParamsTiposUsoPalavra)
def lista_tipos_uso_palavra(
    ativos: bool = False,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Lista os tipos de uso da palavra.

    Parameters
    ----------
    ativos : bool, default=False
        Se True, retorna apenas os tipos de uso de palavra atualmente ativos.

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
        Lista os tipos de uso da palavra.

    """

    return consultar_senado(
        ["senador", "lista", "tiposUsoPalavra"],
        ["ListaTiposUsoPalavra", "TiposUsoPalavra", "TipoUsoPalavra"],
        _ParamsTiposUsoPalavra.de_locais(locals()),
        m.TipoUsoPalavra,
        formato,
        index=index,
        verificar_certificado=verificar_certificado,
        cacheavel=True,
    )


@functools.wraps(lista_tipos_uso_palavra)
def lista_uso_palavra(*args, **kwargs):
    """Nome antigo de `lista_tipos_uso_palavra`.

    Descontinuado: use `senado.lista_tipos_uso_palavra`.
    """
    descontinuado(
        "`senado.lista_uso_palavra` foi renomeada para `senado.lista_tipos_uso_palavra` e o nome "
        "antigo deixa de existir em uma versão futura do 3.x."
    )
    return lista_tipos_uso_palavra(*args, **kwargs)
