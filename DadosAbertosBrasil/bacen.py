'''
Módulo de captura de dados das APIs do Banco Central do Brasil.

Documentação Original
---------------------
SGS - Sistema Gerenciador de Séries Temporais
    https://www3.bcb.gov.br/sgspub/
Cotação do Câmbio
    https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3
'''



from datetime import datetime

import pandas as _pd

from ._utils import parse
from ._utils.get_data import get_data



def _df(path:str, params:dict=None) -> _pd.DataFrame:
    data = get_data(
        endpoint = 'https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/',
        path = path,
        params = params
    )
    return _pd.DataFrame(data['value'])



def moedas():
    '''
    Obtém os nomes e símbolos das principais moedas internacionais.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os nomes e símbolos das principais moedas
        internacionais.

    Exemplos
    --------
    >>> bacen.moedas()
    ...   simbolo                      nome tipo
    ... 0     AUD         Dólar australiano    B
    ... 1     CAD           Dólar canadense    A
    ... 2     CHF              Franco suíço    A
    ... 3     DKK        Coroa dinamarquesa    A
    ... 4     EUR                      Euro    B
    ... 5     GBP           Libra Esterlina    B
    ... 6     JPY                      Iene    A
    ... 7     NOK          Coroa norueguesa    A
    ... 8     SEK               Coroa sueca    A
    ... 9     USD  Dólar dos Estados Unidos    A

    Notas
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

    Ver também
    ----------
    DadosAbertosBrasil.bacen.cambio
        Utilize a função `bacen.moedas` para identificar os argumentos da
        função `bacen.cambio`.

    --------------------------------------------------------------------------
    '''

    df = _df('Moedas')
    df.columns = ['simbolo', 'nome', 'tipo']
    return df



def cambio(
        moedas = 'USD',
        inicio: str = '2000-01-01',
        fim: str = None,
        cotacao: str = 'compra',
        boletim: str = 'fechamento',
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Taxa de câmbio das principais moedas internacionais.
    É possível escolher várias moedas inserindo uma lista no campo `moeda`.
    Defina o período da consulta pelos campos `inicio` e `fim`.

    Parâmetros
    ----------
    moedas : list ou str (default='USD')
        Sigla da moeda ou lista de siglas de moedas que serão pesquisadas no
        formato 'MMM' (três letras). Utilize a função `bacen.moedas` para
        obter a lista de moedas válidas.
    inicio : str (default='2000-01-01')
        String no formato de data 'AAAA-MM-DD' que representa o primeiro dia
        da pesquisa.
    fim : str (default=None)
        String no formato de data 'AAAA-MM-DD' que representa o último dia da
        pesquisa. Caso este campo seja None, será considerada a data de hoje.
    cotacao : str (default='compra')
        Tipo de cotação. Pode ser um dos seguintes valores:
            - 'compra';
            - 'venda'.
    boletim : str (default='fechamento')
        Tipo de boletim. Pode ser um dos seguintes valores:
            - 'abertura';
            - 'intermediário';
            - 'fechamento'.
    index : bool (default=False)
        Define se a coluna 'Data' será o index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo as cotações diárias das moedas selecionadas.

    Exemplos
    --------
    Retornar uma moeda usando argumentos padrões:
        >>> bacen.cambio(moedas='EUR')
        ...            Data      EUR
        ... 0    2000-01-03  1.84601
        ... 1    2000-01-04  1.88695
        ... 2    2000-01-05  1.91121
        ... 3    2000-01-06  1.90357
        ... 4    2000-01-07  1.87790
        ... ...         ...      ...

    Retornar várias moedas, alterando argumentos:
        >>> bacen.cambio(
        >>>     moedas = ['USD', 'CAD'],
        >>>     inicio = '2021-01-01',
        >>>     fim = '2021-01-10',
        >>>     cotacao = 'venda',
        >>>     boletim = 'abertura',
        >>>     index = True
        >>> )
        ...                USD     CAD
        ... Data                      
        ... 2021-01-04  5.1402  4.0500
        ... 2021-01-05  5.3405  4.1890
        ... 2021-01-06  5.3013  4.1798
        ... 2021-01-07  5.3174  4.1833
        ... 2021-01-08  5.3612  4.2237

    Ver também
    ----------
    DadosAbertosBrasil.bacen.moedas
        Utilize a função `bacen.moedas` para identificar as moedas que serão
        usadas no argumento da função `bacen.cambio`.

    --------------------------------------------------------------------------
    '''

    inicio = parse.data(inicio, 'bacen')
    if fim == None:
        fim = datetime.today().strftime('%m-%d-%Y')
    else:
        fim = parse.data(fim, 'bacen')
    
    moedas = parse.moeda(moedas)
    
    try:    
        cotacao_moedas = []
        for moeda in moedas:
            cotacao_moeda = _df(
                "CotacaoMoedaPeriodo(" \
                + "moeda=@moeda," \
                + "dataInicial=@dataInicial," \
                + "dataFinalCotacao=@dataFinalCotacao)" \
                + f"?@moeda='{moeda}'" \
                + f"&@dataInicial='{inicio}'" \
                + f"&@dataFinalCotacao='{fim}'" \
                + f"&$filter=contains(tipoBoletim%2C'{boletim.title()}')" \
                + f"&$select=cotacao{cotacao.title()},dataHoraCotacao"
            )
            
            cotacao_moeda.dataHoraCotacao = cotacao_moeda.dataHoraCotacao \
                .apply(lambda x: datetime.strptime(x[:10], '%Y-%m-%d'))

            cotacao_moedas.append(
                cotacao_moeda.rename(columns = {
                    f'cotacao{cotacao.title()}': moeda,
                    'dataHoraCotacao': 'Data'
                }).groupby('Data').last())

        cotacoes = _pd.concat(cotacao_moedas, axis=1).reset_index()

    except:
        raise TypeError("O campo 'moedas' deve ser o código de três letras maiúsculas da moeda ou um objeto iterável de códigos.")
    
    cotacoes.Data = _pd.to_datetime(cotacoes.Data, format='%Y-%m-%d %H:%M:%S')
    if index:
        cotacoes.set_index('Data', inplace=True)
    
    return cotacoes



def sgs(
        serie: int,
        ultimos: int = None,
        inicio: str = None,
        fim: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Valor mensal do índice IPC-A.

    Parâmetros
    ----------
    serie : int
        Número da série temporal.
        Utilize o seguinte link para obter o número da série desejada:
        https://www3.bcb.gov.br/sgspub/
    ultimos : int (default=None)
        Retorna os últimos N valores da série numérica.
    inicio : str ou datetime (default='2000-01-01')
        Valor datetime ou string no formato de data 'AAAA-MM-DD' que
        representa o primeiro dia da pesquisa.
    fim : str ou datetime (default=None)
        Valor datetime ou string no formato de data 'AAAA-MM-DD' que
        representa o último dia da pesquisa. Caso este campo seja None, será
        considerada a data de hoje.
    index : bool (default=False)
        Define se a coluna 'Data' será o index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os valores da série temporal pesquisada.

    Exemplos
    --------
    Capturar a taxa SELIC desde 2010 até 2021:
        >>> bacen.sgs(serie=432, inicio='2010-01-01', fim='2021-01-01')
        ...            data valor
        ... 0    2010-01-01  8.75
        ... 1    2010-01-02  8.75
        ... 2    2010-01-03  8.75
        ... 3    2010-01-04  8.75
        ... 4    2010-01-05  8.75
        ... ...         ...   ...

    Capturar os últimos 5 valores da meta de inflação:
        >>> bacen.sgs(serie=13521, ultimos=5)
        ...         data valor
        ... 0 2019-01-01  4.25
        ... 1 2020-01-01  4.00
        ... 2 2021-01-01  3.75
        ... 3 2022-01-01  3.50
        ... 4 2023-01-01  3.25

    Capturar toda a série de reservas internacionais (em milhões de dólares)
    usando a data como index do DataFrame:
        >>> bacen.sgs(serie=3546, index=True)
        ...              valor
        ... data              
        ... 1970-12-01    1187
        ... 1971-01-01    1229
        ... 1971-02-01    1280
        ... 1971-03-01    1316
        ... 1971-04-01    1379
        ... ...            ...

    Notas
    -----
    Os argumentos `inicio` e `fim` devem ser usados em conjunto para
    funcionar.

    Ver também
    ----------
    DadosAbertosBrasil.favoritos
        O módulo `favoritos` apresenta as principais séries temporáis do Banco
        Central do Brasil.

    --------------------------------------------------------------------------
    '''

    path = f'dados/serie/bcdata.sgs.{serie}/dados'
    if ultimos is not None:
        path += f'/ultimos/{ultimos}'

    params = []
    if inicio is not None:
        params.append(f"dataInicial={parse.data(inicio, modulo='sgs')}")
    if fim is not None:
        params.append(f"dataFinal={parse.data(fim, modulo='sgs')}")

    if len(params) > 0:
        path += f'?{"&".join(params)}'

    data = get_data(
        endpoint = 'https://api.bcb.gov.br/',
        path = path
    )

    df = _pd.DataFrame(data)

    df.data = _pd.to_datetime(df.data, format='%d/%m/%Y')
    if 'datafim' in df.columns:
        df.datafim = _pd.to_datetime(df.datafim, format='%d/%m/%Y')

    if index:
        df.set_index('data', inplace=True)

    return df