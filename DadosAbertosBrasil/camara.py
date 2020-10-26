'''
Módulo para captura dos dados abertos da Câmara dos Deputados do Brasil

Use o seguinte template para buscar dados:
>>> from DadosAbertosBrasil import camara
>>> camara.{funcao}(cod={opcional}, serie={opcional}, index={True/False})

Documentação da API original: https://dadosabertos.camara.leg.br/swagger/api.html
'''



import warnings

import pandas as pd
import requests



_url = 'https://dadosabertos.camara.leg.br/api/v2/'



def _query(funcao, cod, serie, index, series):
    
    if cod == None:
        data = requests.get(_url + funcao).json()
        df = pd.DataFrame(data['dados'])
        df.drop(columns=df.columns[df.columns.str.startswith('uri')], inplace=True)
        
        if index:
            df.set_index('id', inplace=True)
        
        return df
    
    elif isinstance(cod, int) or funcao == 'votacoes':
        
        if serie in series:
            query = _url + f'/{funcao}/{cod}' if serie == 'informacoes' else _url + f'/{funcao}/{cod}/{serie}'        
            data = requests.get(query).json()
            return data['dados']
        
        else:
            raise TypeError(f"O valor para o argumento 'serie' deve ser um dos seguintes valores tipo string: {series}")
            
    else:
        raise TypeError("O argumento 'cod' deve ser um número inteiro.")



def blocos(cod=None, index=False):
    '''
    Dados sobre os blocos partidários.
    '''

    series = ['informacoes']
    return _query('blocos', cod, 'informacoes', index, series)



def deputados(cod=None, serie='informacoes', index=False):
    '''
    Dados sobre os deputados.
    '''

    series = ['informacoes', 'despesas', 'discursos', 'eventos', 'frentes', 'orgaos']
    return _query('deputados', cod, serie, index, series)



def eventos(cod=None, serie='informacoes', index=False):
    '''
    Dados sobre os eventos ocorridos ou previstos nos diversos órgãos da Câmara.
    '''

    series = ['informacoes', 'deputados', 'orgaos', 'pauta', 'votacoes']
    return _query('eventos', cod, serie, index, series)



def frentes(cod=None, serie='informacoes', index=False):
    '''
    Dados de frentes parlamentares de uma ou mais legislatura.
    '''

    series = ['informacoes', 'membros']
    return _query('frentes', cod, serie, index, series)



def legislaturas(cod=None, serie='informacoes', index=False):
    '''
    Dados dos períodos de mantados e atividades parlamentares na Câmara.
    '''

    series = ['informacoes', 'mesa']
    return _query('legislaturas', cod, serie, index, series)



def orgaos(cod=None, serie='informacoes', index=False):
    '''
    Dados de comissões e outros órgãos legislativos da Câmara.
    '''

    series = ['informacoes', 'eventos', 'membros', 'votacoes']
    return _query('orgaos', cod, serie, index, series)



def partidos(cod=None, serie='informacoes', index=False):
    '''
    Dados dos partidos políticos que tem ou já tiveram parlamentares em exercício na Câmara.
    '''

    series = ['informacoes', 'membros']
    return _query('partidos', cod, serie, index, series)



def proposicoes(cod=None, serie='informacoes', index=False):
    '''
    Dados de proposições na Câmara.
    '''

    series = ['informacoes', 'autores', 'relacionadas', 'temas', 'tramitacoes', 'votacoes']
    return _query('proposicoes', cod, serie, index, series)



def votacoes(cod=None, serie='informacoes', index=False):
    '''
    Dados de votações na Câmara.
    '''

    series = ['informacoes', 'orientacoes', 'votos']
    return _query('votacoes', cod, serie, index, series)



def referencias(funcao, index=False) -> pd.DataFrame:
    '''
    Listas de valores válidos para as funções deste pacote.
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
        data = requests.get(_url + 'referencias/' + referencia[funcao]).json()
        
    else:
        raise TypeError(f"Referência inválida. Insira um dos seguintes valores no campo 'funcao': {list(referencia.keys())}")
    
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
        
        # Id(s) do(s) deputado(s)
        if (id == None) or isinstance(id, int) or isinstance(id, list):
            self.id = id
        else:
            warnings.warn("O campo 'id' deve ser do tipo int ou uma lista de int. Qualquer outro tipo de variável será substituido por None.")
            self.id = None
        
        # Nome dos deputados
        if (nome == None) or isinstance(nome, str):
            self.nome = nome
        else:
            warnings.warn("O campo 'nome' deve ser do tipo string. Qualquer outro tipo de variável será substituido por None.")
            self.nome = None

        # Legislatura(s) dos deputados
        if (legislatura == None) or isinstance(legislatura, int) or isinstance(legislatura, list):
            self.legislatura = legislatura
        else:
            warnings.warn("O campo 'legislatura' deve ser do tipo int ou uma lista de int. Qualquer outro tipo de variável será substituido por None.")
            self.legislatura = None
        
        # UF(s) dos deputados
        if (uf == None) or isinstance(uf, str) or isinstance(uf, list):
            self.uf = uf
        else:
            warnings.warn("O campo 'uf' deve ser um string de duas letras que representa a UF ou uma lista de string. Qualquer outro tipo de variável será substituido por None.")
            self.uf = None       

        # Partido(s) dos deputados
        if (partido == None) or isinstance(partido, str) or isinstance(partido, list):
            self.partido = partido
        else:
            warnings.warn("O campo 'partido' deve ser um string que representa a sigla de um partido ou uma lista de string. Qualquer outro tipo de variável será substituido por None.")
            self.partido = None
            
        # Sexo dos deputados
        if (sexo == None) or isinstance(sexo, str):
            self.sexo = sexo
        else:
            warnings.warn("O campo 'sexo' deve ser uma string igual a 'M' ou 'F'. Qualquer outro tipo de variável será substituido por None.")
            self.sexo = None

        # Página dos resultados
        if (pagina == None) or isinstance(pagina, int):
            self.pagina = pagina
        else:
            warnings.warn("O campo 'pagina' deve ser uma variável do tipo int. Qualquer outro tipo de variável será substituido por None.")
            self.pagina = None
            
        # Quantidade de itens por página
        if (itens == None) or isinstance(itens, int):
            self.itens = itens
        else:
            warnings.warn("O campo 'itens' deve ser uma variável do tipo int. Qualquer outro tipo de variável será substituido por None.")
            self.itens = None

        # Data de início da consulta
        if (inicio == None) or isinstance(inicio, str):
            self.inicio = inicio
        else:
            warnings.warn("O campo 'inicio' deve ser uma string no formato 'AAAA-MM-DD'. Qualquer outro tipo de variável será substituido por None.")
            self.inicio = None
            
        # Data fim da consulta
        if (fim == None) or isinstance(fim, str):
            self.fim = fim
        else:
            warnings.warn("O campo 'fim' deve ser uma string no formato 'AAAA-MM-DD'. Qualquer outro tipo de variável será substituido por None.")
            self.fim = None
            
        # Ordem ascendente (True) ou descendente (False)
        if isinstance(asc, bool):
            self.asc = asc
        else:
            raise TypeError("O campo 'asc' deve ser igual a True ou False.")         
        
        # Ordenar por qual variável
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

        data = requests.get(self.query()).json()
        df = pd.DataFrame(data['dados'])
        df.drop(columns=df.columns[df.columns.str.startswith('uri')], inplace=True)
        
        if index:
            df.set_index('id', inplace=True)
        
        return df