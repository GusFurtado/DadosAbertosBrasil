from typing import Any, Literal, overload

from pydantic import Field, PositiveInt, validate_call

from ..utils import parse
from ..utils.errors import DABInputError, DABLocalidadeError, descontinuado, removida
from ..utils.modelos import Params, com_params, validar
from ..utils.requisicao import Requisicao
from ..utils.saida import resolver_formato, tabela
from ..utils.typing import DataFramePandas, DataFramePolars, Formato, NivelTerritorial, Saida
from . import modelos as m


class _ParamsLocalidades(Params):
    nivel: NivelTerritorial = Field(exclude=True)
    divisoes: NivelTerritorial | None = Field(None, exclude=True)
    localidade: PositiveInt | str | list[PositiveInt | str] | None = Field(None, exclude=True)
    ordenar_por: str | None = Field(None, serialization_alias="orderBy")


@validate_call
def populacao(
    projecao: Literal["populacao", "nascimento", "obito", "incremento"] | None = None,
    localidade: PositiveInt | None = None,
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
    DABLocalidadeError
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
    r = Requisicao("ibge", ["projecoes", "populacao", localidade]).json()

    if projecao is None:
        return r
    elif projecao == "populacao":
        return r["projecao"]["populacao"]
    elif projecao == "nascimento":
        return r["projecao"]["periodoMedio"]["nascimento"]
    elif projecao == "obito":
        return r["projecao"]["periodoMedio"]["obito"]
    else:
        return r["projecao"]["periodoMedio"]["incrementoPopulacional"]


@overload
def localidades(
    nivel: NivelTerritorial = ...,
    divisoes: NivelTerritorial | None = ...,
    localidade: PositiveInt | str | list[PositiveInt | str] = ...,
    ordenar_por: str | None = ...,
    index: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def localidades(
    nivel: NivelTerritorial = ...,
    divisoes: NivelTerritorial | None = ...,
    localidade: PositiveInt | str | list[PositiveInt | str] = ...,
    ordenar_por: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def localidades(
    nivel: NivelTerritorial = ...,
    divisoes: NivelTerritorial | None = ...,
    localidade: PositiveInt | str | list[PositiveInt | str] = ...,
    ordenar_por: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.Localidade]: ...


@overload
def localidades(
    nivel: NivelTerritorial = ...,
    divisoes: NivelTerritorial | None = ...,
    localidade: PositiveInt | str | list[PositiveInt | str] = ...,
    ordenar_por: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def localidades(
    nivel: NivelTerritorial = ...,
    divisoes: NivelTerritorial | None = ...,
    localidade: PositiveInt | str | list[PositiveInt | str] = ...,
    ordenar_por: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def localidades(
    nivel: NivelTerritorial = ...,
    divisoes: NivelTerritorial | None = ...,
    localidade: PositiveInt | str | list[PositiveInt | str] = ...,
    ordenar_por: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsLocalidades)
def localidades(
    nivel: NivelTerritorial = "distritos",
    divisoes: NivelTerritorial | None = None,
    localidade: PositiveInt | str | list[PositiveInt | str] = None,
    ordenar_por: str | None = None,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Obtém o conjunto de localidades do Brasil e suas intrarregiões.

    Parameters
    ----------
    nivel : str, default="distritos"
        Nível geográfico dos dados.

    divisoes : str, optional
        Subdiviões intrarregionais do nível.
        Se None, captura todos os registros do `nivel`.

    localidade : int | str | list[int|str], optional
        ID (os lista de IDs) da localidade que filtrará o `nivel`.

    ordenar_por : str, optional
        Coluna pela qual a tabela será ordenada.

    index : bool, default=False
        Se True, defina a coluna `"id"` como index do DataFrame.
        Ignorado com aviso se `formato` for 'polars'.

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
        Localidades desejadas.

    Raises
    ------
    DABLocalidadeError
        Caso o nível geográfico seja inválido.

    Examples
    --------
    Captura todos os estados do Brasil

    >>> ibge.localidades(nivel="estados")
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

    >>> ibge.localidades(nivel="estados", divisoes="municipios", localidade=33)
             id                nome  microrregiao_id           microrregiao_nome  \
    0   3300100      Angra dos Reis            33013         Baía da Ilha Grande   
    1   3300159             Aperibé            33002      Santo Antônio de Pádua   
    2   3300209            Araruama            33010                       Lagos   
    3   3300225               Areal            33005                   Três Rios   
    4   3300233  Armação dos Búzios            33010                       Lagos   
    ..      ...                 ...              ...                         ...

    Notes
    -----
    API original de códigos de localidades
        https://servicodados.ibge.gov.br/api/docs/localidades

    """

    params = _ParamsLocalidades.de_locais(locals())
    path = ["localidades", nivel]
    if localidade is not None:
        if isinstance(localidade, list):
            localidade = "|".join([str(loc) for loc in localidade])
        path.append(localidade)
    if (divisoes is not None) and (nivel != divisoes):
        path.append(divisoes)

    requisicao = Requisicao(
        "ibge", path, params.para_api(), verificar_certificado=verificar_certificado, cacheavel=True
    )
    formato = resolver_formato(formato)
    if formato == "url":
        return requisicao.url
    bruto = requisicao.bruto()
    if formato == "bruto":
        return bruto
    linhas = m.preparar_localidades(bruto)
    modelo = m.modelo_localidades(linhas)
    return tabela(validar(modelo, linhas), modelo, formato, index=index, index_col="id")


TipoMalha = Literal["geojson", "topojson", "svg"]

_TIPOS_MALHA = {
    "geojson": "application/vnd.geo+json",
    "topojson": "application/json",
    "svg": "image/svg+xml",
}

# `formato` do 2.x, que era o tipo de arquivo: valor antigo -> `tipo`.
_FORMATOS_ANTIGOS_MALHA = {"geojson": "geojson", "json": "topojson", "svg": "svg"}

_NIVEIS_MALHA = {
    "estados",
    "mesorregioes",
    "microrregioes",
    "municipios",
    "regioes-imediatas",
    "regioes-intermediarias",
    "regioes",
    "paises",
}

_DIVISOES_MALHA = {
    "uf",
    "mesorregiao",
    "microrregiao",
    "municipio",
    "regiao-imediata",
    "regiao-intermediaria",
    "regiao",
}


@validate_call
def malha(
    localidade: PositiveInt | str,
    nivel: str = "estados",
    divisoes: str | None = None,
    periodo: PositiveInt = 2020,
    tipo: TipoMalha = "geojson",
    qualidade: Literal["minima", "intermediaria", "maxima"] = "minima",
    formato: Literal["bruto", "url", "svg", "json", "geojson"] = "bruto",
    verificar_certificado: bool | None = None,
) -> dict[str, Any] | str:
    """Malha territorial de uma localidade, em GeoJSON, TopoJSON ou SVG.

    Parameters
    ----------
    localidade : int or str
        Código da localidade desejada, como `53` (Distrito Federal),
        `4209102` (Joinville) ou `'BR'` (Brasil, com `nivel='paises'`).
        Utilize a função `ibge.localidades` para identificar a localidade.

    nivel : str, default='estados'
        Nível geográfico da localidade: 'estados', 'mesorregioes',
        'microrregioes', 'municipios', 'regioes-imediatas',
        'regioes-intermediarias', 'regioes' ou 'paises'.

    divisoes : str, optional
        Subdivisões intrarregionais da malha: 'uf', 'mesorregiao',
        'microrregiao', 'municipio', 'regiao-imediata',
        'regiao-intermediaria' ou 'regiao'.
        Se None, apresenta a malha sem subdivisões.

    periodo : int, default=2020
        Ano da revisão da malha.

    tipo : {'geojson', 'topojson', 'svg'}, default='geojson'
        Tipo de arquivo da malha.

    qualidade : {'minima', 'intermediaria', 'maxima'}, default='minima'
        Qualidade (nível de detalhe) da malha.

    formato : {'bruto', 'url'}, default='bruto'
        - "bruto": o conteúdo da malha: `dict` para GeoJSON e TopoJSON, `str`
          com o SVG;
        - "url": endereço da malha.
        A malha não é uma tabela: `DadosAbertosBrasil.config.formato` não se
        aplica.

        !!! warning "Valores antigos"
            No 2.x, `formato` era o tipo de arquivo. `formato='geojson'`,
            `'json'` (TopoJSON) e `'svg'` (que retornava a URL) continuam
            funcionando com `DeprecationWarning` e deixam de existir em uma
            versão futura do 3.x. Use `tipo`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    dict
        Malha em GeoJSON ou TopoJSON, com `formato='bruto'`.
    str
        SVG da malha, com `tipo='svg'`, ou endereço da malha, com `formato='url'`.

    Raises
    ------
    DABLocalidadeError
        Caso o nível geográfico ou a subdivisão sejam inválidos.
    DABInputError
        Caso `tipo` e um valor antigo de `formato` peçam tipos diferentes.

    Notes
    -----
    API original das malhas territoriais
        https://servicodados.ibge.gov.br/api/docs/malhas?versao=3

    Examples
    --------
    Malha do Distrito Federal (localidade=53) em GeoJSON.

    >>> ibge.malha(localidade=53)
    {'type': 'FeatureCollection',
        'features': [{'type': 'Feature',
            'geometry': {'type': 'Polygon',
                'coordinates': [[[-47.31, -16.0363], ...

    Endereço da malha de Joinville em SVG.

    >>> ibge.malha(
    ...     nivel='municipios',
    ...     localidade=4209102,
    ...     tipo='svg',
    ...     formato='url',
    ... )
    'https://servicodados.ibge.gov.br/api/v3/malhas/municipios/4209102?...'

    Malha do Brasil subdividido por UF em TopoJSON.

    >>> ibge.malha(
    ...     nivel='paises',
    ...     localidade='BR',
    ...     divisoes='uf',
    ...     tipo='topojson',
    ... )
    {'type': 'Topology',
        'arcs': [[[32967, 111009], [-821, 372]], ...

    """

    url_antiga = False
    if formato in _FORMATOS_ANTIGOS_MALHA:
        antigo = _FORMATOS_ANTIGOS_MALHA[formato]
        if tipo != "geojson" and tipo != antigo:
            raise DABInputError(
                f"`formato={formato!r}` é o nome antigo de `tipo={antigo!r}` e conflita com `tipo={tipo!r}`. "
                "Use só `tipo`."
            )
        sugestao = f"`tipo={antigo!r}" + (", formato='url'`" if formato == "svg" else "`")
        descontinuado(
            f"Em `ibge.malha`, `formato={formato!r}` agora é {sugestao}: `formato` passou a ser "
            "'bruto' (conteúdo) ou 'url'."
        )
        tipo = antigo
        # No 2.x, `formato='svg'` retornava a URL.
        url_antiga = formato == "svg"

    nivel = nivel.lower()
    if nivel not in _NIVEIS_MALHA:
        raise DABLocalidadeError(
            f"Nível inválido. Preencha o argumento `nivel` com um dos seguintes valores: {sorted(_NIVEIS_MALHA)}"
        )

    params = {"periodo": periodo, "qualidade": qualidade, "formato": _TIPOS_MALHA[tipo]}
    if divisoes is not None:
        divisoes = divisoes.lower()
        if divisoes not in _DIVISOES_MALHA:
            raise DABLocalidadeError(
                "Subdivisão inválida. Preencha o argumento `divisoes` com um dos seguintes valores: "
                f"{sorted(_DIVISOES_MALHA)}"
            )
        if nivel != divisoes:
            params["intrarregiao"] = divisoes

    requisicao = Requisicao(
        "sidra",
        ["malhas", nivel, localidade],
        params,
        verificar_certificado=verificar_certificado,
    )
    if formato == "url" or url_antiga:
        return requisicao.url
    if tipo == "svg":
        return requisicao.texto()
    return requisicao.bruto()


def coordenadas(*args, **kwargs):
    """Removida no 3.0: o arquivo de coordenadas de setores e bairros saiu do repositório de dados.

    !!! danger "Removida"
        Chamar esta função levanta `DABFuncaoRemovidaError`. O stub deixa de
        existir em uma versão futura do 3.x; veja o guia de migração.
    """
    raise removida("ibge.coordenadas", "O arquivo de coordenadas de setores e bairros saiu do repositório de dados, sem substituto equivalente. Para coordenadas de municípios, use `wiki.municipios()`.")
