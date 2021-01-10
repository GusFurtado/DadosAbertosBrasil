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
    
    keys = [funcao]
    if cod is not None:
        keys.append(str(cod))
        if serie in series:
            if serie != 'informacoes':
                keys.append(serie)
        else:
            raise TypeError(f"O valor de `serie` deve ser um dos seguintes valores: {series}")
            
    data = _api.get(keys)['dados']

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
        self.cod = str(cod)
        self.dados = _api.get(['deputados', self.cod])['dados']
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

        keys = ['deputados', self.cod, 'despesas']
        dados = _api.get(keys=keys, params=params)
        return _pd.DataFrame(dados['dados'])


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

        keys = ['deputados', self.cod, 'discursos']
        dados = _api.get(keys=keys, params=params)
        return _pd.DataFrame(dados['dados'])


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

        keys = ['deputados', self.cod, 'eventos']
        dados = _api.get(keys=keys, params=params)
        df = _pd.DataFrame(dados['dados'])
        if index:
            df.set_index('id', inplace=True)
        return df


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

        keys = ['deputados', self.cod, 'frentes']
        dados = _api.get(keys=keys, params=None)
        df = _pd.DataFrame(dados['dados'])
        if index:
            df.set_index('id', inplace=True)
        return df


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

        keys = ['deputados', self.cod, 'orgaos']
        dados = _api.get(keys=keys, params=params)
        df = _pd.DataFrame(dados['dados'])
        if index:
            df.set_index('idOrgao', inplace=True)
        return df