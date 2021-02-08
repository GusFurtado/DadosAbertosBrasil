'''
Módulo para consultas à informações variadas.
Inclue dados de APIs do Banco Central do Brasil e outras informações úteis.
'''



from datetime import datetime

import pandas as _pd
import requests

from DadosAbertosBrasil import _utils



def moedas() -> _pd.DataFrame:
    '''
    Obtém os nomes e símbolos das principais moedas internacionais.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os nomes e símbolos das principais
        moedas internacionais.

    --------------------------------------------------------------------------
    '''

    query = r"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=100&$format=json"
    return _pd.DataFrame(_pd.read_json(query)['value'].to_list()) \
        .rename(columns = {
            'nomeFormatado': 'Nome',
            'simbolo': 'Símbolo',
            'tipoMoeda': 'Tipo'
        })



def cambio(
        moedas = 'USD',
        inicio: str = '01-01-2000',
        fim: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Taxa de câmbio das principais moedas internacionais.
    É possível escolher várias moedas inserindo uma lista no campo 'moeda'.
    Defina o período da consulta pelos campos `inicio` e `fim`.

    Parâmetros
    ----------
    moedas: list ou str (default='USD')
        Sigla da moeda ou lista de siglas de moedas que será(ão) pesquisada(s).
        Utilize a função favoritos.moedas() para obter uma lista de moedas
        válidas.
    inicio: str (default='01-01-2000')
        String no formato de data 'DD-MM-AAAA' que representa o primeiro dia
        da pesquisa.
    fim: str (default=None)
        String no formato de data 'DD-MM-AAAA' que representa o último dia
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

    if fim == None:
        fim = datetime.today().strftime('%m-%d-%Y')
    
    if isinstance(moedas, str):
        query = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{moedas}'&@dataInicial='{inicio}'&@dataFinalCotacao='{fim}'&$top=10000&$filter=contains(tipoBoletim%2C'Fechamento')&$format=json&$select=cotacaoVenda,dataHoraCotacao"
        cotacoes = _pd.DataFrame(_pd.read_json(query)['value'].to_list()) \
            .rename(columns = {
                'cotacaoVenda': moedas,
                'dataHoraCotacao': 'Data'
            })
        cotacoes = cotacoes[['Data', moedas]]
    
    else:
        try:    
            cotacao_moedas = []
            for moeda in moedas:
                query = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{moeda}'&@dataInicial='{inicio}'&@dataFinalCotacao='{fim}'&$top=10000&$filter=contains(tipoBoletim%2C'Fechamento')&$format=json&$select=cotacaoVenda,dataHoraCotacao"
                cotacao_moeda = _pd.DataFrame(_pd.read_json(query)['value'].to_list())
                cotacao_moeda.dataHoraCotacao = cotacao_moeda.dataHoraCotacao.apply(
                    lambda x: datetime.strptime(x[:10], '%Y-%m-%d')
                )
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
    ipca = ipca.rename(columns={'data': 'Data', 'valor':'IPCA Mensal'})
    
    if index:
        ipca.set_index('Data', inplace=True)
    
    return ipca



def catalogo() -> _pd.DataFrame:
    '''
    Catálogo de iniciativas oficiais de dados abertos no Brasil.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo um catálogo de iniciativas de dados abertos.

    --------------------------------------------------------------------------
    '''

    # URL do repositório no GitHub contendo o catálogo de dados abertos.
    # Créditos: https://github.com/dadosgovbr
    url = 'https://raw.githubusercontent.com/dadosgovbr/catalogos-dados-brasil/master/dados/catalogos.csv'
    
    return _pd.read_csv(url)



def geojson(uf:str) -> dict:
    '''
    Coordenadas dos municípios brasileiros em formato GeoJSON para criação
    de mapas.

    Parâmetros
    ----------
    uf: str
        Nome ou sigla da Unidade Federativa.

    Retorna
    -------
    dict
        Coordenadas em formato .GeoJSON da UF pesquisada.

    --------------------------------------------------------------------------
    '''

    uf = _utils.parse_uf(uf)
    
    mapping = {

        'BR': 100,

        # Região Norte
        'AC': 12,
        'AM': 13,
        'AP': 16,
        'PA': 15,
        'RO': 11,
        'RR': 14,
        'TO': 17,

        # Região Nordeste
        'AL': 27,
        'BA': 29,
        'CE': 23,
        'MA': 21,
        'PB': 25,
        'PE': 26,
        'PI': 22,
        'RN': 24,
        'SE': 28,

        # Região Centro-Oeste
        'DF': 53,
        'GO': 52,
        'MT': 51,
        'MS': 50,

        # Região Sudeste
        'ES': 32,
        'MG': 31,
        'RJ': 33,
        'SP': 35,

        # Região Sul
        'PR': 41,
        'RS': 43,
        'SC': 42

    }
    
    # URL do repositório no GitHub contendo os geojsons.
    # Créditos: https://github.com/tbrugz
    url = f'https://raw.githubusercontent.com/tbrugz/geodata-br/master/geojson/geojs-{mapping[uf]}-mun.json'
    
    return requests.get(url).json()



def codigos_municipios() -> _pd.DataFrame:
    '''
    Lista dos códigos dos municípios do IBGE e do TSE.
    Utilizado para correlacionar dados das duas APIs diferentes.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os códigos do IBGE e do TSE para todos os
        municípios do Brasil.

    --------------------------------------------------------------------------
    '''

    # URL do repositório no GitHub contendo os códigos.
    # Créditos: https://github.com/betafcc
    url = r'https://raw.githubusercontent.com/betafcc/Municipios-Brasileiros-TSE/master/municipios_brasileiros_tse.json'
    df = _pd.read_json(url)
    return df[['codigo_tse', 'codigo_ibge', 'nome_municipio', 'uf', 'capital']]



def perfil_eleitorado() -> _pd.DataFrame:
    '''
    Tabela com perfil do eleitorado por município.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo o perfil do eleitorado em todos os municípios.

    --------------------------------------------------------------------------
    '''

    return _pd.read_csv(
        r'https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/data/Eleitorado.csv',
        encoding = 'latin-1',
        sep = ';'
    )