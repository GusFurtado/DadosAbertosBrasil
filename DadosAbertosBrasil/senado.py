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



def partidos(ativos='S', index=False) -> pd.DataFrame:
    '''
    Lista os partidos políticos.
    Para listas os partidos inativos, defina o campo 'ativo' como 'N'.
    '''

    url = f'{_url}senador/partidos'
    if ativos.upper() == 'N':
        url += '?indAtivos=N'
    
    r = _get_request(url)
    df = pd.DataFrame(r['Partidos']['Partido'])

    if index:
        df.set_index('Codigo', inplace=True)

    df.DataCriacao = pd.to_datetime(df.DataCriacao)
    if ativos.upper() == 'N':
        df.DataExtincao = pd.to_datetime(df.DataExtincao)

    return df



class Senadores:
    '''
    Coleta os dados dos senadores.

    Insira o código do senador no campo 'cod'. Encontre o código pela
    class 'senado.Lista'.
    
    Para ver as informações do senador, chame um dos seguintes
    atributos:
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
        self.cod = cod
        self.dados_completos = _get_request2(_url + f'senador/{cod}')
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

    
    def cargos(self, comissao=None, ativos=None):
        '''
        Obtém a relação de cargos que o senador ja ocupou.

        Preencha o campo 'comissao' com a sigla da comissão para retornar
        apenas os cargos na comissão informada.
        Se o campo ativos for igual a 'S', retorna apenas os cargos atuais.
        '''

        tags = {}

        if comissao is not None:
            tags['comissao'] = comissao
        if ativos is not None:
            tags['indAtivos'] = ativos

        if len(tags) > 0:
            searchtags = _utils.convert_search_tags(tags)
        else:
            searchtags = ''

        return _get_request(_url + f'senador/{self.cod}/cargos{searchtags}')


    def filiacoes(self):
        '''
        Obtém as filiações partidárias que o senador já teve.
        '''

        return _get_request(_url + f'senador/{self.cod}/filiacoes')

    
    def mandatos(self):
        '''
        Obtém os mandatos que o senador já teve.
        '''

        return _get_request(_url + f'senador/{self.cod}/mandatos')


    def comissoes(self, comissao=None, ativos=None):
        '''
        Obtém as comissões de que um senador é membro.

        Preencha o campo 'comissao' para obter apenas a sigla da comissão
        informada.
        Se o campo 'ativos' for igual a 'S', retorna apenas as comissões
        atuais.
        '''

        tags = {}

        if comissao is not None:
            tags['comissao'] = comissao
        if ativos is not None:
            tags['indAtivos'] = ativos

        if len(tags) > 0:
            searchtags = _utils.convert_search_tags(tags)
        else:
            searchtags = ''

        return _get_request(_url + f'senador/{self.cod}/comissoes{searchtags}')


    def votacoes(self, ano=None, numero=None, sigla=None, tramitando=None)
        '''
        Obtém as votações de um senador.

        O campo 'ano' retorna apenas as matérias do ano informado.
        O campo 'numero' retorna apenas as matérias do número informado. 	 
        O campo 'sigla' retorna apenas as matérias da sigla informada. 	 
        O campo 'tramitando' retorna apenas as matérias que estão tramitando
        quando seu valor for igual a 'S', ou apenas as que não estão quando
        seu valor for 'N'. Se não for informado, retorna ambas.
        '''

        tags = {}

        if ano is not None:
            tags['ano'] = ano
        if numero is not None:
            tags['numero'] = numero
        if sigla is not None:
            tags['sigla'] = sigla
        if tramitando is not None:
            tags['tramitando'] = tramitando

        if len(tags) > 0:
            searchtags = _utils.convert_search_tags(tags)
        else:
            searchtags = ''

        return _get_request(_url + f'senador/{self.cod}/votacoes{searchtags}')


    def liderancas(self):
        '''
        Obtém os cargos de liderança de um senador.
        '''

        return _get_request(_url + f'senador/{self.cod}/liderancas')


    def licencas(self, data=None):
        '''
        Obtém as licenças de um senador.

        Retorna as licenças a partir da data especificada no campo 'data'.
        '''

        tags = {}

        if data is not None:
            tags['dataInicio'] = data

        if len(tags) > 0:
            searchtags = _utils.convert_search_tags(tags)
        else:
            searchtags = ''

        return _get_request(_url + f'senador/{self.cod}/licencas{searchtags}')


    def autorias(
            self,
            ano = None,
            numero = None,
            primeiro = None,
            sigla = None,
            tramitando = None
        ):
        '''
        Obtém as matérias de autoria de um senador.

        No campo 'ano' retorna apenas as matérias do ano informado.
        No campo 'numero' retorna apenas as matérias do número informado. 	 
        O campo 'primeiro' aceita os seguintes valores:
            - 'S' retorna apenas as matérias cujo senador é o primeiro autor;
            - 'N' returna apenas as que o senador é coautor;
            - 'T' retorna ambas;
            - Se não for informado, retorna apenas as de primeira autoria. 
        O campo 'sigla' retorna apenas as matérias da sigla informada. 	 
        O campo 'tramitando' aceita os seguintes valores:
            - 'S' retorna apenas as matérias que estão tramitando;
            - 'N' retorna apenas as que não estão tramitando;
            - Se não for informado, retorna ambas.
        '''

        tags = {}

        if ano is not None:
            tags['ano'] = ano
        if numero is not None:
            tags['numero'] = numero
        if primeiro is not None:
            tags['primeiro'] = primeiro
        if sigla is not None:
            tags['sigla'] = sigla
        if tramitando is not None:
            tags['tramitando'] = tramitando

        if len(tags) > 0:
            searchtags = _utils.convert_search_tags(tags)
        else:
            searchtags = ''

        return _get_request(_url + f'senador/{self.cod}/autorias{searchtags}')


    def relatorias(
            self,
            ano = None,
            comissao = None,
            numero = None,
            sigla = None,
            tramitando = None
        ):
        '''
        Obtém as matérias de relatoria de um senador.

        No campo 'ano' retorna apenas as matérias do ano informado.
        No campo 'comissao' retorna apenas as relatorias da comissão informada.
        No campo 'numero' retorna apenas as matérias do número informado. 
        O campo 'sigla' retorna apenas as matérias da sigla informada. 	 
        O campo 'tramitando' aceita os seguintes valores:
            - 'S' retorna apenas as matérias que estão tramitando;
            - 'N' retorna apenas as que não estão tramitando;
            - Se não for informado, retorna ambas.
        '''

        tags = {}

        if ano is not None:
            tags['ano'] = ano
        if comissao is not None:
            tags['comissao'] = comissao
        if numero is not None:
            tags['numero'] = numero
        if sigla is not None:
            tags['sigla'] = sigla
        if tramitando is not None:
            tags['tramitando'] = tramitando

        if len(tags) > 0:
            searchtags = _utils.convert_search_tags(tags)
        else:
            searchtags = ''

        return _get_request(_url + f'senador/{self.cod}/relatorias{searchtags}')


    def discursos(
            self,
            casa = None,
            data_inicio = None,
            data_fim = None,
            numero_sessao = None,
            tipo_pronunciamento = None,
            tipo_sessao = None
        ):
        '''
        Obtém a relação de discursos do senador.

        No campo 'casa', insira a sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        Insira a data de início do período da pesquisa no formato AAAAMMDD
        no campo 'data_inicio'.
        Insira a data de fim do período da pesquisa no formato AAAAMMDD
        no campo 'data_fim'.	 
        Escolha o número da sessão plenária no campo 'numero_sessao'.
        No campo 'tipo_pronunciamento', defina a sigla do tipo de
        pronunciamento.
        No campo 'tipo_sessao', defina o tipo da sessão plenária. 
        '''

        tags = {}

        if casa is not None:
            tags['casa'] = casa
        if data_inicio is not None:
            tags['dataInicio'] = data_inicio
        if data_fim is not None:
            tags['dataFim'] = data_fim
        if numero_sessao is not None:
            tags['numeroSessao'] = numero_sessao
        if tipo_pronunciamento is not None:
            tags['tipoPronunciamento'] = tipo_pronunciamento
        if tipo_sessao is not None:
            tags['tipoSessao'] = tipo_sessao

        if len(tags) > 0:
            searchtags = _utils.convert_search_tags(tags)
        else:
            searchtags = ''

        return _get_request(_url + f'senador/{self.cod}/discursos{searchtags}')


    def apartes(
            self,
            casa = None,
            data_inicio = None,
            data_fim = None,
            numero_sessao = None,
            tipo_pronunciamento = None,
            tipo_sessao = None
        ):
        '''
        Obtém a relação de apartes do senador.

        No campo 'casa', insira a sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        Insira a data de início do período da pesquisa no formato AAAAMMDD
        no campo 'data_inicio'.
        Insira a data de fim do período da pesquisa no formato AAAAMMDD
        no campo 'data_fim'.	 
        Escolha o número da sessão plenária no campo 'numero_sessao'.
        No campo 'tipo_pronunciamento', defina a sigla do tipo de
        pronunciamento.
        No campo 'tipo_sessao', defina o tipo da sessão plenária. 
        '''

        tags = {}

        if casa is not None:
            tags['casa'] = casa
        if data_inicio is not None:
            tags['dataInicio'] = data_inicio
        if data_fim is not None:
            tags['dataFim'] = data_fim
        if numero_sessao is not None:
            tags['numeroSessao'] = numero_sessao
        if tipo_pronunciamento is not None:
            tags['tipoPronunciamento'] = tipo_pronunciamento
        if tipo_sessao is not None:
            tags['tipoSessao'] = tipo_sessao

        if len(tags) > 0:
            searchtags = _utils.convert_search_tags(tags)
        else:
            searchtags = ''

        return _get_request(_url + f'senador/{self.cod}/apartes{searchtags}')


    def historico(self):
        '''
        Obtém todos os detalhes de um parlamentar no(s) mandato(s) como
        senador (mandato atual e anteriores, se houver).
        '''

        return _get_request(_url + f'senador/{self.cod}/historico')