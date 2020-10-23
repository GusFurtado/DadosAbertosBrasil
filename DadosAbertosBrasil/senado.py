'''
Módulo para captura dos dados abertos da Senado Brasileiro

Documentação da API original: http://legis.senado.gov.br/dadosabertos/docs/
'''



import xml.etree.ElementTree as ET

import pandas as pd
import requests



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



# Lista de senadores. O campo serie pode receber os valores 'atual' ou 'afastados'.
def lista(serie='atual'):
    series = ['atual', 'afastados']
    if serie not in series:
        raise TypeError("O campo série deve ser um dos seguintes valores: 'atual' ou 'afastados'")
    return _get_request(_url + f'senador/lista/{serie}')



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



# Lista os partidos políticos
def partidos():
    return _get_request(_url + f'senador/partidos')



# Dados dos Senadores
class Senador():    
    
    def __init__(self, cod):
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