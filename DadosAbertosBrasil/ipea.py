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

Documentação da API original
----------------------------
http://www.ipeadata.gov.br/api/

------------------------------------------------------------------------------
'''



import warnings

import pandas as _pd

from . import API



_api = API('ipea')



def _get(
        query: str,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Captura e formata dados deste módulo.
    '''

    values = _api.get(query)['value']
    df = _pd.DataFrame(values)
    if index:
        df.set_index(df.columns[0], inplace=True)
    return df



class Serie:
    '''
    Dados de uma série IPEA.

    Parâmetros
    ----------
    cod: str
        Código da série que se deseja obter os dados.
        Utilize a função `ipea.lista_series` para identificar a série desejada.
        O código desejado estará na coluna 'SERCODIGO'.
    index: bool (default=False)
        Se True, define a coluna 'SERCODIGO' como index do atributo 'valores'.

    Atributos
    ---------
    cod: str
        Código da série escolhida.
    valores: pandas.core.frame.DataFrame
        Valores históricos da série escolhida.
    metadados: pandas.core.frame.DataFrame
        Metadados da série escolhida.
    base: str
        Nome da base de dados da série.
    fonte_nome: str
        Nome completo da fonte da série, em português.
    fonte_sigla: str
        Sigla ou nome abreviado da fonte da série, em português.
    fonte_url: str
        URL para o site da fonte da série.
    mutiplicador: str
        Nome do fator multiplicador dos valores da série.
    periodicidade: str
        Nome da periodicidade, em português.
    atualizacao: str
        Data da última carga de dados na série.
    comentario: str
        Comentários relativos a série, em português.
    nome: str
        Nome da série, em português.
    unidade: str
        Nome da unidade dos valores da série.
    status: str
        Indica se uma série macroeconômica ainda é atualizada.
        - 'A' (Ativa) para séries atualizadas;
        - 'I' (Inativa) para séries que não são atualizadas.
        As séries regionais ou sociais não possuem este metadado.
    tema: int
        Código de identificação do tema ao qual a série está associada.
    pais: str
        Código de identificação país ou região (como América Latina, Zona do
        Euro, etc.) ao qual a série está associada.
    numerica: bool
        - True: Série possui valores numéricos (tratados como números);
        - False: Série possui valores são alfanuméricos (string).

    --------------------------------------------------------------------------
    '''

    def __init__(
            self,
            cod: str,
            index: bool = False
        ):

        self.cod = cod
        self.valores = _get(f"Metadados(SERCODIGO='{cod}')/Valores", index)
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



def lista_series(index=False) -> _pd.DataFrame:
    '''
    Registros de metadados de todas as séries do IPEA.

    Parâmetros
    ----------
    index: bool (default=False)
        Se True, define a coluna 'SERCODIGO' como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame onde cada coluna é um metadado e cada registro é uma série
        do IPEA.

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
    cod: int (default=None)
        Código do tema, caso queira ver os dados deste tema exclusivamente.
    index: bool (default=False)
        Se True, define a coluna 'TEMCODIGO' como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo um registro de todos os temas das séries do IPEA.

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
    cod: str (default=None)
        Sigla de três letras do país, caso queira ver os dados deste
        país exclusivamente.
    index: bool (default=False)
        Se True, define a coluna 'PAICODIGO' como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo um registro de todos os países das séries do IPEA.

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
    cod: int (default=None)
        Código do território, caso queira ver os dados deste
        território exclusivamente.
    nivel: str (default=None)
        Nome do nível territorial.
        Utilize a função ipea.niveis_territoriais() para verificar
        as opções disponíveis.
    
    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo o registro de todos os territórios
        das séries do IPEA.

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