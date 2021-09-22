'''
Módulo para captura dos dados abertos da Senado Brasileiro.

Mini-Tutorial
-------------
1. Importe o módulo `senado`
>>> from DadosAbertosBrasil import senado

2. Utilize as funções `lista` para identificar o código do Senado desejado.
>>> senado.lista_atual( ... )
>>> senado.lista_afastados( ... )
>>> senado.lista_legislatura( ... )

3. Utilize a class `Senador` para obter as informações do(a) parlamentar.
>>> sen = senado.Senador(cod)

4. Após a class `Senador` ser instanciada, utilize seus métodos para buscas
outros tipos de informação sobre ele(a).
>>> sen.cargos( ... )
>>> sen.votacoes( ... )
>>> ... 

Documentação da API original
----------------------------
http://legis.senado.gov.br/dadosabertos/docs/

------------------------------------------------------------------------------
'''



import pandas as _pd

from ._utils import parse
from ._utils.get_data import get_data



_normalize = _pd.io.json.json_normalize \
    if _pd.__version__[0] == '0' else _pd.json_normalize



def _get_request(
        path: str,
        params: dict = None,
        keys: list = None
    ) -> dict:

    data = get_data(
        endpoint = 'http://legis.senado.gov.br/dadosabertos/',
        path = path,
        params = params
    )

    if keys is not None:
        for key in keys:
            if data is not None:
                if key in data:
                    data = data[key]

    return data



def lista_senadores(
        tipo: str = 'atual',
        uf: str = None,
        sexo: str = None,
        partido: str = None,
        contendo: str = None,
        excluindo: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''Lista de senadores da república.

    Parâmetros
    ----------
    tipo : str {'atual', 'titulares', 'suplentes', 'afastados'}
        - 'atual' (default): Todos os senadores em exercício;
        - 'titulares': Apenas senadores que iniciaram o mandato como titulares;
        - 'suplentes': Apenas senadores que iniciaram o mandato como suplentes;
        - 'afastados': Todos os senadores afastados.
    uf : str (default=None)
        Filtro de Unidade Federativa dos senadores.
    sexo : str (default=None)
        Filtro de sexo dos senadores.
    partido : str (default=None)
        Filtro de partido dos senadores.
    contendo : str (default=None)
        Captura apenas senadores contendo esse texto no nome.
    excluindo : str (default=None)
        Exclui da consulta senadores contendo esse texto no nome.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Tabela com informações básicas dos senadores consultados.

    Erros
    -----
    DAB_UFError
        Caso seja inserida uma UF inválida no argumento `uf`.

    Exemplos
    --------
    Lista todos os senadores ativos, colocando o código como index da tabela.

    >>> senado.lista_senadores(index=True)
    
    Lista senadores do partido PL do Rio de Janeiro.

    >>> senado.lista_senadores(partido='PL', uf='RJ')

    Lista senadores contendo 'Gomes' no nome, exceto os que contém 'Cid'.

    >>> senado.lista_senadores(contendo='Gomes', excluindo='Cid')

    Lista senadoras afastadas do sexo feminino.

    >>> senado.lista_senadores(tipo='afastados', sexo='F')
    
    '''

    tipo = tipo.lower()
    TIPOS = {
        'titulares': {
            'path': 'atual',
            'key': 'ListaParlamentarEmExercicio',
            'params': {'participacao': 'T'}
        },
        'suplentes': {
            'path': 'atual',
            'key': 'ListaParlamentarEmExercicio',
            'params': {'participacao': 'S'}
        },
        'atual': {
            'path': 'atual',
            'key': 'ListaParlamentarEmExercicio',
            'params': {}
        },
        'afastados': {
            'path': 'afastados',
            'key': 'AfastamentoAtual',
            'params': {}
        }
    }

    # Baixar dados
    params = TIPOS[tipo]['params']
    if uf is not None:
        params['uf'] = parse.uf(uf=uf)

    lista = _get_request(
        path = ['senador', 'lista', TIPOS[tipo]['path']],
        keys = [TIPOS[tipo]['key'], 'Parlamentares', 'Parlamentar'],
        params = params
    )

    df = _normalize(lista)

    # Selecionar e renomear colunas
    col_mapping = {
        'IdentificacaoParlamentar.CodigoParlamentar': 'codigo',
        'IdentificacaoParlamentar.NomeParlamentar': 'nome_parlamentar',
        'IdentificacaoParlamentar.NomeCompletoParlamentar': 'nome_completo',
        'IdentificacaoParlamentar.SexoParlamentar': 'sexo',
        'IdentificacaoParlamentar.FormaTratamento': 'forma_tratamento',
        'IdentificacaoParlamentar.UrlFotoParlamentar': 'foto',
        'IdentificacaoParlamentar.UrlPaginaParlamentar': 'pagina_parlamentar',
        'IdentificacaoParlamentar.UrlPaginaParticular': 'pagina_particular',
        'IdentificacaoParlamentar.EmailParlamentar': 'email',
        'IdentificacaoParlamentar.SiglaPartidoParlamentar': 'partido',
        'Mandato.UfParlamentar': 'uf',
        'Mandato.Exercicios.Exercicio.DataInicio': 'data_inicio',
        'Mandato.Exercicios.Exercicio.DataFim': 'data_fim',
        'Mandato.Exercicios.Exercicio.DescricaoCausaAfastamento': 'causa_afastamento'
    }
    df = df[[col for col in df.columns if col in col_mapping.keys()]]
    df.columns = df.columns.map(col_mapping)

    # Filtros
    if sexo is not None:
        sexo = sexo.title()
        SEXOS = {
            'Masculino': 'Masculino',
            'Feminino': 'Feminino',
            'M': 'Masculino',
            'F': 'Feminino'
        }
        df = df[df.sexo == SEXOS[sexo]]

    if (uf is not None) and (tipo == 'afastados'):
        df = df[df.uf == parse.uf(uf=uf)]

    if partido is not None:
        df = df[df.partido == partido.upper()]

    if contendo is not None:
        nome_parlamentar = df.nome_parlamentar.str.contains(contendo)
        nome_completo = df.nome_completo.str.contains(contendo)
        df = df[nome_parlamentar | nome_completo]
        
    if excluindo is not None:
        nome_parlamentar = ~df.nome_parlamentar.str.contains(excluindo)
        nome_completo = ~df.nome_completo.str.contains(excluindo)
        df = df[nome_parlamentar | nome_completo]

    # Corrigir index
    if index:
        df.set_index('codigo', inplace=True)
    else:
        df.reset_index(drop=True, inplace=True)

    return df



def lista_atual(
        participacao: str = None,
        uf: str = None
    ) -> dict:
    '''
    Lista senadores em exercício.

    Parâmetros
    ----------
    participacao : str (default=None)
        Tipo de participação.
        - None: Busca qualquer tipo de participação.
        - 'T': Busca apenas titulares.
        - 'S': Busca apenas suplentes.
    uf : str (default=None)
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
        tags['uf'] = parse.uf(uf)

    path = 'senador/lista/atual'
    keys = ['ListaParlamentarEmExercicio', 'Parlamentares', 'Parlamentar']
    return _get_request(path, tags, keys)



def lista_afastados() -> dict:
    '''
    Lista senadores atualmente afastados.

    Retorna
    -------
    dict
        Dicionário contendo informações dos senadores afastados.

    --------------------------------------------------------------------------
    '''

    url = f'senador/lista/afastados'
    keys = ['AfastamentoAtual', 'Parlamentares', 'Parlamentar']
    return _get_request(url, None, keys)



def lista_legislatura(
        inicio: int,
        fim: int = None,
        exercicio: str = None,
        participacao: str = None,
        uf: str = None
    ) -> dict:
    '''
    Lista senadores de uma legislatura ou de um intervalo de legislaturas.

    Parâmetros
    ----------
    inicio : int
        Código da primeira legislatura da consulta.
    fim : int (default=None)
        Código da última legislatura da consulta.
        Se fim=None, pesquisa apenas pela legislatura do campo `inicio`.
        Caso contrário, pesquisa todas os valores de todas as legislaturas
        entre `inicio` e `fim`. 
    exercicio : str (default=None)
        - 'S': Consulta apenas os senadores que entraram em exercício.
        - 'N': Consulta apenas os senadores que não entratam em exercício.
    participacao : str (default=None)
        Tipo de participação.
        - None: Busca qualquer tipo de participação.
        - 'T': Busca apenas titulares.
        - 'S': Busca apenas suplentes.
    uf : str (default=None)
        Filtra uma unidade federativa.
        Se uf=None, lista senadores de todas as UFs.

    Retorna
    -------
    dict
        Dicionário contendo informações dos senadores das legislaturas
        consultadas.

    --------------------------------------------------------------------------
    '''

    path = f'senador/lista/legislatura/{inicio}'
    
    if fim is not None:
        path += f'/{fim}'

    tags = {}
    if exercicio is not None:
        tags['exercicio'] = exercicio.upper()
    if participacao is not None:
        tags['participacao'] = participacao.upper()
    if uf is not None:
        tags['uf'] = parse.uf(uf)

    keys = ['ListaParlamentarLegislatura', 'Parlamentares', 'Parlamentar']
    return _get_request(path, tags, keys)



def orcamento(
        autor: str = None,
        tipo: str = None,
        ano_execucao: int = None,
        ano_materia: int = None
    ) -> _pd.DataFrame:
    '''Obtém a lista dos lotes de emendas orçamentárias.

    Parâmetros
    ----------
    autor : str (default=None)
        Texto contendo nome do autor.
    tipo : str (default=None)
        Tipo de orçamento.
    ano_execucao : int (default=None)
        Ano que o orçamento foi executado.
    ano_materia : int (default)
        Ano da matéria.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Tabela contendo todas as emendas orçamentárias pesquisadas.

    Exemplos
    --------
    Buscar o orçamento da Lei de Diretrizes Orçamentárias de 2020.

    >>> senado.orcamento(tipo='LDO', ano_execucao=2020)

    Pesquisar por emendas da Adriana Ventura

    >>> senado.orcamento(autor='Adriana')
    
    '''

    # Baixar dados
    data = _get_request(
        path = ['orcamento', 'lista'],
        keys = ['ListaLoteEmendas', 'LotesEmendasOrcamento', 'LoteEmendasOrcamento']
    )
    df = _pd.DataFrame(data)

    # Renomear colunas    
    col_mapping = {
        'NomeAutorOrcamento': 'autor_nome',
        'IndicadorAtivo': 'ativo',
        'EmailAutorOrcamento': 'autor_email',
        'CodigoAutorOrcamento': 'autor_codigo',
        'DataOperacao': 'data_operacao',
        'QuantidadeEmendas': 'quantidade_emendas',
        'AnoExecucao': 'ano_execucao',
        'NumeroMateria': 'numero_materia',
        'AnoMateria': 'ano_materia',
        'SiglaTipoPlOrcamento': 'tipo_sigla',
        'DescricaoTipoPlOrcamento': 'tipo_descricao'
    }
    df.columns = df.columns.map(col_mapping)

    # Corrigir tipos das colunas
    df.ativo = df.ativo == 'Sim'
    df.data_operacao = _pd.to_datetime(df.data_operacao)
    for col in ['autor_codigo', 'quantidade_emendas', 'ano_execucao', 'ano_materia']:
        df[col] = df[col].astype(int)

    # Filtros
    if autor is not None:
        df = df[df.autor_nome.str.contains(autor)]
    if tipo is not None:
        df = df[df.tipo_sigla == tipo]
    if ano_execucao is not None:
        df = df[df.ano_execucao == ano_execucao]
    if ano_materia is not None:
        df = df[df.ano_materia == ano_materia]

    return df.reset_index(drop=True)



def partidos(
        ativos: bool = True,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Lista os partidos políticos.

    Parâmetros
    ----------
    ativos : bool (default=True)
        - True para listar apenas os partidos ativos.
        - False para incluir partidos inativos na lista.
    index : bool (default=False)
        Se True, define a coluna `Codigo` como index do DataFrame.

    Retorna
    -------
    pandas.DataFrame
        DataFrame contendo a lista de partidos políticos consultados.

    --------------------------------------------------------------------------
    '''

    url = 'senador/partidos'
    if not ativos:
        url += '?indAtivos=N'
    
    keys = ['ListaPartidos', 'Partidos', 'Partido']
    r = _get_request(url, None, keys)
    df = _pd.DataFrame(r)

    if index:
        df.set_index('Codigo', inplace=True)

    df.DataCriacao = _pd.to_datetime(df.DataCriacao)
    if not ativos:
        df.DataExtincao = _pd.to_datetime(df.DataExtincao)

    return df



class Senador:
    '''
    Coleta os dados dos senadores.

    Parâmetros
    ----------
    cod : int
        Código de senador que se dejesa consulta.
        O código pode ser encontrado pelas funções `lista_*` deste módulo.

    Atributos
    ---------
    dados : dict
        Dicionário completo de dados do(a) parlamentar.
    nome : str
        Nome do(a) parlamentar.
    nome_completo : str
        Nome completo do(a) parlamentar.
    nascimento : str
        Data de nascimento do(a) parlamentar no formato 'AAAA-MM-DD'.
    partido : str
        Atual partido político do(a) parlamentar.
    sexo : str
        Sexo ('Masculino' ou 'Feminino') do(a) parlamentar.
    tratamento : str
        Pronome de tratamento usado para o(a) parlamentar.

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        keys = ['DetalheParlamentar', 'Parlamentar']
        self.dados = _get_request(f'senador/{cod}', None, keys)
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


    def __repr__(self):
        return f"<DadosAbertosBrasil.senado: Senador{'a' if self.sexo == 'Feminino' else ''} {self.nome}>"


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
            casa: str = None,
            inicio: int = None,
            fim: int = None,
            numero_sessao: int = None,
            tipo_pronunciamento: str = None,
            tipo_sessao: str = None
        ) -> list:
        '''
        Obtém a relação de apartes do senador.

        Parâmetros
        ----------
        casa : str (default=None)
            Sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        inicio : datetime.date ou str (default=None)
            Data inicial do período da pesquisa no formato 'AAAA-MM-DD'
        fim : datetime.date ou str (default=None)
            Data final do período da pesquisa no formato 'AAAA-MM-DD'
        numero_sessao : int (default=None)
            Número da sessão plenária.
        tipo_pronunciamento : str (default=None)
            Sigla do tipo de pronunciamento.
        tipo_sessao : str (default=None)
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
        if inicio is not None:
            tags['dataInicio'] = parse.data(inicio, 'senado')
        if fim is not None:
            tags['dataFim'] = parse.data(fim, 'senado')
        if numero_sessao is not None:
            tags['numeroSessao'] = numero_sessao
        if tipo_pronunciamento is not None:
            tags['tipoPronunciamento'] = tipo_pronunciamento
        if tipo_sessao is not None:
            tags['tipoSessao'] = tipo_sessao

        path = f'senador/{self.cod}/apartes'
        keys = ['ApartesParlamentar', 'Parlamentar', 'Apartes', 'Aparte']
        return _get_request(path, tags, keys)

        
    def autorias(
            self,
            ano: int = None,
            numero: int = None,
            primeiro_autor: bool = None,
            sigla: str = None,
            tramitando: bool = None
        ) -> list:
        '''
        Obtém as matérias de autoria de um senador.

        Parâmetros
        ----------
        ano : int (default=None)
            Retorna apenas as matérias do ano informado.
        numero : int (default=None)
            Retorna apenas as matérias do número informado.
        primeiro_autor : bool (default=None)
            - True: Retorna apenas as matérias cujo senador é o primeiro autor;
            - False: Retorna apenas as que o senador é coautor;
            - None: Retorna ambas.
        sigla : str (default=None)
            Retorna apenas as matérias da sigla informada.
        tramitando : bool (default=None)
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

        path = f'senador/{self.cod}/autorias'
        keys = ['MateriasAutoriaParlamentar', 'Parlamentar', 'Autorias', 'Autoria']
        return _get_request(path, tags, keys)

    
    def cargos(
            self,
            comissao: bool = None,
            ativos: bool = None
        ) -> list:
        '''
        Obtém a relação de cargos que o senador ja ocupou.

        Parâmetros
        ----------
        comissao : str (default=None)
            Retorna apenas os cargos da sigla de comissão informada.
        ativos : bool (default=None)
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

        path = f'senador/{self.cod}/cargos'
        keys = ['CargoParlamentar', 'Parlamentar', 'Cargos', 'Cargo']
        return _get_request(path, tags, keys)


    def comissoes(
            self,
            comissao: str = None,
            ativos: bool = None
        ) -> list:
        '''
        Obtém as comissões de que um senador é membro.

        Parâmetros
        ----------
        comissao : str (default=None)
            Retorna apenas as comissões com a sigla informada.
        ativos : bool (default=None)
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

        path = f'senador/{self.cod}/comissoes'
        keys = ['MembroComissaoParlamentar', 'Parlamentar', 'MembroComissoes', 'Comissao']
        return _get_request(path, tags, keys)


    def discursos(
            self,
            casa: str = None,
            inicio: int = None,
            fim: int = None,
            numero_sessao: int = None,
            tipo_pronunciamento: str = None,
            tipo_sessao: str = None
        ) -> list:
        '''
        Obtém a relação de discursos do senador.

        Parâmetros
        ----------
        casa : str (default=None)
            Sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        inicio : datetime.date ou str (default=None)
            Data inicial do período da pesquisa no formato 'AAAA-MM-DD'
        fim : datetime.date ou str (default=None)
            Data final do período da pesquisa no formato 'AAAA-MM-DD'
        numero_sessao : int (default=None)
            Número da sessão plenária.
        tipo_pronunciamento : str (default=None)
            Sigla do tipo de pronunciamento.
        tipo_sessao : str (default=None)
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
        if inicio is not None:
            tags['dataInicio'] = parse.data(inicio, 'senado')
        if fim is not None:
            tags['dataFim'] = parse.data(fim, 'senado')
        if numero_sessao is not None:
            tags['numeroSessao'] = numero_sessao
        if tipo_pronunciamento is not None:
            tags['tipoPronunciamento'] = tipo_pronunciamento
        if tipo_sessao is not None:
            tags['tipoSessao'] = tipo_sessao

        path = f'senador/{self.cod}/discursos'
        keys = ['DiscursosParlamentar', 'Parlamentar', 'Pronunciamentos', 'Pronunciamento']
        return _get_request(path, tags, keys)


    def filiacoes(self) -> list:
        '''
        Obtém as filiações partidárias que o senador já teve.

        Retorna
        -------
        list of dict
            Lista de filiações do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        path = f'senador/{self.cod}/filiacoes'
        keys = ['FiliacaoParlamentar', 'Parlamentar', 'Filiacoes', 'Filiacao']
        return _get_request(path, None, keys)


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

        path = f'senador/{self.cod}/historico'
        keys = ['DetalheParlamentar', 'Parlamentar']
        d = _get_request(path, None, keys)
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

        path = f'senador/{self.cod}/mandatos'
        keys = ['MandatoParlamentar', 'Parlamentar', 'Mandatos', 'Mandato']
        return _get_request(path, None, keys)


    def liderancas(self) -> list:
        '''
        Obtém os cargos de liderança de um senador.

        Retorna
        -------
        list of dict
            Lista de cargos de liderança do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        path = f'senador/{self.cod}/liderancas'
        keys = ['LiderancaParlamentar', 'Parlamentar', 'Liderancas', 'Lideranca']
        return _get_request(path, None, keys)


    def licencas(
            self,
            inicio: str = None
        ) -> list:
        '''
        Obtém as licenças de um senador.

        Parâmetros
        ----------
        inicio : datetime.date ou str (default=None)
            Retorna as licenças a partir da data especificada.

        Retorna
        -------
        list of dict
            Lista de licenças do(a) parlamentar.

        --------------------------------------------------------------------------
        '''

        tags = {}
        if inicio is not None:
            tags['dataInicio'] = parse.data(inicio, 'senado')

        path = f'senador/{self.cod}/licencas'
        keys = ['LicencaParlamentar', 'Parlamentar', 'Licencas', 'Licenca']
        return _get_request(path, tags, keys)


    def relatorias(
            self,
            ano: int = None,
            comissao: str = None,
            numero: int = None,
            sigla: str = None,
            tramitando: bool = None
        ) -> list:
        '''
        Obtém as matérias de relatoria de um senador.

        Parâmetros
        ----------
        ano : int (default=None)
            Retorna apenas as matérias do ano informado.
        comissao : str (default=None)
            Retorna apenas as relatorias da comissão informada.
        numero : int (default=None)
            Retorna apenas as matérias do número informado. 
        sigla : str (default=None)
            Retorna apenas as matérias da sigla informada.	 
        tramitando : bool (default=None)
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.

        Retorna
        -------
        list of dict
            Lista de matérias de relatoria de um senador.

        ----------------------------------------------------------------------
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

        path = f'senador/{self.cod}/relatorias'
        keys = ['MateriasRelatoriaParlamentar', 'Parlamentar', 'Relatorias', 'Relatoria']
        return _get_request(path, tags, keys)


    def votacoes(
            self,
            ano: int = None,
            numero: int = None,
            sigla: str = None,
            tramitando: bool = None
        ) -> list:
        '''
        Obtém as votações de um senador.

        Parâmetros
        ----------
        ano : int (default=None)
            Retorna apenas as matérias do ano informado.
        numero : int (default=None)
            Retorna apenas as matérias do número informado. 	 
        sigla : str (default=None)
            Retorna apenas as matérias da sigla informada. 	 
        tramitando : bool (default=None)
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

        path = f'senador/{self.cod}/votacoes'
        keys = ['VotacaoParlamentar', 'Parlamentar', 'Votacoes', 'Votacao']
        return _get_request(path, tags, keys)