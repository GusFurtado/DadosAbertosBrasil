"""Módulo de captura de dados das APIs do Banco Central do Brasil.

References
----------
.. [1] SGS - Sistema Gerenciador de Séries Temporais
    https://www3.bcb.gov.br/sgspub/
.. [2] Cotação do Câmbio
    https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3
.. [3] Expectativas de Mercado
    https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/swagger-ui3#/

"""

from datetime import datetime
from typing import Union, Optional

import pandas as pd

from ._utils import parse
from ._utils.get_data import get_data


def _df(path: str, params: dict = None) -> pd.DataFrame:
    data = get_data(
        endpoint="https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/",
        path=path,
        params=params,
    )
    return pd.DataFrame(data["value"])


def moedas() -> pd.DataFrame:
    """Obtém os nomes e símbolos das principais moedas internacionais.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os nomes e símbolos das principais moedas
        internacionais.

    See Also
    --------
    DadosAbertosBrasil.bacen.cambio :
        Utilize a função `bacen.moedas` para identificar os argumentos da
        função `bacen.cambio`.

    Notes
    -----
    Moedas do tipo 'A':
        - Para calcular o valor equivalente em US$ (dólar americano), divida o
          montante na moeda consultada pela respectiva paridade.
        - Para obter o valor em R$ (reais), multiplique o montante na moeda
          consultada pela respectiva taxa.
    Moedas do tipo 'B':
        - Para calcular o valor equivalente em US$ (dólar americano),
          multiplique o montante na moeda consultada pela respectiva paridade.
        - Para obter o valor em R$ (reais), multiplique o montante na moeda
          consultada pela respectiva taxa.

    References
    ----------
    .. [1] Cotação do Câmbio
        https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3

    Examples
    --------
    >>> bacen.moedas()
      simbolo                      nome tipo
    0     AUD         Dólar australiano    B
    1     CAD           Dólar canadense    A
    2     CHF              Franco suíço    A
    3     DKK        Coroa dinamarquesa    A
    4     EUR                      Euro    B
    5     GBP           Libra Esterlina    B
    6     JPY                      Iene    A
    7     NOK          Coroa norueguesa    A
    8     SEK               Coroa sueca    A
    9     USD  Dólar dos Estados Unidos    A

    """

    df = _df("Moedas")
    df.columns = ["simbolo", "nome", "tipo"]
    return df


def cambio(
    moedas="USD",
    inicio: Union[datetime, str] = "2000-01-01",
    fim: Union[datetime, str] = None,
    cotacao: str = "compra",
    boletim: str = "fechamento",
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
    if fim is None:
        fim = datetime.today().strftime("%m-%d-%Y")
    else:
        fim = parse.data(fim, "bacen")

    moedas = parse.moeda(moedas)

    cotacao_moedas = []
    for moeda in moedas:
        cotacao_moeda = _df(
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
        cotacao_moeda.dataHoraCotacao = cotacao_moeda.dataHoraCotacao.apply(
            lambda x: datetime.strptime(x[:10], "%Y-%m-%d")
        )

        cotacao_moedas.append(
            cotacao_moeda.rename(
                columns={f"cotacao{cotacao.title()}": moeda, "dataHoraCotacao": "Data"}
            )
            .groupby("Data")
            .last()
        )

    cotacoes = pd.concat(cotacao_moedas, axis=1).reset_index()

    cotacoes.Data = pd.to_datetime(cotacoes.Data, format="%Y-%m-%d %H:%M:%S")
    if index:
        cotacoes.set_index("Data", inplace=True)

    return cotacoes


def serie(
    cod: int,
    ultimos: Optional[int] = None,
    inicio: Union[datetime, str] = None,
    fim: Union[datetime, str] = None,
    index: bool = False,
) -> pd.DataFrame:
    """Série do Sistema Gerenciador de Série Temporais (SGS) do Banco Central.

    Parameters
    ----------
    cod : int
        Código da série temporal.
        Utilize o seguinte link para obter o número da série desejada:
        https://www3.bcb.gov.br/sgspub/
    ultimos : int, optional
        Retorna os últimos N valores da série numérica.
    inicio : datetime or str, optional
        Valor datetime ou string no formato de data 'AAAA-MM-DD' que
        representa o primeiro dia da pesquisa.
    fim : datetime or str, optional
        Valor datetime ou string no formato de data 'AAAA-MM-DD' que
        representa o último dia da pesquisa. Caso este campo seja None, será
        considerada a data de hoje.
    index : bool, default=False
        Define se a coluna 'data' será o index do DataFrame.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os valores da série temporal pesquisada.

    Raises
    ------
    JSONDecodeError
        Em caso de parâmetros inválidos.

    See Also
    --------
    DadosAbertosBrasil.favoritos :
        O módulo `favoritos` apresenta as principais séries temporáis do Banco
        Central do Brasil.

    Notes
    -----
    Os argumentos `inicio` e `fim` devem ser usados em conjunto para
    funcionar.

    References
    ----------
    .. [1] SGS - Sistema Gerenciador de Séries Temporais
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

    path = f"dados/serie/bcdata.sgs.{cod}/dados"
    if ultimos is not None:
        path += f"/ultimos/{ultimos}"

    params = []
    if inicio is not None:
        params.append(f"dataInicial={parse.data(inicio, modulo='sgs')}")
    if fim is not None:
        params.append(f"dataFinal={parse.data(fim, modulo='sgs')}")

    if len(params) > 0:
        path += f'?{"&".join(params)}'

    data = get_data(endpoint="https://api.bcb.gov.br/", path=path)

    df = pd.DataFrame(data)

    df.data = pd.to_datetime(df.data, format="%d/%m/%Y")
    if "datafim" in df.columns:
        df.datafim = pd.to_datetime(df.datafim, format="%d/%m/%Y")

    if index:
        df.set_index("data", inplace=True)

    return df


def expectativas(
    expectativa: str,
    indicador: Optional[str] = None,
    top: Optional[int] = None,
    ordenar_por: str = "Data",
    asc: bool = False,
) -> pd.DataFrame:
    """Expectativas de mercado para os principais indicadores macroeconômicos.

    Parameters
    ----------
    expectativa : str
        'mensal' ou 'mensais'
            Expectativas de Mercado Mensal
        'selic'
            Expectativas de Mercado Selic
        'trimestral' ou 'trimestrais'
            Expectativas de Mercado Trimestral
        'anual' ou 'anuais'
            Expectativas de Mercado com referência anual
        'inflacao' ou 'inflacao12meses'
            Expectativas de mercado para inflação nos próximos 12 meses
        'top5mensal' ou 'top5mensais'
            Expectativas mensais de mercado para os indicadores do Top 5
        'top5anual' ou 'top5anuais'
            Expectativas de mercado anuais para os indicadores do Top 5
        'instituicoes'.
            Expectativas de mercado informadas pelas instituições credenciadas
    indicador : str, optional
        Capturar apenas o indicador desejado. Deve ser um dos seguintes
        indicadores, desde que esteja de acordo com a `expectativa` escolhida:
            'Balança Comercial',
            'Câmbio',
            'Conta corrente',
            'Dívida bruta do governo geral',
            'Dívida líquida do setor público',
            'IGP-DI',
            'IGP-M',
            'INPC',
            'Investimento direto no país',
            'IPA-DI',
            'IPA-M',
            'IPCA',
            'IPCA Administrados',
            'IPCA Alimentação no domicílio',
            'IPCA Bens industrializados',
            'IPCA Livres',
            'IPCA Serviços',
            'IPCA-15',
            'IPC-FIPE',
            'PIB Agropecuária',
            'PIB Despesa de consumo da administração pública',
            'PIB despesa de consumo das famílias',
            'PIB Exportação de bens e serviços',
            'PIB Formação Bruta de Capital Fixo',
            'PIB Importação de bens e serviços',
            'PIB Indústria',
            'PIB Serviços',
            'PIB Total',
            'Produção industrial',
            'Resultado nominal',
            'Resultado primário',
            'Selic',
            'Taxa de desocupação'
        Caso o valor seja None, retorna todos os indicadores disponíveis.
    top : int, optional
        Número máximo de registros que será retornado.
    ordenar_por : str, default='Data'
        Por qual coluna da tabela os registros serão ordenados.
    asc : bool, default=False
        - Se True, ordena os registros pela coluna selecionada no argumento
          `ordenar_por` em ordem crescente (A-Z ou 0-9);
        - Se False, ordena em ordem descrescente (Z-A ou 9-0).

    Returns
    -------
    pandas.core.frame.DataFrame
        Tabela contendo uma breve estatística descritiva da expectativa de
        mercado de cada indicador poe período de referência.

    Raises
    ------
    ValueError
        Em caso de parâmetros inválidos.

    Notes
    -----
    Base de Cálculo 0:
        Uso das expectativas mais recentes informadas pelas instituições
        participantes a partir do 30º dia anterior à data de cálculo das
        estatísticas.
    Base de Cálculo 1:
        Uso das expectativas mais recentes informadas pelas instituições
        participantes a partir do 4º dia útil anterior à data de cálculo
        das estatísticas.

    References
    ----------
    .. [1] Expectativas de Mercado
        https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/swagger-ui3#/

    Examples
    --------
    >>> bacen.expectativa(expectativa='mensal', indicador='IGP-M')
          Indicador        Data DataReferencia  Media  Mediana  DesvioPadrao  ...
    0         IGP-M  2021-06-25        07/2022   0.31     0.30          0.21  ...
    1         IGP-M  2021-06-25        07/2021   0.64     0.61          0.42  ...
    2         IGP-M  2021-06-25        06/2021   1.25     1.10          0.58  ...
    3         IGP-M  2021-06-25        11/2022   0.47     0.47          0.16  ...
    4         IGP-M  2021-06-25        11/2021   0.50     0.50          0.24  ...
    ..          ...         ...            ...    ...      ...           ...  ...

    >>> bacen.expectativa(
    ...     expectativa = 'trimestral',
    ...     indicador = 'PIB Total',
    ...     top = 3,
    ...     ordenar_por = 'Media',
    ...     asc = True
    ... )
       Indicador        Data DataReferencia  Media  Mediana  DesvioPadrao  ...
    0  PIB Total  2020-06-02         2/2020 -14.00    -14.0          3.92  ...
    1  PIB Total  2020-06-09         2/2020 -14.00    -13.4          3.55  ...
    2  PIB Total  2020-06-01         2/2020 -13.99    -14.0          3.91  ...

    """

    URL = "https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/"

    orderby = f'&%24orderby={ordenar_por}%20{"asc" if asc else "desc"}'
    topn = "" if top is None else f"&%24top={top}"

    expectativa = expectativa.lower()
    if expectativa in ("mensal", "mensais"):
        expec = "ExpectativaMercadoMensais"
        KPIS = (
            "Câmbio",
            "IGP-DI",
            "IGP-M",
            "INPC",
            "IPA-DI",
            "IPA-M",
            "IPCA",
            "IPCA Administrados",
            "IPCA Alimentação no domicílio",
            "IPCA Bens industrializados",
            "IPCA Livres",
            "IPCA Serviços",
            "IPCA-15",
            "IPC-Fipe",
            "Produção industrial",
            "Selic",
            "Taxa de desocupação",
        )
    elif expectativa in ("selic"):
        expec = "ExpectativasMercadoSelic"
        KPIS = ("Selic",)
    elif expectativa in ("trimestral", "trimestrais"):
        expec = "ExpectativasMercadoTrimestrais"
        KPIS = (
            "Câmbio",
            "IPCA",
            "IPCA Administrados",
            "IPCA Alimentação no domicílio",
            "IPCA Bens industrializados",
            "IPCA Livres",
            "IPCA Serviços",
            "PIB Agropecuária",
            "PIB Indústria",
            "PIB Serviços",
            "PIB Total",
            "Taxa de desocupação",
        )
    elif expectativa in ("anual", "anuais"):
        expec = "ExpectativasMercadoAnuais"
        KPIS = (
            "Balança Comercial",
            "Câmbio",
            "Conta corrente",
            "Dívida bruta do governo geral",
            "Dívida líquida do setor público",
            "IGP-DI",
            "IGP-M",
            "INPC",
            "Investimento direto no país",
            "IPA-DI",
            "IPA-M",
            "IPCA",
            "IPCA Administrados",
            "IPCA Alimentação no domicílio",
            "IPCA Bens industrializados",
            "IPCA Livres",
            "IPCA Serviços",
            "IPCA-15",
            "IPC-FIPE",
            "PIB Agropecuária",
            "PIB Despesa de consumo da administração pública",
            "PIB despesa de consumo das famílias",
            "PIB Exportação de bens e serviços",
            "PIB Formação Bruta de Capital Fixo",
            "PIB Importação de bens e serviços",
            "PIB Indústria",
            "PIB Serviços",
            "PIB Total",
            "Produção industrial",
            "Resultado nominal",
            "Resultado primário",
            "Selic",
            "Taxa de desocupação",
        )
    elif expectativa in ("inflacao", "inflacao12meses"):
        expec = "ExpectativasMercadoInflacao12Meses"
        KPIS = (
            "IGP-DI",
            "IGP-M",
            "INPC",
            "IPA-DI",
            "IPA-M",
            "IPCA",
            "IPCA Administrados",
            "IPCA Alimentação no domicílio",
            "IPCA Bens industrializados",
            "IPCA Livres",
            "IPCA Serviços",
            "IPCA-15",
            "IPC-FIPE",
        )
    elif expectativa in ("top5mensal", "top5mensais"):
        expec = "ExpectativasMercadoTop5Mensais"
        KPIS = ("Câmbio", "IGP-DI", "IGP-M", "IPCA", "Selic")
    elif expectativa in ("top5anual", "top5anuais"):
        expec = "ExpectativasMercadoTop5Anuais"
        KPIS = ("Câmbio", "IGP-DI", "IGP-M", "IPCA", "Selic")
    elif expectativa == "instituicoes":
        expec = "ExpectativasMercadoInstituicoes"
        KPIS = (
            "Balança Comercial",
            "Câmbio",
            "Conta corrente",
            "Dívida bruta do governo geral",
            "Dívida líquida do setor público",
            "IGP-DI",
            "IGP-M",
            "INPC",
            "Investimento direto no país",
            "IPA-DI",
            "IPA-M",
            "IPCA",
            "IPCA Administrados",
            "IPCA Alimentação no domicílio",
            "IPCA Bens industrializados",
            "IPCA Livres",
            "IPCA Serviços",
            "IPCA-15",
            "IPC-FIPE",
            "PIB Agropecuária",
            "PIB Despesa de consumo da administração pública",
            "PIB despesa de consumo das famílias",
            "PIB Exportação de bens e serviços",
            "PIB Formação Bruta de Capital Fixo",
            "PIB Importação de bens e serviços",
            "PIB Indústria",
            "PIB Serviços",
            "PIB Total",
            "Produção industrial",
            "Resultado nominal",
            "Resultado primário",
            "Selic",
            "Taxa de desocupação",
        )
    else:
        raise ValueError(
            """Valor inválido para o argumento `expectativa`. Insira um dos seguintes valores:
            - 'mensal' ou 'mensais';
            - 'selic';
            - 'trimestral' ou 'trimestrais';
            - 'anual' ou 'anuais';
            - 'inflacao' ou 'inflacao12meses';
            - 'top5mensal' ou 'top5mensais',
            - 'top5anual' ou 'top5anuais',
            - 'instituicoes'."""
        )

    if indicador is None:
        kpi = ""
    elif indicador in KPIS:
        kpi = f"&%24filter=Indicador%20eq%20'{indicador}'"
    else:
        raise ValueError(
            f"""'{indicador}' é um indicador inválido para expectativa '{expectativa.title()}'. Insira um dos seguintes valores:
        - {", ".join(KPIS)}."""
        )

    path = f"{expec}?%24format=json{orderby}{kpi}{topn}"
    data = get_data(URL, path=path)
    return pd.DataFrame(data["value"])
