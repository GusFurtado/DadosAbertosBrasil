'''
Módulo para captura dos dados abertos da API do IpeaData.

Mini-Tutorial
-------------
1. Importe o módulo `ipea`.
>>> from DadosAbertosBrasil import ipea

2. Busque o código o código alfanumérico da série desejada com a função
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

Documentação da API original
----------------------------
http://www.ipeadata.gov.br/api/

------------------------------------------------------------------------------
'''



import pandas as _pd

from ._utils.get_data import get_data



def _get(
        path: str,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Captura e formata dados deste módulo.
    '''

    values = get_data(
        endpoint = 'http://www.ipeadata.gov.br/api/odata4/',
        path = path
    )['value']

    df = _pd.DataFrame(values)
    if index:
        df.set_index(df.columns[0], inplace=True)
    return df



class Serie:
    '''
    Dados de uma série IPEA.

    Parâmetros
    ----------
    cod : str
        Código da série que se deseja obter os dados.
        Utilize a função `ipea.lista_series` para identificar a série desejada.
        O código desejado estará na coluna 'SERCODIGO'.
    index : bool (default=False)
        Se True, define a coluna 'SERCODIGO' como index do atributo 'valores'.

    Atributos
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

    Exemplos
    --------
        >>> # Utilize as funções `lista` para encontrar a série desejada
        >>> ipea.lista_series()

        >>> # Instancie a classe `Serie` utilizando o código encontrado
        >>> s = ipea.Serie('PAN4_PIBPMV4')

        >>> # Utilize o atributo `dados` para ver a série histórica
        >>> s.dados
        ...        SERCODIGO                    VALDATA      VALVALOR  \
        ... 0   PAN4_PIBPMV4  1996-01-01T00:00:00-02:00  1.893233e+05  \
        ... 1   PAN4_PIBPMV4  1996-04-01T00:00:00-03:00  2.046107e+05  \
        ... 2   PAN4_PIBPMV4  1996-07-01T00:00:00-03:00  2.215132e+05  \
        ... 3   PAN4_PIBPMV4  1996-10-01T00:00:00-03:00  2.393163e+05  \
        ... 4   PAN4_PIBPMV4  1997-01-01T00:00:00-02:00  2.191170e+05  \
        ... ..           ...                        ...           ...  \

        >>> # Para ver os metadados, basta chamar o atributo correspondente
        >>> s.nome
        ... 'PIB nominal'
        >>> s.periodicidade
        ... 'Trimestral'

    Notas
    -----
    Os atributos `dados` e `valores` apresentam os mesmos dados. "Valores" é o
    termo padrão para os dados históricos do Ipeadata, porém o termo "Dados" é
    o padrão do pacote `DadosAbertosBrasil`.

    Ver também
    ----------
    DadosAbertosBrasil.ipea.serie
        Função que coleta os mesmos dados históricos desta classe, porém é
        mais simples e não coleta os metadados da série.

    --------------------------------------------------------------------------
    '''

    def __init__(
            self,
            cod: str,
            index: bool = False
        ):

        self.cod = cod
        self.valores = _get(f"Metadados(SERCODIGO='{cod}')/Valores", index)
        self.valores.VALDATA = _pd.to_datetime(self.valores.VALDATA)
        self.dados = self.valores
        self.metadados = _get(f"Metadados('{cod}')")
        self.base = self.metadados.loc[0, 'BASNOME']
        self.fonte_nome = self.metadados.loc[0, 'FNTNOME']
        self.fonte_sigla = self.metadados.loc[0, 'FNTSIGLA']
        self.fonte_url = self.metadados.loc[0, 'FNTURL']
        self.multiplicador = self.metadados.loc[0, 'MULNOME']
        self.periodicidade = self.metadados.loc[0, 'PERNOME']
        self.atualizacao = self.metadados.loc[0, 'SERATUALIZACAO']
        self.comentario = self.metadados.loc[0, 'SERCOMENTARIO']
        self.nome = self.metadados.loc[0, 'SERNOME']
        self.unidade = self.metadados.loc[0, 'UNINOME']
        self.status = self.metadados.loc[0, 'SERSTATUS']
        self.tema = self.metadados.loc[0, 'TEMCODIGO']
        self.pais = self.metadados.loc[0, 'PAICODIGO']
        self.numerica = self.metadados.loc[0, 'SERNUMERICA']


    def __repr__(self):
        return f"DadosAbertosBrasil.ipea: Dados da série '{self.cod}' ({self.nome})"



def lista_series(index=False) -> _pd.DataFrame:
    '''
    Registros de metadados de todas as séries do IPEA.

    Parâmetros
    ----------
    index : bool (default=False)
        Se True, define a coluna 'SERCODIGO' como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame onde cada coluna é um metadado e cada registro é uma série
        do IPEA.

    Exemplo
    -------
        >>> ipea.lista_series()
        ...            SERCODIGO                                SERNOME  \
        ... 0       ABATE_ABPEAV       Abate - aves - peso das carcaças  \
        ... 1       ABATE_ABPEBV    Abate - bovinos - peso das carcaças  \
        ... 2       ABATE_ABPESU     Abate - suínos - peso das carcaças  \
        ... 3       ABATE_ABQUAV                    Abate - aves - qde.  \
        ... 4       ABATE_ABQUBV                 Abate - bovinos - qde.  \
        ... ...              ...                                    ...  \

        >>> # Utilize o argumento `index=True` para colocar a coluna
            'SERCODIGO' como index do DataFrame.
        >>> ipea.lista_series(index=True)
        ...                                             SERNOME  \
        ... SERCODIGO                                            \
        ... ABATE_ABPEAV       Abate - aves - peso das carcaças  \
        ... ABATE_ABPEBV    Abate - bovinos - peso das carcaças  \
        ... ABATE_ABPESU     Abate - suínos - peso das carcaças  \
        ... ABATE_ABQUAV                    Abate - aves - qde.  \
        ... ABATE_ABQUBV                 Abate - bovinos - qde.  \
        ... ...                                             ...  \

    --------------------------------------------------------------------------
    '''

    return _get('Metadados', index)



def lista_temas(
        cod: int = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Registros de todos os temas cadastrados.

    Parâmetros
    ----------
    cod : int (default=None)
        Código do tema, caso queira ver os dados deste tema exclusivamente.
    index : bool (default=False)
        Se True, define a coluna 'TEMCODIGO' como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo um registro de todos os temas das séries do IPEA.

    Exemplos
    --------
        >>> ipea.lista_temas()
        ...     TEMCODIGO  TEMCODIGO_PAI                  TEMNOME
        ... 0          28            NaN             Agropecuária
        ... 1          23            NaN       Assistência social
        ... 2          10            NaN    Balanço de pagamentos
        ... 3           7            NaN                   Câmbio
        ... 4           5            NaN        Comércio exterior
        ... ..        ...            ...                      ...

        >>> # Utilize o argumento `index=True` para colocar a coluna
            'TEMCODIGO' como index do DataFrame.
        >>> ipea.lista_temas(index=True)
        ...            TEMCODIGO_PAI                  TEMNOME
        ... TEMCODIGO                                        
        ... 28                   NaN             Agropecuária
        ... 23                   NaN       Assistência social
        ... 10                   NaN    Balanço de pagamentos
        ... 7                    NaN                   Câmbio
        ... 5                    NaN        Comércio exterior
        ... ...                  ...                      ...

    --------------------------------------------------------------------------
    '''
    
    if cod is None:
        return _get('Temas', index)
    elif isinstance(cod, int):
        return _get(f'Temas({cod})', index)
    else:
        raise TypeError('Código do tema deve ser um número inteiro.')



def lista_paises(
        cod: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Registros de todos os países cadastrados.

    Parâmetros
    ----------
    cod : str (default=None)
        Sigla de três letras do país, caso queira ver os dados deste
        país exclusivamente.
    index : bool (default=False)
        Se True, define a coluna 'PAICODIGO' como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo um registro de todos os países das séries do IPEA.

    Exemplos
    --------
        >>> ipea.lista_paises()
        ...    PAICODIGO          PAINOME
        ... 0        AFG      Afeganistão
        ... 1        ZAF    África do Sul
        ... 2        DEU         Alemanha
        ... 3       LATI   América Latina
        ... 4        AGO           Angola
        ... ..       ...              ...

        >>> # Utilize o argumento `index=True` para colocar a coluna
            'PAICODIGO' como index do DataFrame.
        >>> ipea.lista_paises(index=True)
        ...                    PAINOME
        ... PAICODIGO                             
        ... AFG            Afeganistão
        ... ZAF          África do Sul
        ... DEU               Alemanha
        ... LATI        América Latina
        ... AGO                 Angola
        ... ...                    ...

    --------------------------------------------------------------------------
    '''

    if cod is None:
        return _get('Paises', index)
    elif isinstance(cod, str):
        return _get(f"Paises('{cod.upper()}')", index)
    else:
        raise TypeError('Código do país deve ser um string de três letras maísculas.')



def lista_territorios(
        cod: int = None,
        nivel: str = None
    ) -> _pd.DataFrame:
    '''
    Registros de todos os territórios brasileiros cadastrados.

    Parâmetros
    ----------
    cod : int (default=None)
        Código do território, caso queira ver os dados deste
        território exclusivamente.
    nivel : str (default=None)
        Nome do nível territorial.
        Utilize a função ipea.niveis_territoriais() para verificar
        as opções disponíveis.
    
    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo o registro de todos os territórios
        das séries do IPEA.

    Exemplos
    --------
        >>> ipea.lista_territorios()
        ...        NIVNOME  TERCODIGO                TERNOME  \
        ... 0                                 (não definido)  \
        ... 1       Brasil          0                 Brasil  \
        ... 2      Regiões          1           Região Norte  \
        ... 3      Estados         11               Rondônia  \
        ... 4   Municípios    1100015  Alta Floresta D'Oeste  \
        ... ..         ...        ...                    ...  \

    --------------------------------------------------------------------------
    '''

    if (cod is None) or (nivel is None):
        return _get('Territorios')
    else:
        n = 'Municipios' if nivel == 'Municípios' else nivel        
        return _get(f"Territorios(TERCODIGO='{cod}',NIVNOME='{n}')")

    

def lista_niveis() -> list:
    '''
    Lista dos possíveis níveis territoriais.

    Retorna
    -------
    list
        Lista de todos os níveis territoriais das séries do IPEA.

    Exemplos
    --------
        >>> ipea.lista_niveis()
        ... ['Brasil', 'Regiões', ... , 'AMC 70-00', 'Outros Países']

    --------------------------------------------------------------------------
    '''

    return [
        'Brasil',
        'Regiões',
        'Estados',
        'Microrregiões',
        'Mesorregiões',
        'Municípios',
        'Municípios por bacia',
        'Área metropolitana',
        'Estado/RM',
        'AMC 20-00',
        'AMC 40-00',
        'AMC 60-00',
        'AMC 1872-00',
        'AMC 91-00',
        'AMC 70-00',
        'Outros Países'
    ]



def serie(
        cod: str,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Valores de uma série IPEA.

    Parâmetros
    ----------
    cod : str
        Código da série que se deseja obter os dados.
        Utilize a função `ipea.lista_series` para identificar a série desejada.
        O código desejado estará na coluna 'SERCODIGO'.
    index : bool (default=False)
        Se True, define a coluna 'SERCODIGO' como index do atributo 'valores'.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Série temporal do Ipeadata em formato de DataFrame.

    Exemplo
    -------
        >>> # Utilize as funções `lista` para encontrar a série desejada
        >>> ipea.lista_series()

        >>> # Utilize o código encontrado como argumento da função `serie`
        >>> ipea.serie('PAN4_PIBPMV4')
        ...        SERCODIGO                    VALDATA      VALVALOR  \
        ... 0   PAN4_PIBPMV4  1996-01-01T00:00:00-02:00  1.893233e+05  \
        ... 1   PAN4_PIBPMV4  1996-04-01T00:00:00-03:00  2.046107e+05  \
        ... 2   PAN4_PIBPMV4  1996-07-01T00:00:00-03:00  2.215132e+05  \
        ... 3   PAN4_PIBPMV4  1996-10-01T00:00:00-03:00  2.393163e+05  \
        ... 4   PAN4_PIBPMV4  1997-01-01T00:00:00-02:00  2.191170e+05  \
        ... ..           ...                        ...           ...  \

    Ver também
    ----------
    DadosAbertosBrasil.ipea.Serie
        Class do módulo `ipea` que coleta os mesmos valores desta função,
        porém também coleta os metadados da série.

    --------------------------------------------------------------------------
    '''
    df = _get(f"Metadados(SERCODIGO='{cod}')/Valores", index)
    df.VALDATA = _pd.to_datetime(df.VALDATA)
    return df