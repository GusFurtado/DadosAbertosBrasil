'''
Módulo para captura dos dados abertos da API do IpeaData.

Use o seguinte template para buscar dados:
>>> from DadosAbertosBrasil import ipea
>>> ipea.{função}(cod={opcional})

Documentação da API original: http://www.ipeadata.gov.br/api/
'''



import pandas as pd



_url = 'http://www.ipeadata.gov.br/api/odata4/'



def _query(funcao):
    return pd.DataFrame(list(pd.read_json(_url + funcao).value))



# Registros de metadados de todas as séries disponíveis para consulta
def series(cod=None, valores=True):
    
    if cod == None:
        return _query('Metadados')
    
    elif isinstance(cod, str):
        if valores:
            return _query(f"Metadados(SERCODIGO='{cod}')/Valores")
        else:
            return _query(f"Metadados('{cod}')")
        
    else:
        raise TypeError('O código da série deve ser tipo string.')


        
# Registros de todos os temas cadastrados.
def temas(cod=None):
    if cod == None:
        return _query('Temas')
    elif isinstance(cod, int):
        return _query(f'Temas({cod})')
    else:
        raise TypeError('Código do tema deve ser um número inteiro.')



# Registros de todos os países cadastrados.
def paises(cod=None):
    if cod == None:
        return _query('Paises')
    elif isinstance(cod, str):
        return _query(f"Paises('{cod}')")
    else:
        raise TypeError('Código do país deve ser um string de três letras maísculas.')


        
# Registros de todos os territórios brasileiros cadastrados.
def territorios(cod=None, nivel=None):
    if (cod == None) and (nivel == None):
        return _query('Territorios')
    else:
        n = 'Municipios' if nivel == 'Municípios' else nivel        
        return _query(f"Territorios(TERCODIGO='{cod}',NIVNOME='{n}')")

    

# Lista dos possíveis níveis territoriais
def niveis_territoriais():
    return [
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
        'Estado/RM'
    ]