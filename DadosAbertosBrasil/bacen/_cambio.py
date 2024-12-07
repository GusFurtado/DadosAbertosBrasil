from datetime import date, datetime
from typing import Literal, Optional

import pandas as pd
from pydantic import Field, validate_call

from ._utils import get_bacen_data
from .._utils import parse


@validate_call
def cambio(
    moedas: list[str] | str = ["USD"],
    inicio: date = date(2000, 1, 1),
    fim: Optional[date] = Field(default_factory=date.today),
    cotacao: Literal["compra", "vendas"] = "compra",
    boletim: Literal["abertura", "intermediário", "fechamento"] = "fechamento",
    index: bool = False,
) -> pd.DataFrame:
    """Taxa de câmbio das principais moedas internacionais.

    É possível escolher várias moedas inserindo uma lista no campo `moeda`.
    Defina o período da consulta pelos campos `inicio` e `fim`.

    Parameters
    ----------
    moedas : str or list of str, default='USD'
        Sigla da moeda ou lista de siglas de moedas que serão pesquisadas no
        formato 'MMM' (três letras). Utilize a função `bacen.moedas` para
        obter a lista de moedas válidas.
    inicio : datetime or str, default='2000-01-01'
        String no formato de data 'AAAA-MM-DD' que representa o primeiro dia
        da pesquisa.
    fim : datetime or str, default=None
        String no formato de data 'AAAA-MM-DD' que representa o último dia da
        pesquisa. Caso este campo seja None, será considerada a data de hoje.
    cotacao : {'compra', 'venda'}, default='compra'
        Tipo de cotação.
    boletim : {'abertura', 'intermediário', 'fechamento'}, default='fechamento'
        Tipo de boletim.
    index : bool, default=False
        Define se a coluna 'Data' será o index do DataFrame.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo as cotações diárias das moedas selecionadas.

    Raises
    ------
    DAB_DataError
        Caso seja inserida uma data inválida.
    DAB_MoedaError
        Caso seja inserida uma moeda inválida.
    ValueError
        Caso nenhum dado seja encontrado devido a argumentos inválidos.

    See Also
    --------
    DadosAbertosBrasil.bacen.moedas :
        Utilize a função `bacen.moedas` para identificar as moedas que serão
        usadas no argumento da função `bacen.cambio`.

    References
    ----------
    .. [1] Cotação do Câmbio
        https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3

    Examples
    --------
    Retornar uma moeda usando argumentos padrões.

    >>> bacen.cambio(moedas='EUR')
                Data      EUR
    0    2000-01-03  1.84601
    1    2000-01-04  1.88695
    2    2000-01-05  1.91121
    3    2000-01-06  1.90357
    4    2000-01-07  1.87790
    ..          ...      ...

    Retornar várias moedas, alterando argumentos.

    >>> bacen.cambio(
    ...     moedas = ['USD', 'CAD'],
    ...     inicio = '2021-01-01',
    ...     fim = '2021-01-10',
    ...     cotacao = 'venda',
    ...     boletim = 'abertura',
    ...     index = True
    ... )
                    USD     CAD
    Data
    2021-01-04  5.1402  4.0500
    2021-01-05  5.3405  4.1890
    2021-01-06  5.3013  4.1798
    2021-01-07  5.3174  4.1833
    2021-01-08  5.3612  4.2237

    """

    inicio = parse.data(inicio, "bacen")
    fim = parse.data(fim, "bacen")
    moedas = parse.moeda(moedas)

    cotacao_moedas = []
    for moeda in moedas:
        cotacao_moeda = get_bacen_data(
            "CotacaoMoedaPeriodo("
            + "moeda=@moeda,"
            + "dataInicial=@dataInicial,"
            + "dataFinalCotacao=@dataFinalCotacao)"
            + f"?@moeda='{moeda}'"
            + f"&@dataInicial='{inicio}'"
            + f"&@dataFinalCotacao='{fim}'"
            + f"&$filter=contains(tipoBoletim%2C'{boletim.title()}')"
            + f"&$select=cotacao{cotacao.title()},dataHoraCotacao"
        )
        if cotacao_moeda.empty:
            raise ValueError(
                "Nenhum dado encontrado. Verifique os argumentos da função."
            )
        cotacao_moeda["dataHoraCotacao"] = cotacao_moeda["dataHoraCotacao"].apply(
            lambda x: datetime.strptime(x[:10], "%Y-%m-%d")
        )
        cotacao_moeda.rename(
            columns={f"cotacao{cotacao.title()}": moeda, "dataHoraCotacao": "data"},
            inplace=True,
        )

        cotacao_moedas.append(cotacao_moeda.groupby("data").last())
    cotacoes = pd.concat(cotacao_moedas, axis=1).reset_index()

    cotacoes["data"] = pd.to_datetime(cotacoes["data"], format="%Y-%m-%d %H:%M:%S")
    if index:
        cotacoes.set_index("data", inplace=True)

    return cotacoes
