# Pacote para captura dos dados abertos da Câmara dos Deputados do Brasil
# Autor: Gustavo Furtado da Silva
#
# Use o seguinte template para buscar dados:
#
# >>> from DadosAbertosBrasil import camara
# >>> camara.{funcao}(cod={opcional}, serie={opcional}, index={True/False})



import pandas as pd
import urllib, json

url = 'https://dadosabertos.camara.leg.br/api/v2/'

def __query(funcao, cod, serie, index, series):
    
    if cod == None:
        response = urllib.request.urlopen(url + funcao)
        data = json.loads(response.read())
        df = pd.DataFrame(data['dados'])
        df.drop(columns=df.columns[df.columns.str[:3] == 'uri'], inplace=True)
        
        if index:
            df.set_index('id', inplace=True)
        
        return df
    
    elif isinstance(cod, int):
        
        if serie in series:
            query = url + f'/{funcao}/{cod}' if serie == 'informacoes' else url + f'/{funcao}/{cod}/{serie}'
            response = urllib.request.urlopen(query)
            data = json.loads(response.read())
            return data['dados']
        else:
            raise TypeError(f"O valor para o argumento 'serie' deve ser um dos seguintes valores tipo string: {series}")
            
    else:
        raise TypeError("O argumento 'cod' deve ser um número inteiro.")

# Dados sobre os blocos partiidários
def blocos(cod=None, index=False):
    series = ['informacoes']
    return __query('blocos', cod, 'informacoes', index, series)

# Dados sobre os deputados
def deputados(cod=None, serie='informacoes', index=False):
    series = ['informacoes', 'despesas', 'discursos', 'eventos', 'frentes', 'orgaos']
    return __query('deputados', cod, serie, index, series)

# Dados sobre os eventos ocorridos ou previstos nos diversos órgãos da Câmara
def eventos(cod=None, serie='informacoes', index=False):
    series = ['informacoes', 'deputados', 'orgaos', 'pauta', 'votacoes']
    return __query('eventos', cod, serie, index, series)

# Dados de frentes parlamentares de uma ou mais legislatura
def frentes(cod=None, serie='informacoes', index=False):
    series = ['informacoes', 'membros']
    return __query('frentes', cod, serie, index, series)

# Dados dos períodos de mantados e atividades parlamentares na Câmara
def legislaturas(cod=None, serie='informacoes', index=False):
    series = ['informacoes', 'mesa']
    return __query('legislaturas', cod, serie, index, series)

# Dados de comissões e outros órgãos legislativos da Câmara
def orgaos(cod=None, serie='informacoes', index=False):
    series = ['informacoes', 'eventos', 'membros', 'votacoes']
    return __query('orgaos', cod, serie, index, series)

# Dados dos partidos políticos que tem ou já tiveram parlamentares em exercício na Câmara
def partidos(cod=None, serie='informacoes', index=False):
    series = ['informacoes', 'membros']
    return __query('partidos', cod, serie, index, series)

# Dados de proposições na Câmara
def proposicoes(cod=None, serie='informacoes', index=False):
    series = ['informacoes', 'autores', 'relacionadas', 'temas', 'tramitacoes', 'votacoes']
    return __query('proposicoes', cod, serie, index, series)

# Dados de votações na Câmara
def votacoes(cod=None, serie='informacoes', index=False):
    series = ['informacoes', 'orientacoes', 'votos']
    return __query('votacoes', cod, serie, index, series)

# Listas de valores válidos para as funções deste pacote
def referencias(funcao, index=False):
    
    referencia = {'codSituacaoDeputados': 'deputados/codSituacao',
                  'siglaUF': 'deputados/siglaUF',
                  'codSituacaoEvento': 'eventos/codSituacaoEvento',
                  'codTipoEvento': 'eventos/codTipoEvento',
                  'codSituacaoOrgao': 'orgaos/codSituacao',
                  'codTipoOrgao': 'orgaos/codTipoOrgao',
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
                  'uf': 'uf'}
    
    if funcao in referencia.keys():
        response = urllib.request.urlopen(url + 'referencias/' + referencia[funcao])
        data = json.loads(response.read())
    else:
        raise TypeError(f"Referência inválida. Insira um dos seguintes valores no campo 'funcao': {list(referencia.keys())}")
    
    df = pd.DataFrame(data['dados'])
    if index:
        df.set_index('cod', inplace=True)
    
    return df

# Lista de deputados, com filtros
def filtrar_deputados(sexo=None, estado=None, partido=None, contendo=None, excluindo=None, index=False):
    
    query = url + 'deputados'
    b = False
    
    if sexo == None:
        pass
    elif sexo == 'F':
        query += '?siglaSexo=F'
        b = True
    elif sexo == 'M':
        query += '?siglaSexo=M'
        b = True
    else:
        raise TypeError("O campo 'sexo' deve conter uma string igual à 'F' ou 'M'.")

    if partido == None:
        pass
    elif isinstance(partido, str):
        query = query + f'&siglaPartido={partido}' if b else query + f'?siglaPartido={partido}'
        b = True
    else:
        raise TypeError("O campo 'partido' deve ser uma sigla em letras maiúsculas que representa um dos partidos políticos brasileiros.")
        
    if estado == None:
        pass
    elif isinstance(estado, str):
        query = query + f'&siglaUf={estado}' if b else query + f'?siglaUf={estado}'
        b = True
    else:
        raise TypeError("O campo 'estado' deve ser uma sigla de duas letras maiúsculas que represente um dos estados brasileiros.")

    response = urllib.request.urlopen(query)
    data = json.loads(response.read())
    df = pd.DataFrame(data['dados'])
    df.drop(columns=df.columns[df.columns.str[:3] == 'uri'], inplace=True)

    if contendo == None:
        pass
    elif isinstance(contendo, str):
        df = df[df.nome.str.contains(contendo)]
    else:
        raise TypeError('O texto procurado deve ser tipo string.')

    if excluindo == None:
        pass
    elif isinstance(excluindo, str):
        df = df[~df.nome.str.contains(excluindo)]
    else:
        raise TypeError('O texto procurado deve ser tipo string.')
        
    df = df.set_index('id') if index else df.reset_index(drop=True)

    return df