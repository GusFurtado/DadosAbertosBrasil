"""Módulo de consulta a informações de interesse público.

Este módulo reúne funções pré-parametrizadas de outros submódulos do 
`DadosAbertosBrasil`, facilitando o acesso a informações diversas e 
amplamente utilizadas.

As funções deste módulo são importadas automaticamente pelo `__init__` 
do supermódulo, proporcionando uma interface simplificada para consultas 
rápidas.

"""

from datetime import date
from typing import Literal, Optional

import pandas as pd
from pydantic import validate_call, PositiveInt

from .. import bacen, ipea
from ..utils import Get, parse, Formato, Output


@validate_call
def bandeira(uf: str, tamanho: PositiveInt = 100) -> str:
    """Gera a URL da WikiMedia para a bandeira de um estado.

    Parameters
    ----------
    uf : str
        Sigla da Unidade Federativa.

    tamanho : int, default=100
        Tamanho em pixels da bandeira.

    Returns
    -------
    str
        URL da bandeira do estado no formato PNG.

    Raises
    ------
    DAB_UFError
        Caso seja inserida uma UF inválida.

    Examples
    --------
    Gera o link para uma imagem da bandeira de Santa Catarina de 200 pixels.

    >>> favoritos.bandeira(uf='SC', tamanho=200)
    'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/' ...

    """

    URL = r"https://upload.wikimedia.org/wikipedia/commons/thumb/"

    bandeira = {
        "BR": f"0/05/Flag_of_Brazil.svg/{tamanho}px-Flag_of_Brazil.svg.png",
        "AC": f"4/4c/Bandeira_do_Acre.svg/{tamanho}px-Bandeira_do_Acre.svg.png",
        "AM": f"6/6b/Bandeira_do_Amazonas.svg/{tamanho}px-Bandeira_do_Amazonas.svg.png",
        "AL": f"8/88/Bandeira_de_Alagoas.svg/{tamanho}px-Bandeira_de_Alagoas.svg.png",
        "AP": f"0/0c/Bandeira_do_Amap%C3%A1.svg/{tamanho}px-Bandeira_do_Amap%C3%A1.svg.png",
        "BA": f"2/28/Bandeira_da_Bahia.svg/{tamanho}px-Bandeira_da_Bahia.svg.png",
        "CE": f"2/2e/Bandeira_do_Cear%C3%A1.svg/{tamanho}px-Bandeira_do_Cear%C3%A1.svg.png",
        "DF": f"3/3c/Bandeira_do_Distrito_Federal_%28Brasil%29.svg/{tamanho}px-Bandeira_do_Distrito_Federal_%28Brasil%29.svg.png",
        "ES": f"4/43/Bandeira_do_Esp%C3%ADrito_Santo.svg/{tamanho}px-Bandeira_do_Esp%C3%ADrito_Santo.svg.png",
        "GO": f"b/be/Flag_of_Goi%C3%A1s.svg/{tamanho}px-Flag_of_Goi%C3%A1s.svg.png",
        "MA": f"4/45/Bandeira_do_Maranh%C3%A3o.svg/{tamanho}px-Bandeira_do_Maranh%C3%A3o.svg.png",
        "MG": f"f/f4/Bandeira_de_Minas_Gerais.svg/{tamanho}px-Bandeira_de_Minas_Gerais.svg.png",
        "MT": f"0/0b/Bandeira_de_Mato_Grosso.svg/{tamanho}px-Bandeira_de_Mato_Grosso.svg.png",
        "MS": f"6/64/Bandeira_de_Mato_Grosso_do_Sul.svg/{tamanho}px-Bandeira_de_Mato_Grosso_do_Sul.svg.png",
        "PA": f"0/02/Bandeira_do_Par%C3%A1.svg/{tamanho}px-Bandeira_do_Par%C3%A1.svg.png",
        "PB": f"b/bb/Bandeira_da_Para%C3%ADba.svg/{tamanho}px-Bandeira_da_Para%C3%ADba.svg.png",
        "PE": f"5/59/Bandeira_de_Pernambuco.svg/{tamanho}px-Bandeira_de_Pernambuco.svg.png",
        "PI": f"3/33/Bandeira_do_Piau%C3%AD.svg/{tamanho}px-Bandeira_do_Piau%C3%AD.svg.png",
        "PR": f"9/93/Bandeira_do_Paran%C3%A1.svg/{tamanho}px-Bandeira_do_Paran%C3%A1.svg.png",
        "RJ": f"7/73/Bandeira_do_estado_do_Rio_de_Janeiro.svg/{tamanho}px-Bandeira_do_estado_do_Rio_de_Janeiro.svg.png",
        "RO": f"f/fa/Bandeira_de_Rond%C3%B4nia.svg/{tamanho}px-Bandeira_de_Rond%C3%B4nia.svg.png",
        "RN": f"3/30/Bandeira_do_Rio_Grande_do_Norte.svg/{tamanho}px-Bandeira_do_Rio_Grande_do_Norte.svg.png",
        "RR": f"9/98/Bandeira_de_Roraima.svg/{tamanho}px-Bandeira_de_Roraima.svg.png",
        "RS": f"6/63/Bandeira_do_Rio_Grande_do_Sul.svg/{tamanho}px-Bandeira_do_Rio_Grande_do_Sul.svg.png",
        "SC": f"1/1a/Bandeira_de_Santa_Catarina.svg/{tamanho}px-Bandeira_de_Santa_Catarina.svg.png",
        "SE": f"b/be/Bandeira_de_Sergipe.svg/{tamanho}px-Bandeira_de_Sergipe.svg.png",
        "SP": f"2/2b/Bandeira_do_estado_de_S%C3%A3o_Paulo.svg/{tamanho}px-Bandeira_do_estado_de_S%C3%A3o_Paulo.svg.png",
        "TO": f"f/ff/Bandeira_do_Tocantins.svg/{tamanho}px-Bandeira_do_Tocantins.svg.png",
        # Extintos
        "FN": f"3/3b/Fernando_de_Noronha%2C_PE_-_Bandeira.svg/{tamanho}px-Fernando_de_Noronha%2C_PE_-_Bandeira.svg.png",
        "GB": f"c/c3/Bandeira_do_Estado_da_Guanabara_%281960%E2%80%931975%29.png/{tamanho}px-Bandeira_do_Estado_da_Guanabara_%281960%E2%80%931975%29.png",
    }

    return URL + bandeira[parse.uf(uf, extintos=True)]


@validate_call
def brasao(uf: str, tamanho: PositiveInt = 100) -> str:
    """Gera a URL da WikiMedia para o brasão de um estado.

    Parameters
    ----------
    uf : str
        Sigla da Unidade Federativa.

    tamanho : int, default=100
        Tamanho em pixels da bandeira.

    Returns
    -------
    str
        URL da bandeira do estado no formato PNG.

    Raises
    ------
    DAB_UFError
        Caso seja inserida uma UF inválida.

    Examples
    --------
    Gera o link para uma imagem do brasão de Santa Catarina de 200 pixels.

    >>> favoritos.brasao(uf='SC', tamanho=200)
    'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/' ...

    """

    URL = r"https://upload.wikimedia.org/wikipedia/commons/thumb/"

    brasao = {
        "BR": f"b/bf/Coat_of_arms_of_Brazil.svg/{tamanho}px-Coat_of_arms_of_Brazil.svg.png",
        "AC": f"5/52/Brasão_do_Acre.svg/{tamanho}px-Brasão_do_Acre.svg.png",
        "AM": f"2/2c/Bras%C3%A3o_do_Amazonas.svg/{tamanho}px-Bras%C3%A3o_do_Amazonas.svg.png",
        "AL": f"5/5c/Bras%C3%A3o_do_Estado_de_Alagoas.svg/{tamanho}px-Bras%C3%A3o_do_Estado_de_Alagoas.svg.png",
        "AP": f"6/63/Bras%C3%A3o_do_Amap%C3%A1.svg/{tamanho}px-Bras%C3%A3o_do_Amap%C3%A1.svg.png",
        "BA": f"1/12/Bras%C3%A3o_do_estado_da_Bahia.svg/{tamanho}px-Bras%C3%A3o_do_estado_da_Bahia.svg.png",
        "CE": f"f/fe/Bras%C3%A3o_do_Cear%C3%A1.svg/{tamanho}px-Bras%C3%A3o_do_Cear%C3%A1.svg.png",
        "DF": f"e/e0/Bras%C3%A3o_do_Distrito_Federal_%28Brasil%29.svg/{tamanho}px-Bras%C3%A3o_do_Distrito_Federal_%28Brasil%29.svg.png",
        "ES": f"a/a0/Bras%C3%A3o_do_Esp%C3%ADrito_Santo.svg/{tamanho}px-Bras%C3%A3o_do_Esp%C3%ADrito_Santo.svg.png",
        "GO": f"b/bf/Bras%C3%A3o_de_Goi%C3%A1s.svg/{tamanho}px-Bras%C3%A3o_de_Goi%C3%A1s.svg.png",
        "MA": f"a/ab/Brasão_do_Maranhão.svg/{tamanho}px-Brasão_do_Maranhão.svg.png",
        "MG": f"d/d2/Brasão_de_Minas_Gerais.svg/{tamanho}px-Brasão_de_Minas_Gerais.svg.png",
        "MT": f"0/04/Brasão_de_Mato_Grosso.png/{tamanho}px-Brasão_de_Mato_Grosso.png",
        "MS": f"f/fa/Brasão_de_Mato_Grosso_do_Sul.svg/{tamanho}px-Brasão_de_Mato_Grosso_do_Sul.svg.png",
        "PA": f"b/bc/Brasão_do_Pará.svg/{tamanho}px-Brasão_do_Pará.svg.png",
        "PB": f"f/fd/Brasão_da_Paraíba.svg/{tamanho}px-Brasão_da_Paraíba.svg.png",
        "PE": f"0/04/Brasão_do_estado_de_Pernambuco.svg/{tamanho}px-Brasão_do_estado_de_Pernambuco.svg.png",
        "PI": f"a/ad/Brasão_do_Piauí.svg/{tamanho}px-Brasão_do_Piauí.svg.png",
        "PR": f"4/49/Brasão_do_Paraná.svg/{tamanho}px-Brasão_do_Paraná.svg.png",
        "RJ": f"5/5b/Brasão_do_estado_do_Rio_de_Janeiro.svg/{tamanho}px-Brasão_do_estado_do_Rio_de_Janeiro.svg.png",
        "RO": f"f/f1/Brasão_de_Rondônia.svg/{tamanho}px-Brasão_de_Rondônia.svg.png",
        "RN": f"2/26/Brasão_do_Rio_Grande_do_Norte.svg/{tamanho}px-Brasão_do_Rio_Grande_do_Norte.svg.png",
        "RR": f"e/ed/Brasão_de_Roraima.svg/{tamanho}px-Brasão_de_Roraima.svg.png",
        "RS": f"3/38/Brasão_do_Rio_Grande_do_Sul.svg/{tamanho}px-Brasão_do_Rio_Grande_do_Sul.svg.png",
        "SC": f"6/65/Brasão_de_Santa_Catarina.svg/{tamanho}px-Brasão_de_Santa_Catarina.svg.png",
        "SE": f"5/52/Brasão_de_Sergipe.svg/{tamanho}px-Brasão_de_Sergipe.svg.png",
        "SP": f"1/1a/Brasão_do_estado_de_São_Paulo.svg/{tamanho}px-Brasão_do_estado_de_São_Paulo.svg.png",
        "TO": f"c/cc/Brasão_do_Tocantins.svg/{tamanho}px-Brasão_do_Tocantins.svg.png",
        # Extintos
        "FN": f"5/5a/Fernando_de_Noronha%2C_PE_-_Bras%C3%A3o.svg/{tamanho}px-Fernando_de_Noronha%2C_PE_-_Bras%C3%A3o.svg.png",
        "GB": f"c/cf/Bras%C3%A3o_do_Estado_da_Guanabara_%281960%E2%80%931975%29.png/{tamanho}px-Bras%C3%A3o_do_Estado_da_Guanabara_%281960%E2%80%931975%29.png",
    }

    return URL + brasao[parse.uf(uf, extintos=True)]


@validate_call
def catalogo(
    formato: Literal["pandas", "url"] = "pandas",
) -> pd.DataFrame | str:
    """Catálogo de iniciativas oficiais de dados abertos no Brasil.

    Parameters
    ----------
    formato : {"pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    Returns
    -------
    pandas.core.frame.DataFrame | str
        Catálogo de iniciativas de dados abertos.

    Notes
    -----
    Fonte dos dados
        https://github.com/dadosgovbr

    Examples
    --------
    >>> favoritos.catalogo()
                                                   Título  ...
    0                      Alagoas em dados e informações  ...
    1                             Fortaleza Dados Abertos  ...
    2                              Dados abertos – TCM-CE  ...
    3                      Dados abertos Distrito Federal  ...
    4                       Dados abertos – Governo do ES  ...
    ..                                                ...  ...

    """

    URL = "https://raw.githubusercontent.com/dadosgovbr/catalogos-dados-brasil/master/dados/catalogos.csv"

    match formato:
        case "pandas":
            return pd.read_csv(URL)
        case "url":
            return URL


@validate_call
def codigos_municipios(
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Lista dos códigos dos municípios do IBGE e do TSE.

    Utilizado para correlacionar dados das duas APIs diferentes.

    Parameters
    ----------
    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        Códigos do IBGE e do TSE para todos os municípios do Brasil.

    Notes
    -----
    Fonte dos dados
        https://github.com/betafcc

    Examples
    --------
    >>> favoritos.codigos_municipios()
          codigo_tse  codigo_ibge nome_municipio  uf  capital
    0           1120      1200013     ACRELÂNDIA  AC        0
    1           1570      1200054   ASSIS BRASIL  AC        0
    2           1058      1200104      BRASILÉIA  AC        0
    3           1007      1200138         BUJARI  AC        0
    4           1015      1200179       CAPIXABA  AC        0
    ..           ...          ...            ...  ..      ...

    """

    return Get(
        endpoint="github",
        path=[
            "betafcc",
            "Municipios-Brasileiros-TSE",
            "master",
            "municipios_brasileiros_tse.json",
        ],
        verify=verificar_certificado,
    ).get(formato)


@validate_call
def ipca(
    ultimos: Optional[PositiveInt] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Índice nacional de preços ao consumidor-amplo (IPCA).

    Esta é uma função de fácil acesso à série temporal 433 do módulo `bacen`.

    Parameters
    ----------
    ultimos : int, optional
        Retorna os últimos N valores da série numérica.

    inicio : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o primeiro dia da pesquisa.

    fim : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o último dia da pesquisa. Caso este campo seja None, será
        considerada a data de hoje.

    index : bool, default=False
        Define se a coluna 'data' será o index do DataFrame.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        DataFrame contendo os valores da série temporal.

    Notes
    -----
    Os argumentos `inicio` e `fim` devem ser usados em conjunto para funcionar.

    Examples
    --------
    Os quatro valores mais recentes.

    >>> favoritos.ipca(ultimos=4)
            data valor
    0 2021-03-01  0.93
    1 2021-04-01  0.31
    2 2021-05-01  0.83
    3 2021-06-01  0.53

    Os valores entre Janeiro e Abril de 2021 usando a data como índice.

    >>> favoritos.ipca(inicio='2021-01-01', fim='2021-04-01', index=True)
               valor
    data
    2021-01-01  0.25
    2021-02-01  0.86
    2021-03-01  0.93
    2021-04-01  0.31

    """

    return bacen.serie(
        cod=433,
        ultimos=ultimos,
        inicio=inicio,
        fim=fim,
        index=index,
        formato=formato,
        verificar_certificado=verificar_certificado,
    )


@validate_call
def perfil_eleitorado(
    formato: Literal["pandas", "url"] = "pandas"
) -> pd.DataFrame | str:
    """Tabela com perfil do eleitorado por município.

    Parameters
    ----------
    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    Returns
    -------
    pandas.core.frame.DataFrame | str
        Perfil do eleitorado em todos os municípios.

    Examples
    --------
    >>> favoritos.perfil_eleitorado()
          NR_ANO_ELEICAO  CD_PAIS NM_PAIS SG_REGIAO NM_REGIAO SG_UF     NM_UF  ...
    0               2020        1  Brasil         N     Norte    AC      Acre  ...
    1               2020        1  Brasil         N     Norte    AC      Acre  ...
    ..               ...      ...     ...       ...       ...   ...       ...  ...

    """

    URL = r"https://raw.githubusercontent.com/GusFurtado/dab_assets/main/data/eleitorado.csv"

    match formato:
        case "pandas":
            return pd.read_csv(URL, encoding="latin-1", sep=";")
        case "url":
            return URL


@validate_call
def pib(
    periodo: Literal["anual", "trimestral"] = "anual",
    tipo: Literal["nominal", "real"] = "real",
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Variação percentual do Produto Interno Bruto Real.

    Esta é uma função de fácil acesso às séries temporais de PIB do módulo `ipea`.

    Parameters
    ----------
    periodo : {"anual", "trimestral"}, default="anual"
        Granularidade dos valores.

    tipo : {"nominal", "real"}, default="real"
        - "nominal": Valores absolutos do PIB em reais;
        - "real": Variação real do PIB no período.

    index : bool, default=False
        Define a coluna `data` como index da tabela.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        Valores do PIB real ou nominal.

    Examples
    --------
    Capturar PIB trimestral.

    >>> favoritos.pib(periodo="trimestral")
              data      valor
    0   1997-01-01   3.400572
    1   1997-04-01   4.754002
    2   1997-07-01   1.791279
    3   1997-10-01   3.738518
    4   1998-01-01   1.007575
    ..         ...        ...

    Capturar PIB anual, pondo o período como index da tabela.

    >>> favoritos.pib(periodo="anual", index=True)
                   valor
    data
    1997-01-01  3.394846
    1998-01-01  0.338098
    1999-01-01  0.467938
    2000-01-01  4.387949
    2001-01-01  1.389896
    ...              ...

    """

    match periodo, tipo:
        case "anual", "real":
            cod = "SCN10_PIBG10"
        case "anual", "nominal":
            cod = "SCN10_PIBN10"
        case "trimestral", "real":
            cod = "PAN4_PIBPMG4"
        case "trimestral", "nominal":
            cod = "PAN4_PIBPMV4"

    df = ipea.serie(
        cod=cod,
        index=False,
        formato=formato,
        verificar_certificado=verificar_certificado,
    )

    if formato != "pandas":
        return df

    assert not df.empty, "Problema na série do IPEA"
    df.drop(columns=["codigo", "nivel", "territorio"], inplace=True)
    if index:
        df.set_index("data", inplace=True)

    return df


@validate_call
def rentabilidade_poupanca(
    ultimos: Optional[PositiveInt] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Rentailidade dos depósitos de poupança a partir de Maio de 2012.

    Esta é uma função de fácil acesso à série temporal 195 do módulo `bacen`.

    Parameters
    ----------
    ultimos : int, optional
        Retorna os últimos N valores da série numérica.

    inicio : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o primeiro dia da pesquisa.

    fim : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o último dia da pesquisa. Caso este campo seja None, será
        considerada a data de hoje.

    index : bool, default=False
        Define se a coluna 'data' será o index do DataFrame.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        DataFrame contendo os valores da série temporal.

    Notes
    -----
    Os argumentos `inicio` e `fim` devem ser usados em conjunto para funcionar.

    Examples
    --------
    Os quatro valores mais recentes.

    >>> favoritos.rentabilidade_poupanca(ultimos=4)
            data    datafim   valor
    0 2021-07-05 2021-08-05  0.2446
    1 2021-07-06 2021-08-06  0.2446
    2 2021-07-07 2021-08-07  0.2446
    3 2021-07-08 2021-08-08  0.2446

    Os valores entre Janeiro e Abril de 2021 usando a data como índice.

    >>> favoritos.rentabilidade_poupanca(inicio="2021-01-01", fim="2021-04-01", index=True)
                  datafim   valor
    data
    2021-01-01 2021-02-01  0.1159
    2021-01-02 2021-02-02  0.1159
    2021-01-03 2021-02-03  0.1159
    2021-01-04 2021-02-04  0.1159
    2021-01-05 2021-02-05  0.1159
    ...               ...     ...

    """

    return bacen.serie(
        cod=195,
        ultimos=ultimos,
        inicio=inicio,
        fim=fim,
        index=index,
        formato=formato,
        verificar_certificado=verificar_certificado,
    )


@validate_call
def reservas_internacionais(
    periodo: Literal["diario", "mensal"] = "mensal",
    ultimos: Optional[PositiveInt] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Reservar internacionais mensais ou diárias.

    Esta é uma função de fácil acesso às séries temporais 3546 e 13621
    do módulo `bacen`.

    Parameters
    ----------
    periodo : {"mensal", "diario"}, default="mensal"
        Período dos dados consultados.

    ultimos : int, optional
        Retorna os últimos N valores da série numérica.

    inicio : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o primeiro dia da pesquisa.

    fim : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o último dia da pesquisa. Caso este campo seja None, será
        considerada a data de hoje.

    index : bool, default=False
        Define se a coluna `"data"` será o index do DataFrame.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        DataFrame contendo os valores da série temporal.

    Notes
    -----
    Os argumentos `inicio` e `fim` devem ser usados em conjunto para funcionar.

    Examples
    --------
    Os quatro valores diários mais recentes.

    >>> favoritos.reservas_internacionais(periodo="diario", ultimos=4)
            data   valor
    0 2021-07-05  353870
    1 2021-07-06  354086
    2 2021-07-07  354140
    3 2021-07-08  354303

    Os valores mensais entre Janeiro e Abril de 2021 usando a data como
    índice.

    >>> favoritos.reservas_internacionais(
    ...     periodo = "mensal",
    ...     inicio = "2021-01-01",
    ...     fim = "2021-04-01",
    ...     index = True
    ... )
                 valor
    data
    2021-01-01  355416
    2021-02-01  356070
    2021-03-01  347413
    2021-04-01  350996

    """

    match periodo:
        case "diario":
            cod = 13621
        case "mensal":
            cod = 3546

    return bacen.serie(
        cod=cod,
        ultimos=ultimos,
        inicio=inicio,
        fim=fim,
        index=index,
        formato=formato,
        verificar_certificado=verificar_certificado,
    )


@validate_call
def risco_brasil(
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Valores diários do Risco-Brasil, disponibilizados pela J.P. Morgan
    desde 1994.

    Esta é uma função de fácil acesso à série temporal 'JPM366_EMBI366' do
    módulo `ipea`.

    Parameters
    ----------
    index : bool, default=False
        Define a coluna `data` como index da tabela.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        Tabela contendo os valores diários do Risco-Brasil.

    Examples
    --------
    >>> favoritos.risco_brasil()
                data   valor
    0     1994-04-29  1120.0
    1     1994-04-30     NaN
    2     1994-05-01     NaN
    3     1994-05-02  1131.0
    4     1994-05-03  1081.0
    ..           ...     ...

    """

    df = ipea.serie(
        cod="JPM366_EMBI366",
        index=False,
        formato=formato,
        verificar_certificado=verificar_certificado,
    )

    if formato != "pandas":
        return df

    df.drop(columns=["codigo", "nivel", "territorio"], inplace=True)
    if index:
        df.set_index("data", inplace=True)

    return df


@validate_call
def salario_minimo(
    tipo: Literal["nominal", "pcc", "real"] = "nominal",
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Valores do salário-mínimo mensal brasileiro desde 1940.

    Esta é uma função de fácil acesso às série temporais do módulo `ipea`.

    Parameters
    ----------
    tipo : {"nominal", "real", "pcc"}, default="nominal"
        Tipo de salário-mínimo.
        - "nominal": Salário-mínimo nominal;
        - "real": Salário-mínimo real (abatido pela inflação);
        - "ppc": Salario-mínimo por Paridade de Poder de Compra.

    index : bool, default=False
        Define a coluna `data` como index da tabela.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        Tabela contendo os valores mensais do salário-mínimo.

    Examples
    --------
    Forma mais simples da função.

    >>> favoritos.salario_minimo()
               data         valor
    0    1940-07-01  8.727273e-14
    1    1940-08-01  8.727273e-14
    2    1940-09-01  8.727273e-14
    3    1940-10-01  8.727273e-14
    4    1940-11-01  8.727273e-14
    ..          ...           ...

    Salário-mínimo real usando a data como índice da tabela.

    >>> favoritos.salario_minimo(tipo="real", index=True)
                      valor
    data
    1940-07-01   962.321161
    1940-08-01   959.634185
    1940-09-01   958.771291
    1940-10-01   943.765421
    1940-11-01   922.546843
    ...                 ...

    """

    match tipo:
        case "nominal":
            cod = "MTE12_SALMIN12"
        case "real":
            cod = "GAC12_SALMINRE12"
        case "ppc":
            cod = "GAC12_SALMINDOL12"

    df = ipea.serie(
        cod=cod,
        index=False,
        formato=formato,
        verificar_certificado=verificar_certificado,
    )

    if formato != "pandas":
        return df

    assert not df.empty, "Problema na série do IPEA"
    df.drop(columns=["codigo", "nivel", "territorio"], inplace=True)
    if index:
        df.set_index("data", inplace=True)

    return df


@validate_call
def selic(
    periodo: Literal["diario", "mensal", "meta"] = "meta",
    anualizado: bool = True,
    ultimos: Optional[PositiveInt] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Taxa de juros - Meta Selic definida pelo COPOM.

    Esta é uma função de fácil acesso à série temporal 432 do módulo `bacen`.

    Parameters
    ----------
    periodo : {"meta", "diario", "mensal"}, default="meta"
        Tipo da série que será retornada.
        - "meta": Meta anual do COPOM;
        - "diario": Intervalo de dados por dia.
        - "mensal": Intervalo de dados por mês.

    anualizado : bool, default=True
        Se True, anualiza a série mantendo o período.
        Esse argumento é ignorado quando `periodo == "meta"`.

    ultimos : int, optional
        Retorna os últimos N valores da série numérica.

    inicio : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o primeiro dia da pesquisa.

    fim : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o último dia da pesquisa. Caso este campo seja None, será
        considerada a data de hoje.

    index : bool, default=False
        Define se a coluna "data" será o index do DataFrame.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        DataFrame contendo os valores da série temporal.

    Notes
    -----
    Os argumentos `inicio` e `fim` devem ser usados em conjunto para funcionar.

    Examples
    --------
    Busca a taxa mensal anualizada dos quatro meses mais recentes.

    >>> import DadosAbertosBrasil as dab
    >>> dab.selic(
    ...     periodo = "mensal",
    ...     anualizado = True,
    ...     ultimos = 4
    ... )
            data  valor
    0 2021-11-01   7.65
    1 2021-12-01   8.76
    2 2022-01-01   9.15
    3 2022-02-01  10.47

    Captura a meta SELIC corrente.

    >>> dab.selic(periodo="meta", ultimos=1)
            data  valor
    0 2022-03-16  10.75

    Captura os valores não anualizados da primeira semada de Janeiro/2022,
    utilizando a data como índice.

    >>> dab.selic(
    ...     periodo = "diario",
    ...     anualizado = False,
    ...     inicio = "2022-01-03",
    ...     fim = "2022-01-07",
    ...     index = True
    ... )
                   valor
    data
    2022-01-03  0.034749
    2022-01-04  0.034749
    2022-01-05  0.034749
    2022-01-06  0.034749
    2022-01-07  0.034749

    """

    match periodo, anualizado:
        case "meta", _:
            cod = 432
        case "diario", True:
            cod = 1178
        case "diario", False:
            cod = 11
        case "mensal", True:
            cod = 4189
        case "mensal", False:
            cod = 4390

    return bacen.serie(
        cod=cod,
        ultimos=ultimos,
        inicio=inicio,
        fim=fim,
        index=index,
        formato=formato,
        verificar_certificado=verificar_certificado,
    )


@validate_call
def taxa_referencial(
    ultimos: Optional[PositiveInt] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Taxa referencial (TR).

    Esta é uma função de fácil acesso à série temporal 226 do módulo `bacen`.

    Parameters
    ----------
    ultimos : int, optional
        Retorna os últimos N valores da série numérica.

    inicio : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o primeiro dia da pesquisa.

    fim : date, optional
        Valor datetime ou string no formato de data `"AAAA-MM-DD"` que
        representa o último dia da pesquisa. Caso este campo seja None, será
        considerada a data de hoje.

    index : bool, default=False
        Define se a coluna 'data' será o index do DataFrame.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        DataFrame contendo os valores da série temporal.

    Notes
    -----
    Os argumentos `inicio` e `fim` devem ser usados em conjunto para funcionar.

    Examples
    --------
    Os quatro valores mais recentes.

    >>> favoritos.taxa_referencial(ultimos=4)
            data    datafim   valor
    0 2021-07-05 2021-08-05  0.0000
    1 2021-07-06 2021-08-06  0.0000
    2 2021-07-07 2021-08-07  0.0000
    3 2021-07-08 2021-08-08  0.0000

    Os valores entre Janeiro e Abril de 2021 usando a data como índice.

    >>> favoritos.taxa_referencial(inicio="2021-01-01", fim="2021-04-01", index=True)
                  datafim   valor
    data
    2021-01-01 2021-02-01  0.0000
    2021-01-02 2021-02-02  0.0000
    2021-01-03 2021-02-03  0.0000
    2021-01-04 2021-02-04  0.0000
    2021-01-05 2021-02-05  0.0000
    ...               ...     ...

    """

    return bacen.serie(
        cod=226,
        ultimos=ultimos,
        inicio=inicio,
        fim=fim,
        index=index,
        formato=formato,
        verificar_certificado=verificar_certificado,
    )
