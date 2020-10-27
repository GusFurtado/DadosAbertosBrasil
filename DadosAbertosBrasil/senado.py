'''
Módulo para captura dos dados abertos da Senado Brasileiro

Documentação da API original: http://legis.senado.gov.br/dadosabertos/docs/
'''



import xml.etree.ElementTree as ET

import pandas as pd
import requests

from . import _utils



_url = r'http://legis.senado.gov.br/dadosabertos/'



class _XmlListConfig(list):
    def __init__(self, aList):
        for element in aList:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    self.append(_XmlDictConfig(element))
                elif element[0].tag == element[1].tag:
                    self.append(_XmlListConfig(element))
            elif element.text:
                text = element.text.strip()
                if text:
                    self.append(text)

                    
class _XmlDictConfig(dict):
    def __init__(self, parent_element):
        if parent_element.items():
            self.update(dict(parent_element.items()))
        for element in parent_element:
            if element:
                if len(element) == 1 or element[0].tag != element[1].tag:
                    aDict = _XmlDictConfig(element)
                else:
                    aDict = {element[0].tag: _XmlListConfig(element)}
                if element.items():
                    aDict.update(dict(element.items()))
                self.update({element.tag: aDict})
            elif element.items():
                self.update({element.tag: dict(element.items())})
            else:
                self.update({element.tag: element.text})


          
def _get_request(url):
    r = requests.get(url)
    tree = ET.fromstring(r.text)
    return _XmlDictConfig(tree)



class Lista:
    '''
    Gera uma lista de senadores.
    Liste suplentes em atividade definindo o campo 'participacao' como 'S'.
    Filtre por UF pelo campo 'uf'.
    Utilize os métodos 'atual', 'afastado' ou 'legislatura' para escolher um
    tipo de lista.
    '''

    def __init__(self, participacao=None, uf=None):

        tags = {}

        if participacao is not None:
            tags['participacao'] = participacao
        if uf is not None:
            tags['uf'] = _utils.parse_uf(uf)

        if len(tags) > 0:
            self.searchtags = _utils.convert_search_tags(tags)
        else:
            self.searchtags = ''

        
    def atual(self) -> dict:
        '''
        Obtém a lista de senadores em exercício.
        '''

        url = f'{_url}senador/lista/atual{self.searchtags}'
        return _get_request(url)['Parlamentares']['Parlamentar']


    def afastados(self) -> dict:
        '''
        Obtém a lista dos senadores atualmente afastados.
        '''

        url = f'{_url}senador/lista/afastados'
        return _get_request(url)['Parlamentares']['Parlamentar']


    def legislatura(self, inicio: int, fim=None, exercicio=None) -> dict:
        '''
        Obtém a lista de senadores de uma legislatura ou de um intervalo de
        legislaturas.
        Defina o código da legislatura que seja consultado no campo 'inicio'.
        Para consultar um intervalo de legislaturas, preenche o campo 'fim'.
        Caso 'fim == None', será consultado apenas a legislatura 'inicio'.
        Defina o campo 'exercicio' como 'S' para consultar apenas os senadores
        que entraram em exercício.
        '''

        url = f'{_url}senador/lista/legislatura/{inicio}'
        
        if fim is not None:
            url += f'/{fim}'

        if exercicio is not None:

            if self.searchtags == '':
                self.searchtags = '?'
            else:
                self.searchtags += '&'

            self.searchtags += f'exercicio={exercicio}'
        
        url += self.searchtags

        return _get_request(url)['Parlamentares']['Parlamentar']



# Obtém os detalhes do senador
def senador(cod, serie=None):
    if serie == None:
        s = ''
    else:
        series = ['cargos', 'filiacoes', 'mandatos', 'comissoes', 'votacoes', 'liderancas', 'licencas', 'autorias', 'relatorias', 'discursos', 'apartes', 'historico']
        if serie not in series:
            raise TypeError(f"O campo série deve ser um dos seguintes valores: {series}")
        else:
            s = '/' + serie
    return _get_request(_url + f'senador/{cod}{s}')



def partidos(ativo='S', index=False) -> pd.DataFrame:
    '''
    Lista os partidos políticos.
    Para listas os partidos inativos, defina o campo 'ativo' como 'N'.
    '''

    url = f'{_url}senador/partidos'
    if ativo.upper() == 'N':
        url += '?indAtivos=N'
    
    r = _get_request(url)
    df = pd.DataFrame(r['Partidos']['Partido'])

    if index:
        df.set_index('Codigo', inplace=True)

    df.DataCriacao = pd.to_datetime(df.DataCriacao)
    if ativo.upper() == 'N':
        df.DataExtincao = pd.to_datetime(df.DataExtincao)

    return df



class Senadores:
    '''
    Coleta os dados dos senadores.
    Insira o código do senador no campo 'cod'. Encontre o código pela função
    senado.lista().
    
    Para ver as informações do senador, chame um dos seguintes atributos:
        - identificacao
        - .dados_basicos
        - .dados
        - .dados_completos
        - .ultimo_mandato
        - .cursos
        - .profissoes
        - .outras_informacoes
    '''

    def __init__(self, cod: int):
        self.dados_completos = _get_request(_url + f'senador/{cod}')
        d = self.dados_completos['Parlamentar']
        self.identificacao = d['IdentificacaoParlamentar']
        self.dados_basicos = d['DadosBasicosParlamentar']

        if 'UltimoMandato' in d:
            self.ultimo_mandato = d['UltimoMandato']
        
        if 'OutrasInformacoes' in d:
            self.outras_informacoes = d['OutrasInformacoes']

        if 'HistoricoAcademico' in d:
            self.cursos = self.dados_completos['Parlamentar']['HistoricoAcademico']

        if 'Profissoes' in d:
            self.profissoes = self.dados_completos['Parlamentar']['Profissoes']
    
        d = {}
        for i in list(self.dados_completos['Parlamentar'].keys())[:-2]:
            d.update(self.dados_completos['Parlamentar'][i])
        self.dados = d