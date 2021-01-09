'''
Módulo para captura dos dados abertos da Senado Brasileiro.

Exemplos
--------
Utilize as funções `lista` para identificar o código do Senado desejado.
>>> from DadosAbertosBrasil import senado
>>> senado.lista_atual( ... )
>>> senado.lista_afastados( ... )
>>> senado.lista_legislatura( ... )

Utilize a classe Senador para obter as informações do(a) parlamentar.
>>> sen = senado.Senador(cod)

Após a class Senador ser instanciada, utilize seus métodos para buscas
outros tipos de informação sobre ele(a).
>>> sen.cargos( ... )
>>> sen.votacoes( ... )
>>> ... 

Documentação da API original: http://legis.senado.gov.br/dadosabertos/docs/
'''



import pandas as pd
import requests

from . import _utils



_URL = r'http://legis.senado.gov.br/dadosabertos/'



def _get_request(url:str, keys=None) -> dict:
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

    --------------------------------------------------------------------------
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

    url = f'{_URL}senador/lista/atual{searchtags}'
    keys = ['ListaParlamentarEmExercicio', 'Parlamentares', 'Parlamentar']
    return _get_request(url, keys)



def lista_afastados() -> dict:
    '''
    Lista senadores atualmente afastados.

    Retorna
    -------
    dict
        Dicionário contendo informações dos senadores afastados.

    --------------------------------------------------------------------------
    '''

    url = f'{_URL}senador/lista/afastados'
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

    --------------------------------------------------------------------------
    '''

    url = f'{_URL}senador/lista/legislatura/{inicio}'
    
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

    --------------------------------------------------------------------------
    '''

    url = f'{_URL}senador/partidos'
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



class Senador:
    '''
    Coleta os dados dos senadores.

    Parâmetros
    ----------
    cod: int
        Código de senador que se dejesa consulta.
        O código pode ser encontrado pelas funções `lista_*` deste módulo.

    Atributos
    ---------
    dados: dict
        Dicionário completo de dados do(a) parlamentar.
    nome: str
        Nome do(a) parlamentar.
    nome_completo: str
        Nome completo do(a) parlamentar.
    nascimento: str
        Data de nascimento do(a) parlamentar no formato 'AAAA-MM-DD'.
    partido: str
        Atual partido político do(a) parlamentar.
    sexo: str
        Sexo ('Masculino' ou 'Feminino') do(a) parlamentar.
    tratamento: str
        Pronome de tratamento usado para o(a) parlamentar.

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        keys = ['DetalheParlamentar', 'Parlamentar']
        self.dados = _get_request(f'{_URL}senador/{cod}', keys)
        self.nome = self._get_info(
            ['IdentificacaoParlamentar', 'NomeParlamentar'])
        self.nome_completo = self._get_info(
            ['IdentificacaoParlamentar', 'NomeCompletoParlamentar'])
        self.nascimento = self._get_info(
            ['DadosBasicosParlamentar', 'DataNascimento'])
        self.partido = self._get_info(
            ['IdentificacaoParlamentar', 'SiglaPartidoParlamentar'])
        self.sexo = self._get_info(
            ['IdentificacaoParlamentar', 'SexoParlamentar'])
        self.tratamento = self._get_info(
            ['IdentificacaoParlamentar', 'FormaTratamento'])


    def _get_info(self, keys:list):
        x = self.dados
        try:
            for key in keys:
                x = x[key]
            return x
        except (KeyError, TypeError):
            return None


    def apartes(
            self,
            casa = None,
            data_inicio = None,
            data_fim = None,
            numero_sessao = None,
            tipo_pronunciamento = None,
            tipo_sessao = None
        ) -> list:
        '''
        Obtém a relação de apartes do senador.

        Parâmetros
        ----------
        casa: str (default=None)
            Sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        data_inicio: int (default=None)
            Data inicial do período da pesquisa no formato AAAAMMDD
        data_fim: int (default=None)
            Data final do período da pesquisa no formato AAAAMMDD
        numero_sessao: int (default=None)
            Número da sessão plenária.
        tipo_pronunciamento: str (default=None)
            Sigla do tipo de pronunciamento.
        tipo_sessao: str (default=None)
            Tipo da sessão plenária.
        
        Retorna
        -------
        list of dict
            Lista de apartes do(a) parlamentar.

        --------------------------------------------------------------------------
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

        searchtags = _utils.convert_search_tags(tags) if len(tags)>0 else ''
        url = f'{_URL}senador/{self.cod}/apartes{searchtags}'
        keys = ['ApartesParlamentar', 'Parlamentar', 'Apartes', 'Aparte']
        return _get_request(url, keys)

        
    def autorias(
            self,
            ano = None,
            numero = None,
            primeiro_autor = None,
            sigla = None,
            tramitando = None
        ) -> list:
        '''
        Obtém as matérias de autoria de um senador.

        Parâmetros
        ----------
        ano: int (default=None)
            Retorna apenas as matérias do ano informado.
        numero: int (default=None)
            Retorna apenas as matérias do número informado.
        primeiro_autor: bool (default=None)
            - True: Retorna apenas as matérias cujo senador é o primeiro autor;
            - False: Retorna apenas as que o senador é coautor;
            - None: Retorna ambas.
        sigla: str (default=None)
            Retorna apenas as matérias da sigla informada.
        tramitando: bool (default=None)
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.

        Retorna
        -------
        list of dict
            Lista de matérias de autoria do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        tags = {}
        if ano is not None:
            tags['ano'] = ano
        if numero is not None:
            tags['numero'] = numero
        if primeiro_autor is not None:
            tags['primeiro'] = 'S' if primeiro_autor else 'N'
        else:
            tags['primeiro'] = 'T'
        if sigla is not None:
            tags['sigla'] = sigla
        if tramitando is not None:
            tags['tramitando'] = 'S' if tramitando else 'N'

        searchtags = _utils.convert_search_tags(tags) if len(tags)>0 else ''
        url = f'{_URL}senador/{self.cod}/autorias{searchtags}'
        keys = ['MateriasAutoriaParlamentar', 'Parlamentar', 'Autorias', 'Autoria']
        return _get_request(url, keys)

    
    def cargos(self, comissao=None, ativos=None) -> list:
        '''
        Obtém a relação de cargos que o senador ja ocupou.

        Parâmetros
        ----------
        comissao: str (default=None)
            Retorna apenas os cargos da sigla de comissão informada.
        ativos: bool (default=None)
            - True: Retorna apenas os cargos atuais;
            - False: Retorna apenas os cargos já finalizadas;
            - None: Retorna ambos.

        Retorna
        -------
        list of dict
            Lista de comissões que o(a) parlamentar seja membro.

        --------------------------------------------------------------------------
        '''

        tags = {}
        if comissao is not None:
            tags['comissao'] = comissao
        if ativos is not None:
            tags['indAtivos'] = 'S' if ativos else 'N'

        searchtags = _utils.convert_search_tags(tags) if len(tags)>0 else ''
        url = f'{_URL}senador/{self.cod}/cargos{searchtags}'
        keys = ['CargoParlamentar', 'Parlamentar', 'Cargos', 'Cargo']
        return _get_request(url, keys)


    def comissoes(self, comissao=None, ativos=None) -> list:
        '''
        Obtém as comissões de que um senador é membro.

        Parâmetros
        ----------
        comissao: str (default=None)
            Retorna apenas as comissões com a sigla informada.
        ativos: bool (default=None)
            - True: Retorna apenas as comissões atuais;
            - False: Retorna apenas as comissões já finalizadas;
            - None: Retorna ambas.

        Retorna
        -------
        list of dict
            Lista de comissões que o(a) parlamentar seja membro.

        --------------------------------------------------------------------------
        '''

        tags = {}
        if comissao is not None:
            tags['comissao'] = comissao
        if ativos is not None:
            tags['indAtivos'] = 'S' if ativos else 'N'

        searchtags = _utils.convert_search_tags(tags) if len(tags)>0 else ''
        url = f'{_URL}senador/{self.cod}/comissoes{searchtags}'
        keys = ['MembroComissaoParlamentar', 'Parlamentar', 'MembroComissoes', 'Comissao']
        return _get_request(url, keys)


    def discursos(
            self,
            casa = None,
            data_inicio = None,
            data_fim = None,
            numero_sessao = None,
            tipo_pronunciamento = None,
            tipo_sessao = None
        ) -> list:
        '''
        Obtém a relação de discursos do senador.

        Parâmetros
        ----------
        casa: str (default=None)
            Sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        data_inicio: int (default=None)
            Data inicial do período da pesquisa no formato AAAAMMDD
        data_fim: int (default=None)
            Data final do período da pesquisa no formato AAAAMMDD
        numero_sessao: int (default=None)
            Número da sessão plenária.
        tipo_pronunciamento: str (default=None)
            Sigla do tipo de pronunciamento.
        tipo_sessao: str (default=None)
            Tipo da sessão plenária.
        
        Retorna
        -------
        list of dict
            Lista de discursos do(a) parlamentar.

        --------------------------------------------------------------------------
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

        searchtags = _utils.convert_search_tags(tags) if len(tags)>0 else ''
        url = f'{_URL}senador/{self.cod}/discursos{searchtags}'
        keys = ['DiscursosParlamentar', 'Parlamentar', 'Pronunciamentos', 'Pronunciamento']
        return _get_request(url, keys)


    def filiacoes(self) -> list:
        '''
        Obtém as filiações partidárias que o senador já teve.

        Retorna
        -------
        list of dict
            Lista de filiações do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        url = f'{_URL}senador/{self.cod}/filiacoes'
        keys = ['FiliacaoParlamentar', 'Parlamentar', 'Filiacoes', 'Filiacao']
        return _get_request(url, keys)


    def historico(self) -> dict:
        '''
        Obtém todos os detalhes de um parlamentar no(s) mandato(s) como
        senador (mandato atual e anteriores, se houver).

        Retorna
        -------
        dict
            Dados históricos do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        url = f'{_URL}senador/{self.cod}/historico'
        keys = ['DetalheParlamentar', 'Parlamentar']
        d = _get_request(url, keys)
        d.pop('OutrasInformacoes', None)
        d.pop('UrlGlossario', None)
        return d

    
    def mandatos(self) -> list:
        '''
        Obtém os mandatos que o senador já teve.

        Retorna
        -------
        list of dict
            Lista de mandatos do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        url = f'{_URL}senador/{self.cod}/mandatos'
        keys = ['MandatoParlamentar', 'Parlamentar', 'Mandatos', 'Mandato']
        return _get_request(url, keys)


    def liderancas(self) -> list:
        '''
        Obtém os cargos de liderança de um senador.

        Retorna
        -------
        list of dict
            Lista de cargos de liderança do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        url = f'{_URL}senador/{self.cod}/liderancas'
        keys = ['LiderancaParlamentar', 'Parlamentar', 'Liderancas', 'Lideranca']
        return _get_request(url, keys)


    def licencas(self, data=None):
        '''
        Obtém as licenças de um senador.

        Parâmetros
        ----------
        data: str (default=None)
            Retorna as licenças a partir da data especificada.

        Retorna
        -------
        list of dict
            Lista de licenças do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        tags = {}
        if data is not None:
            tags['dataInicio'] = data

        searchtags = _utils.convert_search_tags(tags) if len(tags)>0 else ''
        url = f'{_URL}senador/{self.cod}/licencas{searchtags}'
        keys = ['LicencaParlamentar', 'Parlamentar', 'Licencas', 'Licenca']
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

        Parâmetros
        ----------
        ano: int (default=None)
            Retorna apenas as matérias do ano informado.
        comissao: str (default=None)
            Retorna apenas as relatorias da comissão informada.
        numero: int (default=None)
            Retorna apenas as matérias do número informado. 
        sigla: str (default=None)
            Retorna apenas as matérias da sigla informada.	 
        tramitando: bool (default=None)
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.
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
            tags['tramitando'] = 'S' if tramitando else 'N'

        searchtags = _utils.convert_search_tags(tags) if len(tags)>0 else ''
        url = f'{_URL}senador/{self.cod}/relatorias{searchtags}'
        keys = ['MateriasRelatoriaParlamentar', 'Parlamentar', 'Relatorias', 'Relatoria']
        return _get_request(url, keys)


    def votacoes(
            self,
            ano = None,
            numero = None,
            sigla = None,
            tramitando = None
        ) -> list:
        '''
        Obtém as votações de um senador.

        Parâmetros
        ----------
        ano: int (default=None)
            Retorna apenas as matérias do ano informado.
        numero: int (default=None)
            Retorna apenas as matérias do número informado. 	 
        sigla: str (default=None)
            Retorna apenas as matérias da sigla informada. 	 
        tramitando: bool (default=None)
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.

        Retorna
        -------
        list of dict
            Lista de votações do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        tags = {}
        if ano is not None:
            tags['ano'] = ano
        if numero is not None:
            tags['numero'] = numero
        if sigla is not None:
            tags['sigla'] = sigla
        if tramitando is not None:
            tags['tramitando'] = 'S' if tramitando else 'N'

        searchtags = _utils.convert_search_tags(tags) if len(tags)>0 else ''
        url = f'{_URL}senador/{self.cod}/votacoes{searchtags}'
        keys = ['VotacaoParlamentar', 'Parlamentar', 'Votacoes', 'Votacao']
        return _get_request(url, keys)