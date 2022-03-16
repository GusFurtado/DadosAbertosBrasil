"""Submódulo IBGE contendo os wrappers da API do SIDRA.

Este submódulo é importado automaticamente com o módulo `ibge`.

>>> from DadosAbertosBrasil import ibge

References
----------
.. [1] API SIDRA
    http://api.sidra.ibge.gov.br/

"""

from typing import Optional, Union

import pandas as pd
import requests

from DadosAbertosBrasil._utils.get_data import get_data



_normalize = pd.io.json.json_normalize \
    if pd.__version__[0] == '0' else pd.json_normalize



def lista_tabelas(
        contendo: Optional[str] = None,
        excluindo: Optional[str] = None,
        assunto: Optional[Union[int, str]] = None,
        classificacao: Optional[Union[int, str]] = None,
        periodo: Optional[str] = None,
        periodicidade: Optional[Union[int, str]] = None,
        nivel: Optional[Union[int, str]] = None,
        pesquisa: Optional[str] = None,
        index: bool = False
    ) -> pd.DataFrame:
    """Lista de tabelas disponíveis no SIDRA.

    Parameters
    ----------
    contendo : str, optional
        Termo que deve estar contido no nome ou no comentário da série.
    excluindo : str | list[str], optional
        Termo ou lista de termos que não pode aparecer no nome da série.
        Sobrepõe o argumento `contendo`.
    assunto : str | int, optional
        Filtrar por código do assunto. 
        Utilize a função `ibge.referencias('a')` para encontrar o código.
    classificacao : str | int, optional
        Filtrar por código do classificacao.
        Utilize a função `ibge.referencias('c')` para encontrar o código. 
    periodo : str, optional
        Filtrar por código do periodo. 
        Utilize a função `ibge.referencias('p')` para encontrar o código.
    periodicidade : str | int, optional
        Filtrar por código do periodicidade. 
        Utilize a função `ibge.referencias('e')` para encontrar o código.
    nivel : str | int, optional
        Filtrar por código do nivel.
        Utilize a função `ibge.referencias('n')` para encontrar o código. 
    pesquisa : str, optional
        Código de duas letras da pesquisa que será buscada.
        Utilize a função `ibge.lista_pesquisas` para encontrar o código.
    index : bool, default=False
        Se True, define a coluna 'tabela_id' como index do DataFrame.

    Returns
    -------
    pandas.core.frame.DataFrame
        Lista de tabelas disponíveis no SIDRA.

    Examples
    --------
    Forma mais simples da função.

    >>> ibge.lista_tabelas()    
        tabela_id                                        tabela_nome  ...
    0        1732  Dados gerais das empresas por faixas de pessoa...  ...
    1        1735  Dados gerais das unidades locais por faixas de...  ...
    2        1734  Dados gerais das unidades locais por faixas de...  ...
    3        1733  Dados gerais das unidades locais por faixas de...  ...
    4        2869  Empresas e outras organizações e suas unidades...  ...

    Listar tabelas do Censo Demográfico (pesquisa 'CD'), contendo o termo
    'rendimento' no título, porém não contendo 'Distribuição', definindo a
    coluna `tabela_id` como index do DataFrame.

    >>> ibge.lista_tabelas(
    ...     pesquisa = 'CD',
    ...     contendo = 'rendimento',
    ...     excluindo = 'Distribuição',
    ...     index = True
    ... )
                                                     tabela_nome pesquisa_id  ...
    tabela_id                                                               
    171        Chefes de domicílios particulares permanentes ...          CD  ...
    3534       Domicílios particulares permanentes com rendim...          CD  ...
    3525       Domicílios particulares permanentes com rendim...          CD  ...
    2428       Domicílios particulares permanentes com rendim...          CD  ...
    2427       Domicílios particulares permanentes com rendim...          CD  ...

    """

    params = {}

    if assunto is not None:
        params['assunto'] = assunto

    if classificacao is not None:
        params['classificacao'] = classificacao

    if periodo is not None:
        params['periodo'] = periodo

    if periodicidade is not None:
        if isinstance(periodicidade, int):
            periodicidade = f'P{periodicidade}'
        params['periodicidade'] = periodicidade.upper()

    if nivel is not None:
        if isinstance(nivel, int):
            nivel = f'N{nivel}'
        params['nivel'] = nivel.upper()

    data = get_data(
        endpoint = 'https://servicodados.ibge.gov.br/api/v3/agregados/',
        path = '',
        params = params
    )
    df = _normalize(
        data,
        'agregados',
        ['id', 'nome'],
        record_prefix = 'tabela_',
        meta_prefix = 'pesquisa_'
    )
    df.tabela_id = pd.to_numeric(df.tabela_id)

    if isinstance(contendo, str):
        df = df[df.tabela_nome.str.upper().str.contains(contendo.upper())]

    if excluindo is not None:
        if isinstance(excluindo, str):
            excluindo = [excluindo]
        for termo in excluindo:
            df = df[~df.SERNOME.str.upper().str.contains(termo.upper())]

    if isinstance(pesquisa, str):
        df = df[df.pesquisa_id.str.upper() == pesquisa.upper()]

    if index:
        df.set_index('tabela_id', inplace=True)

    return df



def lista_pesquisas(
        index: bool = False
    ) -> pd.DataFrame:
    """Lista de pesquisas disponíveis no SIDRA.

    Esta função é utilizada para identificar o código usado pela função
    `ibge.lista_tabelas`.

    Parameters
    ----------
    index : bool, default=False
        Se True, define a coluna 'pesquisa_id' como index do DataFrame.

    Returns
    -------
    pandas.core.frame.DataFrame
        Lista de pesquisas disponíveis no SIDRA.

    Examples
    --------
    >>> ibge.lista_pesquisas()
       pesquisa_id                                      pesquisa_nome
    0           CL                       Cadastro Central de Empresas
    1           CA                                 Censo Agropecuário
    2           ME           Censo Comum do Mercosul, Bolívia e Chile
    3           CD                                  Censo Demográfico
    4           CM                             Contagem da População 
    ..         ...                                                ...
    
    """

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
    """Metadados da tabela desejada.

    Parameters
    ----------
    tabela : int
        Código numérico da tabela desejada.
        Utilize a função `ibge.lista_tabelas` para encontrar o código.

    Attributes
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

    Examples
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

    """

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


    def __repr__(self) -> str:
        return f'<DadosAbertosBrasil.ibge: Metadados da Tabela {self.cod} - {self.nome}>'


    def __str__(self) -> str:
        return self.nome



def sidra(
        tabela: int,
        periodos: Union[list, int, str] = 'last',
        variaveis: Union[list, int, str] = 'allxp',
        localidades: dict = {1: 'all'},
        classificacoes: Optional[dict] = None,
        ufs_extintas: bool = False,
        decimais: Optional[int] = None,
        retorna: str = 'dataframe'
    ) -> Union[pd.DataFrame, dict, str]:
    """Função para captura de dados do SIDRA - Sistema IBGE de Recuperação
    Automática.

    Parameters
    ----------
    tabela : int
        Código numérico identificador da tabela.
    periodos : list or int or str, default='last'
        Períodos de consulta desejados:
            - 'last': Último período;
            - 'last n': Últimos n períodos;
            - 'first': Primeiro período;
            - 'first n': Primeiros n períodos;
            - 'all': Todos os períodos disponíveis;
            - list: Lista de períodos desejados;
            - int: Um período específico;
            - Range de períodos separados por hífen.
    variaveis : list or int or str, default='allxp'
        Variáveis de consulta desejadas:
            - 'all': Todas as variáveis disponíveis;
            - 'allxp': Todas as variáveis, exceto as percentuais;
            - list: Lista de variáveis;
            - int: Uma variáveis específica.
    localidades : dict, default={1:'all'}
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
    classificacoes : dict, optional
        Dicionário de classificações e categorias.
        As chaves do dicionário devem ser o código da classificação.
        Os valores do dicionário devem ser:
            - 'all': Todas as categorias desta classificação;
            - 'allxt': Todas as categorias, exceto as totais;
            - list: Lista de categorias desejadas;
            - int: Uma categoria específica.
    ufs_extintas : bool, default=False
        Se True, adiciona as UFs extintas (se disponível na tabela).
            - 20: Fernando de Noronha
            - 34: Guanabara
    decimais : int, optional
        Número de fixo de casas decimais do resultado, entre 0 e 9.
        Se None, utiliza o padrão de cada variável. 
    retorna : str, default='dataframe'
        Formato do dado retornado:
            - 'dataframe': Retorna um DataFrame Pandas;
            - 'json': Retorna um dicionário no formato json original;
            - 'url': Retorna a URL para consulta.

    Returns
    -------
    pandas.core.frame.DataFrame
        Se retorna='dataframe', retorna um DataFrame com os resultados.
    dict
        Se retorna='json', retorna um dicionário no formato json original.
    str
        Se retorna='url', retorna a URL para consulta.

    """

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

    df = pd.DataFrame(data[1:])
    df.columns = data[0].values()
    return df



def referencias(
        cod: str,
        index: bool = False
    ) -> pd.DataFrame:
    """Obtém uma base de códigos para utilizar como argumento na busca do SIDRA.

    Parameters
    ----------
    cod : {'A', 'C', 'N', 'P', 'E', 'V'}
        - 'A': Assuntos;
        - 'C': Classificações;
        - 'N': Níveis geográficos;
        - 'P': Períodos;
        - 'E': Periodicidades;
        - 'V': Variáveis.
    index: bool, default=False
        Defina True caso o campo 'id' deva ser o index do DataFrame.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo todas as referências do código pesquisado.

    Raises
    ------
    ValueError
        Caso o código da referência seja inválido.

    Examples
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

    """

    cod = cod.lower()
    if cod in ('a', 'assuntos'):
        s = 'A'
    elif cod in ('c', 'classificacoes'):
        s = 'C'
    elif cod in ('n', 't', 'niveis', 'territorios'):
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
    df = pd.DataFrame(data)

    if index:
        df.set_index('id', inplace=True)
    
    return df
