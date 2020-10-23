'''
Módulo para captura dos dados abertos das APIs do IBGE.

Essa pacote inclui os seguintes serviços de dados do IBGE:
- Nomes 2.0
- Agregados 3.0 (SIDRA)
- Malhas Geográficas 2.0
- Projeções 1.0
- Localidades 1.0

Documentação da API original: https://servicodados.ibge.gov.br/api/docs 
'''



import pandas as pd
import requests



_normalize = pd.io.json.json_normalize if pd.__version__[0] == '0' else pd.json_normalize
_url = 'https://servicodados.ibge.gov.br/api/v3/agregados'



# Obtém a frequência de nascimentos por década para o(s) nome(s) consultado(s)
def nomes(nomes, sexo=None, localidade=None):
    
    if isinstance(nomes, str):
        s = nomes
    if isinstance(nomes, list):
        s = ''
        for nome in nomes:
            s += nome + '|'
    if sexo != None:
        s += f'?sexo={sexo}'
    if localidade != None:
        s += f'?localidade={localidade}'

    json = pd.read_json(
        f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{s}"
    )

    nomes = ['PERIODO'] + json.nome.to_list()
    df = pd.DataFrame(json.res[0])
    df = df[['periodo', 'frequencia']]

    for i in json.res[1:]:
        df = pd.merge(
            df,
            pd.DataFrame(i),
            left_on='periodo',
            right_on='periodo'
        )

    df.columns = nomes    

    return df



# Obtém a frequência de nascimentos por UF para o nome consultado
def nomes_uf(nome):
    
    if isinstance(nome, str):

        json = pd.read_json(
            f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}?groupBy=UF"
        )

        df = pd.DataFrame(
            [json[json.localidade == i].res.values[0][0] for i in json.localidade]
        )

        df.index = json.localidade
        df.sort_index(inplace=True)
        
    else:
        raise TypeError("O argumento 'nome' deve ser do tipo string.")
    
    return df



# Obtém o ranking dos nomes segundo a frequência de nascimentos por década
def nomes_ranking(decada=None, sexo=None, localidade=None):
    
    query = 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking'
    sep = '?'
    
    if decada != None:
        if isinstance(decada, int):
            query += f'?decada={decada}'
            sep = '&'
        else:
            raise TypeError("O argumento 'decada' deve ser um número inteiro multiplo de 10.")
    
    if localidade != None:
        if isinstance(localidade, int):
            query += f'{sep}localidade={localidade}'
            sep = '&'
        else:
            raise TypeError("O argumento 'localidade' deve ser um número inteiro.")
            
    if sexo != None:
        if sexo == 'M' or sexo == 'F':
            query += f'{sep}sexo={sexo}'
        else:
            raise TypeError("O argumento 'sexo' deve ser um tipo 'string' igual a 'M' para masculino ou 'F' para feminino.")
    
    return pd.DataFrame(
        pd.read_json(query).res[0]
    ).set_index('ranking')



# Obtém o conjunto de agregados, agrupados pelas respectivas pesquisas
class Agregados:

    def __init__(self, index=False):
        data = requests.get(_url).json()

        df = _normalize(
            data,
            'agregados',
            ['id', 'nome'],
            record_prefix = 'agregado_',
            meta_prefix = 'pesquisa_'
        )
        
        df.agregado_id = pd.to_numeric(df.agregado_id)

        self.dados = df.set_index('agregado_id', drop = True) \
            .sort_index() if index else df

        self.pesquisas = df[['pesquisa_id', 'pesquisa_nome']] \
            .drop_duplicates().reset_index(drop=True)
    
    # Filtra lista de agregados
    def filtrar(self, pesquisa=None, contendo=None, excluindo=None):
        df = self.dados
        
        # Filtrar pesquisa
        if isinstance(pesquisa, str):
            df = df[df.pesquisa_id == pesquisa]
        elif pesquisa == None:
            pass
        else:
            raise TypeError("O argumento 'pesquisa' deve ser tipo string com duas letrar maiúsculas.")
            
        # Filtrar séries contendo texto
        if isinstance(contendo, str):
            df = df[df.agregado_nome.str.contains(contendo)]
        elif contendo == None:
            pass
        else:
            raise TypeError('O texto procurado deve ser tipo string.')
            
        # Filtrar séries não contendo texto
        if isinstance(excluindo, str):
            df = df[~df.agregado_nome.str.contains(excluindo)]
        elif excluindo == None:
            pass
        else:
            raise TypeError('O texto procurado deve ser tipo string.')
            
        return df



# Metadados dos agregados
class Metadados:
    
    def __init__(self, agregado):
        data = requests.get(_url + f'/{agregado}/metadados').json()
        self.dados = data
        self.id = data['id']
        self.nome = data['nome']
        self.assunto = data['assunto']
        self.periodos = data['periodicidade']
        self.localidades = data['nivelTerritorial']
        self.variaveis = data['variaveis']
        self.classificacoes = data['classificacoes']


        
# Classe para obter dados do SIDRA - Sistema IBGE de Recuperação Automática
class Sidra:

    # Argumentos iniciais
    def __init__(
            self,
            agregado = None,
            periodos = None,
            variaveis = None,
            localidades = {'N1': 'all'},
            classificacoes = None
    ):
        
        self.agregado = agregado
        self.periodos = periodos
        self.variaveis = variaveis
        self.localidades = localidades
        self.classificacoes = classificacoes

    def __converter_lista(self, lista, sep='|'):
        if isinstance(lista, list):
            s = str(lista[0])
            for i in lista[1:]:
                s += f'{sep}{i}'
        else:
            s = lista
        return s
    
    def __convertar_dicionario(self, dicionario):
        b = True
        for i in dicionario:
            if b:
                s = f"{i}[{self.__converter_lista(dicionario[i], sep=',')}]"
                b = False
            else:
                s += f"|{i}[{self.__converter_lista(dicionario[i], sep=',')}]"
        return s
            
    # Contrói a query com os argumentos da classe
    def query(self):
        query = f'{_url}/{self.agregado}/'
        query += f'periodos/{self.__converter_lista(self.periodos)}/'
        query += f'variaveis/{self.__converter_lista(self.variaveis)}?'
        query += f'localidades={self.__convertar_dicionario(self.localidades)}'
        if self.classificacoes != None:
            query += f'&classificacao={self.__convertar_dicionario(self.classificacoes)}'
        return query
    
    # Roda query com os argumentos da classe
    def rodar(self):
        return requests.get(self.query()).json()



# Obtém uma base de códigos para utilizar como argumento na busca do SIDRA
def referencias(cod, index=False):

    if cod in ['A', 'a', 'assuntos']:
        s = 'A'
    elif cod in ['C', 'c', 'classificacoes']:
        s = 'C'
    elif cod in ['N', 'n', 'niveis_geograficos', 'T', 't', 'territorios']:
        s = 'N'
    elif cod in ['P', 'p', 'periodos']:
        s = 'P'
    elif cod in ['E', 'e', 'periodicidades']:
        s = 'E'
    elif cod in ['V', 'v', 'variaveis']:
        s = 'V'
    else:
        raise TypeError("O campo 'cod' deve ser um tipo string.")
        
    data = requests.get(f'https://servicodados.ibge.gov.br/api/v3/agregados?acervo={s}').json()
    df = pd.DataFrame(data)

    if index:
        df.set_index('id', inplace=True)
    
    return df


   
# Obtém a projecao da população referente ao Brasil
def populacao(projecao=None, localidade=None):
    
    query = f'https://servicodados.ibge.gov.br/api/v1/projecoes/populacao'
    if localidade != None:
        if isinstance(localidade, int):
            query += f'/{localidade}'
        else:
            raise TypeError("O argumento 'localidade' deve ser um número inteiro.")
            
    r = requests.get(query).json()
    
    if projecao == None:
        return r
    elif projecao == 'populacao':
        return r['projecao']['populacao']
    elif projecao == 'nascimento':
        return r['projecao']['periodoMedio']['nascimento']
    elif projecao == 'obito':
        return r['projecao']['periodoMedio']['obito']
    else:
        raise TypeError("O argumento 'projecao' deve ser um dos seguintes valores tipo string: 'populacao', 'nascimento' ou 'obito'.")



# Obtém o conjunto de distritos do Brasil
def localidades():

    loc = _normalize(
        requests.get(
            r'https://servicodados.ibge.gov.br/api/v1/localidades/distritos'
        ).json()
    )
    
    loc.columns = [
        'distrito_id',
        'municipio_id',
        'microrregiao_id',
        'uf_id',
        'uf',
        'regiao_id',
        'regiao',
        'regiao_sigla',
        'uf_sigla',
        'mesorregiao_id',
        'mesorregiao',
        'microrregiao',
        'municipio',
        'distrito'
    ]
    
    loc = loc[[
        'distrito_id',
        'distrito',
        'municipio_id',
        'municipio',
        'microrregiao_id',
        'microrregiao',
        'mesorregiao_id',
        'mesorregiao',
        'uf_id',
        'uf',
        'uf_sigla',
        'regiao_id',
        'regiao',
        'regiao_sigla'
    ]]

    return loc



# Obtém a URL para a malha referente ao identificador da localidade
def malha(localidade=''):
    return 'https://servicodados.ibge.gov.br/api/v2/malhas/' + str(localidade)



# Obtém as coordenadas de todas as localidades brasileiras
def coordenadas():
    return pd.read_excel(
        r'https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/data/Coordenadas.xlsx'
    )