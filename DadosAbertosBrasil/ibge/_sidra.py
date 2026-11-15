from typing import Any, Literal, overload

from pydantic import Field, validate_call

from ..utils.modelos import Params, com_params, validar
from ..utils.requisicao import Requisicao
from ..utils.saida import consultar, resolver_formato
from ..utils.saida import tabela as _tabela
from ..utils.typing import DataFramePandas, DataFramePolars, Formato, Saida
from . import modelos as m


def _periodicidade(p: int | float | str) -> str:
    if isinstance(p, (int, float)):
        p = f"P{int(p)}"
    return p.upper()


class _ParamsTabelas(Params):
    contendo: str | None = Field(None, exclude=True)
    excluindo: str | list[str] | None = Field(None, exclude=True)
    assunto: int | str | None = None
    classificacao: int | str | None = None
    periodo: dict | str | None = None
    periodicidade: int | str | None = None
    nivel: int | str | None = None
    pesquisa: str | None = Field(None, exclude=True)

    def para_api(self) -> dict:
        params = super().para_api()
        periodo = self.periodo
        if isinstance(periodo, dict):
            for p in periodo:
                periodo = f"{_periodicidade(p)}[{[periodo[p]]}]"
            params["periodo"] = periodo
        if self.periodicidade is not None:
            params["periodicidade"] = _periodicidade(self.periodicidade)
        if self.nivel is not None:
            nivel = f"N{self.nivel}" if isinstance(self.nivel, int) else self.nivel
            params["nivel"] = nivel.upper()
        return params


class _ParamsSidra(Params):
    tabela: int = Field(exclude=True)
    periodos: list | int | str = Field("last", exclude=True)
    variaveis: list | int | str = Field("allxp", exclude=True)
    localidades: dict = Field(exclude=True)
    classificacoes: dict | None = Field(None, exclude=True)
    ufs_extintas: bool = Field(False, exclude=True)
    decimais: int | None = Field(None, exclude=True)


class _ParamsReferencias(Params):
    cod: str = Field(exclude=True)


@overload
def lista_tabelas(
    contendo: str | None = ...,
    excluindo: str | None = ...,
    assunto: int | str | None = ...,
    classificacao: int | str | None = ...,
    periodo: dict | str | None = ...,
    periodicidade: int | str | None = ...,
    nivel: int | str | None = ...,
    pesquisa: str | None = ...,
    index: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def lista_tabelas(
    contendo: str | None = ...,
    excluindo: str | None = ...,
    assunto: int | str | None = ...,
    classificacao: int | str | None = ...,
    periodo: dict | str | None = ...,
    periodicidade: int | str | None = ...,
    nivel: int | str | None = ...,
    pesquisa: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def lista_tabelas(
    contendo: str | None = ...,
    excluindo: str | None = ...,
    assunto: int | str | None = ...,
    classificacao: int | str | None = ...,
    periodo: dict | str | None = ...,
    periodicidade: int | str | None = ...,
    nivel: int | str | None = ...,
    pesquisa: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.Tabela]: ...


@overload
def lista_tabelas(
    contendo: str | None = ...,
    excluindo: str | None = ...,
    assunto: int | str | None = ...,
    classificacao: int | str | None = ...,
    periodo: dict | str | None = ...,
    periodicidade: int | str | None = ...,
    nivel: int | str | None = ...,
    pesquisa: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def lista_tabelas(
    contendo: str | None = ...,
    excluindo: str | None = ...,
    assunto: int | str | None = ...,
    classificacao: int | str | None = ...,
    periodo: dict | str | None = ...,
    periodicidade: int | str | None = ...,
    nivel: int | str | None = ...,
    pesquisa: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def lista_tabelas(
    contendo: str | None = ...,
    excluindo: str | None = ...,
    assunto: int | str | None = ...,
    classificacao: int | str | None = ...,
    periodo: dict | str | None = ...,
    periodicidade: int | str | None = ...,
    nivel: int | str | None = ...,
    pesquisa: str | None = ...,
    index: bool = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsTabelas)
def lista_tabelas(
    contendo: str | None = None,
    excluindo: str | None = None,
    assunto: int | str | None = None,
    classificacao: int | str | None = None,
    periodo: dict | str | None = None,
    periodicidade: int | str | None = None,
    nivel: int | str | None = None,
    pesquisa: str | None = None,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
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

    params = _ParamsTabelas.de_locais(locals())
    termos = [excluindo] if isinstance(excluindo, str) else (excluindo or [])

    def filtro(t: m.Tabela) -> bool:
        nome = (t.tabela_nome or "").upper()
        if isinstance(contendo, str) and contendo.upper() not in nome:
            return False
        if any(termo.upper() in nome for termo in termos):
            return False
        return not isinstance(pesquisa, str) or (t.pesquisa_id or "").upper() == pesquisa.upper()

    requisicao = Requisicao("sidra", ["agregados"], params.para_api(), verificar_certificado=verificar_certificado)
    return consultar(
        requisicao,
        m.Tabela,
        formato,
        index=index,
        index_col="tabela_id",
        preparar=m.preparar_tabelas,
        filtro=filtro,
    )


@overload
def lista_pesquisas(index: bool = ..., formato: Literal["bruto"] | None = ...) -> Any: ...


@overload
def lista_pesquisas(index: bool = ..., *, formato: Literal["json"]) -> list[dict[str, Any]]: ...


@overload
def lista_pesquisas(index: bool = ..., *, formato: Literal["pydantic"]) -> list[m.Pesquisa]: ...


@overload
def lista_pesquisas(index: bool = ..., *, formato: Literal["pandas"]) -> DataFramePandas: ...


@overload
def lista_pesquisas(index: bool = ..., *, formato: Literal["polars"]) -> DataFramePolars: ...


@overload
def lista_pesquisas(index: bool = ..., *, formato: Literal["url"]) -> str: ...


def lista_pesquisas(
    index: bool = False,
    formato: Formato | None = None,
) -> Saida:
    """Lista de pesquisas disponíveis no SIDRA.

    Esta função é utilizada para identificar o código usado pela função
    `ibge.lista_tabelas`.

    Parameters
    ----------
    index : bool, default=False
        Se True, define a coluna 'pesquisa_id' como index do DataFrame.
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

    Returns
    -------
    pandas.core.frame.DataFrame | polars.DataFrame
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

    def preparar(dados):
        pesquisas = {p["id"]: {"pesquisa_id": p["id"], "pesquisa_nome": p["nome"]} for p in dados}
        return list(pesquisas.values())

    return consultar(
        Requisicao("sidra", ["agregados"], cacheavel=True),
        m.Pesquisa,
        formato,
        index=index,
        index_col="pesquisa_id",
        preparar=preparar,
    )


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
        data = Requisicao("sidra", ["agregados", tabela, "metadados"]).json()

        self.dados = data
        self.cod = tabela
        self.nome = data["nome"]
        self.assunto = data["assunto"]
        self.periodos = data["periodicidade"]
        self.localidades = data["nivelTerritorial"]
        self.variaveis = data["variaveis"]
        self.classificacoes = data["classificacoes"]

    def __repr__(self) -> str:
        return (
            f"<DadosAbertosBrasil.ibge: Metadados da Tabela {self.cod} - {self.nome}>"
        )

    def __str__(self) -> str:
        return self.nome


@overload
def sidra(
    tabela: int,
    periodos: list | int | str = ...,
    variaveis: list | int | str = ...,
    localidades: dict = ...,
    classificacoes: dict | None = ...,
    ufs_extintas: bool = ...,
    decimais: int | None = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def sidra(
    tabela: int,
    periodos: list | int | str = ...,
    variaveis: list | int | str = ...,
    localidades: dict = ...,
    classificacoes: dict | None = ...,
    ufs_extintas: bool = ...,
    decimais: int | None = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def sidra(
    tabela: int,
    periodos: list | int | str = ...,
    variaveis: list | int | str = ...,
    localidades: dict = ...,
    classificacoes: dict | None = ...,
    ufs_extintas: bool = ...,
    decimais: int | None = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.ValorSidra]: ...


@overload
def sidra(
    tabela: int,
    periodos: list | int | str = ...,
    variaveis: list | int | str = ...,
    localidades: dict = ...,
    classificacoes: dict | None = ...,
    ufs_extintas: bool = ...,
    decimais: int | None = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def sidra(
    tabela: int,
    periodos: list | int | str = ...,
    variaveis: list | int | str = ...,
    localidades: dict = ...,
    classificacoes: dict | None = ...,
    ufs_extintas: bool = ...,
    decimais: int | None = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def sidra(
    tabela: int,
    periodos: list | int | str = ...,
    variaveis: list | int | str = ...,
    localidades: dict = ...,
    classificacoes: dict | None = ...,
    ufs_extintas: bool = ...,
    decimais: int | None = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsSidra)
def sidra(
    tabela: int,
    periodos: list | int | str = "last",
    variaveis: list | int | str = "allxp",
    localidades: dict = {1: "all"},  # noqa: B006
    classificacoes: dict | None = None,
    ufs_extintas: bool = False,
    decimais: int | None = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
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
        Série de dados do SIDRA.

    """

    _ParamsSidra.de_locais(locals())
    path = ["values", "t", tabela]

    def juntar(valor) -> str:
        return ",".join(str(i) for i in valor) if isinstance(valor, list) else str(valor)

    if periodos is not None:
        path += ["p", juntar(periodos)]
    if variaveis is not None:
        path += ["v", juntar(variaveis)]
    for n in localidades:
        path += [f"n{n}", juntar(localidades[n])]
    for c in classificacoes or {}:
        path += [f"c{c}", juntar(classificacoes[c])]
    path += ["u", "y" if ufs_extintas else "n", "d", decimais or "s"]

    requisicao = Requisicao("https://apisidra.ibge.gov.br/", path, verificar_certificado=verificar_certificado)
    formato = resolver_formato(formato)
    if formato == "url":
        return requisicao.url
    bruto = requisicao.bruto()
    if formato == "bruto":
        return bruto
    modelo = m.modelo_sidra(bruto[0])
    return _tabela(validar(modelo, bruto[1:]), modelo, formato)


@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.ReferenciaSidra]: ...


@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def referencias(
    cod: Literal["assuntos", "classificacoes", "niveis", "periodos", "periodicidades", "territorios", "variaveis"],
    index: bool = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsReferencias)
def referencias(
    cod: Literal[
        "assuntos",
        "classificacoes",
        "niveis",
        "periodos",
        "periodicidades",
        "territorios",
        "variaveis",
    ],
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Obtém uma base de códigos para utilizar como argumento na busca do SIDRA.

    Parameters
    ----------
    cod : str
        Uma das referências a seguir:
        - "assuntos"
        - "classificacoes"
        - "niveis"
        - "periodos"
        - "periodicidades"
        - "territorios"
        - "variaveis"

    index: bool, default=False
        Defina True caso o campo `"cod"` deva ser o index do DataFrame.
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
        Referências do código pesquisado.

    Examples
    --------
    Lista assuntos.

    >>> ibge.referencias("assuntos")
         cod                                    referencia
    0    148                         Abastecimento de água
    1     70                              Abate de animais
    2    110                Acesso a esgotamento sanitário
    3    147                             Acesso à internet
    4    107  Acesso a serviço de coleta de lixo doméstico
    ..    ..                                            ..

    Lista classificações usando o `cod` da classificação como index
    do DataFrame.

    >>> ibge.referencias("classificacoes", index=True)
                                                  referencia
    cod
    588    Acessibilidade possível na maior parte das via...
    957    Acesso à Internet por telefone móvel celular p...
    681                    Acesso a televisão por assinatura
    12236                               Adequação da moradia
    806                      Adubação, calagem e agrotóxicos
    ...                                                  ...

    """

    CODIGOS = {
        "assuntos": "A",
        "classificacoes": "C",
        "niveis": "N",
        "territorios": "T",
        "periodos": "P",
        "periodicidades": "E",
        "variaveis": "V",
    }
    _ParamsReferencias.de_locais(locals())
    return consultar(
        Requisicao(
            "sidra", ["agregados"], {"acervo": CODIGOS[cod]}, verificar_certificado=verificar_certificado, cacheavel=True
        ),
        m.ReferenciaSidra,
        formato,
        index=index,
        index_col="cod",
    )
