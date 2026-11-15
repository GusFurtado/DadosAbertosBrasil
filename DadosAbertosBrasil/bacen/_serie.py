from datetime import date
from typing import Any, Literal, overload

from pydantic import Field, PositiveInt, validate_call

from ..utils.modelos import Params, com_params
from ..utils.requisicao import Requisicao
from ..utils.saida import consultar
from ..utils.typing import DataFramePandas, DataFramePolars, Formato, Saida
from . import modelos as m


class _ParamsSerie(Params):
    formato_data = "%d/%m/%Y"

    cod: PositiveInt = Field(exclude=True)
    ultimos: PositiveInt | None = Field(None, exclude=True)
    inicio: date | None = Field(None, serialization_alias="dataInicial")
    fim: date | None = Field(None, serialization_alias="dataFinal")


@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    index: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    index: bool = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    index: bool = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.ValorSerie]: ...


@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    index: bool = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    index: bool = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    index: bool = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsSerie)
def serie(
    cod: PositiveInt,
    ultimos: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Série do Sistema Gerenciador de Série Temporais (SGS) do Banco Central.

    Parameters
    ----------
    cod : int
        Código da série temporal.
        Utilize o seguinte link para obter o número da série desejada:
        https://www3.bcb.gov.br/sgspub/

    ultimos : int, optional
        Retorna os últimos N valores da série numérica.

    inicio : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o primeiro dia da pesquisa.

    fim : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o último dia da pesquisa. Caso este campo seja None, será
        considerada a data de hoje.

    index : bool, default=False
        Define se a coluna `"data"` será o index do DataFrame.
        Ignorado com aviso se `formato` for 'polars'.

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
        Valores da série temporal pesquisada.

    Raises
    ------
    JSONDecodeError
        Em caso de parâmetros inválidos.

    See Also
    --------
    DadosAbertosBrasil.favoritos
        O módulo `favoritos` apresenta as principais séries temporáis do Banco
        Central do Brasil.

    Notes
    -----
    Os argumentos `inicio` e `fim` devem ser usados em conjunto para funcionar.

    API original do SGS - Sistema Gerenciador de Séries Temporais
        https://www3.bcb.gov.br/sgspub/

    Examples
    --------
    Capturar a taxa SELIC desde 2010 até 2021.

    >>> bacen.serie(cod=432, inicio='2010-01-01', fim='2021-01-01')
               data valor
    0    2010-01-01  8.75
    1    2010-01-02  8.75
    2    2010-01-03  8.75
    3    2010-01-04  8.75
    4    2010-01-05  8.75
    ..          ...   ...

    Capturar os últimos 5 valores da meta de inflação.

    >>> bacen.serie(cod=13521, ultimos=5)
            data valor
    0 2019-01-01  4.25
    1 2020-01-01  4.00
    2 2021-01-01  3.75
    3 2022-01-01  3.50
    4 2023-01-01  3.25

    Capturar toda a série de reservas internacionais (em milhões de dólares)
    usando a data como index do DataFrame.

    >>> bacen.serie(cod=3546, index=True)
                 valor
    data
    1970-12-01    1187
    1971-01-01    1229
    1971-02-01    1280
    1971-03-01    1316
    1971-04-01    1379
    ...            ...

    """

    params = _ParamsSerie.de_locais(locals())
    path = ["dados", "serie", f"bcdata.sgs.{cod}", "dados"]
    if ultimos is not None:
        path += ["ultimos", ultimos]
    return consultar(
        Requisicao("sgs", path, params.para_api(), verificar_certificado=verificar_certificado),
        m.ValorSerie,
        formato,
        index=index,
        index_col="data",
    )
