'''Submódulo IBGE contendo funções diversas.

Este submódulo é importado automaticamente com o módulo `ibge`.

>>> from DadosAbertosBrasil import ibge

'''
from typing import Union

import pandas as _pd
import requests

from DadosAbertosBrasil._utils import parse
from DadosAbertosBrasil._utils.errors import DAB_LocalidadeError
from DadosAbertosBrasil._utils.get_data import get_data



_normalize = _pd.io.json.json_normalize \
    if _pd.__version__[0] == '0' else _pd.json_normalize



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



def localidades(
        nivel: str = 'distritos',
        divisoes: str = None,
        localidade: Union[int, str, list] = None,
        ordenar_por: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''Obtém o conjunto de localidades do Brasil e suas intrarregiões.

    Parameters
    ----------
    nivel : str (default='distritos')
        Nível geográfico dos dados.
    divisoes : str (default=None)
        Subdiviões intrarregionais do nível.
        Se None, captura todos os registros do `nivel`.
    localidade : int | str | list (default=None)
        ID (os lista de IDs) da localidade que filtrará o `nivel`.
    ordenar_por : str (default=None)
        Coluna pela qual a tabela será ordenada.
    index : bool (default=False)
        Se True, defina a coluna 'id' como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os localidades desejadas.

    Erros
    -----
    DAB_LocalidadeError
        Caso o nível geográfico seja inválido.

    Exemplos
    --------
    Captura todos os estados do Brasil

    >>> ibge.localidades(nivel='estados')
        id sigla                 nome  regiao_id regiao_sigla   regiao_nome
    0   11    RO             Rondônia          1            N         Norte
    1   12    AC                 Acre          1            N         Norte
    2   13    AM             Amazonas          1            N         Norte
    3   14    RR              Roraima          1            N         Norte
    4   15    PA                 Pará          1            N         Norte
    .. ...   ...                  ...        ...          ...           ...

    Captura todos os distritos do Brasil, colocando o ID como index.

    >>> ibge.localidades(index=True)
                              nome  municipio_id  ... regiao_sigla   regiao_nome
    id                                            ...                           
    520005005      Abadia de Goiás       5200050  ...           CO  Centro-Oeste
    310010405  Abadia dos Dourados       3100104  ...           SE       Sudeste
    520010005            Abadiânia       5200100  ...           CO  Centro-Oeste
    520010010       Posse d'Abadia       5200100  ...           CO  Centro-Oeste
    310020305               Abaeté       3100203  ...           SE       Sudeste
    ...                        ...           ...  ...          ...           ...

    Captura todos os municípios do estado do Rio de Janeiro (localidade=33)

    >>> ibge.localidades(nivel='estados', divisoes='municipios', localidade=33)
             id                nome  microrregiao_id           microrregiao_nome  \
    0   3300100      Angra dos Reis            33013         Baía da Ilha Grande   
    1   3300159             Aperibé            33002      Santo Antônio de Pádua   
    2   3300209            Araruama            33010                       Lagos   
    3   3300225               Areal            33005                   Três Rios   
    4   3300233  Armação dos Búzios            33010                       Lagos   
    ..      ...                 ...              ...                         ...

    Documentação original
    ---------------------
    https://servicodados.ibge.gov.br/api/docs/localidades

    '''

    NIVEIS = {
        'distritos',
        'estados',
        'mesorregioes',
        'microrregioes',
        'municipios',
        'regioes-imediatas',
        'regioes-intermediarias',
        'regioes',
        'paises'
    }

    nivel = nivel.lower()
    if nivel not in NIVEIS:
        raise DAB_LocalidadeError(f'''Nível inválido:
        Preencha o argumento `nivel` com um dos seguintes valores:
        {NIVEIS}''')

    path = ['localidades', nivel]
    params = {}

    if localidade is not None:
        if isinstance(localidade, list):
            localidade = '|'.join([str(loc) for loc in localidade])
        path.append(localidade)

    if divisoes is not None:
        divisoes = divisoes.lower()
        if divisoes not in NIVEIS:
            raise DAB_LocalidadeError(f'''Subdivisões inválida:
            Preencha o argumento `divisoes` com um dos seguintes valores:
            {NIVEIS}''')
        if nivel != divisoes:
            path.append(divisoes)
        
    if ordenar_por is not None:
        params['orderBy'] = ordenar_por
    
    data = get_data(
        endpoint = 'https://servicodados.ibge.gov.br/api/v1/',
        path = path,
        params = params
    )

    df = _normalize(data)

    def _loc_columns(x: str) -> str:
        y = x.replace('-', '_').split('.')
        return f'{y[-2]}_{y[-1]}' if len(y)>1 else y[0]
    df.columns = df.columns.map(_loc_columns)

    if index:
        df.set_index('id', inplace=True)
        
    return df



def malha(
        localidade: int,
        nivel: str = 'estados',
        divisoes: str = None,
        periodo: int = 2020,
        formato: str = 'svg',
        qualidade: str = 'maxima'
    ) -> _pd.DataFrame:
    '''Obtém a URL para a malha referente ao identificador da localidade.

    Parâmetros
    ----------
    localidade : int (default=None)
        Código da localidade desejada.
        Utilize a função `ibge.localidades` para identificar a localidade.
    nivel : str (default='estados')
        Nível geográfico dos dados.
    divisoes : str (default=None)
        Subdiviões intrarregionais do nível.
        Se None, apresenta a malha sem subdivisões.
    periodo : int (default=2020)
        Ano da revisão da malha.
    formato : str {'svg', 'json', 'geojson'} (default='svg')
        Formato dos dados da malha.
    qualidade : str {'minima', 'intermediaria', 'maxima'} (default='maxima')
        Qualidade de imagem da malha.

    Retorna
    -------
    str
        Se formato='svg', retorna a URL da malha da localidade desejada.
    json
        Se formato='json', retorna a malha em formato TopoJSON.
    geojson
        Se formato='geojson', retorna a malha em formato GeoJSON.

    Erros
    -----
    DAB_LocalidadeError
        Caso o nível geográfico seja inválido.

    Exemplos
    --------
    Captura a malha do Distrito Federal (localidade=53) em formato GeoJSON.

    >>> ibge.malha(localidade=53, formato='geojson')
    {'type': 'FeatureCollection',
        'features': [{'type': 'Feature',
            'geometry': {'type': 'Polygon',
                'coordinates': [[[-47.31, -16.0363], ...

    Captura a malha de Joinville em formato SVG com qualidade mínima.

    >>> ibge.malha(
    ...     nivel = 'municipios',
    ...     localidade = 4209102,
    ...     formato = 'svg',
    ...     qualidade = 'minima'
    ... )
    'https://servicodados.ibge.gov.br/api/v3/malhas/municipios/4209102?...'

    Captura a malha do Brasil subdividido por UF em formato TopoJSON.

    >>> ibge.malha(
    ...     nivel = 'paises',
    ...     localidade = 'BR',
    ...     divisoes = 'uf',
    ...     formato = 'json'
    ... )
    {'type': 'Topology',
        'arcs': [[[32967, 111009], [-821, 372]],
            [[32146, 111381],
            [133, 124],
            [15, 106], ...

    Documentação original
    ---------------------
    https://servicodados.ibge.gov.br/api/docs/malhas?versao=3

    '''

    FORMATOS = {
        'svg': 'image/svg+xml',
        'geojson': 'application/vnd.geo+json',
        'json': 'application/json'
    }

    NIVEIS = {
        'estados',
        'mesorregioes',
        'microrregioes',
        'municipios',
        'regioes-imediatas',
        'regioes-intermediarias',
        'regioes',
        'paises'    
    }

    DIVISOES = {
        'uf',
        'mesorregiao',
        'microrregiao',
        'municipio',
        'regiao-imediata',
        'regiao-intermediaria',
        'regiao'
    }

    nivel = nivel.lower()
    if nivel not in NIVEIS:
        raise DAB_LocalidadeError(f'''Nível inválido:
        Preencha o argumento `nivel` com um dos seguintes valores:
        {NIVEIS}''')

    path = ['malhas', nivel, localidade]

    params = {
        'periodo': periodo,
        'qualidade': qualidade.lower(),
        'formato': FORMATOS[formato.lower()]
    }

    if divisoes is not None:
        divisoes = divisoes.lower()
        if divisoes not in DIVISOES:
            raise DAB_LocalidadeError(f'''Subdivisões inválida:
            Preencha o argumento `divisoes` com um dos seguintes valores:
            {DIVISOES}''')
        if nivel != divisoes:
            params['intrarregiao'] = divisoes

    url = 'https://servicodados.ibge.gov.br/api/v3/'
    url += '/'.join([str(p) for p in path])

    data = requests.get(
        url = url,
        params = params
    )
    
    if formato.lower().endswith('json'):
        return data.json()
    else:
        return data.url



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

    return _pd.read_csv(
        r'https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/data/coordenadas.csv',
        sep = ';'
    )
