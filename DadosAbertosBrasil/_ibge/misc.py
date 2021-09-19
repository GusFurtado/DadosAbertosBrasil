'''Submódulo IBGE contendo funções diversas.

Este submódulo é importado automaticamente com o módulo `ibge`.

>>> from DadosAbertosBrasil import ibge

'''
from typing import Union

import pandas as _pd
import requests

from DadosAbertosBrasil._utils import parse



_normalize = _pd.io.json.json_normalize \
    if _pd.__version__[0] == '0' else _pd.json_normalize



def populacao(
        projecao: str = None,
        localidade: int = None
    ) -> Union[dict, int]:
    '''Obtém a projecao da população referente ao Brasil.

    Parâmetros
    ----------
    projecao : str (default=None)
        - 'populacao' obtém o valor projetado da população total da localidade;
        - 'nascimento' obtém o valor projetado de nascimentos da localidade
        - 'obito' obtém o valor projetado de óbitos da localidade;
        - 'incremento' obtém o incremento populacional projetado.
        - None obtém um dicionário com todos os valores anteriores.
    localidade : int (default=None)
        Código da localidade desejada.
        Por padrão, obtém os valores do Brasil.
        Utilize a função `ibge.localidades` para identificar
        a localidade desejada.

    Retorna
    -------
    dict ou int:
        Valor(es) projetado(s) para o indicador escolhido.

    Erros
    -----
    DAB_LocalidadeError
        Caso código da localidade seja inválido.
    ValueError
        Caso o argumento `projecao` seja inválido.

    Exemplos
    --------
    Projeção de óbito do Brasil.

    >>> ibge.populacao('obito')
    45000

    Obter dados do Rio de Janeiro (localidade 33)

    >>> ibge.populacao(localidade=33)
    {
        'localidade': '33',
        'horario': '03/07/2021 19:15:48',
        'projecao': {
            'populacao': 17459953,
            'periodoMedio': {
                'incrementoPopulacional': 330508
            }
        }
    }

    '''

    localidade = parse.localidade(localidade, '')
    query = f'https://servicodados.ibge.gov.br/api/v1/projecoes/populacao/{localidade}'
            
    r = requests.get(query).json()
    
    if projecao == None:
        return r
    elif projecao == 'populacao':
        return r['projecao']['populacao']
    elif projecao == 'nascimento':
        return r['projecao']['periodoMedio']['nascimento']
    elif projecao == 'obito':
        return r['projecao']['periodoMedio']['obito']
    elif projecao == 'incremento':
        return r['projecao']['periodoMedio']['incrementoPopulacional']
    else:
        raise ValueError('''O argumento 'projecao' deve ser um dos seguintes valores tipo string:
            - 'populacao';
            - 'nascimento';
            - 'obito';
            - 'incremento'.''')



def _loc_columns(x: str) -> str:
    '''Função de suporte à função `ibge.localidades`.
    Usada para renomear as colunas do DataFrame de distritos.
    
    '''

    y = x.replace('-', '_').split('.')
    return f'{y[-2]}_{y[-1]}' if len(y)>1 else y[0]



def localidades() -> _pd.DataFrame:
    '''Obtém o conjunto de distritos do Brasil.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame contendo todas as divisões de distritos do Brasil.

    Exemplos
    --------
    >>> ibge.localidades()
                  id                 nome  municipio_id       municipio_nome  \
    0      520005005      Abadia de Goiás       5200050      Abadia de Goiás  \
    1      310010405  Abadia dos Dourados       3100104  Abadia dos Dourados  \
    2      520010005            Abadiânia       5200100            Abadiânia  \
    3      520010010       Posse d'Abadia       5200100            Abadiânia  \
    4      310020305               Abaeté       3100203               Abaeté  \
    ..           ...                  ...           ...                  ...

    '''

    df = _normalize(
        requests.get(
            r'https://servicodados.ibge.gov.br/api/v1/localidades/distritos'
        ).json()
    )

    df.columns = df.columns.map(_loc_columns)
    return df.loc[:,~df.columns.duplicated()]



def malha(localidade:int=None) -> str:
    '''Obtém a URL para a malha referente ao identificador da localidade.

    Parâmetros
    ----------
    localidade : int (default=None)
        Código da localidade desejada.
        Por padrão, obtém a malha do Brasil.
        Utilize a função `ibge.localidades` para identificar
        a localidade desejada.

    Retorna
    -------
    str
        URL da malha da localidade desejada.

    Erros
    -----
    DAB_LocalidadeError
        Caso o código da localidade seja inválido.

    Exemplos
    --------
    >>> ibge.malha(localidade=4209102)
    https://servicodados.ibge.gov.br/api/v2/malhas/4209102

    '''

    localidade = parse.localidade(localidade, '')
    return f'https://servicodados.ibge.gov.br/api/v2/malhas/{localidade}'



def coordenadas() -> _pd.DataFrame:
    '''Obtém as coordenadas de todas as localidades brasileiras, incluindo
    latitude, longitude e altitude.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame das coordenadas de todas as localidade brasileiras.

    Exemplos
    --------
    >>> ibge.coordenadas()
           GM_PONTO     ID     CD_GEOCODIGO    TIPO   CD_GEOCODBA NM_BAIRRO  \
    0           NaN      1  110001505000001  URBANO  1.100015e+11   Redondo  \
    1           NaN      2  110001515000001  URBANO           NaN       NaN  \
    2           NaN      3  110001520000001  URBANO           NaN       NaN  \
    3           NaN      4  110001525000001  URBANO           NaN       NaN  \
    4           NaN      5  110001530000001  URBANO           NaN       NaN  \
    ..          ...     ..              ...     ...           ...       ...  \

    '''

    return _pd.read_csv(
        r'https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/data/coordenadas.csv',
        sep = ';'
    )
