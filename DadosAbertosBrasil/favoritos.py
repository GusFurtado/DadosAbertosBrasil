'''
Módulo para consultas à informações variadas.
Inclue dados de APIs do Banco Central do Brasil e outras informações úteis.
'''



from datetime import datetime

import pandas as _pd
import requests

from ._utils import parse



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
    r = requests.get(query)
    df = _pd.DataFrame(r.json()['value'])
    df.columns = ['Símbolo', 'Nome', 'Tipo']
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

    uf = parse.uf(uf)
    
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



def bandeira(uf:str, tamanho:int=100) -> str:
    '''
    Gera a URL da WikiMedia para a bandeira de um estado de um tamanho
    escolhido.

    Parâmetros
    ----------
    uf: str
        Sigla da Unidade Federativa.
    tamanho: int (default=100)
        Tamanho em pixels da bandeira.

    Retorna
    -------
    str
        URL da bandeira do estado no formato PNG.

    --------------------------------------------------------------------------
    '''
    
    URL = r'https://upload.wikimedia.org/wikipedia/commons/thumb/'
    
    bandeira = {
        'AC': f'4/4c/Bandeira_do_Acre.svg/{tamanho}px-Bandeira_do_Acre.svg.png',
        'AM': f'6/6b/Bandeira_do_Amazonas.svg/{tamanho}px-Bandeira_do_Amazonas.svg.png',
        'AL': f'8/88/Bandeira_de_Alagoas.svg/{tamanho}px-Bandeira_de_Alagoas.svg.png',
        'AP': f'0/0c/Bandeira_do_Amap%C3%A1.svg/{tamanho}px-Bandeira_do_Amap%C3%A1.svg.png',
        'BA': f'2/28/Bandeira_da_Bahia.svg/{tamanho}px-Bandeira_da_Bahia.svg.png',
        'CE': f'2/2e/Bandeira_do_Cear%C3%A1.svg/{tamanho}px-Bandeira_do_Cear%C3%A1.svg.png',
        'DF': f'3/3c/Bandeira_do_Distrito_Federal_%28Brasil%29.svg/{tamanho}px-Bandeira_do_Distrito_Federal_%28Brasil%29.svg.png',
        'ES': f'4/43/Bandeira_do_Esp%C3%ADrito_Santo.svg/{tamanho}px-Bandeira_do_Esp%C3%ADrito_Santo.svg.png',
        'GO': f'b/be/Flag_of_Goi%C3%A1s.svg/{tamanho}px-Flag_of_Goi%C3%A1s.svg.png',
        'MA': f'4/45/Bandeira_do_Maranh%C3%A3o.svg/{tamanho}px-Bandeira_do_Maranh%C3%A3o.svg.png',
        'MG': f'f/f4/Bandeira_de_Minas_Gerais.svg/{tamanho}px-Bandeira_de_Minas_Gerais.svg.png',
        'MT': f'0/0b/Bandeira_de_Mato_Grosso.svg/{tamanho}px-Bandeira_de_Mato_Grosso.svg.png',
        'MS': f'6/64/Bandeira_de_Mato_Grosso_do_Sul.svg/{tamanho}px-Bandeira_de_Mato_Grosso_do_Sul.svg.png',
        'PA': f'0/02/Bandeira_do_Par%C3%A1.svg/{tamanho}px-Bandeira_do_Par%C3%A1.svg.png',
        'PB': f'b/bb/Bandeira_da_Para%C3%ADba.svg/{tamanho}px-Bandeira_da_Para%C3%ADba.svg.png',
        'PE': f'5/59/Bandeira_de_Pernambuco.svg/{tamanho}px-Bandeira_de_Pernambuco.svg.png',
        'PI': f'3/33/Bandeira_do_Piau%C3%AD.svg/{tamanho}px-Bandeira_do_Piau%C3%AD.svg.png',
        'PR': f'9/93/Bandeira_do_Paran%C3%A1.svg/{tamanho}px-Bandeira_do_Paran%C3%A1.svg.png',
        'RJ': f'7/73/Bandeira_do_estado_do_Rio_de_Janeiro.svg/{tamanho}px-Bandeira_do_estado_do_Rio_de_Janeiro.svg.png',
        'RO': f'f/fa/Bandeira_de_Rond%C3%B4nia.svg/{tamanho}px-Bandeira_de_Rond%C3%B4nia.svg.png',
        'RN': f'3/30/Bandeira_do_Rio_Grande_do_Norte.svg/{tamanho}px-Bandeira_do_Rio_Grande_do_Norte.svg.png',        
        'RR': f'9/98/Bandeira_de_Roraima.svg/{tamanho}px-Bandeira_de_Roraima.svg.png',
        'RS': f'6/63/Bandeira_do_Rio_Grande_do_Sul.svg/{tamanho}px-Bandeira_do_Rio_Grande_do_Sul.svg.png',
        'SC': f'1/1a/Bandeira_de_Santa_Catarina.svg/{tamanho}px-Bandeira_de_Santa_Catarina.svg.png',
        'SE': f'b/be/Bandeira_de_Sergipe.svg/{tamanho}px-Bandeira_de_Sergipe.svg.png',
        'SP': f'2/2b/Bandeira_do_estado_de_S%C3%A3o_Paulo.svg/{tamanho}px-Bandeira_do_estado_de_S%C3%A3o_Paulo.svg.png',
        'TO': f'f/ff/Bandeira_do_Tocantins.svg/{tamanho}px-Bandeira_do_Tocantins.svg.png',        
    }
    
    return URL + bandeira[parse.uf(uf)]