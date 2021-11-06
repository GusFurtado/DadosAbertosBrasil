"""Função que captura os dados das APIs.

Adiciona o endpoint, path e parâmetros do request e retorna um arquivo JSON.

"""

from typing import List, Optional, Union

import pandas as pd
import requests

from . import errors



_normalize = pd.io.json.json_normalize \
    if pd.__version__[0] == '0' else pd.json_normalize



def get_data(
        endpoint: str,
        path: Union[str, list],
        params: Optional[dict] = None
    ) -> dict:
    """Coleta os dados requisitados das APIs REST.

    Parameters
    ----------
    endpoint : str
        Diretório base da API desejada.
    path : list or str
        Caminho de parâmetros para acessar a função desejada.
        Pode ser uma string de parâmetros unidos por barras '/' ou pode ser
        uma lista de strings na ordem correta. Os dois métodos produzem o
        mesmo resultado.
    params : dict, optional
        Dicionário de parâmetros de busca que serão enviados para o request.

    Returns
    -------
    dict
        Dados brutos coletados da API.

    """

    if isinstance(path, list):
        path = [str(p) for p in path]
        path = '/'.join(path)

    return requests.get(
        url = endpoint + path,
        headers = {'Accept':'application/json'},
        params = params
    ).json()

"""
        return get_and_format(
            api = 'senado',
            path = ,
            params = params,
            unpack_keys = ,
            cols_to_rename = cols_to_rename,
            cols_to_int = ,
            cols_to_date = ,
            cols_to_bool = ,
            true_value = 'Sim',
            false_value = 'Não',
            index_col = 'codigo',
            index = index,
            formato = formato
        )
"""

def get_and_format(
        api: str,
        path: Union[str, list],
        params: Optional[dict] = None,
        unpack_keys: Optional[List[str]] = None,
        cols_to_rename: Optional[dict] = None,
        cols_to_int: Optional[List[str]] = None,
        cols_to_date: Optional[List[str]] = None,
        cols_to_bool: Optional[List[str]] = None,
        true_value: Optional[str] = None,
        false_value: Optional[str] = None,
        index_col: Optional[str] = None,
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[dict, pd.DataFrame]:

    ENDPOINTS = {
        'camara': 'https://dadosabertos.camara.leg.br/api/v2/',
        'senado': 'http://legis.senado.gov.br/dadosabertos/'
    }

    data = get_data(
        endpoint = ENDPOINTS[api],
        path = path,
        params = params
    )

    if unpack_keys is not None:
        for key in unpack_keys:
            if data is not None:
                if key in data:
                    data = data[key]
    if data is None:
        raise errors.DAB_InputError(
            'Nenhum dado encontrado. Verifique os parâmetros da consulta.'
        )

    if formato != 'dataframe':
        return data

    df = _normalize(data)
    df = df[[col for col in cols_to_rename.keys() if col in df.columns]]
    df.columns = df.columns.map(cols_to_rename)

    if isinstance(cols_to_int, list):
        for col in cols_to_int:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col],
                    errors = 'coerce',
                    downcast = 'integer'
                )

    if isinstance(cols_to_date, list):
        for col in cols_to_date:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])

    if isinstance(cols_to_bool, list):
        for col in cols_to_bool:
            if col in df.columns:
                df[col] = df[col].map({
                    true_value: True,
                    false_value: False
                })

    if index and (index_col is not None) and (not df.empty):
        df.set_index(index_col, inplace=True)

    return df
