from typing import Literal, Optional

from pydantic import Field, validate_call

from ..utils.modelos import Params, com_params, validar
from ..utils.requisicao import Requisicao
from ..utils.saida import consultar, tabela
from ..utils.typing import Formato, Saida
from . import modelos as m


def _valores(cod: str, verificar_certificado: bool | None) -> Requisicao:
    return Requisicao(
        "ipea", [f"Metadados(SERCODIGO='{cod}')", "Valores"], chaves=["value"], verificar_certificado=verificar_certificado
    )


class _ParamsSeries(Params):
    contendo: str | None = Field(None, exclude=True)
    excluindo: str | list[str] | None = Field(None, exclude=True)
    fonte: str | None = Field(None, exclude=True)
    ativo: bool | None = Field(None, exclude=True)
    numerica: bool | None = Field(None, exclude=True)


class _ParamsSerie(Params):
    cod: str = Field(exclude=True)


class Serie:
    """Dados de uma série IPEA.

    Parameters
    ----------
    cod : str
        Código da série que se deseja obter os dados.
        Utilize a função `ipea.lista_series` para identificar a série desejada.
        O código desejado estará na coluna 'codigo'.

    index : bool, default=False
        Se True, define a coluna 'data' como index do atributo 'valores'.
        Ignorado com aviso se `formato` for 'polars'.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    formato : {"json", "pydantic", "pandas", "polars"}, default="pandas"
        Formato dos atributos `valores` e `metadados`.

    Attributes
    ---------
    cod : str
        Código da série escolhida.

    valores : list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame
        Dados históricos da série escolhida. Alias de `dados`.

    dados : list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame
        Dados históricos da série escolhida. Alias de `valores`.

    metadados : list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame
        Metadados da série escolhida.

    base : str
        Nome da base de dados da série.

    fonte_nome : str
        Nome completo da fonte da série, em português.

    fonte_sigla : str
        Sigla ou nome abreviado da fonte da série, em português.

    fonte_url : str
        URL para o site da fonte da série.

    mutiplicador : str
        Nome do fator multiplicador dos valores da série.

    periodicidade : str
        Nome da periodicidade, em português.

    atualizacao : str
        Data da última carga de dados na série.

    comentario : str
        Comentários relativos a série, em português.

    nome : str
        Nome da série, em português.

    unidade : str
        Nome da unidade dos valores da série.

    status : str
        Indica se uma série macroeconômica ainda é atualizada.
        - 'A' (Ativa) para séries atualizadas;
        - 'I' (Inativa) para séries que não são atualizadas.
        As séries regionais ou sociais não possuem este metadado.

    tema : int
        Código de identificação do tema ao qual a série está associada.

    pais : str
        Código de identificação país ou região (como América Latina, Zona do
        Euro, etc.) ao qual a série está associada.

    numerica : bool
        - True: Série possui valores numéricos (tratados como números);
        - False: Série possui valores são alfanuméricos (string).

    Notes
    -----
    Os atributos `dados` e `valores` apresentam os mesmos dados. "Valores" é o
    termo padrão para os dados históricos do Ipeadata, porém o termo "Dados" é
    o padrão do pacote `DadosAbertosBrasil`.

    See Also
    --------
    DadosAbertosBrasil.ipea.serie
        Função que coleta os mesmos dados históricos desta classe, porém é
        mais simples e não coleta os metadados da série.

    Examples
    --------
    1. Utilize as funções `lista` para encontrar a série desejada.

    >>> ipea.lista_series()

    2. Instancie a classe `Serie` utilizando o código encontrado.

    >>> s = ipea.Serie('PAN4_PIBPMV4')

    3. Utilize o atributo `dados` para ver a série histórica.

    >>> s.dados
              codigo                       data         valor  \
    0   PAN4_PIBPMV4  1996-01-01T00:00:00-02:00  1.893233e+05
    1   PAN4_PIBPMV4  1996-04-01T00:00:00-03:00  2.046107e+05
    2   PAN4_PIBPMV4  1996-07-01T00:00:00-03:00  2.215132e+05
    3   PAN4_PIBPMV4  1996-10-01T00:00:00-03:00  2.393163e+05
    4   PAN4_PIBPMV4  1997-01-01T00:00:00-02:00  2.191170e+05
    ..           ...                        ...           ...

    4. Para ver os metadados, basta chamar o atributo correspondente.

    >>> s.nome
    'PIB nominal'
    >>> s.periodicidade
    'Trimestral'

    """

    def __init__(
        self,
        cod: str,
        index: bool = False,
        verificar_certificado: bool | None = None,
        formato: Literal["json", "pydantic", "pandas", "polars"] | None = None,
    ):
        formato = formato or "pandas"
        valores = validar(m.ValorSerie, _valores(cod, verificar_certificado).json())
        self.valores = tabela(valores, m.ValorSerie, formato, index=index, index_col="data")
        self.dados = self.valores
        self.cod = cod

        metadados = validar(
            m.Metadados,
            Requisicao(
                "ipea", [f"Metadados('{cod}')"], chaves=["value"], verificar_certificado=verificar_certificado
            ).json(),
        )
        registro = metadados[0]
        self.registro = registro
        self.base = registro.base
        self.fonte_nome = registro.fonte_nome
        self.fonte_sigla = registro.fonte_sigla
        self.fonte_url = registro.fonte_url
        self.multiplicador = registro.multiplicador
        self.periodo = registro.periodo
        self.ultima_atualizacao = registro.ultima_atualizacao
        self.comentario = registro.comentario
        self.nome = registro.nome
        self.unidade = registro.unidade
        self.ativo = registro.ativo
        self.tema = registro.tema
        self.pais = registro.codigo_pai
        self.numerica = registro.numerica
        self.metadados = tabela(metadados, m.Metadados, formato)

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.ipea: Dados da série '{self.cod}'>"

    def __str__(self) -> str:
        return self.nome


@validate_call
@com_params(_ParamsSeries)
def lista_series(
    contendo: Optional[str] = None,
    excluindo: Optional[str | list[str]] = None,
    fonte: Optional[str] = None,
    ativo: Optional[bool] = None,
    numerica: Optional[bool] = None,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Registros de metadados de todas as séries do IPEA.

    Parameters
    ----------
    contendo : str, optional
        Termo que deve estar contido no nome ou no comentário da série.

    excluindo : str | list[str], optional
        Termo ou lista de termos que não pode aparecer no nome da série.
        Sobrepõe o argumento `contendo`.

    fonte : str, optional
        Retorna apenas as séries desta fonte.

    ativo : bool, optional
        Se True, retorna apenas séries ativas.
        Se False, retorna apenas séries inativas.
        Se None, retorna todas as séries.

    numerica : bool, optional
        Se True, retorna apenas séries numéricas.
        Se False, não retorna as séries numéricas.
        Se None, retorna todas as séries.

    index : bool, default=False
        Se True, define a coluna 'codigo' como index do DataFrame.
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
        Lista de séries do IPEA.

    Example
    -------
    Forma mais simples da função.

    >>> ipea.lista_series()
                  codigo                                   nome  ...
    0       ABATE_ABPEAV       Abate - aves - peso das carcaças  ...
    1       ABATE_ABPEBV    Abate - bovinos - peso das carcaças  ...
    2       ABATE_ABPESU     Abate - suínos - peso das carcaças  ...
    3       ABATE_ABQUAV                    Abate - aves - qde.  ...
    4       ABATE_ABQUBV                 Abate - bovinos - qde.  ...
    ...              ...                                    ...  ...

    Utilize o argumento `index=True` para colocar a coluna `codigo`
    como index do DataFrame.

    >>> ipea.lista_series(index=True)
                                                   nome  ...
    codigo                                               ...
    ABATE_ABPEAV       Abate - aves - peso das carcaças  ...
    ABATE_ABPEBV    Abate - bovinos - peso das carcaças  ...
    ABATE_ABPESU     Abate - suínos - peso das carcaças  ...
    ABATE_ABQUAV                    Abate - aves - qde.  ...
    ABATE_ABQUBV                 Abate - bovinos - qde.  ...
    ...                                             ...  ...

    """

    termos = [excluindo] if isinstance(excluindo, str) else (excluindo or [])

    def contem(texto: str | None, termo: str) -> bool:
        return isinstance(texto, str) and termo.upper() in texto.upper()

    def filtro(serie: m.Metadados) -> bool:
        if contendo is not None and not (contem(serie.nome, contendo) or contem(serie.comentario, contendo)):
            return False
        if any(contem(serie.nome, termo) for termo in termos):
            return False
        if fonte is not None and not (contem(serie.fonte_sigla, fonte) or contem(serie.fonte_nome, fonte)):
            return False
        if ativo is not None and serie.ativo != ativo:
            return False
        return numerica is None or serie.numerica == numerica

    _ParamsSeries.de_locais(locals())
    return consultar(
        Requisicao("ipea", ["Metadados"], chaves=["value"], verificar_certificado=verificar_certificado, cacheavel=True),
        m.Metadados,
        formato,
        index=index,
        filtro=filtro,
    )


@validate_call
@com_params(_ParamsSerie)
def serie(
    cod: str,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Valores de uma série IPEA.

    Parameters
    ----------
    cod : str
        Código da série que se deseja obter os dados.
        Utilize a função `ipea.lista_series` para identificar a série desejada.
        O código desejado estará na coluna 'codigo'.

    index : bool, default=False
        Se True, define a coluna 'data' como index do DataFrame.
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
        Valores de uma série temporal do Ipeadata.

    Example
    -------
    1. Utilize as funções `lista` para encontrar a série desejada.

    >>> ipea.lista_series()

    2. Utilize o código encontrado como argumento da função `serie`.
    
    >>> ipea.serie('PAN4_PIBPMV4')
              codigo                       data         valor  \
    0   PAN4_PIBPMV4  1996-01-01T00:00:00-02:00  1.893233e+05  \
    1   PAN4_PIBPMV4  1996-04-01T00:00:00-03:00  2.046107e+05  \
    2   PAN4_PIBPMV4  1996-07-01T00:00:00-03:00  2.215132e+05  \
    3   PAN4_PIBPMV4  1996-10-01T00:00:00-03:00  2.393163e+05  \
    4   PAN4_PIBPMV4  1997-01-01T00:00:00-02:00  2.191170e+05  \
    ..           ...                        ...           ...  \

    See Also
    --------
    DadosAbertosBrasil.ipea.Serie
        Class do módulo `ipea` que coleta os mesmos valores desta função,
        porém também coleta os metadados da série.

    """

    _ParamsSerie.de_locais(locals())
    return consultar(_valores(cod, verificar_certificado), m.ValorSerie, formato, index=index, index_col="data")
