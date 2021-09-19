'''Função que captura os dados das APIs.

Adiciona o endpoint, path e parâmetros do request e retorna um arquivo JSON.

'''
from typing import Union

import requests



def get_data(
        endpoint: str,
        path: Union[str, list],
        params: dict = None
    ) -> dict:
    '''Coleta os dados requisitados das APIs REST.

    Parâmetros
    ----------
    endpoint : str
        Diretório base da API desejada.
    path : list ou str
        Caminho de parâmetros para acessar a função desejada.
        Pode ser uma string de parâmetros unidos por barras '/' ou pode ser
        uma lista de strings na ordem correta. Os dois métodos produzem o
        mesmo resultado.
    params : dict (default=None)
        Dicionário de parâmetros de busca que serão enviados para o request.

    Retorna
    -------
    dict
        Dados brutos coletados da API.

    '''

    if isinstance(path, list):
        path = [str(p) for p in path]
        path = '/'.join(path)

    return requests.get(
        url = endpoint + path,
        headers = {'Accept':'application/json'},
        params = params
    ).json()