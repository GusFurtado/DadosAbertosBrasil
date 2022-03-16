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



# Retrocompatibilidade com pandas v0.x
_normalize = pd.io.json.json_normalize \
    if pd.__version__[0] == '0' else pd.json_normalize



def lista_tabelas(
        contendo: Optional[str] = None,
        excluindo: Optional[str] = None,
        assunto: Optional[Union[int, str]] = None,
        classificacao: Optional[Union[int, str]] = None,
        periodo: Optional[Union[dict, str]] = None,
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
        Busque apenas as tabelas referentes ao assunto desejado.
        Os assuntos são identificados por um código numérico e podem ser
        obtidos com auxílio da função `ibge.referencias('a')`.
        Exemplo: O assunto "Abate de Animais" possui o código 70, portanto
        pesquise por tabelas deste assunto pelo argumento `assunto=70`.
    classificacao : str | int, optional
        Busque apenas as tabelas referentes à classificação desejada.
        As classificações são identificadas por um código numérico e podem ser
        obtidas com auxílio da função `ibge.referencias('c')`.
        Exemplo: A classificação "Agricultura familiar" possui o código 12896,
        portanto pesquise por tabelas contendo essa classificação através do
        argumento `classificacao=12896`. 
    periodo : dict | str, optional
        Busque apenas as tabelas referentes ao período desejado.
        Os períodos devem ser um dicionário no formato `{periodicidade:periodo}`
        ou um string no formato `'Px[xxxxxx]'`.
        Exemplo: `{5: 202001}` ou `'P5[202001]'`. Obtém as pesquisas cujos
        agregados disponibilizam resultados para o mês (P5) de janeiro de
        2020 (202001). Observe que é necessário informar a periodicidade (P5),
        devido a períodos que compartilham o mesmo identificador - 202001 pode
        significar o mês de Janeiro de 2020, o primeiro trimestre de 2020 ou
        ainda o primeiro semestre de 2020.
        A função `ibge.referencias('p')` retorna todos os períodos disponíveis.
    periodicidade : str | int, optional
        Busque apenas as tabelas que contém essa periodicidade de divulgação.
        Utilize a função `ibge.referencias('e')` para encontrar o código.
        Exemplo: A periodicidade "mensal" possui o código 5, portanto pesquise
        por tabelas de periodicidade mensal através do argumento
        `periodicidade=5`.
    nivel : str | int, optional
        Busque apenas as tabelas disponíveis neste nível geográfico.
        Utilize a função `ibge.referencias('n')` para encontrar o código.
        Exemplo: O nível "Município" possui o código 6, portanto pesquise por
        tabelas contendo esse nível geográfico através do argumento `nivel=6`.
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
    Forma mais simples da função. Retorna todas as tabelas.

    >>> ibge.lista_tabelas()    

    Listas tabelas cujo assunto é "Trabalho" (17), com periodicidade
    trimestral (9) a um nível geográfico municipal (6) contendo classificação
    por grupo de idade (58).

    >>> ibge.lista_tabelas(
    ...     assunto = 17,
    ...     periodicidade = 9,
    ...     nivel = 6,
    ...     classificacao = 58
    ... )

    Listar tabelas do Censo Demográfico (pesquisa 'CD'), contendo o termo
    'rendimento' no título, porém não contendo 'Distribuição', definindo a
    coluna `tabela_id` como index do DataFrame.

    >>> ibge.lista_tabelas(
    ...     pesquisa = 'CD',
    ...     contendo = 'rendimento',
    ...     excluindo = 'distribuição',
    ...     index = True
    ... )

    Buscar por tabelas que contenham o IPCA de Dezembro de 2019 (P5[201912]).

    >>> ibge.lista_tabelas(
    ...     contendo = 'ipca',
    ...     periodo = {5: 201912}
    ... )

    """

    params = {}

    def parse_periodicidade(p):
        if isinstance(p, int) or isinstance(p, float):
            p = f'P{int(p)}'
        return p.upper()

    if assunto is not None:
        params['assunto'] = assunto

    if classificacao is not None:
        params['classificacao'] = classificacao

    if periodo is not None:
        if isinstance(periodo, dict):
            for p in periodo:
                periodo = f'{parse_periodicidade(p)}[{[periodo[p]]}]'
        params['periodo'] = periodo

    if periodicidade is not None:
        params['periodicidade'] = parse_periodicidade(periodicidade)

    if nivel is not None:
        if isinstance(nivel, int):
            nivel = f'N{nivel}'
        params['nivel'] = nivel.upper()

    data = get_data(
        endpoint = 'https://servicodados.ibge.gov.br/api/v3/',
        path = ['agregados'],
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
        endpoint = 'https://servicodados.ibge.gov.br/api/v3/',
        path = ['agregados']
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
            endpoint = 'https://servicodados.ibge.gov.br/api/v3/',
            path = ['agregados', tabela, 'metadados']
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
    path += f'/u/{u}/d/{decimais or "s"}'

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
        Defina True caso o campo 'cod' deva ser o index do DataFrame.

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
         cod                                    referencia
    0    148                         Abastecimento de água
    1     70                              Abate de animais
    2    110                Acesso a esgotamento sanitário
    3    147                             Acesso à internet
    4    107  Acesso a serviço de coleta de lixo doméstico
    ..    ..                                            ..

    Lista classificações usando o `cod` da classificação como index
    do DataFrame.
    
    >>> ibge.referencias('c', index=True)
                                                  referencia
    cod                                                      
    588    Acessibilidade possível na maior parte das via...
    957    Acesso à Internet por telefone móvel celular p...
    681                    Acesso a televisão por assinatura
    12236                               Adequação da moradia
    806                      Adubação, calagem e agrotóxicos
    ...                                                  ...

    """

    try:
        s = cod.lower()
        if s.endswith('s'):
            s = s[:-1]
        s = {
            'a': 'A',
            'assunto': 'A',
            'c': 'C',
            'classificacao': 'C',
            'classificacoe': 'C',
            'n': 'N',
            'nivel': 'N',
            'nivei': 'N',
            't': 'T',
            'territorio': 'T',
            'p': 'P',
            'periodo': 'P',
            'e': 'E',
            'periodicidade': 'E',
            'v': 'V',
            'variavel': 'V',
            'variavei': 'V'
        }[s]

    except AttributeError:
        raise TypeError('Código da referência `cod` deve ser do tipo `str`.')

    except KeyError:
        raise KeyError(f"Código de referência '{cod}' inválido.")
        
    data = get_data(
        endpoint = r'https://servicodados.ibge.gov.br/api/v3/',
        path = ['agregados'],
        params = {'acervo': s}
    )
    df = pd.DataFrame(data)
    df.columns = ['cod', 'referencia']

    if index:
        df.set_index('cod', inplace=True)
    
    return df
