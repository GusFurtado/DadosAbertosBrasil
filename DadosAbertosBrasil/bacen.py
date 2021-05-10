'''
Módulo de captura de dados do Banco Central do Brasil.

Documentação Original
---------------------
Cotação do Câmbio
    https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3
'''



from datetime import datetime

import pandas as _pd

from ._utils import parse
from ._utils.get_data import get_data



def _df(path:str, params:dict) -> _pd.DataFrame:
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
        DataFrame contendo os nomes e símbolos das principais
        moedas internacionais.

    --------------------------------------------------------------------------
    '''
    df = _df(
        path = 'Moedas',
        params = None
    )
    df.columns = ['simbolo', 'nome', 'tipo']
    return df



def cambio(
        moedas = 'USD',
        inicio: str = '2000-01-01',
        fim: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Taxa de câmbio das principais moedas internacionais.
    É possível escolher várias moedas inserindo uma lista no campo `moeda`.
    Defina o período da consulta pelos campos `inicio` e `fim`.

    Parâmetros
    ----------
    moedas: list ou str (default='USD')
        Sigla da moeda ou lista de siglas de moedas que será(ão) pesquisada(s).
        Utilize a função `favoritos.moedas` para obter uma lista de moedas
        válidas.
    inicio: str (default='2000-01-01')
        String no formato de data 'AAAA-MM-DD' que representa o primeiro dia
        da pesquisa.
    fim: str (default=None)
        String no formato de data 'AAAA-MM-DD' que representa o último dia
        da pesquisa.
        Caso este campo seja None, será considerada a data de hoje.
    index: bool (default=False)
        Define se a coluna 'Data' será o index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo o valor cambial da(s) moeda(s) selecionada(s)
        por dia.

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
                f"CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{moeda}'&@dataInicial='{inicio}'&@dataFinalCotacao='{fim}'&$filter=contains(tipoBoletim%2C'Fechamento')&$select=cotacaoVenda,dataHoraCotacao",
                params = None
            )
            
            cotacao_moeda.dataHoraCotacao = cotacao_moeda.dataHoraCotacao \
                .apply(lambda x: datetime.strptime(x[:10], '%Y-%m-%d'))

            cotacao_moedas.append(
                cotacao_moeda.rename(columns = {
                    'cotacaoVenda': moeda,
                    'dataHoraCotacao': 'Data'
                }).groupby('Data').last())

        cotacoes = _pd.concat(cotacao_moedas, axis=1).reset_index()

    except:
        raise TypeError("O campo 'moedas' deve ser o código de três letras maiúsculas da moeda ou um objeto iterável de códigos.")
    
    cotacoes.Data = _pd.to_datetime(cotacoes.Data, format='%Y-%m-%d %H:%M:%S')
    if index:
        cotacoes.set_index('Data', inplace=True)
    
    return cotacoes



def ipca(index:bool=False) -> _pd.DataFrame:
    '''
    Valor mensal do índice IPC-A.

    Parâmetros
    ----------
    index: bool (default=False)
        Define se a coluna 'Data' será o index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo o valor do índice IPC-A por mês.

    --------------------------------------------------------------------------
    '''

    ipca_query = r'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4448/dados?formato=json'
    ipca = _pd.read_json(ipca_query)
    ipca.data = _pd.to_datetime(ipca.data)
    ipca.columns = ['Data', 'IPCA Mensal']
    
    if index:
        ipca.set_index('Data', inplace=True)
    
    return ipca