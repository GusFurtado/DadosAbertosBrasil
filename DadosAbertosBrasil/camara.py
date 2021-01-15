'''
Módulo para captura dos dados abertos da Câmara dos Deputados do Brasil

Use o seguinte template para buscar dados:
>>> from DadosAbertosBrasil import camara
>>> camara.{funcao}(cod={opcional}, serie={opcional}, index={True/False})

Documentação da API original: https://dadosabertos.camara.leg.br/swagger/api.html
'''



import warnings

import pandas as _pd

from . import API



_api = API('camara')



def _df(dados:dict, index_col=None) -> _pd.DataFrame:
    '''
    Converte dados brutos da API em um DataFrame.

    Parâmetros
    ----------
    dados: dict
        Dados brutos da API.
    index_col: str (default=None)
        Nome da coluna que será usada como index do DataFrame.

    Retorna
    -------
    pandas.core.frames.DataFrame
        Dados convertidos em DataFrame.
    '''

    df = _pd.DataFrame(dados['dados'])
    if index_col is not None:
        df.set_index(index_col, inplace=True)

    return df



def _query(
        funcao: str,
        series: list,
        cod = None,
        serie = 'informacoes',
        index = False,
    ) -> _pd.DataFrame:
    '''
    Função que constrói queries de busca.

    Parâmetros
    ----------
    funcao: str
        Função que se deseja buscar.
    series: list
        Lista de séries disponíveis dentro da função.
    cod: int ou str (default=None)
        ID do item que se deseja obter informações.
    serie: str (default='informacoes')
        Série escolhida dentro da lista `series`.
        Este argumento é ignorado quando `cod=None`.
    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.
        Este argumento só é valido quando `cod=None`.

    Retorna
    -------
    pandas.DataFrame ou dict
        - DataFrame quando uma lista de códigos for retornada.
        - dict quando as infomações de apenas um código foram consultadas. 

    --------------------------------------------------------------------------
    '''
    
    path = [funcao]
    if cod is not None:
        path.append(str(cod))
        if serie in series:
            if serie != 'informacoes':
                path.append(serie)
        else:
            raise TypeError(f"O valor de `serie` deve ser um dos seguintes valores: {series}")
            
    data = _api.get(path)['dados']

    if cod is None:
        df = _pd.DataFrame(data)
        df = df.loc[:,~df.columns.str.startswith('uri')]
        if index:
            df.set_index('id', inplace=True)
        
        return df
    return data



def blocos(cod=None, index=False):
    '''
    Dados sobre os blocos partidários.

    Parâmetros
    ----------
    cod: int ou str (default=None)
        ID do item que se deseja obter informações.
    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame ou dict
        - Se `cod=None`, retorna DataFrame com lista de blocos partidários.
        - Caso contrário, retorna dict de informações do bloco partidário.

    --------------------------------------------------------------------------
    '''

    series = ['informacoes']
    return _query('blocos', series, cod, 'informacoes', index)



def eventos(cod=None, serie='informacoes', index=False):
    '''
    Dados sobre os eventos ocorridos ou previstos nos diversos órgãos da Câmara.

    Parâmetros
    ----------
    cod: int ou str (default=None)
        ID do item que se deseja obter informações.
    serie: str (default='informacoes')
        Dados que se deseja consultar:
        - 'informacoes';
        - 'deputados';
        - 'orgaos';
        - 'pauta';
        - 'votacoes'.
    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame ou dict
        - Se `cod=None`, retorna DataFrame com lista de eventos.
        - Caso contrário, retorna dict de informações do evento.

    --------------------------------------------------------------------------
    '''

    series = ['informacoes', 'deputados', 'orgaos', 'pauta', 'votacoes']
    return _query('eventos', series, cod, serie, index)



def frentes(cod=None, serie='informacoes', index=False):
    '''
    Dados de frentes parlamentares de uma ou mais legislatura.

    Parâmetros
    ----------
    cod: int ou str (default=None)
        ID do item que se deseja obter informações.
    serie: str (default='informacoes')
        Dados que se deseja consultar:
        - 'informacoes';
        - 'membros'.
    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame ou dict
        - Se `cod=None`, retorna DataFrame com lista de frentes parlamentares.
        - Caso contrário, retorna dict de informações da frente parlamentar.

    --------------------------------------------------------------------------
    '''

    series = ['informacoes', 'membros']
    return _query('frentes', series, cod, serie, index)



def legislaturas(cod=None, serie='informacoes', index=False):
    '''
    Dados dos períodos de mantados e atividades parlamentares na Câmara.

    Parâmetros
    ----------
    cod: int ou str (default=None)
        ID do item que se deseja obter informações.
    serie: str (default='informacoes')
        Dados que se deseja consultar:
        - 'informacoes';
        - 'mesa'.
    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame ou dict
        - Se `cod=None`, retorna DataFrame com lista de legislaturas.
        - Caso contrário, retorna dict de informações da legislatura.

    --------------------------------------------------------------------------
    '''

    series = ['informacoes', 'mesa']
    return _query('legislaturas', series, cod, serie, index)



def orgaos(cod=None, serie='informacoes', index=False):
    '''
    Dados de comissões e outros órgãos legislativos da Câmara.

    Parâmetros
    ----------
    cod: int ou str (default=None)
        ID do item que se deseja obter informações.
    serie: str (default='informacoes')
        Dados que se deseja consultar:
        - 'informacoes';
        - 'eventos';
        - 'membros';
        - 'votacoes'.
    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame ou dict
        - Se `cod=None`, retorna DataFrame com lista de órgãos legislativos.
        - Caso contrário, retorna dict de informações do órgão legislativo.

    --------------------------------------------------------------------------
    '''

    series = ['informacoes', 'eventos', 'membros', 'votacoes']
    return _query('orgaos', series, cod, serie, index)



def partidos(cod=None, serie='informacoes', index=False):
    '''
    Dados dos partidos políticos que tem ou já tiveram parlamentares
    em exercício na Câmara.

    Parâmetros
    ----------
    cod: int ou str (default=None)
        ID do item que se deseja obter informações.
    serie: str (default='informacoes')
        Dados que se deseja consultar:
        - 'informacoes';
        - 'membros'.
    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame ou dict
        - Se `cod=None`, retorna DataFrame com lista de partidos políticos.
        - Caso contrário, retorna dict de informações do partido político.

    --------------------------------------------------------------------------
    '''

    series = ['informacoes', 'membros']
    return _query('partidos', series, cod, serie, index)



def proposicoes(cod=None, serie='informacoes', index=False):
    '''
    Dados de proposições na Câmara.

    Parâmetros
    ----------
    cod: int ou str (default=None)
        ID do item que se deseja obter informações.
    serie: str (default='informacoes')
        Dados que se deseja consultar:
        - 'informacoes';
        - 'autores';
        - 'relacionadas';
        - 'temas';
        - 'tramitacoes';
        - 'votacoes'.
    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame ou dict
        - Se `cod=None`, retorna DataFrame com lista de proposições.
        - Caso contrário, retorna dict de informações da proposição.

    --------------------------------------------------------------------------
    '''

    series = [
        'informacoes',
        'autores',
        'relacionadas',
        'temas',
        'tramitacoes',
        'votacoes'
    ]

    return _query('proposicoes', series, cod, serie, index)



def votacoes(cod=None, serie='informacoes', index=False):
    '''
    Dados de votações na Câmara.

    Parâmetros
    ----------
    cod: int ou str (default=None)
        ID do item que se deseja obter informações.
    serie: str (default='informacoes')
        Dados que se deseja consultar:
        - 'informacoes';
        - 'orientacoes';
        - 'votos'.
    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame ou dict
        - Se `cod=None`, retorna DataFrame com lista de votações.
        - Caso contrário, retorna dict de informações da votação.

    --------------------------------------------------------------------------
    '''

    series = ['informacoes', 'orientacoes', 'votos']
    return _query('votacoes', series, cod, serie, index)



def referencias(funcao, index=False) -> _pd.DataFrame:
    '''
    Listas de valores válidos para as funções deste pacote.

    Parâmetros
    ----------
    funcao: str
        - 'codSituacaoDeputados',
        - 'siglaUF',
        - 'codSituacaoEvento',
        - 'codTipoEvento',
        - 'codSituacaoOrgao',
        - 'codTipoOrgao',
        - 'codTipoAutor',
        - 'codSituacaoProposicao',
        - 'codTema',
        - 'codTipoTramitacao',
        - 'siglaTipo',
        - 'situacoesDeputado'
        - 'situacoesEvento'
        - 'situacoesOrgao'
        - 'situacoesProposicao'
        - 'tiposEvento'
        - 'tiposOrgao'
        - 'tiposProposicao'
        - 'tiposTramitacao'
        - 'uf'

    index: bool (default=False)
        Se True, define a coluna código como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista das referências válidas.

    '''
    
    referencia = {
        'codSituacaoDeputados': 'deputados/codSituacao',
        'siglaUF': 'deputados/siglaUF',
        'codSituacaoEvento': 'eventos/codSituacaoEvento',
        'codTipoEvento': 'eventos/codTipoEvento',
        'codSituacaoOrgao': 'orgaos/codSituacao',
        'codTipoOrgao': 'orgaos/codTipoOrgao',
        'codTipoAutor': 'proposicoes/codTipoAutor',
        'codSituacaoProposicao': 'proposicoes/codSituacao',
        'codTema': 'proposicoes/codTema',
        'codTipoTramitacao': 'proposicoes/codTipoTramitacao',
        'siglaTipo': 'proposicoes/siglaTipo',
        'situacoesDeputado': 'situacoesDeputado',
        'situacoesEvento': 'situacoesEvento',
        'situacoesOrgao': 'situacoesOrgao',
        'situacoesProposicao': 'situacoesProposicao',
        'tiposEvento': 'tiposEvento',
        'tiposOrgao': 'tiposOrgao',
        'tiposProposicao': 'tiposProposicao',
        'tiposTramitacao': 'tiposTramitacao',
        'uf': 'uf'
    }
    
    if funcao in referencia.keys():
        data = _api.get(f'referencias/{referencia[funcao]}')
    else:
        raise TypeError(f"Referência inválida. Insira um dos seguintes valores para `funcao`: {list(referencia.keys())}")
    
    df = _pd.DataFrame(data['dados'])
    if index:
        df.set_index('cod', inplace=True)
    
    return df



class Deputado:
    '''
    Retorna os dados cadastrais de um parlamentar que, em algum momento
    da história e por qualquer período, entrou em exercício na Câmara.

    Parâmetros
    ----------
    cod: int
        Código do parlamentar.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código de identificação.
    condicao_eleitoral: str
        Condição eleitoral.
    cpf: str
        Número do CPF.
    descricao_status: str
        Descrição do último status.
    email: str
        E-mail.
    escolaridade: str
        Escolaridade.
    falecimento: str
        Data de falecimento no formato 'AAAA-MM-DD'.
        Retorna vazio caso o parlamentar não tenha falecido.
    foto: str
        URL da foto.
    gabinete: dict
        Informações de identificação e contato do gabinete.
    legislatura: int
        ID da legislatura mais recente.
    municipio_nascimento: str
        Município de nascimento.
    nascimento: str
        Data de nascimento no formato 'AAAA-MM-DD'.
    nome: str
        Nome mais comum.
    nome_completo: str
        Nome civil completo.
    nome_eleitoral: str
        Nome utilizado na campanha eleitoral.
    partido: str
        Último partido.
    rede_social: list
        Lista de nomes em redes sociais.
    sexo: str
        - 'M': Masculino;
        - 'F': Feminino.
    situacao: str
        Situação do último status.
    uf: str
        Sigla da Unidade Federativa pela qual foi eleito.
    uf_nascimento: str
        Unidade Federativa de nascimento.
    ultima_atualizacao: str
        Dia e horário da última atualização de status.
    uri: str
        Endereço para coleta de dados direta pela API.
    website: str
        Website.

    Exemplos
    --------
    Coletar partido mais recente do deputado Rodrigo Maia.
    >>> cod = 74693   # Código do deputado
    >>> dep = camara.Deputado(cod=cod)
    >>> dep.partido
    ... 'DEM'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['deputados', str(cod)])['dados']
        self.condicao_eleitoral = self.dados['ultimoStatus']['condicaoEleitoral']
        self.cpf = self.dados['cpf']
        self.descricao_status = self.dados['ultimoStatus']['descricaoStatus']
        self.email = self.dados['ultimoStatus']['email']
        self.escolaridade = self.dados['escolaridade']
        self.falecimento = self.dados['dataFalecimento']
        self.foto = self.dados['ultimoStatus']['urlFoto']
        self.gabinete = self.dados['ultimoStatus']['gabinete']
        self.legislatura = self.dados['ultimoStatus']['idLegislatura']
        self.municipio_nascimento = self.dados['municipioNascimento']
        self.nascimento = self.dados['dataNascimento']       
        self.nome = self.dados['ultimoStatus']
        self.nome_completo = self.dados['nomeCivil']
        self.nome_eleitoral = self.dados['ultimoStatus']['nomeEleitoral']
        self.partido = self.dados['ultimoStatus']['siglaPartido']
        self.rede_social = self.dados['redeSocial']
        self.sexo = self.dados['sexo']
        self.situacao = self.dados['ultimoStatus']['situacao']
        self.uf = self.dados['ultimoStatus']['siglaUf']
        self.uf_nascimento = self.dados['ufNascimento']
        self.ultima_atualizacao = self.dados['ultimoStatus']['data']
        self.uri = self.dados['uri']
        self.website = self.dados['urlWebsite']


    def despesas(
            self,
            legislatura = None,
            ano = None,
            mes = None,
            fornecedor = None,
            pagina = None,
            itens = None,
            ordem = None,
            ordenar_por = None
        ) -> _pd.DataFrame:
        '''
        As despesas com exercício parlamentar do deputado.

        Dá acesso aos registros de pagamentos e reembolsos feitos pela Câmara
        em prol do deputado, a título da Cota para Exercício da Atividade
        Parlamentar, a chamada "cota parlamentar".
        Se não forem passados os parâmetros de tempo, o serviço retorna os
        dados dos seis meses anteriores à requisição.

        Parâmetros
        ----------
        legislatura: int
            ID da legislatura em que tenham ocorrido as despesas.
        ano: int
            Ano de ocorrência das despesas.
        mes: int
            Número do mês de ocorrência das despesas.
        fornecedor: int
            CNPJ de uma pessoa jurídica, ou CPF de uma pessoa física,
            fornecedora do produto ou serviço (apenas números).
        pagina: int
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido
            pelo parâmetro itens. Se omitido, assume o valor 1.
        itens: int
            Número máximo de itens na página que se deseja obter com
            esta requisição.
        ordem: str
            O sentido da ordenação:
            - 'asc': De A a Z ou 0 a 9;
            - 'desc': De Z a A ou 9 a 0.
        ordenar_por: str
            Nome do campo pelo qual a lista deverá ser ordenada:
            qualquer um dos campos do retorno, e também idLegislatura.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de despesas com exercício parlamentar do deputado.

        ----------------------------------------------------------------------
        '''

        params = {}
        if legislatura is not None:
            params['idLegislatura'] = legislatura
        if ano is not None:
            params['ano'] = ano
        if mes is not None:
            params['mes'] = mes
        if fornecedor is not None:
            params['cnpjCpfFornecedor'] = fornecedor
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        if ordem is not None:
            params['ordem'] = ordem
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['deputados', str(self.cod), 'despesas']
        dados = _api.get(path=path, params=params)
        return _df(dados)


    def discursos(
            self,
            legislatura = None,
            inicio = None,
            fim = None,
            pagina = None,
            itens = None,
            ordem = None,
            ordenar_por = None
        ) -> _pd.DataFrame:
        '''
        Os discursos feitos por um deputado em eventos diversos.

        Retorna uma lista de informações sobre os pronunciamentos feitos
        pelo deputado que tenham sido registrados, em quaisquer eventos,
        nos sistemas da Câmara.
        Caso os parâmetros de tempo não sejam configurados na requisição,
        são buscados os discursos ocorridos nos sete dias anteriores ao
        da requisição.

        Parâmetros
        ----------
        legislatura: int
            Número da legislatura a qual os dados buscados devem corresponder.
        inicio: str
            Data de início de um intervalo de tempo, no formato AAAA-MM-DD.
        fim: str
            Data de término de um intervalo de tempo, no formato AAAA-MM-DD.
        ordenar_por: str
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        ordem: str
            O sentido da ordenação:
            - 'asc': De A a Z ou 0 a 9,
            - 'desc': De Z a A ou 9 a 0.
        itens: int
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        pagina: int
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de discursos feitos por um deputado em eventos diversos.

        ----------------------------------------------------------------------
        '''

        params = {}
        if legislatura is not None:
            params['idLegislatura'] = legislatura
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        if ordem is not None:
            params['ordem'] = ordem
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['deputados', str(self.cod), 'discursos']
        dados = _api.get(path=path, params=params)
        return _df(dados)


    def eventos(
            self,
            legislatura = None,
            inicio = None,
            fim = None,
            pagina = None,
            itens = None,
            ordem = None,
            ordenar_por = None,
            index = False
        ) -> _pd.DataFrame:
        '''
        Uma lista de eventos com a participação do parlamentar.

        Retorna uma lista de objetos evento nos quais a participação do
        parlamentar era ou é prevista.
        Se não forem passados parâmetros de tempo, são retornados os eventos
        num período de cinco dias, sendo dois antes e dois depois do dia da
        requisição.

        Parâmetros
        ----------
        legislatura: int
            Número da legislatura a qual os dados buscados devem corresponder.
        inicio: str
            Data de início de um intervalo de tempo, no formato AAAA-MM-DD.
        fim: str
            Data de término de um intervalo de tempo, no formato AAAA-MM-DD.
        ordenar_por: str
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        ordem: str
            O sentido da ordenação:
            - 'asc': De A a Z ou 0 a 9,
            - 'desc': De Z a A ou 9 a 0.
        itens: int
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        pagina: int
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de discursos feitos por um deputado em eventos diversos.

        ----------------------------------------------------------------------
        '''

        params = {}
        if legislatura is not None:
            params['idLegislatura'] = legislatura
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        if ordem is not None:
            params['ordem'] = ordem
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['deputados', str(self.cod), 'eventos']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def frentes(self, index=False):
        '''
        As frentes parlamentares das quais um deputado é integrante.

        Retorna uma lista de informações básicas sobre as frentes
        parlamentares das quais o parlamentar seja membro, ou, no caso de
        frentes existentes em legislaturas anteriores, tenha encerrado a
        legislatura como integrante.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de frentes parlamentares das quais um deputado é integrante.

        ----------------------------------------------------------------------
        '''

        path = ['deputados', str(self.cod), 'frentes']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def orgaos(
            self,
            legislatura = None,
            inicio = None,
            fim = None,
            pagina = None,
            itens = None,
            ordem = None,
            ordenar_por = None,
            index = False
        ) -> _pd.DataFrame:
        '''
        Os órgãos dos quais um deputado é integrante.

        Retorna uma lista de órgãos, como as comissões e procuradorias,
        dos quais o deputado participa ou participou durante um intervalo
        de tempo.
        Cada item identifica um órgão, o cargo ocupado pelo parlamentar neste
        órgão (como presidente, vice-presidente, titular ou suplente) e as
        datas de início e fim da ocupação deste cargo.
        Se não for passado algum parâmetro de tempo, são retornados os órgãos
        ocupados pelo parlamentar no momento da requisição. Neste caso a
        lista será vazia se o deputado não estiver em exercício.

        Parâmetros
        ----------
        inicio: str
            Data de início de um intervalo de tempo, no formato AAAA-MM-DD.
        fim: str
            Data de término de um intervalo de tempo, no formato AAAA-MM-DD.
        ordenar_por: str
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        ordem: str
            O sentido da ordenação:
            - 'asc': De A a Z ou 0 a 9,
            - 'desc': De Z a A ou 9 a 0.
        itens: int
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        pagina: int
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        index: bool (default=False)
            Se True, define a coluna `idOrgao` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos órgãos dos quais um deputado é integrante.

        ----------------------------------------------------------------------
        '''

        params = {}
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        if ordem is not None:
            params['ordem'] = ordem
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['deputados', str(self.cod), 'orgaos']
        dados = _api.get(path=path, params=params)
        index_col = 'idOrgao' if index else None
        return _df(dados, index_col)



class Evento:
    '''
    Retorna um conjunto detalhado de informações sobre o evento da Câmara.

    Parâmetros
    ----------
    cod: int
        Código numérico do evento do qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico do evento.
    andar: str
        Andar do prédio onde ocorreu o evento.
    descricao: str
        Descrição do evento.
    descricao_tipo: str
        Tipo do evento.
    fases: str
        Fases do evento.
    fim: str
        Data e horário que o evento foi finalizado no formato 'AAAA-MM-DD'.
    inicio: str
        Data e horário que o evento foi iniciado no formato 'AAAA-MM-DD'.
    local: str
        Local onde ocorreu o evento.
    local_externo: str
        Local externo do evento.
    lista_orgaos: list of dict
        Lista de orgãos e informações sobre os mesmos.
    predio: str
        Prédio que ocorreu o evento.
    requerimentos: list of dict
        Requerimentos do evento.
    sala: str
        Sala do prédio onde ocorreu o evento.
    situacao: str
        Situação do evento.
    uri: str
        Endereço para coleta de dados direta pela API do evento.
    uri_convidados: str
        Endereço para coleta de dados direta pela API dos convidados.
    uri_deputados: str
        Endereço para coleta de dados direta pela API dos deputados.
    url_documento_pauta: str
        Endereço URL para visualizar a pauta do evento.
    url_registro: str
        Endereço URL onde o evento foi registrado.

    Exemplos
    --------
    Obter a URL para assistir ao evento #59265.
    >>> ev = camara.Evento(cod=59265)
    >>> ev.url_registro
    ... 'https://www.youtube.com/watch?v=8D2gjMrTnMA'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['eventos', str(cod)])['dados']
        self.andar = self.dados['localCamra']['andar']
        self.descricao = self.dados['descricao']
        self.descricao_tipo = self.dados['descricaoTipo']
        self.fases = self.dados['fases']
        self.fim = self.dados['dataHoraFim']
        self.inicio = self.dados['dataHoraInicio']
        self.local = self.dados['localCamara']['nome']
        self.local_externo = self.dados['localExterno']
        self.lista_orgaos = self.dados['orgaos']
        self.predio = self.dados['localCamara']['predio']
        self.requerimentos = self.dados['requerimentos']
        self.sala = self.dados['localCamara']['sala']
        self.situacao = self.dados['situacao']
        self.uri = self.dados['uri']
        self.uri_convidados = self.dados['uriConvidados']
        self.uri_deputados = self.dados['uriDeputados']
        self.url_documento_pauta = self.dados['urlDocumentoPauta']
        self.url_registro = self.dados['urlRegistro']


    def deputados(self, index=False) -> _pd.DataFrame:
        '''
        Os deputados participantes de um evento específico.

        Retorna uma lista de dados resumidos sobre deputados participantes do
        evento. Se o evento já ocorreu, a lista identifica os deputados que
        efetivamente registraram presença no evento. Se o evento ainda não
        ocorreu, a lista mostra os deputados que devem participar do evento,
        por serem convidados ou por serem membros do(s) órgão(s) responsável
        pelo evento.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos deputados participantes de um evento específico.

        ----------------------------------------------------------------------
        '''

        path = ['eventos', str(self.cod), 'deputados']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def orgaos(self, index=False) -> _pd.DataFrame:
        '''
        Lista de órgãos organizadores do evento.

        Retorna uma lista em que cada item é um conjunto mínimo de dados sobre
        o(s) órgão(s) responsável(is) pelo evento.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de órgãos organizadores do evento.

        ----------------------------------------------------------------------
        '''

        path = ['eventos', str(self.cod), 'orgaos']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def pauta(self, index=False) -> _pd.DataFrame:
        '''
        Lista de proposições que foram ou deverão ser avaliadas em um evento
        de caráter deliberativo.

        Se o evento for de caráter deliberativo (uma reunião ordinária,
        por exemplo) este serviço retorna a lista de proposições previstas
        para avaliação pelos parlamentares. Cada item identifica, se as
        informações estiverem disponíveis, a proposição avaliada, o regime
        de preferência para avaliação, o relator e seu parecer, o resultado
        da apreciação e a votação realizada.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `ordem` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de proposições do evento.

        ----------------------------------------------------------------------
        '''

        path = ['eventos', str(self.cod), 'pauta']
        dados = _api.get(path=path, params=None)
        index_col = 'ordem' if index else None
        return _df(dados, index_col)


    def votacoes(self, index=False) -> _pd.DataFrame:
        '''
        Informações detalhadas de votações sobre o evento.

        Retorna uma lista de dados básicos sobre votações que tenham sido
        realizadas no evento. Votações só ocorrem em eventos de caráter
        deliberativo. Dados complementares sobre cada votação listada podem
        ser obtidos no recurso.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de de votações sobre o evento.

        ----------------------------------------------------------------------
        '''

        path = ['eventos', str(self.cod), 'votacoes']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Frente:
    '''
    Informações detalhadas sobre uma frente parlamentar.

    Parâmetros
    ----------
    cod: int
        Código numérico da frente parlamentar da qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico da frente parlamentar.
    coordenador: dict
        Informações do(a) coordenador(a) da frente parlamentar.
    documento: str
        URL do documento da frente parlamentar.
    email: str
        E-mail de contato.
    id_sitacao: int
        ID da situação da frente parlamentar.
    keywords: str
        Palavras-chaves da frente parlamentar.
    legislatura: int
        ID da legislatura da frente parlamentar.
    situacao: str
        Situação da frente parlamentar.
    telefone: str
        Telefone de contato.
    titulo: str
        Título da frente parlamentar.
    uri: str
        Endereço para coleta de dados direta pela API da frente parlamentar.
    website: str
        URL do website da frente parlamentar.

    Exemplos
    --------
    Obter título da frente parlamentar #54258.
    >>> fr = camara.Frente(cod=54258)
    >>> fr.url_registro
    ... 'Frente Parlamentar Mista da Telessaúde'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['frentes', str(cod)])['dados']
        self.coordenador = self.dados['coordenador']
        self.documento = self.dados['urlDocumento']
        self.email = self.dados['email']
        self.id_sitacao = self.dados['idSituacao']
        self.keywords = self.dados['keywords']
        self.legislatura = self.dados['idLegislatura']
        self.situacao = self.dados['situacao']
        self.telefone = self.dados['telefone']
        self.titulo = self.dados['titulo']
        self.uri = self.dados['uri']
        self.website = self.dados['urlWebsite']
        

    def membros(self, index=False) -> _pd.DataFrame:
        '''
        Os deputados que participam da frente parlamentar.

        Uma lista dos deputados participantes da frente parlamentar e os
        papéis que exerceram nessa frente (signatário, coordenador ou
        presidente). Observe que, mesmo no caso de frentes parlamentares
        mistas (compostas por deputados e senadores), são retornados apenas
        dados sobre os deputados.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos deputados que participam da frente parlamentar.

        ----------------------------------------------------------------------
        '''

        path = ['frentes', str(self.cod), 'membros']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Legislatura:
    '''
    Informações extras sobre uma determinada legislatura da Câmara.

    Parâmetros
    ----------
    cod: int
        Código numérico da legislatura da qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico da legislatura.
    inicio: str
        Primeiro dia da legislatura.
    fim: str
        Último dia da legislatura.
    uri: str
        Endereço para coleta de dados direta pela API da legislatura.

    Exemplos
    --------
    Obter o primeiro e último dia da legislatura #56.
    >>> leg = camara.Legislatura(cod=54)
    >>> leg.inicio
    ... '2011-02-01'
    >>> leg.fim
    ... '2015-01-31'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['legislaturas', str(cod)])['dados']
        self.fim = self.dados['dataFim']
        self.inicio = self.dados['dataInicio']
        self.uri = self.dados['uri']


    def mesa(self, inicio=None, fim=None, index=False) -> _pd.DataFrame:
        '''
        Quais deputados fizeram parte da Mesa Diretora em uma legislatura.

        Retorna uma lista com dados básicos sobre todos os deputados que
        ocuparam algum posto na Mesa Diretora da Câmara em algum período de
        tempo dentro da legislatura. Normalmente, cada legislatura tem duas
        Mesas Diretoras, com presidente, dois vice-presidentes, quatro
        secretários parlamentares e os suplentes dos secretários.

        Parâmetros
        ----------
        inicio: str (default=None)
            Dia de início do intervalo de tempo do qual se deseja saber a
            composição da Mesa, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término do intervalo de tempo do qual se deseja saber a
            composição da Mesa, no formato 'AAAA-MM-DD'.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos deputados que participam da frente parlamentar.

        ----------------------------------------------------------------------
        '''

        params = {}
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim

        path = ['legislaturas', str(self.cod), 'mesa']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Partido:
    '''
    Informações detalhadas sobre um partido.

    Parâmetros
    ----------
    cod: int
        Código numérico do partido do qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico do partido.
    facebook: str
        URL da página no Facebook do partido.
    legislatura: str
        Código numérico da última legislatura.
    lider: dict
        Informações sobre o líder do partido.
    logo: str
        URL da logo do partido.
    nome: str
        Nome completo do partido.
    numero: int
        Número eleitoral do partido.
    sigla: str
        Sigla do partido.
    situacao: str
        Situação do partido.
    total_membros: str
        Total de membros do partido.
    total_posse: str
        Total de posse do partido.
    ultima_atualizacao: str
        Última atualização das informações sobre o partido.
    uri: str
        Endereço para coleta de dados direta pela API do partido.
    uri_membros: str
        Endereço para coleta de dados direta pela API dos membros do partido.
    website: str
        URL do website do partido.


    Exemplos
    --------
    Obter o nome completo do partido #36899.
    >>> p = camara.Partido(cod=36899)
    >>> p.nome
    ... 'Movimento Democrático Brasileiro'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['partidos', str(cod)])['dados']
        self.facebook = self.dados['urlFacebook']
        self.legislatura = self.dados['status']['idLegislatura']
        self.lider = self.dados['status']['lider']
        self.logo = self.dados['urlLogo']
        self.nome = self.dados['nome']
        self.numero = self.dados['numeroEleitoral']
        self.sigla = self.dados['sigla']
        self.situacao = self.dados['status']['situacao']
        self.total_membros = self.dados['status']['totalMembros']
        self.total_posse = self.dados['status']['totalPosse']
        self.ultima_atualizacao = self.dados['status']['data']
        self.uri = self.dados['uri']
        self.uri_membros = self.dados['status']['uriMembros']
        self.website = self.dados['urlWebSite']


    def membros(
            self,
            inicio = None,
            fim = None,
            legislatura = None,
            pagina = None,
            itens = None,
            ordenar_por = None,
            ordem = None,
            index = False
        ) -> _pd.DataFrame:
        '''
        Uma lista dos parlamentares de um partido durante um período.

        Retorna uma lista de deputados que estão ou estiveram em exercício
        pelo partido. Opcionalmente, pode-se usar os parâmetros `inicio`,
        `fim` ou `legislatura` para se obter uma lista de deputados filiados
        ao partido num certo intervalo de tempo. Isso é equivalente à função
        `lista_deputados` com filtro por partido, mas é melhor para obter
        informações sobre membros de partidos já extintos.

        Parâmetros
        ----------
        inicio: str (default=None)
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        legislatura: int (default=None)
            Número da legislatura, à qual os dados buscados devem corresponder.
        ordenar_por: str (default=None)
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        ordem: str (default=None)
            O sentido da ordenação:
            - 'asc': De A a Z ou 0 a 9;
            - 'desc': De Z a A ou 9 a 0.
        itens: int (default=None)
            Número máximo de itens na “página” que se deseja obter com esta
            requisição.
        pagina: int (default=None)
            Número da “página” de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos parlamentares de um partido durante um período.

        ----------------------------------------------------------------------
        '''

        params = {}
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if legislatura is not None:
            params['idLegislatura'] = legislatura
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        if ordem is not None:
            params['ordem'] = ordem
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['partidos', str(self.cod), 'membros']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Bloco:
    '''
    Informações sobre um bloco partidário específico.

    Parâmetros
    ----------
    cod: int
        Código numérico do bloco partidário do qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico do bloco partidário.
    legislatura: str
        Legislatura do bloco partidário.
    nome: str
        Nome do bloco partidário.
    uri: str
        Endereço para coleta de dados direta pela API do bloco partidário.

    Exemplos
    --------
    Obter o nome do bloco #576.
    >>> bl = camara.Bloco(cod=576)
    >>> bl.nome
    ... 'PSL, PTB'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['blocos', str(cod)])['dados']
        self.legislatura = self.dados['idLegislatura']
        self.nome = self.dados['nome']
        self.uri = self.dados['uri']



class Proposicao:
    '''
    Informações detalhadas sobre uma proposição específica.

    Parâmetros
    ----------
    cod: int
        Código numérico da proposição da qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico da proposição.
    uri: str
        Endereço para coleta de dados direta pela API da proposição.
    tipo_sigla: str
        Sigla do tipo de proposição.
    tipo_codigo: int
        Código numérico do tipo de proposição.
    numero: int
        Número da proposição.
    ano: int
        Ano da proposição.
    ementa: str
        Ementa da proposição.
    apresentacao: str
        Horário da apresentação da proposição no formato 'AAAA-MM-DD HH:MM'.
    uri_orgao_numerador: str
        Endereço para coleta de dados direta pela API do órgão numerador.
    ultima_atualizacao: str
        Data da última atualização do status da proposição.
    sequencia: int
        Sequência da proposição.
    sigla_orgao: str
        Sigla do órgão.
    uri_orgao: str
        Endereço para coleta de dados direta pela API do órgão.
    uri_ultimo_relator: str
        Endereço para coleta de dados direta pela API do último relaltor.
    regime: str
        Regime da proposição.
    descricao_tramitacao: str
        Descrição da tramitação.
    cod_tipo_tramitacao: str
        Código do tipo da tramitação.
    descricao_situacao: str
        Descrição da situação da proposição.
    cod_situacao: int
        Código númerico da situação da proposição.
    despacho: str
        Despacho.
    url: str
        URL da proposição.
    ambito: str
        Âmbito da proposição.
    uri_autores: str
        Endereço para coleta de dados direta pela API dos autores.
    descricao_tipo: str
        Descrição do tipo da proposição.
    ementa_detalhada: str
        Ementa detalhada da proposição.
    keywords: str
        Palavras-chaves da proposição.
    uri_proposicao_principal: str
        Endereço para coleta de dados direta pela API da proposição principal.
    uri_proposicao_anterior: str
        Endereço para coleta de dados direta pela API da proposição anterior.
    uri_proposicao_posterior: str
        Endereço para coleta de dados direta pela API da proposição posterior.
    url_inteiro_teor: str
        URL do inteiro teor.
    urn_final: str
        URN final.
    texto: str
        Texto da proposição.
    justificativa: str
        Justificativa da proposição.

    Exemplos
    --------
    Obter a ementa da proposição #15990.
    >>> prop = camara.Proposicao(cod=15990)
    >>> prop.ementa
    ... ''Cria salvaguardas para a tecnologia no campo nuclear...'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['proposicoes', str(cod)])['dados']
        self.uri = self.dados['uri']
        self.tipo_sigla = self.dados['siglaTipo']
        self.tipo_codigo = self.dados['codTipo']
        self.numero = self.dados['numero']
        self.ano = self.dados['ano']
        self.ementa = self.dados['ementa']
        self.apresentacao = self.dados['dataApresentacao']
        self.uri_orgao_numerador = self.dados['uriOrgaoNumerador']
        self.ultima_atualizacao = self.dados['statusProposicao']['dataHora']
        self.sequencia = self.dados['statusProposicao']['sequencia']
        self.sigla_orgao = self.dados['statusProposicao']['siglaOrgao']
        self.uri_orgao = self.dados['statusProposicao']['uriOrgao']
        self.uri_ultimo_relator = self.dados['statusProposicao']['uriUltimoRelator']
        self.regime = self.dados['statusProposicao']['regime']
        self.descricao_tramitacao = self.dados['statusProposicao']['descricaoTramitacao']
        self.cod_tipo_tramitacao = self.dados['statusProposicao']['codTipoTramitacao']
        self.descricao_situacao = self.dados['statusProposicao']['descricaoSituacao']
        self.cod_situacao = self.dados['statusProposicao']['codSituacao']
        self.despacho = self.dados['statusProposicao']['despacho']
        self.url = self.dados['statusProposicao']['url']
        self.ambito = self.dados['statusProposicao']['ambito']
        self.uri_autores = self.dados['uriAutores']
        self.descricao_tipo = self.dados['descricaoTipo']
        self.ementa_detalhada = self.dados['ementaDetalhada']
        self.keywords = self.dados['keywords']
        self.uri_proposicao_principal = self.dados['uriPropPrincipal']
        self.uri_proposicao_anterior = self.dados['uriPropAnterior']
        self.uri_proposicao_posterior = self.dados['uriPropPosterior']
        self.url_inteiro_teor = self.dados['urlInteiroTeor']
        self.urn_final = self.dados['urnFinal']
        self.texto = self.dados['texto']
        self.justificativa = self.dados['justificativa']


    def autores(self) -> _pd.DataFrame:
        '''
        Lista pessoas e/ou entidades autoras da proposição.

        Retorna uma lista em que cada item identifica uma pessoa ou entidade
        que é autora da proposição. Além de deputados, também podem ser
        autores de proposições os senadores, a sociedade civil, assembleias
        legislativas e os poderes Executivo e Judiciário.
        Pelo Regimento da Câmara, todos os que assinam uma proposição são
        considerados autores (art. 102), tanto os proponentes quanto os
        apoiadores.
        Para obter mais informações sobre cada autor, é recomendável acessar,
        se disponível, a URL que é valor do campo uri.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista pessoas e/ou entidades autoras da proposição.

        ----------------------------------------------------------------------
        '''

        path = ['proposicoes', str(self.cod), 'autores']
        dados = _api.get(path=path, params=None)
        return _df(dados, None)


    def relacionadas(self, index=False) -> _pd.DataFrame:
        '''
        Uma lista de proposições relacionadas a uma em especial.

        Lista de informações básicas sobre proposições que de alguma forma se
        relacionam com a proposição, como pareceres, requerimentos,
        substitutivos, etc.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de proposições relacionadas a uma em especial.

        ----------------------------------------------------------------------
        '''

        path = ['proposicoes', str(self.cod), 'relacionadas']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def temas(self, index=False) -> _pd.DataFrame:
        '''
        Lista de áreas temáticas de uma proposição.

        Lista em que cada item traz informações sobre uma área temática à qual
        a proposição se relaciona, segundo classificação oficial do Centro de
        Documentação e Informação da Câmara.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `codTema` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de áreas temáticas de uma proposição.

        ----------------------------------------------------------------------
        '''

        path = ['proposicoes', str(self.cod), 'temas']
        dados = _api.get(path=path, params=None)
        index_col = 'codTema' if index else None
        return _df(dados, index_col)


    def tramitacoes(self, inicio=None, fim=None, index=False) -> _pd.DataFrame:
        '''
        O histórico de passos na tramitação de uma proposta.

        Lista que traz, como cada item, um “retrato” de informações que podem
        ser alteradas a cada etapa de tramitação na vida da proposição (como
        regime de tramitação e situação) e informações sobre o que causou esse
        novo estado. Esta representação das tramitações ainda é provisória.

        Parâmetros
        ----------
        inicio: str (default=None)
            Data de início da tramitação, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término da tramitação, no formato 'AAAA-MM-DD'.
        index: bool (default=False)
            Se True, define a coluna `sequencia` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de passos na tramitação de uma proposta.

        ----------------------------------------------------------------------
        '''

        params = {}
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim

        path = ['proposicoes', str(self.cod), 'tramitacoes']
        dados = _api.get(path=path, params=params)
        index_col = 'sequencia' if index else None
        return _df(dados, index_col)


    def votacoes(
            self,
            ordem = None,
            ordenar_por = None,
            index = False
        ) -> _pd.DataFrame:
        '''
        Informações detalhadas de votações sobre a proposição.

        Retorna uma lista de identificadores básicos sobre as votações na
        Câmara que tiveram a proposição como objeto ou como afetada pelos seus
        resultados. Dados complementares sobre cada votação listada podem ser
        obtidos pelo objeto `camara.Votacao`.

        Parâmetros
        ----------
        ordem: str (default=None)
            O sentido da ordenação:
            - 'asc': De A a Z ou 0 a 9;
            - 'desc': De Z a A ou 9 a 0.
        ordenar_por: str (default=None)
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de votações sobre a proposição.

        ----------------------------------------------------------------------
        '''

        params = {}
        if ordem is not None:
            params['ordem'] = ordem
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['proposicoes', str(self.cod), 'votacoes']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)