import requests
from io import BytesIO
from zipfile import ZipFile

import pandas as pd

from DadosAbertosBrasil import _utils


class DetalheVotacaoMunZona():
    
    def __init__(self, ano):
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_munzona/detalhe_votacao_munzona_{ano}.zip'
        r = requests.get(url)
        self.ano = ano
        self.zipfile = ZipFile(BytesIO(r.content))
        
    def abrir(self, uf):
        uf = _utils.parse_uf(uf)
        
        if self.ano <= 2012:
            
            txt = []
            for i in self.zipfile.open(f'detalhe_votacao_munzona_{self.ano}_{uf}.txt', mode='r'):
                txt.append(i.decode('latin-1').replace('"', '').split(';'))
    
            columns = [
                'DATA_GERACAO',
                'HORA_GERACAO',
                'ANO_ELEICAO',
                'NUM_TURNO',
                'DESCRICAO_ELEICAO',
                'SIGLA_UF',
                'SIGLA_UE',
                'CODIGO_MUNICIPIO',
                'NOME_MUNICIPIO',
                'NUMERO_ZONA',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'QTD_APTOS',
                'QTD_SECOES',
                'QTD_SECOES_AGREGADAS',
                'QTD_APTOS_TOT',
                'QTD_SECOES_TOT',
                'QTD_COMPARECIMENTO',
                'QTD_ABSTENCOES',
                'QTD_VOTOS_NOMINAIS',
                'QTD_VOTOS_BRANCOS',
                'QTD_VOTOS_NULOS',
                'QTD_VOTOS_LEGENDA',
                'QTD_VOTOS_ANULADOS_APU_SEP',
                'DATA_ULT_TOTALIZACAO',
                'HORA_ULT_TOTALIZACAO'
            ]

            return pd.DataFrame(txt, columns=columns)            
            
        else:
            file = f'detalhe_votacao_munzona_{self.ano}_{uf}.csv'
            return pd.read_csv(self.zipfile.open(file, mode='r'), encoding='latin-1', sep=';')
        
        
class VotacaoPartidoMunZona():
    
    def __init__(self, ano):
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/votacao_partido_munzona/votacao_partido_munzona_{ano}.zip'
        r = requests.get(url)
        self.ano = ano
        self.zipfile = ZipFile(BytesIO(r.content))
        
    def abrir(self, uf):
        uf = _utils.parse_uf(uf)
        
        if self.ano <= 2012:
            
            txt = []
            for i in self.zipfile.open(f'votacao_partido_munzona_{self.ano}_{uf}.txt', mode='r'):
                txt.append(i.decode('latin-1').replace('"', '').split(';'))
    
            columns = [
                'DATA_GERACAO',
                'HORA_GERACAO',
                'ANO_ELEICAO',
                'NUM_TURNO',
                'DESCRICAO_ELEICAO',
                'SIGLA_UF',
                'SIGLA_UE',
                'CODIGO_MUNICIPIO',
                'NOME_MUNICIPIO',
                'NUMERO_ZONA',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'TIPO_LEGENDA',
                'NOME_COLIGACAO',
                'COMPOSICAO_LEGENDA',
                'SIGLA_PARTIDO',
                'NUMERO_PARTIDO',
                'NOME_PARTIDO',
                'QTDE_VOTOS_NOMINAIS',
                'QTDE_VOTOS_LEGENDA',
                'SEQUENCIAL_COLIGACAO'
            ]

            return pd.DataFrame(txt, columns=columns)
            
        else:
            file = f'votacao_partido_munzona_{self.ano}_{uf}.csv'
            return pd.read_csv(self.zipfile.open(file, mode='r'), encoding='latin-1', sep=';')