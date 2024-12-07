from typing import Optional

import pandas as pd
from pydantic import validate_call, PositiveInt

from ._utils import get_ipea_data


_RENOMEAR_COLUNAS = {
    "TEMCODIGO": "codigo",
    "TEMCODIGO_PAI": "pai",
    "TEMNOME": "nome",
    "NIVNOME": "nivel",
    "TERCODIGO": "codigo",
    "TERNOME": "nome",
    "TERNOMEPADRAO": "nome_padrao",
    "TERCAPITAL": "capital",
    "TERAREA": "area",
    "NIVAMC": "amc",
    "PAICODIGO": "codigo",
    "PAINOME": "nome",
}


@validate_call
def lista_temas(
    cod: Optional[PositiveInt] = None,
    pai: Optional[PositiveInt] = None,
    index: bool = False,
) -> pd.DataFrame:
    """Registros de todos os temas cadastrados.

    Parameters
    ----------
    cod : int, optional
        Código do tema, caso queira ver os dados deste tema exclusivamente.
    pai : int, optional
        Filtrar temas por código pai.
    index : bool, default=False
        Se True, define a coluna 'codigo' como index do DataFrame.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo um registro de todos os temas das séries do IPEA.

    Examples
    --------
    Busca todos os temas.

    >>> ipea.lista_temas()
           codigo            pai                     nome
    0          28            NaN             Agropecuária
    1          23            NaN       Assistência social
    2          10            NaN    Balanço de pagamentos
    3           7            NaN                   Câmbio
    4           5            NaN        Comércio exterior
    ..        ...            ...                      ...

    Busca todos os subtemas do código 18.

    >>> ipea.lista_temas(pai=18)
           codigo            pai               nome
    11         54           18.0  Deputado Estadual
    12         55           18.0   Deputado Federal
    16         63           18.0         Eleitorado
    22         56           18.0         Governador
    ..        ...            ...                ...

    Utilize o argumento `index=True` para colocar a coluna 'codigo'
    como index do DataFrame.

    >>> ipea.lista_temas(index=True)
                         pai                     nome
    codigo
    28                   NaN             Agropecuária
    23                   NaN       Assistência social
    10                   NaN    Balanço de pagamentos
    7                    NaN                   Câmbio
    5                    NaN        Comércio exterior
    ...                  ...                      ...

    """

    if cod is None:
        df = get_ipea_data("Temas")
    else:
        df = get_ipea_data(f"Temas({cod})")
    df.rename(columns=_RENOMEAR_COLUNAS, inplace=True)

    if pai is not None:
        df = df[df["pai"] == pai]

    if index:
        df.set_index("codigo", inplace=True)

    return df


@validate_call
def lista_paises(cod: Optional[str] = None, index: bool = False) -> pd.DataFrame:
    """Registros de todos os países cadastrados.

    Parameters
    ----------
    cod : str, optional
        Sigla de três letras do país, caso queira ver os dados deste
        país exclusivamente.
    index : bool, default=False
        Se True, define a coluna 'codigo' como index do DataFrame.

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo um registro de todos os países das séries do IPEA.

    Examples
    --------
    Forma mais simples da função.

    >>> ipea.lista_paises()
          codigo             nome
    0        AFG      Afeganistão
    1        ZAF    África do Sul
    2        DEU         Alemanha
    3       LATI   América Latina
    4        AGO           Angola
    ..       ...              ...

    Utilize o argumento `index=True` para colocar a coluna `codigo`
    como index do DataFrame.

    >>> ipea.lista_paises(index=True)
                          nome
    codigo
    AFG            Afeganistão
    ZAF          África do Sul
    DEU               Alemanha
    LATI        América Latina
    AGO                 Angola
    ...                    ...

    """

    if cod is None:
        df = get_ipea_data("Paises")
    elif isinstance(cod, str):
        df = get_ipea_data(f"Paises('{cod.upper()}')")
    df.rename(columns=_RENOMEAR_COLUNAS, inplace=True)

    if index:
        df.set_index("codigo", inplace=True)

    return df


@validate_call
def lista_territorios(
    capital: Optional[bool] = None,
    amc: Optional[bool] = None,
    cod: Optional[int] = None,
    nivel: Optional[str] = None,
) -> pd.DataFrame:
    """Registros de todos os territórios brasileiros cadastrados.

    Parameters
    ----------
    capital : bool, optional
        Se True, retorna apenas territórios que são capitais.
        Se False, retorna apenas territórios que não são capitais.
        Se None, retorna todos os territórios.
    amc : bool, optional
        Se True, retorna apenas territórios que são AMC.
        Se False, retorna apenas territórios que não são AMC.
        Se None, retorna todos os territórios.
    cod : int, optional
        Código do território, caso queira ver os dados deste
        território exclusivamente.
    nivel : str, optional
        Nome do nível territorial.
        Utilize a função `ipea.niveis_territoriais` para verificar
        as opções disponíveis.
    
    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo o registro de todos os territórios
        das séries do IPEA.

    Notes
    -----
    O número de municípios brasileiros aumentou de 3.951 em 1970 para 5.507
    em 2000. As mudanças nos contornos e áreas geográficas dos municípios
    devidas à criação de novos municípios impedem comparações intertemporais
    consistentes de variáveis demográficas, econômicas e sociais em nível
    municipal. Para isso, é necessário agregar municípios em "Áreas Mínimas
    Comparáveis" (AMC). Acesse o "Dicionário de Conceitos" do IPEA para mais
    informações.

    Examples
    --------
    Buscar todos os territórios.

    >>> ipea.lista_territorios()
             nivel     codigo                   nome  ...  \
    0                                 (não definido)  ...
    1       Brasil          0                 Brasil  ...
    2      Regiões          1           Região Norte  ...
    3      Estados         11               Rondônia  ...
    4   Municípios    1100015  Alta Floresta D'Oeste  ...
    ..         ...        ...                    ...  ...

    Buscar apenas capitais.

    >>> ipea.lista_territorios(capital=True)
                nivel   codigo            nome     nome_padrao capital  ...  \
    26     Municípios  1100205     Porto Velho     PORTO VELHO    True  ...   
    109    Municípios  1200401      Rio Branco      RIO BRANCO    True  ...   
    263    Municípios  1302603          Manaus          MANAUS    True  ...   
    360    Municípios  1400100       Boa Vista       BOA VISTA    True  ...
    ...           ...      ...             ...             ...     ...  ...

    """

    if (cod is None) or (nivel is None):
        df = get_ipea_data("Territorios")
    else:
        n = "Municipios" if nivel == "Municípios" else nivel
        df = get_ipea_data(f"Territorios(TERCODIGO='{cod}',NIVNOME='{n}')")
    df.rename(columns=_RENOMEAR_COLUNAS, inplace=True)

    if capital is not None:
        df = df[df["capital"] == capital]

    if amc is not None:
        df = df[df["amc"] == amc]

    return df


def lista_niveis() -> list[str]:
    """Lista dos possíveis níveis territoriais.

    Returns
    -------
    list of str
        Lista de todos os níveis territoriais das séries do IPEA.

    Examples
    --------
    >>> ipea.lista_niveis()
    ['Brasil', 'Regiões', ... , 'AMC 70-00', 'Outros Países']

    """

    return [
        "Brasil",
        "Regiões",
        "Estados",
        "Microrregiões",
        "Mesorregiões",
        "Municípios",
        "Municípios por bacia",
        "Área metropolitana",
        "Estado/RM",
        "AMC 20-00",
        "AMC 40-00",
        "AMC 60-00",
        "AMC 1872-00",
        "AMC 91-00",
        "AMC 70-00",
        "Outros Países",
    ]
