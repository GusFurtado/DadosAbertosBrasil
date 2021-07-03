'''Módulo para captura dos dados abertos das APIs do IBGE.

Serviços Disponíveis
--------------------
- Nomes 2.0
- Agregados 3.0 (SIDRA)
- Malhas Geográficas 2.0
- Projeções 1.0
- Localidades 1.0

Mini-Tutorial de SIDRA
----------------------
1. Importe o módulo `ibge`.
>>> from DadosAbertosBrasil import ibge

2. Utilize a função `lista_tabelas` com os filtros necessários para encontrar
a tabela desejada.
>>> ibge.lista_tabelas( ... )

3. Utilize as funções `lista_pesquisas` e `referencias` para facilitar a busca.
>>> pesquisas = ibge.lista_pesquisas( ... )
>>> referencias = ibge.referencias( ... )

4. Após obter o código numérico da tabela, insira-o como argumento de um
objeto `Metadados`.
>>> dados = ibge.Metadados(tabela)

5. Pelos atributos do objeto `Metadados`, veja quais são os valores
disponíveis para consulta desta tabela.
>>> print(dados.periodos)
>>> print(dados.variaveis)
>>> print(dados.localidades)
>>> print(dados.classificacoes)

6. Utilize os valores encontrados nos metadados da tabela para alimentar a
função `sidra`.
>>> ibge.sidra( ... )

Documentação da API original
----------------------------
Serviços
    https://servicodados.ibge.gov.br/api/docs
SIDRA
    http://api.sidra.ibge.gov.br/

'''
from typing import Union

import pandas as _pd
import requests

from ._utils import parse
from ._utils.get_data import get_data



_normalize = _pd.io.json.json_normalize \
    if _pd.__version__[0] == '0' else _pd.json_normalize



def nomes(
        nomes: Union[list, str],
        sexo: str = None,
        localidade: int = None
    ) -> _pd.DataFrame:
    '''Obtém a frequência de nascimentos por década dos nomes consultados.
    
    Defina o campo `nomes` com um string ou uma lista de string.
    Use os argumentos opcionais para definir sexo e localidade dos nomes.

    Parâmetros
    ----------
    nomes : list ou str
        Nome ou lista de nomes a ser consultado.
    sexo : str (default=None)
        - 'M' para consultar apenas o nome de pessoas do sexo masculino;
        - 'F' para consultar apenas o nome de pessoas do sexo feminino;
        - None para consultar ambos.
    localidade : int (default=None)
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

    Erros
    -----
    DAB_LocalidadeError
        Caso o código da localidade seja inválido.
    ValueError
        Caso nenhum valor seja encontrado ou em caso de um argumento inválido.

    Exemplos
    --------
    Forma mais simples da função.

    >>> ibge.nomes('Joao')
    nome           JOAO
    periodo            
    1930[         60155
    [1930,1940[  141772
    [1940,1950[  256001
    [1950,1960[  396438
    [1960,1970[  429148
    [1970,1980[  279975
    [1980,1990[  273960
    [1990,2000[  352552
    [2000,2010[  794118

    Quantidade de nascimento de "João" no Rio de Janeiro (localidade 33)
    e do sexo masculino ('M').

    >>> ibge.nomes('Joao', sexo='M', localidade=33)
    nome          JOAO
    periodo           
    1930[         3592
    [1930,1940[   9207
    [1940,1950[  16860
    [1950,1960[  25221
    [1960,1970[  25839
    [1970,1980[  15477
    [1980,1990[  16114
    [1990,2000[  26862
    [2000,2010[  68741

    '''
    
    if isinstance(nomes, list):
        nomes = '|'.join(nomes)

    params = {}
    if sexo is not None:
        params['sexo'] = sexo
    if localidade is not None:
        params['localidade'] = parse.localidade(localidade)

    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nomes}"
    data = requests.get(url, params=params).json()
    json = _pd.DataFrame(data)

    dfs = [_pd.DataFrame(json.res[i]).set_index('periodo') for i in json.index]
    df = _pd.concat(dfs, axis=1)
    df.columns = json.nome

    return df



def nomes_uf(nome: str) -> _pd.DataFrame:
    '''Obtém a frequência de nascimentos por UF para o nome consultado.

    Parâmetros
    ----------
    nome : str
        Nome que se deseja pesquisar.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo a frequência de nascimentos do nome pesquisado,
        agrupado por Unidade da Federação.

    Exemplos
    --------
    >>> ibge.nomes_uf('Joao')

                populacao  frequencia  proporcao
    localidade                                  
    11            1562409       23366    1495.51
    12             733559       10383    1415.43
    13            3483985       41234    1183.53
    14             450479        5664    1257.33
    ..                ...         ...        ...

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
    '''Obtém o ranking dos nomes segundo a frequência de nascimentos por década.

    Parâmetros
    ----------
    decada : int (default=None)
        Deve ser um número múltiplo de 10 no formato AAAA.
    sexo : str (default=None)
        - 'M' para consultar apenas o nome de pessoas do sexo masculino;
        - 'F' para consultar apenas o nome de pessoas do sexo feminino;
        - None para consultar ambos.
    localidade : int (default=None)
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

    Erros
    -----
    DAB_LocalidadeError
        Caso o código da localidade seja inválido.

    Exemplos
    --------
    Forma mais simples da função.

    >>> ibge.nomes_ranking()
                nome  frequencia
    ranking                       
    1            MARIA    11734129
    2             JOSE     5754529
    3              ANA     3089858
    4             JOAO     2984119
    ..             ...         ...

    Ranking de nomes femininos no Rio de Janeiro na decada de 1990.

    >>> ibge.nomes_ranking(decada=1990, localidade=33, sexo='F')
                nome  frequencia
    ranking                       
    1              ANA       44284
    2            MARIA       27944
    3            ALINE       26084
    4          VANESSA       24225
    ..             ...         ...

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
        params.append(f'localidade={parse.localidade(localidade)}')
            
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



def lista_tabelas(
        pesquisa: str = None,
        contendo: str = None,
        excluindo: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''Lista de tabelas disponíveis no SIDRA.

    Parâmetros
    ----------
    pesquisa : str (default=None)
        Código de duas letras da pesquisa que será buscada.
        Utilize a função `ibge.lista_pesquisas` para encontrar o código.
    contendo : str (default=None)
        Buscar apenas tabelas que contenham essa sequência de caracteres.
    excluindo : str (default=None)
        Buscar tabelas que não contenham essa sequência de caracteres.
    index : bool (default=False)
        Se True, define a coluna 'tabela_id' como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de tabelas disponíveis no SIDRA.

    Exemplos
    --------
    Forma mais simples da função.

    >>> ibge.lista_tabelas()    
        tabela_id                                        tabela_nome  \
    0        1732  Dados gerais das empresas por faixas de pessoa...  \
    1        1735  Dados gerais das unidades locais por faixas de...  \
    2        1734  Dados gerais das unidades locais por faixas de...  \
    3        1733  Dados gerais das unidades locais por faixas de...  \
    4        2869  Empresas e outras organizações e suas unidades...  \

    Listar tabelas do Censo Demográfico (pesquisa 'CD'), contendo o termo
    'rendimento' no título, porém não contendo 'Distribuição', definindo a
    coluna `tabela_id` como index do DataFrame.

    >>> ibge.lista_tabelas(
    ...     pesquisa = 'CD',
    ...     contendo = 'rendimento',
    ...     excluindo = 'Distribuição',
    ...     index = True
    ... )
                                                     tabela_nome pesquisa_id  \
    tabela_id                                                                 \
    171        Chefes de domicílios particulares permanentes ...          CD  \
    3534       Domicílios particulares permanentes com rendim...          CD  \
    3525       Domicílios particulares permanentes com rendim...          CD  \
    2428       Domicílios particulares permanentes com rendim...          CD  \
    2427       Domicílios particulares permanentes com rendim...          CD  \

    '''

    data = get_data(
        endpoint = 'https://servicodados.ibge.gov.br/api/v3/agregados/',
        path = ''
    )
    df = _normalize(
        data,
        'agregados',
        ['id', 'nome'],
        record_prefix = 'tabela_',
        meta_prefix = 'pesquisa_'
    )
    df.tabela_id = _pd.to_numeric(df.tabela_id)

    if isinstance(pesquisa, str):
        df = df[df.pesquisa_id == pesquisa.upper()]
    elif pesquisa == None:
        pass
    else:
        raise TypeError("O argumento 'pesquisa' deve ser tipo string com duas letras.")
        
    if isinstance(contendo, str):
        df = df[df.tabela_nome.str.contains(contendo)]
    elif contendo == None:
        pass
    else:
        raise TypeError('O texto procurado deve ser tipo string.')
        
    if isinstance(excluindo, str):
        df = df[~df.tabela_nome.str.contains(excluindo)]
    elif excluindo == None:
        pass
    else:
        raise TypeError('O texto procurado deve ser tipo string.')

    if index:
        df.set_index('tabela_id', inplace=True)

    return df



def lista_pesquisas(
        index: bool = False
    ) -> _pd.DataFrame:
    '''Lista de pesquisas disponíveis no SIDRA.

    Esta função é utilizada para identificar o código usado pela função
    `ibge.lista_tabelas`.

    Parâmetros
    ----------
    index : bool (default=False)
        Se True, define a coluna 'pesquisa_id' como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de pesquisas disponíveis no SIDRA.

    Exemplos
    --------
    >>> ibge.lista_pesquisas()
       pesquisa_id                                      pesquisa_nome
    0           CL                       Cadastro Central de Empresas
    1           CA                                 Censo Agropecuário
    2           ME           Censo Comum do Mercosul, Bolívia e Chile
    3           CD                                  Censo Demográfico
    4           CM                             Contagem da População 
    ..         ...                                                ...
    
    '''

    data = get_data(
        endpoint = 'https://servicodados.ibge.gov.br/api/v3/agregados/',
        path = ''
    )
    df = _normalize(
        data,
        'agregados',
        ['id', 'nome'],
        record_prefix = 'tabela_',
        meta_prefix = 'pesquisa_'
    )
    df = df[['pesquisa_id', 'pesquisa_nome']] \
        .drop_duplicates().reset_index(drop=True)

    if index:
        df.set_index('pesquisa_id', inplace=True)

    return df



class Metadados:
    '''Metadados da tabela desejada.

    Parâmetros
    ----------
    tabela : int
        Código numérico da tabela desejada.
        Utilize a função `ibge.lista_tabelas` para encontrar o código.

    Atributos
    ---------
    dados : dict
        Lista completa de metadados da tabela.
    cod : int
        Código numérico da tabela.
    nome : str
        Nome da tabela.
    assunto : str
        Assunto da tabela.
    periodos : dict
        Dicionário contendo a frequência, início e fim da tabela.
    localidades : dict
        Dicionário contendo os níveis territoriais da tabela.
    variaveis : list of dict
        Lista de variáveis disponíveis para a tabela.
    classificacoes : list of dict
        Lista de classificações e categorias disponíveis para a tabela.

    Exemplos
    --------
    1. Crie uma instância de `Metadados` utilizando o código da tabela SIDRA
    como argumento.

    >>> m = ibge.Metadados(tabela=1301)

    2. Chame os atributos para obter informações sobre a tabela.

    >>> m.nome
    'Área e Densidade demográfica da unidade territorial'
    >>> m.assunto
    'Território'
    >>> m.periodos
    {'frequencia': 'anual', 'inicio': 2010, 'fim': 2010}

    '''

    def __init__(self, tabela: int):
        data = get_data(
            endpoint = 'https://servicodados.ibge.gov.br/api/v3/agregados/',
            path = f'/{tabela}/metadados'
        )

        self.dados = data
        self.cod = tabela
        self.nome = data['nome']
        self.assunto = data['assunto']
        self.periodos = data['periodicidade']
        self.localidades = data['nivelTerritorial']
        self.variaveis = data['variaveis']
        self.classificacoes = data['classificacoes']


    def __repr__(self):
        return f'DadosAbertosBrasil.ibge: Metadados da Tabela {self.cod} - {self.nome}'



def sidra(
        tabela: int,
        periodos: Union[list, int, str] = 'last',
        variaveis: Union[list, int, str] = 'allxp',
        localidades: dict = {1: 'all'},
        classificacoes: dict = None,
        ufs_extintas: bool = False,
        decimais: int = None,
        retorna: str = 'dataframe'
    ) -> Union[_pd.DataFrame, dict, str]:
    '''Função para captura de dados do SIDRA - Sistema IBGE de Recuperação
    Automática.

    Parâmetros
    ----------
    tabela : int
        Código numérico identificador da tabela.
    periodos : list, int ou str (default='last')
        Períodos de consulta desejados:
            - 'last': Último período;
            - 'last n': Últimos n períodos;
            - 'first': Primeiro período;
            - 'first n': Primeiros n períodos;
            - 'all': Todos os períodos disponíveis;
            - list: Lista de períodos desejados;
            - int: Um período específico;
            - Range de períodos separados por hífen.
    variaveis : list, int ou str (default='allxp')
        Variáveis de consulta desejadas:
            - 'all': Todas as variáveis disponíveis;
            - 'allxp': Todas as variáveis, exceto as percentuais;
            - list: Lista de variáveis;
            - int: Uma variáveis específica.
    localidades : dict (default={1:'all'})
        Localidades por nível territorial.
        As chaves dos dicionários devem ser o código de nível territorial:
            - 1: Brasil;
            - 2: Grande região (N, NE, SE, S, CO);
            - 3: Unidade da Federação (UFs);
            - 6: Município;
            - 7: Região metropolitana;
            - 8: Mesorregião geográfica;
            - 9: Microrregião geográfica;
            - 13: Região metropolitana e subdivisão;
            - 14: Região Integrada de Desenvolvimento;
            - 15: Aglomeração urbana.
        Os valores do dicionário devem ser:
            - 'all': Todas as localidades do nível territorial.
            - list: Códigos dos territórios desejados.
            - int: Um território específico.
    classificacoes : dict (default=None)
        Dicionário de classificações e categorias.
        As chaves do dicionário devem ser o código da classificação.
        Os valores do dicionário devem ser:
            - 'all': Todas as categorias desta classificação;
            - 'allxt': Todas as categorias, exceto as totais;
            - list: Lista de categorias desejadas;
            - int: Uma categoria específica.
    ufs_extintas : bool (default=False)
        Se True, adiciona as UFs extintas (se disponível na tabela).
            - 20: Fernando de Noronha
            - 34: Guanabara
    decimais : int (default=None)
        Número de fixo de casas decimais do resultado, entre 0 e 9.
        Se None, utiliza o padrão de cada variável. 
    retorna : str (default='dataframe')
        Formato do dado retornado:
            - 'dataframe': Retorna um DataFrame Pandas;
            - 'json': Retorna um dicionário no formato json original;
            - 'url': Retorna a URL para consulta.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Se retorna='dataframe', retorna um DataFrame com os resultados.
    dict
        Se retorna='json', retorna um dicionário no formato json original.
    str
        Se retorna='url', retorna a URL para consulta.

    '''

    path = f'http://api.sidra.ibge.gov.br/values/t/{tabela}'

    if periodos is not None:
        if isinstance(periodos, list):
            periodos = ','.join([str(i) for i in periodos])
        path += f'/p/{periodos}'

    if variaveis is not None:
        if isinstance(variaveis, list):
            variaveis = ','.join([str(i) for i in variaveis])
        path += f'/v/{variaveis}'

    for n in localidades:
        if isinstance(localidades[n], list):
            valor = ','.join([str(i) for i in localidades[n]])
        else:
            valor = localidades[n]
        path += f'/n{n}/{valor}'

    if classificacoes is not None:
        for c in classificacoes:
            if isinstance(classificacoes[c], list):
                valor = ','.join([str(i) for i in classificacoes[c]])
            else:
                valor = classificacoes[c]
            path += f'/c{c}/{valor}'

    u = 'y' if ufs_extintas else 'n'
    d = 's' if decimais is None else decimais
    path += f'/u/{u}/d/{d}'

    if retorna == 'url':
        return path

    data = requests.get(path).json()
    if retorna == 'json':
        return data

    df = _pd.DataFrame(data[1:])
    df.columns = data[0].values()
    return df



def referencias(
        cod: str,
        index: bool = False
    ) -> _pd.DataFrame:
    '''Obtém uma base de códigos para utilizar como argumento na busca do SIDRA.

    Parâmetros
    ----------
    cod : str
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

    Erros
    -----
    ValueError
        Caso o código da referência seja inválido.

    Exemplos
    --------
    Lista assuntos.

    >>> ibge.referencias('a')
          id                                       literal
    0    148                         Abastecimento de água
    1     70                              Abate de animais
    2    110                Acesso a esgotamento sanitário
    3    147                             Acesso à internet
    4    107  Acesso a serviço de coleta de lixo doméstico
    ..    ..                                            ..

    Lista classificações usando o `ìd` da classificação como index
    do DataFrame.
    
    >>> ibge.referencias('c', index=True)
                                                     literal
    id                                                      
    588    Acessibilidade possível na maior parte das via...
    957    Acesso à Internet por telefone móvel celular p...
    681                    Acesso a televisão por assinatura
    12236                               Adequação da moradia
    806                      Adubação, calagem e agrotóxicos
    ...                                                  ...

    '''

    cod = cod.lower()
    if cod in ('a', 'assuntos'):
        s = 'A'
    elif cod in ('c', 'classificacoes'):
        s = 'C'
    elif cod in ('n', 't', 'niveis_geograficos', 'territorios'):
        s = 'N'
    elif cod in ('p', 'periodos'):
        s = 'P'
    elif cod in ('e', 'periodicidades'):
        s = 'E'
    elif cod in ('v', 'variaveis'):
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
    ) -> Union[dict, int]:
    '''Obtém a projecao da população referente ao Brasil.

    Parâmetros
    ----------
    projecao : str (default=None)
        - 'populacao' obtém o valor projetado da população total da localidade;
        - 'nascimento' obtém o valor projetado de nascimentos da localidade
        - 'obito' obtém o valor projetado de óbitos da localidade;
        - 'incremento' obtém o incremento populacional projetado.
        - None obtém um dicionário com todos os valores anteriores.
    localidade : int (default=None)
        Código da localidade desejada.
        Por padrão, obtém os valores do Brasil.
        Utilize a função `ibge.localidades` para identificar
        a localidade desejada.

    Retorna
    -------
    dict ou int:
        Valor(es) projetado(s) para o indicador escolhido.

    Erros
    -----
    DAB_LocalidadeError
        Caso código da localidade seja inválido.
    ValueError
        Caso o argumento `projecao` seja inválido.

    Exemplos
    --------
    Projeção de óbito do Brasil.

    >>> ibge.populacao('obito')
    45000

    Obter dados do Rio de Janeiro (localidade 33)

    >>> ibge.populacao(localidade=33)
    {
        'localidade': '33',
        'horario': '03/07/2021 19:15:48',
        'projecao': {
            'populacao': 17459953,
            'periodoMedio': {
                'incrementoPopulacional': 330508
            }
        }
    }

    '''

    localidade = parse.localidade(localidade, '')
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
    elif projecao == 'incremento':
        return r['projecao']['periodoMedio']['incrementoPopulacional']
    else:
        raise ValueError('''O argumento 'projecao' deve ser um dos seguintes valores tipo string:
            - 'populacao';
            - 'nascimento';
            - 'obito';
            - 'incremento'.''')



def _loc_columns(x: str) -> str:
    '''Função de suporte à função `ibge.localidades`.
    Usada para renomear as colunas do DataFrame de distritos.
    
    '''

    y = x.replace('-', '_').split('.')
    return f'{y[-2]}_{y[-1]}' if len(y)>1 else y[0]



def localidades() -> _pd.DataFrame:
    '''Obtém o conjunto de distritos do Brasil.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo todas as divisões de distritos do Brasil.

    Exemplos
    --------
    >>> ibge.localidades()
                  id                 nome  municipio_id       municipio_nome  \
    0      520005005      Abadia de Goiás       5200050      Abadia de Goiás  \
    1      310010405  Abadia dos Dourados       3100104  Abadia dos Dourados  \
    2      520010005            Abadiânia       5200100            Abadiânia  \
    3      520010010       Posse d'Abadia       5200100            Abadiânia  \
    4      310020305               Abaeté       3100203               Abaeté  \
    ..           ...                  ...           ...                  ...

    '''

    df = _normalize(
        requests.get(
            r'https://servicodados.ibge.gov.br/api/v1/localidades/distritos'
        ).json()
    )

    df.columns = df.columns.map(_loc_columns)
    return df.loc[:,~df.columns.duplicated()]



def malha(localidade:int=None) -> str:
    '''Obtém a URL para a malha referente ao identificador da localidade.

    Parâmetros
    ----------
    localidade : int (default=None)
        Código da localidade desejada.
        Por padrão, obtém a malha do Brasil.
        Utilize a função `ibge.localidades` para identificar
        a localidade desejada.

    Retorna
    -------
    str
        URL da malha da localidade desejada.

    Erros
    -----
    DAB_LocalidadeError
        Caso o código da localidade seja inválido.

    Exemplos
    --------
    >>> ibge.malha(localidade=4209102)
    https://servicodados.ibge.gov.br/api/v2/malhas/4209102

    '''

    localidade = parse.localidade(localidade, '')
    return f'https://servicodados.ibge.gov.br/api/v2/malhas/{localidade}'



def coordenadas() -> _pd.DataFrame:
    '''Obtém as coordenadas de todas as localidades brasileiras, incluindo
    latitude, longitude e altitude.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame das coordenadas de todas as localidade brasileiras.

    Exemplos
    --------
    >>> ibge.coordenadas()
           GM_PONTO     ID     CD_GEOCODIGO    TIPO   CD_GEOCODBA NM_BAIRRO  \
    0           NaN      1  110001505000001  URBANO  1.100015e+11   Redondo  \
    1           NaN      2  110001515000001  URBANO           NaN       NaN  \
    2           NaN      3  110001520000001  URBANO           NaN       NaN  \
    3           NaN      4  110001525000001  URBANO           NaN       NaN  \
    4           NaN      5  110001530000001  URBANO           NaN       NaN  \
    ..          ...     ..              ...     ...           ...       ...  \

    '''

    return _pd.read_excel(
        r'https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/data/Coordenadas.xlsx'
    )