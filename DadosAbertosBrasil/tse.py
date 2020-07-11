import requests
from io import BytesIO
from zipfile import ZipFile
import warnings

import pandas as pd

from DadosAbertosBrasil import _utils


future_warning = 'Este módulo está nas etapas iniciais de desenvolvimento e as funções disponibilizadas são apenas um preview do que está por vir.'

warnings.warn(future_warning, FutureWarning)


class VotacaoPartidoMunZona():
    
    def __init__(self, ano):
        self.file = 'votacao_partido_munzona'
        self.ano = ano
        
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/{self.file}/{self.file}_{ano}.zip'
        r = requests.get(url)
        self.zipfile = ZipFile(BytesIO(r.content))
        
    def abrir(self, uf):
        uf = _utils.parse_uf(uf)
        
        if self.ano <= 2012:
            
            txt = []
            for i in self.zipfile.open(f'{self.file}_{self.ano}_{uf}.txt', mode='r'):
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
            file = f'{self.file}_{self.ano}_{uf}.csv'
            return pd.read_csv(self.zipfile.open(file, mode='r'), encoding='latin-1', sep=';')

        
class VotacaoCandidatoMunZona():
    
    def __init__(self, ano):
        self.file = 'votacao_candidato_munzona'
        self.ano = ano
        
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/{self.file}/{self.file}_{ano}.zip'
        r = requests.get(url)
        self.zipfile = ZipFile(BytesIO(r.content))
        
    def abrir(self, uf):
        uf = _utils.parse_uf(uf)
        
        if self.ano <= 2012:
            
            txt = []
            for i in self.zipfile.open(f'{self.file}_{self.ano}_{uf}.txt', mode='r'):
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
                'NUMERO_CAND',
                'SQ_CANDIDATO',
                'NOME_CANDIDATO',
                'NOME_URNA_CANDIDATO',
                'DESCRICAO_CARGO',
                'COD_SIT_CAND_SUPERIOR',
                'DESC_SIT_CAND_SUPERIOR',
                'CODIGO_SIT_CANDIDATO',
                'DESC_SIT_CANDIDATO',
                'CODIGO_SIT_CAND_TOT',
                'DESC_SIT_CAND_TOT',
                'NUMERO_PARTIDO',
                'SIGLA_PARTIDO',
                'NOME_PARTIDO'
            ]
        
            return pd.DataFrame(txt, columns=columns)
            
        else:
            file = f'{self.file}_{self.ano}_{uf}.csv'
            return pd.read_csv(self.zipfile.open(file, mode='r'), encoding='latin-1', sep=';')
        
        
class DetalheVotacaoSecao():
    
    def __init__(self, ano):
        self.file = 'detalhe_votacao_secao'
        self.ano = ano
        
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/{self.file}/{self.file}_{ano}.zip'
        r = requests.get(url)
        self.zipfile = ZipFile(BytesIO(r.content))
        
        
    def abrir(self, uf):
        uf = _utils.parse_uf(uf)
        
        if self.ano <= 2012:
            
            txt = []
            for i in self.zipfile.open(f'{self.file}_{self.ano}_{uf}.txt', mode='r'):
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
                'NUMERO_SECAO',
                'CODIGO_CARGO',
                'DESCRICAO_CARGO',
                'QTD_APTOS',
                'QTD_COMPARECIMENTO',
                'QTD_ABSTENCOES',
                'QT_VOTOS_NOMINAIS',
                'QT_VOTOS_BRANCOS',
                'QT_VOTOS_NULOS',
                'QT_VOTOS_LEGENDA',
                'QT_VOTOS_ANULADOS_APU_SEP'
            ]
        
            return pd.DataFrame(txt, columns=columns)            
            
        else:
            file = f'{self.file}_{self.ano}_{uf}.csv'
            return pd.read_csv(self.zipfile.open(file, mode='r'), encoding='latin-1', sep=';')
        
        
class DetalheVotacaoMunZona():
    
    
    def __init__(self, ano):
        self.file = 'detalhe_votacao_munzona'
        self.ano = ano
        
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/{self.file}/{self.file}_{ano}.zip'
        r = requests.get(url)
        self.zipfile = ZipFile(BytesIO(r.content))
        
        
    def abrir(self, uf):
        uf = _utils.parse_uf(uf)
        
        if self.ano <= 2012:
            
            txt = []
            for i in self.zipfile.open(f'{self.file}_{self.ano}_{uf}.txt', mode='r'):
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
            file = f'{self.file}_{self.ano}_{uf}.csv'
            return pd.read_csv(self.zipfile.open(file, mode='r'), encoding='latin-1', sep=';')