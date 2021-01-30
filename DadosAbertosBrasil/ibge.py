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



import pandas as _pd
import requests

from . import _utils



_normalize = _pd.io.json.json_normalize \
    if _pd.__version__[0] == '0' else _pd.json_normalize

_URL = 'https://servicodados.ibge.gov.br/api/v3/agregados'



def nomes(
        nomes: list,
        sexo: str = None,
        localidade: int = None
    ) -> _pd.DataFrame:
    '''
    Obtém a frequência de nascimentos por década dos nomes consultados.
    Defina o campo 'nomes' com um string ou uma lista de string.
    Use os argumentos opcionais para definir sexo e localidade dos nomes.

    Parametros
    ----------
    nomes: list ou str
        Nome ou lista de nomes a ser consultado.
    sexo: str (default=None)
        - 'M' para consultar apenas o nome de pessoas do sexo masculino;
        - 'F' para consultar apenas o nome de pessoas do sexo feminino;
        - None para consultar ambos.
    localidade: int ou str (opcional)
        Caso deseje obter a frequência referente a uma dada localidade,
        informe o parâmetro localidade. Por padrão, assume o valor BR,
        mas pode ser o identificador de um município ou de uma UF.
        Utilize a função `ibge.localidade` para encontrar a localidade
        desejada.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo a frequência de nascimentos por década para
        o(s) nome(s) consultado(s).

    --------------------------------------------------------------------------
    '''
    
    if isinstance(nomes, str):
        s = nomes
    if isinstance(nomes, list):
        s = '|'.join(nomes)

    if sexo != None:
        s += f'?sexo={sexo}'

    if localidade is not None:
        s += f'?localidade={_utils.parse_localidade(localidade)}'

    json = _pd.read_json(
        f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{s}"
    )

    dfs = [_pd.DataFrame(json.res[i]).set_index('periodo') for i in json.index]
    df = _pd.concat(dfs, axis=1)
    df.columns = json.nome

    return df



def nomes_uf(nome: str) -> _pd.DataFrame:
    '''
    Obtém a frequência de nascimentos por UF para o nome consultado.

    Parâmetros
    ----------
    nome: str
        Nome que se deseja pesquisar.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo a frequência de nascimentos do nome pesquisado,
        agrupado por Unidade da Federação.

    --------------------------------------------------------------------------
    '''
    
    if isinstance(nome, str):

        json = _pd.read_json(
            f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}?groupBy=UF"
        )

        df = _pd.DataFrame(
            [json[json.localidade == i].res.values[0][0] for i in json.localidade]
        )

        df.index = json.localidade
        df.sort_index(inplace=True)
        
    else:
        raise TypeError("O argumento 'nome' deve ser do tipo string.")
    
    return df



def nomes_ranking(
        decada: int = None,
        sexo: str = None,
        localidade: int = None
    ) -> _pd.DataFrame:
    '''
    Obtém o ranking dos nomes segundo a frequência de nascimentos por década.

    Parâmetros
    ----------
    decada: int (default=None)
        Deve ser um número múltiplo de 10 no formato AAAA.
    sexo: str (default=None)
        - 'M' para consultar apenas o nome de pessoas do sexo masculino;
        - 'F' para consultar apenas o nome de pessoas do sexo feminino;
        - None para consultar ambos.
    localidade: int ou str (default=None)
        Caso deseje obter o ranking de nomes referente a uma dada localidade,
        informe o parâmetro localidade. Por padrão, assume o valor BR,
        mas pode ser o identificador de um município ou de uma UF.
        Utilize a função `ibge.localidade` para encontrar a localidade
        desejada.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os nomes mais populadores dentro do universo de
        parâmetros pesquisados.

    --------------------------------------------------------------------------
    '''
    
    query = 'https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking'
    params = []
    
    if decada is not None:
        decada_error = "O argumento 'decada' deve ser um número inteiro multiplo de 10."
        if isinstance(decada, int):
            if decada%10 == 0:
                params.append(f'decada={decada}')
            else:
                raise ValueError(decada_error)
        else:
            raise TypeError(decada_error)
    
    if localidade is not None:
        params.append(f'localidade={_utils.parse_localidade(localidade)}')
            
    if sexo is not None:
        if sexo in ['M', 'm', 'F', 'f']:
            params.append(f'sexo={sexo.upper()}')
        else:
            raise ValueError("O argumento 'sexo' deve ser um tipo 'string' igual a 'M' para masculino ou 'F' para feminino.")
    
    params = '&'.join(params)
    if params != '':
        query += f'?{params}'
    
    return _pd.DataFrame(
        _pd.read_json(query).res[0]
    ).set_index('ranking')



class Agregados:
    '''
    Obtém o conjunto de agregados, agrupados pelas respectivas pesquisas.
    '''

    def __init__(self, index=False):
        data = requests.get(_URL).json()

        df = _normalize(
            data,
            'agregados',
            ['id', 'nome'],
            record_prefix = 'agregado_',
            meta_prefix = 'pesquisa_'
        )
        
        df.agregado_id = _pd.to_numeric(df.agregado_id)

        self.dados = df.set_index('agregado_id', drop = True) \
            .sort_index() if index else df

        self.pesquisas = df[['pesquisa_id', 'pesquisa_nome']] \
            .drop_duplicates().reset_index(drop=True)
    

    def filtrar(self, pesquisa=None, contendo=None, excluindo=None) -> _pd.DataFrame:
        '''
        Filtra lista de agregados.
        Defina o tipo da pesquisa ou filtre agregados contendo ou não determinado substring.
        '''

        df = self.dados
        
        if isinstance(pesquisa, str):
            df = df[df.pesquisa_id == pesquisa]
        elif pesquisa == None:
            pass
        else:
            raise TypeError("O argumento 'pesquisa' deve ser tipo string com duas letrar maiúsculas.")
            
        if isinstance(contendo, str):
            df = df[df.agregado_nome.str.contains(contendo)]
        elif contendo == None:
            pass
        else:
            raise TypeError('O texto procurado deve ser tipo string.')
            
        if isinstance(excluindo, str):
            df = df[~df.agregado_nome.str.contains(excluindo)]
        elif excluindo == None:
            pass
        else:
            raise TypeError('O texto procurado deve ser tipo string.')
            
        return df



class Metadados:
    '''
    Metadados dos agregados.
    Veja os dados, id, nome, assunto, período, localidades, variáveis e classificações do agregado escolhido.
    '''

    def __init__(self, agregado: int):
        data = requests.get(_URL + f'/{agregado}/metadados').json()
        self.dados = data
        self.id = data['id']
        self.nome = data['nome']
        self.assunto = data['assunto']
        self.periodos = data['periodicidade']
        self.localidades = data['nivelTerritorial']
        self.variaveis = data['variaveis']
        self.classificacoes = data['classificacoes']


        
class Sidra:
    '''
    Classe para obter dados do SIDRA - Sistema IBGE de Recuperação Automática.
    '''

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


    def __converter_lista(self, lista, sep='|') -> str:
        if isinstance(lista, list):
            s = str(lista[0])
            for i in lista[1:]:
                s += f'{sep}{i}'
        else:
            s = lista
        return s


    def __convertar_dicionario(self, dicionario: dict) -> str:
        b = True
        for i in dicionario:
            if b:
                s = f"{i}[{self.__converter_lista(dicionario[i], sep=',')}]"
                b = False
            else:
                s += f"|{i}[{self.__converter_lista(dicionario[i], sep=',')}]"
        return s
            

    def query(self) -> str:
        '''
        Apresenta a query com os argumentos definidos.
        '''

        query = f'{_URL}/{self.agregado}/'
        query += f'periodos/{self.__converter_lista(self.periodos)}/'
        query += f'variaveis/{self.__converter_lista(self.variaveis)}?'
        query += f'localidades={self.__convertar_dicionario(self.localidades)}'
        if self.classificacoes != None:
            query += f'&classificacao={self.__convertar_dicionario(self.classificacoes)}'
        return query
    

    def rodar(self) -> dict:
        '''
        Roda a query com os argumentos definidos.
        '''

        return requests.get(self.query()).json()



def referencias(
        cod: str,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Obtém uma base de códigos para utilizar como argumento na busca do SIDRA.

    Parâmetros
    ----------
    cod: str
        - 'A': Assuntos;
        - 'C': Classificações;
        - 'N': Níveis geográficos;
        - 'P': Períodos;
        - 'E': Periodicidades;
        - 'V': Variáveis.
    index: bool (default=False)
        Defina True caso o campo 'id' deva ser o index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo todas as referências do código pesquisado.

    --------------------------------------------------------------------------
    '''

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
        raise ValueError("O campo 'cod' deve ser do tipo string.")
        
    data = requests.get(f'https://servicodados.ibge.gov.br/api/v3/agregados?acervo={s}').json()
    df = _pd.DataFrame(data)

    if index:
        df.set_index('id', inplace=True)
    
    return df


   
def populacao(
        projecao: str = None,
        localidade: int = None
    ):
    '''
    Obtém a projecao da população referente ao Brasil.

    Parametros
    ----------
    projecao: str (default=None)
        - 'populacao' obtém o valor projetado da população total da localidade;
        - 'nascimento' obtém o valor projetado de nascimentos da localidade
        - 'obito' obtém o valor projetado de óbitos da localidade;
        - None obtém um dicionário com todos os valores anteriores.
    localidade: int ou str (default=None)
        Código da localidade desejada.
        Por padrão, obtém os valores do Brasil.
        Utilize a função ibge.localidades() para identificar
        a localidade desejada.

    Retorna
    -------
    dict ou int:
        Valor(es) projetado(s) para o indicador escolhido.

    --------------------------------------------------------------------------
    '''

    localidade = _utils.parse_localidade(localidade, '')
    query = f'https://servicodados.ibge.gov.br/api/v1/projecoes/populacao/{localidade}'
            
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



def _loc_columns(x: str) -> str:
    '''
    Função de suporte à função ibge.localidades().
    Usada para renomear as colunas do DataFrame de distritos.
    '''

    y = x.replace('-', '_').split('.')
    return f'{y[-2]}_{y[-1]}' if len(y)>1 else y[0]



def localidades() -> _pd.DataFrame:
    '''
    Obtém o conjunto de distritos do Brasil.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo todas as divisões de distritos do Brasil.

    --------------------------------------------------------------------------
    '''

    df = _normalize(
        requests.get(
            r'https://servicodados.ibge.gov.br/api/v1/localidades/distritos'
        ).json()
    )

    df.columns = df.columns.map(_loc_columns)
    return df.loc[:,~df.columns.duplicated()]



def malha(localidade:int=None) -> str:
    '''
    Obtém a URL para a malha referente ao identificador da localidade.

    Parametros
    ----------
    localidade: int ou str (default = '')
        Código da localidade desejada.
        Por padrão, obtém a malha do Brasil.
        Utilize a função `ibge.localidades` para identificar
        a localidade desejada.

    Retorna
    -------
    str
        URL da malha da localidade desejada.

    --------------------------------------------------------------------------
    '''

    localidade = _utils.parse_localidade(localidade, '')
    return f'https://servicodados.ibge.gov.br/api/v2/malhas/{localidade}'



def coordenadas() -> _pd.DataFrame:
    '''
    Obtém as coordenadas de todas as localidades brasileiras, incluindo
    latitude, longitude e altitude.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame das coordenadas de todas as localidade brasileiras.

    --------------------------------------------------------------------------
    '''

    return _pd.read_excel(
        r'https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/data/Coordenadas.xlsx'
    )