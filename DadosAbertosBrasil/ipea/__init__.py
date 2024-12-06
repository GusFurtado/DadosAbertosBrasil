"""Módulo para captura dos dados abertos da API do IpeaData.

Mini-Tutorial
-------------
1. Importe o módulo `ipea`.
>>> from DadosAbertosBrasil import ipea

2. Busque o código alfanumérico da série desejada com a função
`ipea.lista_series`.
>>> ipea.lista_series( ... )

3. Para facilitar a busca, filtre temas, países ou níveis territoriais com
as outras funções `lista`.
>>> temas = ipea.lista_temas( ... )
>>> paises = ipea.lista_paises( ... )
>>> territorios = ipea.lista_territorios( ... )
>>> niveis = ipea.lista_niveis( ... )

4. Instancie o objeto `Serie` utilizando o código encontrado.
>>> serie = ipea.Serie(cod)

5. Utilize os atributos para visualizar valores e metadados do série.
>>> serie.metadados
>>> serie.valores

6. Alternativamente, utilize a função `ipea.serie` para coletar apenas os
valores da série, sem os metadados. Está é uma forma simplificada e mais
rápida de obter os dados de uma série.

References
----------
.. [1] http://www.ipeadata.gov.br/api/

"""

from typing import List, Optional, Union

import pandas as pd

from .._utils.get_data import get_data


def _get(path: str) -> pd.DataFrame:
    """Captura e formata dados deste módulo.

    Parameters
    ----------
    path : str
        Parâmetros da coleta.

    Returns
    -------
    pandas.core.frame.DataFrame

    """

    values = get_data(endpoint="http://www.ipeadata.gov.br/api/odata4/", path=path)
    return pd.DataFrame(values["value"])


class Serie:
    """Dados de uma série IPEA.

    Parameters
    ----------
    cod : str
        Código da série que se deseja obter os dados.
        Utilize a função `ipea.lista_series` para identificar a série desejada.
        O código desejado estará na coluna 'codigo'.
    index : bool, default=False
        Se True, define a coluna 'codigo' como index do atributo 'valores'.

    Attributes
    ---------
    cod : str
        Código da série escolhida.
    valores : pandas.core.frame.DataFrame
        Dados históricos da série escolhida. Alias de `dados`.
    dados : pandas.core.frame.DataFrame
        Dados históricos da série escolhida. Alias de `valores`.
    metadados : pandas.core.frame.DataFrame
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

    def __init__(self, cod: str, index: bool = False):

        # DataFrame
        self.valores = _get(f"Metadados(SERCODIGO='{cod}')/Valores")
        self.valores.rename(
            columns={
                "SERCODIGO": "codigo",
                "VALDATA": "data",
                "VALVALOR": "valor",
                "NIVNOME": "nivel",
                "TERCODIGO": "territorio",
            },
            inplace=True,
        )

        if "data" in self.valores.columns:
            self.valores.data = pd.to_datetime(self.valores.data, utc=True).dt.date
            if index:
                self.valores.set_index("data", inplace=True)

        self.dados = self.valores

        # Atributos
        self.cod = cod
        self.metadados = _get(f"Metadados('{cod}')")
        self.base = self.metadados.loc[0, "BASNOME"]
        self.fonte_nome = self.metadados.loc[0, "FNTNOME"]
        self.fonte_sigla = self.metadados.loc[0, "FNTSIGLA"]
        self.fonte_url = self.metadados.loc[0, "FNTURL"]
        self.multiplicador = self.metadados.loc[0, "MULNOME"]
        self.periodo = self.metadados.loc[0, "PERNOME"]
        self.ultima_atualizacao = self.metadados.loc[0, "SERATUALIZACAO"]
        self.comentario = self.metadados.loc[0, "SERCOMENTARIO"]
        self.nome = self.metadados.loc[0, "SERNOME"]
        self.unidade = self.metadados.loc[0, "UNINOME"]
        self.ativo = self.metadados.loc[0, "SERSTATUS"]
        self.tema = self.metadados.loc[0, "TEMCODIGO"]
        self.pais = self.metadados.loc[0, "PAICODIGO"]
        self.numerica = self.metadados.loc[0, "SERNUMERICA"]

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.ipea: Dados da série '{self.cod}'>"

    def __str__(self) -> str:
        return self.nome


def lista_series(
    contendo: Optional[str] = None,
    excluindo: Optional[Union[str, List[str]]] = None,
    fonte: Optional[str] = None,
    ativo: Optional[bool] = None,
    numerica: Optional[bool] = None,
    index: bool = False,
) -> pd.DataFrame:
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

    Returns
    -------
    pandas.core.frame.DataFrame
        DataFrame onde cada coluna é um metadado e cada registro é uma série
        do IPEA.

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

    df = _get("Metadados")

    if isinstance(contendo, str):
        contendo = contendo.upper()
        f1 = df.SERNOME.str.upper().str.contains(contendo)
        f2 = df.SERCOMENTARIO.str.upper().str.contains(contendo)
        df = df[f1 | f2]

    if excluindo is not None:
        if isinstance(excluindo, str):
            excluindo = [excluindo]
        for termo in excluindo:
            df = df[~df.SERNOME.str.upper().str.contains(termo.upper())]

    if isinstance(fonte, str):
        fonte = fonte.upper()
        f1 = df.FNTSIGLA.str.upper().str.contains(fonte)
        f2 = df.FNTNOME.str.upper().str.contains(fonte)
        df = df[f1 | f2]

    if isinstance(ativo, bool):
        status = "A" if ativo else "I"
        df = df[df.SERSTATUS == status]

    if isinstance(numerica, bool):
        df = df[df.SERNUMERICA == numerica]

    df.rename(
        columns={
            "SERCODIGO": "codigo",
            "SERNOME": "nome",
            "SERCOMENTARIO": "comentario",
            "SERATUALIZACAO": "ultima_atualizacao",
            "BASNOME": "base",
            "FNTSIGLA": "fonte_sigla",
            "FNTNOME": "fonte_nome",
            "FNTURL": "fonte_url",
            "PERNOME": "periodo",
            "UNINOME": "unidade",
            "MULNOME": "multiplicador",
            "SERSTATUS": "ativo",
            "TEMCODIGO": "tema",
            "PAICODIGO": "codigo_pai",
            "SERNUMERICA": "numerica",
        },
        inplace=True,
    )

    df.ativo = df.ativo.map({"A": True, "I": False}).astype(bool)

    if index:
        df.set_index("codigo", inplace=True)

    return df


def lista_temas(
    cod: Optional[int] = None, pai: Optional[int] = None, index: bool = False
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
        df = _get("Temas")
    elif isinstance(cod, int):
        df = _get(f"Temas({cod})")
    else:
        raise TypeError("Código do tema deve ser um número inteiro.")

    if pai is not None:
        df = df[df.TEMCODIGO_PAI == pai]

    df.rename(
        columns={
            "TEMCODIGO": "codigo",
            "TEMCODIGO_PAI": "pai",
            "TEMNOME": "nome",
        },
        inplace=True,
    )

    if index:
        df.set_index("codigo", inplace=True)

    return df


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
        df = _get("Paises")
    elif isinstance(cod, str):
        df = _get(f"Paises('{cod.upper()}')")
    else:
        raise TypeError("Código do país deve ser um string de três letras maísculas.")

    df.rename(columns={"PAICODIGO": "codigo", "PAINOME": "nome"}, inplace=True)

    if index:
        df.set_index("codigo", inplace=True)

    return df


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
        df = _get("Territorios")
    else:
        n = "Municipios" if nivel == "Municípios" else nivel
        df = _get(f"Territorios(TERCODIGO='{cod}',NIVNOME='{n}')")

    df.rename(
        columns={
            "NIVNOME": "nivel",
            "TERCODIGO": "codigo",
            "TERNOME": "nome",
            "TERNOMEPADRAO": "nome_padrao",
            "TERCAPITAL": "capital",
            "TERAREA": "area",
            "NIVAMC": "amc",
        },
        inplace=True,
    )

    if isinstance(capital, bool):
        df = df[df.capital == capital]

    if isinstance(amc, bool):
        df = df[df.amc == amc]

    return df


def lista_niveis() -> List[str]:
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


def serie(cod: str, index: bool = False) -> pd.DataFrame:
    """Valores de uma série IPEA.

    Parameters
    ----------
    cod : str
        Código da série que se deseja obter os dados.
        Utilize a função `ipea.lista_series` para identificar a série desejada.
        O código desejado estará na coluna 'codigo'.
    index : bool, default=False
        Se True, define a coluna 'data' como index do DataFrame.

    Returns
    -------
    pandas.core.frame.DataFrame
        Série temporal do Ipeadata em formato de DataFrame.

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

    df = _get(f"Metadados(SERCODIGO='{cod}')/Valores")

    df.rename(
        columns={
            "SERCODIGO": "codigo",
            "VALDATA": "data",
            "VALVALOR": "valor",
            "NIVNOME": "nivel",
            "TERCODIGO": "territorio",
        },
        inplace=True,
    )

    if "data" in df.columns:
        df.data = pd.to_datetime(df.data, utc=True).dt.date
        if index:
            df.set_index("data", inplace=True)

    return df
