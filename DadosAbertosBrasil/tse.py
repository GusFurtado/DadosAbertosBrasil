'''
Módulo para extração dos dados abertos dos arquivos do TSE.

Documentação da API original: https://www.tse.jus.br/eleicoes/estatisticas/repositorio-de-dados-eleitorais-1
'''



from io import BytesIO
from zipfile import ZipFile

import pandas as pd
import requests

from DadosAbertosBrasil import _utils



def _read_csv(zipfile: ZipFile, file: str) -> pd.DataFrame:
    '''
    Abre uma pasta ZIP e extrai um arquivo dela.
    '''

    return pd.read_csv(
        zipfile.open(file, mode = 'r'),
        encoding = 'latin-1',
        sep = ';'  
    )



class VotacaoPartidoMunZona():
    '''
    Quantos votos cada partido recebeu por município e zona eleitoral.
    Defina o ano para baixar a pasta zip e defina a UF para abrí-la.
    '''
    
    def __init__(self, ano: int) -> ZipFile:
        '''
        Baixa a pasta zippada do ano definido.
        '''

        self.file = 'votacao_partido_munzona'
        self.ano = ano
        
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/{self.file}/{self.file}_{ano}.zip'
        r = requests.get(url)
        self.zipfile = ZipFile(BytesIO(r.content))


    def abrir(self, uf: str) -> pd.DataFrame:
        '''
        Abre o arquivo da UF dentro da pasta zippada.
        '''

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
            return _read_csv(self.zipfile, file)

        

class VotacaoCandidatoMunZona():
    '''
    Quantos votos cada candidato recebeu por município e zona eleitoral.
    Defina o ano para baixar a pasta zip e defina a UF para abrí-la.
    '''
    
    def __init__(self, ano: int) -> ZipFile:
        '''
        Baixa a pasta zippada do ano definido.
        '''

        self.file = 'votacao_candidato_munzona'
        self.ano = ano
        
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/{self.file}/{self.file}_{ano}.zip'
        r = requests.get(url)
        self.zipfile = ZipFile(BytesIO(r.content))


    def abrir(self, uf: str) -> pd.DataFrame:
        '''
        Abre o arquivo da UF dentro da pasta zippada.
        '''

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
            return _read_csv(self.zipfile, file)
        
      
        
class DetalheVotacaoSecao():
    '''
    Detalhe da apuração por seção eleitoral.
    Defina o ano para baixar a pasta zip e defina a UF para abrí-la.
    '''
    
    def __init__(self, ano: int) -> ZipFile:
        '''
        Baixa a pasta zippada do ano definido.
        '''

        self.file = 'detalhe_votacao_secao'
        self.ano = ano
        
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/{self.file}/{self.file}_{ano}.zip'
        r = requests.get(url)
        self.zipfile = ZipFile(BytesIO(r.content))
        
        
    def abrir(self, uf: str) -> pd.DataFrame:
        '''
        Abre o arquivo da UF dentro da pasta zippada.
        '''
        
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
            return _read_csv(self.zipfile, file)
        
        
        
class DetalheVotacaoMunZona():
    '''
    Detalhe da apuração por município e zona.
    Defina o ano para baixar a pasta zip e defina a UF para abrí-la.
    '''
    
    def __init__(self, ano: int) -> ZipFile:
        '''
        Baixa a pasta zippada do ano definido.
        '''
   
        self.file = 'detalhe_votacao_munzona'
        self.ano = ano
        
        url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/{self.file}/{self.file}_{ano}.zip'
        r = requests.get(url)
        self.zipfile = ZipFile(BytesIO(r.content))
        
        
    def abrir(self, uf: str) -> pd.DataFrame:
        '''
        Abre o arquivo da UF dentro da pasta zippada.
        '''

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
            return _read_csv(self.zipfile, file)
        
        
    
def votacao_secao(ano: int, uf: str) -> pd.DataFrame:
    '''
    Votação por seção eleitoral.
    '''
    
    file = 'votacao_secao'
    uf = _utils.parse_uf(uf)
    url = f'http://agencia.tse.jus.br/estatistica/sead/odsele/{file}/{file}_{ano}_{uf}.zip'
    r = requests.get(url)
    zipfile = ZipFile(BytesIO(r.content))
    return _read_csv(zipfile, file)



def perfil_eleitorado() -> pd.DataFrame:
    '''
    Tabela com perfil do eleitorado por município.
    '''

    return pd.read_csv(
        r'https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/data/Eleitorado.csv',
        encoding = 'latin-1',
        sep = ';'
    )