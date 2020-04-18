# Pacote para captura dos dados abertos da API IpeaData
# Autor: Gustavo Furtado da Silva
#
# Use o seguinte template para buscar dados:
#
# >>> from DadosAbertosBrasil import ipea
# >>> ipea.{função}(cod={opcional})



import pandas as pd

url = 'http://www.ipeadata.gov.br/api/odata4/'

def __query(funcao):
    return pd.DataFrame(list(pd.read_json(url + funcao).value))

# Registros de metadados de todas as séries disponíveis para consulta
def series(cod=None, valores=True):
    
    if cod == None:
        return __query('Metadados')
    
    elif isinstance(cod, str):
        if valores:
            return __query(f"Metadados(SERCODIGO='{cod}')/Valores")
        else:
            return __query(f"Metadados('{cod}')")
        
    else:
        raise TypeError('O código da série deve ser tipo string.')

# Registros de todos os temas cadastrados.
def temas(cod=None):
    if cod == None:
        return __query('Temas')
    elif isinstance(cod, int):
        return __query(f'Temas({cod})')
    else:
        raise TypeError('Código do tema deve ser um número inteiro.')
        
# Registros de todos os países cadastrados.
def paises(cod=None):
    if cod == None:
        return __query('Paises')
    elif isinstance(cod, str):
        return __query(f"Paises('{cod}')")
    else:
        raise TypeError('Código do país deve ser um string de três letras maísculas.')

# Registros de todos os territórios cadastrados.
def territorios(cod=None, nivel=None):
    if (cod == None) and (nivel == None):
        return __query('Territorios')
    else:
        return __query(f"Territorios(TERCODIGO='{cod}',NIVNOME='{nivel}')")

# Os níveis territoriais possíveis
def niveis_territoriais():
    return ['',
            'Brasil',
            'Regiões',
            'Estados',
            'Municípios',
            'AMC 91-00',
            'Microrregiões',
            'Mesorregiões',
            'AMC 20-00',
            'AMC 40-00',
            'AMC 60-00',
            'AMC 70-00',
            'AMC 1872-00',
            'Área metropolitana',
            'Estado/RM']