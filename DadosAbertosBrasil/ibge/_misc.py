"""Submódulo IBGE contendo funções diversas.

Este submódulo é importado automaticamente com o módulo `ibge`.

>>> from DadosAbertosBrasil import ibge

"""

from typing import Literal, Optional

import pandas as pd
from pydantic import validate_call, PositiveInt
import requests

from DadosAbertosBrasil._utils import parse
from DadosAbertosBrasil._utils.errors import DAB_LocalidadeError
from DadosAbertosBrasil._utils.get_data import get_data


@validate_call
def populacao(
    projecao: Optional[
        Literal["populacao", "nascimento", "obito", "incremento"]
    ] = None,
    localidade: Optional[PositiveInt] = None,
) -> dict | int:
    """Obtém a projecao da população referente ao Brasil.

    Parameters
    ----------
    projecao : {'populacao', 'nascimento', 'obito', 'incremento'}, optional
        - 'populacao' obtém o valor projetado da população total da localidade;
        - 'nascimento' obtém o valor projetado de nascimentos da localidade
        - 'obito' obtém o valor projetado de óbitos da localidade;
        - 'incremento' obtém o incremento populacional projetado.
        - None obtém um dicionário com todos os valores anteriores.
    localidade : int, optional
        Código da localidade desejada.
        Por padrão, obtém os valores do Brasil. Utilize a função
        `ibge.localidades` para identificar a localidade desejada.

    Returns
    -------
    dict
        Dicionário de projeções.
    int
        Valor projetado para o indicador escolhido.

    Raises
    ------
    DAB_LocalidadeError
        Caso código da localidade seja inválido.
    ValueError
        Caso o argumento `projecao` seja inválido.

    Examples
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

    """

    localidade = parse.localidade(localidade, "")
    query = f"https://servicodados.ibge.gov.br/api/v1/projecoes/populacao/{localidade}"

    r = requests.get(query).json()

    if projecao is None:
        return r
    elif projecao == "populacao":
        return r["projecao"]["populacao"]
    elif projecao == "nascimento":
        return r["projecao"]["periodoMedio"]["nascimento"]
    elif projecao == "obito":
        return r["projecao"]["periodoMedio"]["obito"]
    elif projecao == "incremento":
        return r["projecao"]["periodoMedio"]["incrementoPopulacional"]
    else:
        raise ValueError(
            """O argumento 'projecao' deve ser um dos seguintes valores tipo string:
            - 'populacao';
            - 'nascimento';
            - 'obito';
            - 'incremento'."""
        )


@validate_call
def localidades(
    nivel: str = "distritos",
    divisoes: Optional[str] = None,
    localidade: PositiveInt | str | list = None,
    ordenar_por: Optional[str] = None,
    index: bool = False,
) -> pd.DataFrame:
    """Obtém o conjunto de localidades do Brasil e suas intrarregiões.

    Parameters
    ----------
    nivel : str, default='distritos'
        Nível geográfico dos dados.
    divisoes : str, optional
        Subdiviões intrarregionais do nível.
        Se None, captura todos os registros do `nivel`.
    localidade : int or str or list, optional
        ID (os lista de IDs) da localidade que filtrará o `nivel`.
    ordenar_por : str, optional
        Coluna pela qual a tabela será ordenada.
    index : bool, default=False
        Se True, defina a coluna 'id' como index do DataFrame.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo os localidades desejadas.

    Raises
    ------
    DAB_LocalidadeError
        Caso o nível geográfico seja inválido.

    Examples
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

    References
    ----------
    .. [1] https://servicodados.ibge.gov.br/api/docs/localidades

    """

    NIVEIS = {
        "distritos",
        "estados",
        "mesorregioes",
        "microrregioes",
        "municipios",
        "regioes-imediatas",
        "regioes-intermediarias",
        "regioes",
        "paises",
    }

    nivel = nivel.lower()
    if nivel not in NIVEIS:
        raise DAB_LocalidadeError(
            f"""Nível inválido:
        Preencha o argumento `nivel` com um dos seguintes valores:
        {NIVEIS}"""
        )

    path = ["localidades", nivel]
    params = {}

    if localidade is not None:
        if isinstance(localidade, list):
            localidade = "|".join([str(loc) for loc in localidade])
        path.append(localidade)

    if divisoes is not None:
        divisoes = divisoes.lower()
        if divisoes not in NIVEIS:
            raise DAB_LocalidadeError(
                f"""Subdivisões inválida:
            Preencha o argumento `divisoes` com um dos seguintes valores:
            {NIVEIS}"""
            )
        if nivel != divisoes:
            path.append(divisoes)

    if ordenar_por is not None:
        params["orderBy"] = ordenar_por

    data = get_data(
        endpoint="https://servicodados.ibge.gov.br/api/v1/", path=path, params=params
    )

    df = pd.json_normalize(data)

    def _loc_columns(x: str) -> str:
        y = x.replace("-", "_").split(".")
        return f"{y[-2]}_{y[-1]}" if len(y) > 1 else y[0]

    df.columns = df.columns.map(_loc_columns)
    df = df.loc[:, ~df.columns.duplicated()]

    if index:
        df.set_index("id", inplace=True)

    return df


@validate_call
def malha(
    localidade: PositiveInt,
    nivel: str = "estados",
    divisoes: Optional[str] = None,
    periodo: PositiveInt = 2020,
    formato: Literal["svg", "json", "geojson"] = "geojson",
    qualidade: Literal["minima", "intermediaria", "maxima"] = "minima",
) -> str | dict:
    """Obtém a URL para a malha referente ao identificador da localidade.

    Parameters
    ----------
    localidade : int, optional
        Código da localidade desejada.
        Utilize a função `ibge.localidades` para identificar a localidade.
    nivel : str, default='estados'
        Nível geográfico dos dados.
    divisoes : str, optional
        Subdiviões intrarregionais do nível.
        Se None, apresenta a malha sem subdivisões.
    periodo : int, default=2020
        Ano da revisão da malha.
    formato : {'svg', 'json', 'geojson'}, default='svg'
        Formato dos dados da malha.
    qualidade : {'minima', 'intermediaria', 'maxima'}, default='minima'
        Qualidade de imagem da malha.

    Returns
    -------
    str
        Se formato='svg', retorna a URL da malha da localidade desejada.
    dict
        Se formato='json', retorna a malha em formato TopoJSON.
    dict
        Se formato='geojson', retorna a malha em formato GeoJSON.

    Raises
    ------
    DAB_LocalidadeError
        Caso o nível geográfico seja inválido.

    References
    ----------
    .. [1] https://servicodados.ibge.gov.br/api/docs/malhas?versao=3

    Examples
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

    """

    FORMATOS = {
        "svg": "image/svg+xml",
        "geojson": "application/vnd.geo+json",
        "json": "application/json",
    }

    NIVEIS = {
        "estados",
        "mesorregioes",
        "microrregioes",
        "municipios",
        "regioes-imediatas",
        "regioes-intermediarias",
        "regioes",
        "paises",
    }

    DIVISOES = {
        "uf",
        "mesorregiao",
        "microrregiao",
        "municipio",
        "regiao-imediata",
        "regiao-intermediaria",
        "regiao",
    }

    nivel = nivel.lower()
    if nivel not in NIVEIS:
        raise DAB_LocalidadeError(
            f"""Nível inválido:
        Preencha o argumento `nivel` com um dos seguintes valores:
        {NIVEIS}"""
        )

    path = ["malhas", nivel, localidade]

    params = {
        "periodo": periodo,
        "qualidade": qualidade,
        "formato": FORMATOS[formato],
    }

    if divisoes is not None:
        divisoes = divisoes.lower()
        if divisoes not in DIVISOES:
            raise DAB_LocalidadeError(
                f"""Subdivisões inválida:
            Preencha o argumento `divisoes` com um dos seguintes valores:
            {DIVISOES}"""
            )
        if nivel != divisoes:
            params["intrarregiao"] = divisoes

    url = "https://servicodados.ibge.gov.br/api/v3/"
    url += "/".join([str(p) for p in path])

    data = requests.get(url=url, params=params)

    if formato.lower().endswith("json"):
        return data.json()
    else:
        return data.url


def coordenadas() -> pd.DataFrame:
    """Obtém as coordenadas de todas as localidades brasileiras, incluindo
    latitude, longitude e altitude.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame das coordenadas de todas as localidade brasileiras.

    Examples
    --------
    >>> ibge.coordenadas()
           GM_PONTO     ID     CD_GEOCODIGO    TIPO   CD_GEOCODBA NM_BAIRRO  ...
    0           NaN      1  110001505000001  URBANO  1.100015e+11   Redondo  ...
    1           NaN      2  110001515000001  URBANO           NaN       NaN  ...
    2           NaN      3  110001520000001  URBANO           NaN       NaN  ...
    3           NaN      4  110001525000001  URBANO           NaN       NaN  ...
    4           NaN      5  110001530000001  URBANO           NaN       NaN  ...
    ..          ...     ..              ...     ...           ...       ...  ...

    """

    return pd.read_csv(
        r"https://raw.githubusercontent.com/GusFurtado/dab_assets/main/data/coordenadas.csv",
        sep=";",
    )
