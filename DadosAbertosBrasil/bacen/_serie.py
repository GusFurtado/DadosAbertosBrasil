from datetime import date
from typing import Optional

import pandas as pd
from pydantic import validate_call, PositiveInt

from ..utils import Get, parse, Formato, Output


@validate_call
def serie(
    cod: PositiveInt,
    ultimos: Optional[PositiveInt] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
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

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
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

    path = ["dados", "serie", f"bcdata.sgs.{cod}", "dados"]
    if ultimos is not None:
        path += ["ultimos", str(ultimos)]

    params = []
    if inicio is not None:
        params.append(f"dataInicial={parse.data(inicio, modulo='sgs')}")
    if fim is not None:
        params.append(f"dataFinal={parse.data(fim, modulo='sgs')}")

    if len(params) > 0:
        path += [f'?{"&".join(params)}']

    data = Get(
        endpoint="sgs",
        path=path,
        verify=verificar_certificado,
    ).get(formato)

    if formato == "pandas":
        data["data"] = pd.to_datetime(data["data"], format="%d/%m/%Y")
        if "datafim" in data.columns:
            data["datafim"] = pd.to_datetime(data["datafim"], format="%d/%m/%Y")

        if index:
            data.set_index("data", inplace=True)

    return data
