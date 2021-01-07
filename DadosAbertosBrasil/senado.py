'''
Módulo para captura dos dados abertos da Senado Brasileiro

Documentação da API original: http://legis.senado.gov.br/dadosabertos/docs/
'''



import pandas as pd
import requests

from . import _utils



_url = r'http://legis.senado.gov.br/dadosabertos/'



def _get_request(url: str, keys=None) -> dict:
    data = requests.get(url, headers={'Accept':'application/json'}).json()

    if keys is not None:
        for key in keys:
            if data is not None:
                if key in data:
                    data = data[key]

    return data


        
def lista_atual(participacao=None, uf=None) -> dict:
    '''
    Lista senadores em exercício.

    Parâmetros
    ----------
    participacao: str (default=None)
        Tipo de participação.
        - None: Busca qualquer tipo de participação.
        - 'T': Busca apenas titulares.
        - 'S': Busca apenas suplentes.
    uf: str (default=None)
        Filtra uma unidade federativa.
        Se uf=None, lista senadores de todas as UFs.

    Retorna
    -------
    dict
        Dicionário contendo informações dos senadores em exercício.
    '''

    tags = {}

    if participacao is not None:
        tags['participacao'] = participacao.upper()
    if uf is not None:
        tags['uf'] = _utils.parse_uf(uf)

    if len(tags) > 0:
        searchtags = _utils.convert_search_tags(tags)
    else:
        searchtags = ''

    url = f'{_url}senador/lista/atual{searchtags}'
    keys = ['ListaParlamentarEmExercicio', 'Parlamentares', 'Parlamentar']
    return _get_request(url, keys)



def lista_afastados() -> dict:
    '''
    Lista senadores atualmente afastados.

    Retorna
    -------
    dict
        Dicionário contendo informações dos senadores afastados.
    '''

    url = f'{_url}senador/lista/afastados'
    keys = ['AfastamentoAtual', 'Parlamentares', 'Parlamentar']
    return _get_request(url, keys)



def lista_legislatura(
        inicio: int,
        fim = None,
        exercicio = None,
        participacao = None,
        uf = None
    ) -> dict:
    '''
    Lista senadores de uma legislatura ou de um intervalo de legislaturas.

    Parâmetros
    ----------
    inicio: int
        Código da primeira legislatura da consulta.
    fim: int (default=None)
        Código da última legislatura da consulta.
        Se fim=None, pesquisa apenas pela legislatura do campo `inicio`.
        Caso contrário, pesquisa todas os valores de todas as legislaturas
        entre `inicio` e `fim`. 
    exercicio: str (default=None)
        - 'S': Consulta apenas os senadores que entraram em exercício.
        - 'N': Consulta apenas os senadores que não entratam em exercício.
    participacao: str (default=None)
        Tipo de participação.
        - None: Busca qualquer tipo de participação.
        - 'T': Busca apenas titulares.
        - 'S': Busca apenas suplentes.
    uf: str (default=None)
        Filtra uma unidade federativa.
        Se uf=None, lista senadores de todas as UFs.

    Retorna
    -------
    dict
        Dicionário contendo informações dos senadores das legislaturas
        consultadas.
    '''

    url = f'{_url}senador/lista/legislatura/{inicio}'
    
    if fim is not None:
        url += f'/{fim}'

    tags = {}

    if exercicio is not None:
        tags['exercicio'] = exercicio.upper()
    if participacao is not None:
        tags['participacao'] = participacao.upper()
    if uf is not None:
        tags['uf'] = _utils.parse_uf(uf)

    if len(tags) > 0:
        searchtags = _utils.convert_search_tags(tags)
    else:
        searchtags = ''
    
    url += searchtags

    keys = ['ListaParlamentarLegislatura', 'Parlamentares', 'Parlamentar']
    return _get_request(url, keys)



def partidos(ativos=True, index=False) -> pd.DataFrame:
    '''
    Lista os partidos políticos.

    Parâmetros
    ----------
    ativos: bool (default=True)
        - True para listar apenas os partidos ativos.
        - False para incluir partidos inativos na lista.
    index: bool (default=False)
        Se True, define a coluna `Codigo` como index do DataFrame.

    Retorna
    -------
    pandas.DataFrame
        DataFrame contendo a lista de partidos políticos consultados.
    '''

    url = f'{_url}senador/partidos'
    if not ativos:
        url += '?indAtivos=N'
    
    keys = ['ListaPartidos','Partidos', 'Partido']
    r = _get_request(url, keys)
    df = pd.DataFrame(r)

    if index:
        df.set_index('Codigo', inplace=True)

    df.DataCriacao = pd.to_datetime(df.DataCriacao)
    if not ativos:
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
        keys = ['DetalheParlamentar', 'Parlamentar']
        self.dados = _get_request(f'{_url}senador/{cod}', keys)
        self.dados.pop('OutrasInformacoes', None)
        self.dados.pop('UrlGlossario', None)
        self.identificacao = self.dados['IdentificacaoParlamentar']
        self.dados_basicos = self.dados['DadosBasicosParlamentar']

    
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

        url = f'{_url}senador/{self.cod}/cargos{searchtags}'
        keys = ['CargoParlamentar', 'Parlamentar', 'Cargos', 'Cargo']
        return _get_request(url, keys)


    def filiacoes(self):
        '''
        Obtém as filiações partidárias que o senador já teve.
        '''

        url = f'{_url}senador/{self.cod}/filiacoes'
        keys = ['FiliacaoParlamentar', 'Parlamentar', 'Filiacoes', 'Filiacao']
        return _get_request(url, keys)

    
    def mandatos(self):
        '''
        Obtém os mandatos que o senador já teve.
        '''

        url = f'{_url}senador/{self.cod}/mandatos'
        keys = ['MandatoParlamentar', 'Parlamentar', 'Mandatos', 'Mandato']
        return _get_request(url, keys)


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

        url = f'{_url}senador/{self.cod}/comissoes{searchtags}'
        keys = ['MembroComissaoParlamentar', 'Parlamentar', 'MembroComissoes', 'Comissao']
        return _get_request(url, keys)


    def votacoes(self, ano=None, numero=None, sigla=None, tramitando=None):
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

        url = f'{_url}senador/{self.cod}/votacoes{searchtags}'
        keys = ['VotacaoParlamentar', 'Parlamentar', 'Votacoes', 'Votacao']
        return _get_request(url, keys)


    def liderancas(self):
        '''
        Obtém os cargos de liderança de um senador.
        '''

        url = f'{_url}senador/{self.cod}/liderancas'
        keys = ['LiderancaParlamentar', 'Parlamentar', 'Liderancas', 'Lideranca']
        return _get_request(url, keys)


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

        url = f'{_url}senador/{self.cod}/licencas{searchtags}'
        keys = ['LicencaParlamentar', 'Parlamentar', 'Licencas', 'Licenca']
        return _get_request(url, keys)


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

        url = f'{_url}senador/{self.cod}/autorias{searchtags}'
        keys = ['MateriasAutoriaParlamentar', 'Parlamentar', 'Autorias', 'Autoria']
        return _get_request(url, keys)


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

        url = f'{_url}senador/{self.cod}/relatorias{searchtags}'
        keys = ['MateriasRelatoriaParlamentar', 'Parlamentar', 'Relatorias', 'Relatoria']
        return _get_request(url, keys)


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

        url = f'{_url}senador/{self.cod}/discursos{searchtags}'
        keys = ['DiscursosParlamentar', 'Parlamentar', 'Pronunciamentos', 'Pronunciamento']
        return _get_request(url, keys)


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

        url = f'{_url}senador/{self.cod}/apartes{searchtags}'
        keys = ['ApartesParlamentar', 'Parlamentar', 'Apartes', 'Aparte']
        return _get_request(url, keys)


    def historico(self):
        '''
        Obtém todos os detalhes de um parlamentar no(s) mandato(s) como
        senador (mandato atual e anteriores, se houver).
        '''

        url = f'{_url}senador/{self.cod}/historico'
        keys = ['DetalheParlamentar', 'Parlamentar']
        d = _get_request(url, keys)
        d.pop('OutrasInformacoes', None)
        d.pop('UrlGlossario', None)
        return d