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
        url_cols: Optional[List[str]] = None,
        url: bool = True,
        index_col: str = 'codigo',
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[dict, pd.DataFrame]:
    """Função padrão para coleta e formatação de dados JSON.

    Parameters
    ----------
    api : {'camara', 'senado'}
        Seleciona o endpoint da API desejada.
    path : str or list of str
        Diretório dos dados a partir do endpoint.
    params : dict, optional
        Parâmetros do request HTTP.
    unpack_keys : list of str, optional
        Lista de chaves do arquivo JSON para acessar os dados relevantes.
    cols_to_rename : dict, optional
        Colunas que serão renomeadas.
    cols_to_int : list of str, optional
        Lista de colunas que serão convertidas em `int`.
    cols_to_date : list of str, optional
        Lista de colunas que serão convertidas em `datetime`.
    cols_to_bool : list of str, optional
        Lista de colunas que serão convertidas em `bool`.
    true_value : str, optional
        Valor que será convertido para `True` nas colunas listadas pelo
        argumento `cols_to_bool`.
    false_value : str, optional
        Valor que será convertido para `False` nas colunas listadas pelo
        argumento `cols_to_bool`.
    url_cols : list of str, optional
        Lista das colunas que serão removidas ou não pelo argumento `url`.
    url : bool, default=True
        Retorna ou não as colunas contendo URI, URL ou e-mails.
    index_col : str, default='codigo'
        Nome da coluna que será o index do DataFrame, caso o argumento `index`
        seja igual a `True`.
    index : bool, default=False
        Se True, define a coluna de `index_col` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'.
    formato : {'dataframe', 'json'}, default='dataframe'
        Formato do dado que será retornado.
        Os dados no formato 'json' são mais completos, porém alguns filtros
        podem não ser aplicados.

    Returns
    -------
    pandas.core.frame.DataFrame
        Se formato = 'dataframe', retorna os dados formatados em uma tabela.
    list of dict
        Se formato = 'json', retorna os dados brutos no formato json.

    Raises
    ------
    DadosAbertosBrasil._utils.errors.DAB_InputError
        Caso nenhum dado seja encontrado.
    
    """

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

    if not url:
        df.drop(columns=url_cols, inplace=True)

    if index and (not df.empty):
        df.set_index(index_col, inplace=True)

    return df



class DAB_Base:
    """Base para os objetos DadosAbertosBrasil.

    Parameters
    ----------
    api : {'camara', 'senado'}
        Referência da API que será consultada.
    path : str or list of str
        Argumentos da consulta via URL.
    unpack_keys : str or list of str
        Lista de keys do arquivo JSON onde estão os dados.
    error_key : str
        Key que deve estar contida no arquivo JSON.
    atributos : dict[str, str]
        Dicionário de atributos e respectivos unpack_keys.

    Attributes
    ----------
    dados : dict
        Arquivo JSON em seu formato bruto.

    Raises
    ------
    DadosAbertosBrasil._utils.errors.DAB_InputError
        Quando os dados do Senador não forem encontrado, por qualquer que seja
        o motivo.

    """

    def __init__(
            self,
            api: str,
            path: Union[str, List[str]],
            unpack_keys: Union[str, List[str]],
            error_key: str,
            atributos: dict
        ):

        self.dados = get_and_format(
            api = api,
            path = path,
            unpack_keys = unpack_keys,
            formato = 'json'
        )

        if error_key not in self.dados:
            raise errors.DAB_InputError('Dados não encontrados.')

        for attr in atributos:
            self._set_attribute(attr, atributos)


    def _set_attribute(self, attr:str, attr_dict:dict) -> None:
        """Converte os dados JSON em atributos para o objeto.

        Parameters
        ----------
        attr : str
            Nome do atributo.
        attr_dict : dict
            Dicionário de atributos (JSON).
        
        """

        x = self.dados
        try:
            for key in attr_dict[attr]:
                x = x[key]
            setattr(self, attr, x)
        except (KeyError, TypeError):
            return
