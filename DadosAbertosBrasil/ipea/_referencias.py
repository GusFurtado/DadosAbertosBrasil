
from typing import Any, Literal, overload

from pydantic import Field, PositiveInt, validate_call

from ..utils.modelos import Params, com_params
from ..utils.requisicao import Requisicao
from ..utils.saida import consultar
from ..utils.typing import DataFramePandas, DataFramePolars, Formato, Saida
from . import modelos as m


class _ParamsTemas(Params):
    cod: PositiveInt | None = Field(None, exclude=True)
    pai: PositiveInt | None = Field(None, exclude=True)


class _ParamsPaises(Params):
    cod: str | None = Field(None, exclude=True)


class _ParamsTerritorios(Params):
    capital: bool | None = Field(None, exclude=True)
    amc: bool | None = Field(None, exclude=True)
    cod: int | None = Field(None, exclude=True)
    nivel: str | None = Field(None, exclude=True)


def _ipea(path: str, verificar_certificado: bool | None) -> Requisicao:
    return Requisicao("ipea", [path], chaves=["value"], verificar_certificado=verificar_certificado, cacheavel=True)


@overload
def lista_temas(
    cod: PositiveInt | None = ...,
    pai: PositiveInt | None = ...,
    index: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def lista_temas(
    cod: PositiveInt | None = ...,
    pai: PositiveInt | None = ...,
    index: bool = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def lista_temas(
    cod: PositiveInt | None = ...,
    pai: PositiveInt | None = ...,
    index: bool = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.Tema]: ...


@overload
def lista_temas(
    cod: PositiveInt | None = ...,
    pai: PositiveInt | None = ...,
    index: bool = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def lista_temas(
    cod: PositiveInt | None = ...,
    pai: PositiveInt | None = ...,
    index: bool = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def lista_temas(
    cod: PositiveInt | None = ...,
    pai: PositiveInt | None = ...,
    index: bool = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsTemas)
def lista_temas(
    cod: PositiveInt | None = None,
    pai: PositiveInt | None = None,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Registros de todos os temas cadastrados.

    Parameters
    ----------
    cod : int, optional
        Código do tema, caso queira ver os dados deste tema exclusivamente.

    pai : int, optional
        Filtrar temas por código pai.

    index : bool, default=False
        Se True, define a coluna 'codigo' como index do DataFrame.
        Só se aplica ao formato 'pandas'; com 'polars', é ignorado com aviso.

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": JSON original da API, como veio;
        - "pydantic": lista de modelos Pydantic, um por registro;
        - "pandas": DataFrame pandas;
        - "polars": DataFrame polars;
        - "url": endereço da consulta.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
        Registros de todos os temas das séries do IPEA.

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

    _ParamsTemas.de_locais(locals())
    return consultar(
        _ipea("Temas" if cod is None else f"Temas({cod})", verificar_certificado),
        m.Tema,
        formato,
        index=index,
        filtro=None if pai is None else (lambda tema: tema.pai == pai),
    )


@overload
def lista_paises(
    cod: str | None = ...,
    index: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def lista_paises(
    cod: str | None = ..., index: bool = ..., *, formato: Literal["json"], verificar_certificado: bool | None = ...
) -> list[dict[str, Any]]: ...


@overload
def lista_paises(
    cod: str | None = ..., index: bool = ..., *, formato: Literal["pydantic"], verificar_certificado: bool | None = ...
) -> list[m.Pais]: ...


@overload
def lista_paises(
    cod: str | None = ..., index: bool = ..., *, formato: Literal["pandas"], verificar_certificado: bool | None = ...
) -> DataFramePandas: ...


@overload
def lista_paises(
    cod: str | None = ..., index: bool = ..., *, formato: Literal["polars"], verificar_certificado: bool | None = ...
) -> DataFramePolars: ...


@overload
def lista_paises(
    cod: str | None = ..., index: bool = ..., *, formato: Literal["url"], verificar_certificado: bool | None = ...
) -> str: ...


@validate_call
@com_params(_ParamsPaises)
def lista_paises(
    cod: str | None = None,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Registros de todos os países cadastrados.

    Parameters
    ----------
    cod : str, optional
        Sigla de três letras do país, caso queira ver os dados deste
        país exclusivamente.

    index : bool, default=False
        Se True, define a coluna 'codigo' como index do DataFrame.
        Só se aplica ao formato 'pandas'; com 'polars', é ignorado com aviso.

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": JSON original da API, como veio;
        - "pydantic": lista de modelos Pydantic, um por registro;
        - "pandas": DataFrame pandas;
        - "polars": DataFrame polars;
        - "url": endereço da consulta.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
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

    _ParamsPaises.de_locais(locals())
    return consultar(
        _ipea("Paises" if cod is None else f"Paises('{cod.upper()}')", verificar_certificado),
        m.Pais,
        formato,
        index=index,
    )


@overload
def lista_territorios(
    capital: bool | None = ...,
    amc: bool | None = ...,
    cod: int | None = ...,
    nivel: str | None = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def lista_territorios(
    capital: bool | None = ...,
    amc: bool | None = ...,
    cod: int | None = ...,
    nivel: str | None = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def lista_territorios(
    capital: bool | None = ...,
    amc: bool | None = ...,
    cod: int | None = ...,
    nivel: str | None = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.Territorio]: ...


@overload
def lista_territorios(
    capital: bool | None = ...,
    amc: bool | None = ...,
    cod: int | None = ...,
    nivel: str | None = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def lista_territorios(
    capital: bool | None = ...,
    amc: bool | None = ...,
    cod: int | None = ...,
    nivel: str | None = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def lista_territorios(
    capital: bool | None = ...,
    amc: bool | None = ...,
    cod: int | None = ...,
    nivel: str | None = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsTerritorios)
def lista_territorios(
    capital: bool | None = None,
    amc: bool | None = None,
    cod: int | None = None,
    nivel: str | None = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
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
    
    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": JSON original da API, como veio;
        - "pydantic": lista de modelos Pydantic, um por registro;
        - "pandas": DataFrame pandas;
        - "polars": DataFrame polars;
        - "url": endereço da consulta.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
        Registros de todos os territórios das séries do IPEA.

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

    _ParamsTerritorios.de_locais(locals())
    if (cod is None) or (nivel is None):
        path = "Territorios"
    else:
        n = "Municipios" if nivel == "Municípios" else nivel
        path = f"Territorios(TERCODIGO='{cod}',NIVNOME='{n}')"

    def filtro(territorio: m.Territorio) -> bool:
        if capital is not None and territorio.capital != capital:
            return False
        return amc is None or territorio.amc == amc

    return consultar(_ipea(path, verificar_certificado), m.Territorio, formato, filtro=filtro)


def lista_niveis() -> list[str]:
    """Lista dos possíveis níveis territoriais.

    Returns
    -------
    list[str]
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
