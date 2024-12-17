from typing import Optional

import pandas as pd
from pydantic import validate_call

from ..utils import Get, Formato, Output


_RENOMEAR_COLUNAS = {
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
    "VALDATA": "data",
    "VALVALOR": "valor",
    "NIVNOME": "nivel",
    "TERCODIGO": "territorio",
}


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

    def __init__(
        self,
        cod: str,
        index: bool = False,
        verificar_certificado: bool = True,
    ):
        self.valores = Get(
            endpoint="ipea",
            path=[f"Metadados(SERCODIGO='{cod}')", "Valores"],
            verify=verificar_certificado,
            cols_to_rename=_RENOMEAR_COLUNAS,
            unpack_keys=["value"],
        ).pandas

        if "data" in self.valores.columns:
            self.valores["data"] = pd.to_datetime(
                self.valores["data"], utc=True
            ).dt.date
            if index:
                self.valores.set_index("data", inplace=True)

        # Atributos
        self.dados = self.valores
        self.cod = cod
        self.metadados = Get(
            endpoint="ipea",
            path=[f"Metadados('{cod}')"],
            verify=verificar_certificado,
            unpack_keys=["value"],
        ).pandas
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


@validate_call
def lista_series(
    contendo: Optional[str] = None,
    excluindo: Optional[str | list[str]] = None,
    fonte: Optional[str] = None,
    ativo: Optional[bool] = None,
    numerica: Optional[bool] = None,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
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

    data = Get(
        endpoint="ipea",
        path=["Metadados"],
        unpack_keys=["value"],
        cols_to_rename=_RENOMEAR_COLUNAS,
        index=index,
        verify=verificar_certificado,
    ).get(formato)

    if formato == "pandas":
        if contendo is not None:
            contendo = contendo.upper()
            f1 = data["nome"].str.upper().str.contains(contendo)
            f2 = data["comentario"].str.upper().str.contains(contendo)
            data = data[f1 | f2]

        if excluindo is not None:
            if isinstance(excluindo, str):
                excluindo = [excluindo]
            for termo in excluindo:
                data = data[~data["nome"].str.upper().str.contains(termo.upper())]

        if fonte is not None:
            fonte = fonte.upper()
            f1 = data["fonte_sigla"].str.upper().str.contains(fonte)
            f2 = data["fonte_nome"].str.upper().str.contains(fonte)
            data = data[f1 | f2]

        if ativo is not None:
            status = "A" if ativo else "I"
            data = data[data["ativo"] == status]

        if numerica is not None:
            data = data[data["numerica"] == numerica]

        data["ativo"] = data["ativo"].map({"A": True, "I": False}).astype(bool)

    return data


@validate_call
def serie(
    cod: str,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
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

    df = Get(
        endpoint="ipea",
        path=[f"Metadados(SERCODIGO='{cod}')", "Valores"],
        unpack_keys=["value"],
        cols_to_rename=_RENOMEAR_COLUNAS,
        verify=verificar_certificado,
    ).get(formato)

    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], utc=True).dt.date
        if index:
            df.set_index("data", inplace=True)

    return df
