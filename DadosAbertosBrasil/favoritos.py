# Módulo para fácil acesso a dados selecionados
# Autor: Gustavo Furtado da Silva



import pandas as pd
from datetime import datetime

# Principais moedas internacionais
def moedas():
    query = r"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/Moedas?$top=100&$format=json"
    return pd.DataFrame(pd.read_json(query)['value'].to_list())

# Taxa de câmbio das principais moedas internacionais
def cambio(moedas='USD', data_inicial='01-01-2000', data_final='01-01-2020'):

    if isinstance(moedas, str):
        query = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{moedas}'&@dataInicial='{data_inicial}'&@dataFinalCotacao='{data_final}'&$top=10000&$filter=contains(tipoBoletim%2C'Fechamento')&$format=json&$select=cotacaoVenda,dataHoraCotacao"
        cotacoes = pd.DataFrame(pd.read_json(query)['value'].to_list())
    else:
        try:    
            cotacao_moedas = []
            for moeda in moedas:
                query = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda='{moeda}'&@dataInicial='{data_inicial}'&@dataFinalCotacao='{data_final}'&$top=10000&$filter=contains(tipoBoletim%2C'Fechamento')&$format=json&$select=cotacaoVenda,dataHoraCotacao"
                cotacao_moeda = pd.DataFrame(pd.read_json(query)['value'].to_list())
                cotacao_moeda.dataHoraCotacao = cotacao_moeda.dataHoraCotacao.apply(lambda x: datetime.strptime(x[:10], '%Y-%m-%d'))
                cotacao_moedas.append(cotacao_moeda.rename(columns={'cotacaoVenda': moeda}).set_index('dataHoraCotacao'))

            cotacoes = pd.concat(cotacao_moedas, axis=1)

        except:
            raise TypeError("O campo 'moedas' deve ser o código de três letras maiúsculas da moeda ou um objeto iterável de códigos.")
    
    return cotacoes

# Valor mensal do índice IPC-A
def ipca():

    ipca_query = r'https://api.bcb.gov.br/dados/serie/bcdata.sgs.4448/dados?formato=json'
    ipca = pd.read_json(ipca_query)
    ipca.data = pd.to_datetime(ipca.data)
    ipca = ipca.set_index('data').rename(columns={'valor':'IPCA Mensal'})
    
    return ipca

# Catalogo de iniciativas oficiais de dados abertos no Brasil
def catalogo():
    return pd.read_csv('https://raw.githubusercontent.com/dadosgovbr/catalogos-dados-brasil/master/dados/catalogos.csv')