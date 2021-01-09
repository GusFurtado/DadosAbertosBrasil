'''
Módulo para captura dos dados abertos da Câmara dos Deputados do Brasil

Use o seguinte template para buscar dados:
>>> from DadosAbertosBrasil import camara
>>> camara.{funcao}(cod={opcional}, serie={opcional}, index={True/False})

Documentação da API original: https://dadosabertos.camara.leg.br/swagger/api.html
'''



import warnings

import pandas as pd

from . import API



api = API('camara')



def _query(
        funcao: str,
        series: list,
        cod = None,
        serie = 'informacoes',
        index = False,
    ) -> pd.DataFrame:
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
            
    data = api.get(keys)['dados']

    if cod is None:
        df = pd.DataFrame(data)
        df = df[~df.columns.str.startswith('uri')]
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



def deputados(cod=None, serie='informacoes', index=False):
    '''
    Dados sobre os deputados.
    '''

    series = ['informacoes', 'despesas', 'discursos', 'eventos', 'frentes', 'orgaos']
    return _query('deputados', series, cod, serie, index)



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



def referencias(funcao, index=False) -> pd.DataFrame:
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
        data = api.get(f'referencias/{referencia[funcao]}')
    else:
        raise TypeError(f"Referência inválida. Insira um dos seguintes valores para `funcao`: {list(referencia.keys())}")
    
    df = pd.DataFrame(data['dados'])
    if index:
        df.set_index('cod', inplace=True)
    
    return df



class Deputados():
    '''
    Consulta dados dos deputados federais.
    Utilize os argumentos para pesquisar por id, nome, legislatura, uf, partido e sexo.
    Ordene os resultados pelos parâmetros 'ordenar_por' e 'asc'.
    '''
    
    def __init__(
            self,
            id = None,
            nome = None,
            legislatura = None,
            uf = None,
            partido = None,
            sexo = None,
            pagina = None,
            itens = None,
            inicio = None,
            fim = None,
            asc = True,
            ordenar_por = 'nome'
        ):
        
        if (id == None) or isinstance(id, int) or isinstance(id, list):
            self.id = id
        else:
            warnings.warn("O campo 'id' deve ser do tipo int ou uma lista de int. Qualquer outro tipo de variável será substituido por None.")
            self.id = None
        
        if (nome == None) or isinstance(nome, str):
            self.nome = nome
        else:
            warnings.warn("O campo 'nome' deve ser do tipo string. Qualquer outro tipo de variável será substituido por None.")
            self.nome = None

        if (legislatura == None) or isinstance(legislatura, int) or isinstance(legislatura, list):
            self.legislatura = legislatura
        else:
            warnings.warn("O campo 'legislatura' deve ser do tipo int ou uma lista de int. Qualquer outro tipo de variável será substituido por None.")
            self.legislatura = None
        
        if (uf == None) or isinstance(uf, str) or isinstance(uf, list):
            self.uf = uf
        else:
            warnings.warn("O campo 'uf' deve ser um string de duas letras que representa a UF ou uma lista de string. Qualquer outro tipo de variável será substituido por None.")
            self.uf = None       

        if (partido == None) or isinstance(partido, str) or isinstance(partido, list):
            self.partido = partido
        else:
            warnings.warn("O campo 'partido' deve ser um string que representa a sigla de um partido ou uma lista de string. Qualquer outro tipo de variável será substituido por None.")
            self.partido = None
            
        if (sexo == None) or isinstance(sexo, str):
            self.sexo = sexo
        else:
            warnings.warn("O campo 'sexo' deve ser uma string igual a 'M' ou 'F'. Qualquer outro tipo de variável será substituido por None.")
            self.sexo = None

        if (pagina == None) or isinstance(pagina, int):
            self.pagina = pagina
        else:
            warnings.warn("O campo 'pagina' deve ser uma variável do tipo int. Qualquer outro tipo de variável será substituido por None.")
            self.pagina = None
            
        if (itens == None) or isinstance(itens, int):
            self.itens = itens
        else:
            warnings.warn("O campo 'itens' deve ser uma variável do tipo int. Qualquer outro tipo de variável será substituido por None.")
            self.itens = None

        if (inicio == None) or isinstance(inicio, str):
            self.inicio = inicio
        else:
            warnings.warn("O campo 'inicio' deve ser uma string no formato 'AAAA-MM-DD'. Qualquer outro tipo de variável será substituido por None.")
            self.inicio = None
            
        if (fim == None) or isinstance(fim, str):
            self.fim = fim
        else:
            warnings.warn("O campo 'fim' deve ser uma string no formato 'AAAA-MM-DD'. Qualquer outro tipo de variável será substituido por None.")
            self.fim = None
            
        if isinstance(asc, bool):
            self.asc = asc
        else:
            raise TypeError("O campo 'asc' deve ser igual a True ou False.")         
        
        if ordenar_por in ['id', 'idLegislatura', 'nome', 'siglaUF', 'siglaPartido']:
            self.ordenar_por = ordenar_por
        else:
            raise TypeError("O campo 'ordenar_por' deve ser igual a 'id', 'idLegislatura', 'nome', 'siglaUF' ou 'siglaPartido'.")
            
        
    def _converter_lista(self, key, values):

        if values == None:
            s = None
        else:
            if isinstance(values, list):
                s = ''
                for value in values:
                    s += f'{key}={value}&'
            else:
                s = f'{key}={values}&'
        return s
    

    def query(self) -> str:
        '''
        Apresenta a URL da query com os argumentos definidor.
        '''
        
        query = r'https://dadosabertos.camara.leg.br/api/v2/deputados?'
        
        if self.id is not None:
            query += self._converter_lista('id', self.id)
            
        if self.nome is not None:
            query += f'nome={self.nome}&'
            
        if self.legislatura is not None:
            query += self._converter_lista('idLegislatura', self.legislatura)
            
        if self.uf is not None:
            query += self._converter_lista('siglaUf', self.uf)
            
        if self.partido is not None:
            query += self._converter_lista('siglaPartido', self.partido)
            
        if self.sexo is not None:
            query += f'siglaSexo={self.sexo}&'
            
        if self.pagina is not None:
            query += f'pagina={self.pagina}&'
            
        if self.itens is not None:
            query += f'itens={self.itens}&'
            
        if self.inicio is not None:
            query += f'dataInicio={self.inicio}&'
            
        if self.fim is not None:
            query += f'dataFim={self.fim}&'
            
        query += 'ordem=ASC&' if self.asc else 'ordem=DESC&'
        query += f'ordenarPor={self.ordenar_por}'

        return query
    

    def rodar(self, index=False) -> pd.DataFrame:
        '''
        Roda query com os argumentos definidos.
        '''

        import requests
        data = requests.get(self.query()).json()
        df = pd.DataFrame(data['dados'])
        df.drop(columns=df.columns[df.columns.str.startswith('uri')], inplace=True)
        
        if index:
            df.set_index('id', inplace=True)
        
        return df