'''
Módulo para captura dos dados abertos da API do IpeaData.

Utilize a classe ipea.Serie(cod) para obtér os valores históricos da série.

Use o seguinte template para obter os parâmetros de referência:
>>> from DadosAbertosBrasil import ipea
>>> ipea.<parâmetro>(cod <opcional>)

Os parâmetros disponíveis são:
- ipea.metadados;
- ipea.temas;
- ipea.paises;
- ipea.territorios.

Documentação da API original: http://www.ipeadata.gov.br/api/
'''



import warnings

import pandas as pd



def _query(funcao: str) -> pd.DataFrame:
    _URL = 'http://www.ipeadata.gov.br/api/odata4/'
    return pd.DataFrame(list(pd.read_json(_URL + funcao).value))



class Serie:
    '''
    Dados de uma série IPEA.

    Parâmetros
    ----------
    cod: str
        Código da série que se deseja obter os dados.
        Utilize a função ipea.series() para identificar a série desejada.
        Utilize a coluna 'SERCODIGO'.

    Atributos
    ---------
    cod: str
        Código da série escolhida.
    valores: pd.DataFrame
        Valores históricos da série escolhida.
    metadados: pd.DataFrame
        Metadados da série escolhida.
    '''

    def __init__(self, cod: str):
        self.cod = cod
        self.valores = _query(f"Metadados(SERCODIGO='{cod}')/Valores")
        self.metadados = _query(f"Metadados('{cod}')")



def metadados(cod=None) -> pd.DataFrame:
    '''
    Registros de metadados e valores de todas as séries do IPEA.

    Parâmetros
    ----------
    cod: str (default = None)
        Código da série que se deseja obter os dados.
        Caso cod = None, obtém os metadados de todas as séries disponíveis.

    Retorna
    -------
    pd.DataFrame
        DataFrame contendo os metadados de todas séries disponíveis (default),
        ou apenas de uma série escolhida.
        Utilize a coluna 'SERCODIGO' para alimentar o campo 'cod'
        da classe ipea.Serie(cod).
    '''

    if cod is None:
        return _query('Metadados')
    elif isinstance(cod, str):
        return _query(f"Metadados('{cod}')")
    else:
        raise TypeError('O código da série deve ser tipo string.')



def series(cod=None, valores=True) -> pd.DataFrame:
    '''
    Registros de metadados e valores de todas as séries do IPEA.

    Parâmetros
    ----------
    cod: int (default = None)
        Código da série que se deseja obter os dados.
        Caso cod = None, obtém os metadados de todas as séries disponíveis.
    valores: bool (default = True)
        - True: Obtém os valores da série desejada;
        - False: Obtém os metadados da série desejada.
        Esse argumento é ignorado caso cod = None.

    Retorna
    -------
    pd.DataFrame
        - Se cod = None: Metadados das séries disponíveis;
        - Se cod = int: Valores da série desejada;
        - Se valores = False: Metadados da série desejada.
    '''

    warnings.warn(
        'Função depreciada.\nSerá removida nas próximas atualizações.',
        DeprecationWarning
    )

    if cod is None:
        return _query('Metadados')
    
    elif isinstance(cod, str):
        if valores:
            return _query(f"Metadados(SERCODIGO='{cod}')/Valores")
        else:
            return _query(f"Metadados('{cod}')")
        
    else:
        raise TypeError('O código da série deve ser tipo string.')



def temas(cod=None) -> pd.DataFrame:
    '''
    Registros de todos os temas cadastrados.

    Parâmetros
    ----------
    cod: int (opcional)
        Código do tema, caso queira ver os dados deste tema exclusivamente.

    Retorna
    -------
    pd.DataFrame
        DataFrame contendo um registro de todos os temas das séries do IPEA.
    '''
    
    if cod is None:
        return _query('Temas')
    elif isinstance(cod, int):
        return _query(f'Temas({cod})')
    else:
        raise TypeError('Código do tema deve ser um número inteiro.')



def paises(cod=None) -> pd.DataFrame:
    '''
    Registros de todos os países cadastrados.

    Parâmetros
    ----------
    cod: str (opcional)
        Sigla de três letras do país, caso queira ver os dados deste
        país exclusivamente.

    Retorna
    -------
    pd.DataFrame
        DataFrame contendo um registro de todos os países das séries do IPEA.
    '''

    if cod is None:
        return _query('Paises')
    elif isinstance(cod, str):
        return _query(f"Paises('{cod.upper()}')")
    else:
        raise TypeError('Código do país deve ser um string de três letras maísculas.')



def territorios(cod=None, nivel=None) -> pd.DataFrame:
    '''
    Registros de todos os territórios brasileiros cadastrados.

    Parâmetros
    ----------
    cod: int (opcional)
        Código do território, caso queira ver os dados deste
        território exclusivamente.
    nivel: str (opcional)
        Nome do nível territorial.
        Utilize a função ipea.niveis_territoriais() para verificar
        as opções disponíveis.
    
    Retorna
    -------
    pd.DataFrame
        DataFrame contendo o registro de todos os territórios
        das séries do IPEA.
    '''

    if (cod is None) and (nivel is None):
        return _query('Territorios')
    else:
        n = 'Municipios' if nivel == 'Municípios' else nivel        
        return _query(f"Territorios(TERCODIGO='{cod}',NIVNOME='{n}')")

    

def niveis_territoriais() -> list:
    '''
    Lista dos possíveis níveis territoriais.

    Retorna
    -------
    list
        Lista de todos os níveis territoriais das séries do IPEA.
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