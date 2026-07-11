import json
from functools import cached_property
from typing import Literal

import pandas as pd
import requests
from pydantic import BaseModel
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .endpoints import ENDPOINTS
from .errors import DAB_InputError
from .typing import Formato, Output


class Get(BaseModel):
    """Função padrão para coleta e formatação de dados JSON.

    Parameters
    ----------
    endpoint : str
        Seleciona o endpoint da API desejada.
        Consultar `_utils.endpoints.ENDPOINTS`.
    path : list[str]
        Diretório dos dados a partir do endpoint.
    params : dict, optional
        Parâmetros do request HTTP.
    unpack_keys : list[str], optional
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
    url : bool, default=True
        Retorna ou não as colunas contendo URI, URL ou e-mails.
    url_cols : list of str, optional
        Lista das colunas que serão removidas ou não pelo argumento `url`.
    index : bool, default=False
        Se True, define a coluna de `index_col` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'.
    index_col : str, default='codigo'
        Nome da coluna que será o index do DataFrame, caso o argumento `index`
        seja igual a `True`.
    timeout : int, default=30
        Timeout em segundos para a requisição HTTP.

    """

    # url
    endpoint: str
    path: list[str]

    # json
    params: dict | None = None
    verify: bool = True
    unpack_keys: list[str] | None = None
    timeout: int = 30

    # pandas
    cols_to_rename: dict | None = None
    cols_to_int: list[str] | None = None
    cols_to_date: list[str] | None = None
    cols_to_bool: list[str] | None = None
    true_value: str | None = None
    false_value: str | None = None
    remover_url: bool = False
    url_cols: list[str] | None = None
    index: bool = False
    index_col: str = "codigo"

    @cached_property
    def _session(self) -> requests.Session:
        """Cria uma sessão HTTP com retry adapters."""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        session.headers.update({"Accept": "application/json"})
        return session

    @cached_property
    def url(self) -> str:
        endpoint = ENDPOINTS.get(self.endpoint, self.endpoint)
        path = "/".join(self.path)
        return endpoint + path

    @cached_property
    def json(self) -> dict:
        response = self._session.get(
            url=self.url,
            params=self.params,
            verify=self.verify,
            timeout=self.timeout,
        )
        response.raise_for_status()

        data = response.json()

        if isinstance(data, str):
            data = json.loads(data)

        if self.unpack_keys is not None:
            for key in self.unpack_keys:
                if data is not None and key in data:
                    data = data[key]
        if data is None:
            raise DAB_InputError(
                "Nenhum dado encontrado. Verifique os parâmetros da consulta."
            )

        return data

    @cached_property
    def pandas(self) -> pd.DataFrame:
        df = pd.json_normalize(self.json)

        if self.cols_to_rename is not None:
            df = df[[col for col in self.cols_to_rename if col in df.columns]]
            df.columns = df.columns.map(self.cols_to_rename)

        if self.cols_to_int is not None:
            for col in self.cols_to_int:
                if col in df.columns:
                    df[col] = pd.to_numeric(
                        df[col], errors="coerce", downcast="integer"
                    )

        if self.cols_to_date is not None:
            for col in self.cols_to_date:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col])

        if self.cols_to_bool is not None:
            for col in self.cols_to_bool:
                if col in df.columns:
                    df[col] = df[col].map(
                        {self.true_value: True, self.false_value: False}
                    )

        if self.remover_url:
            df.drop(columns=self.url_cols, inplace=True)

        if self.index and (not df.empty):
            df.set_index(self.index_col, inplace=True)

        return df

    def get(self, formato: Formato = "pandas") -> Output:
        match formato:
            case "json":
                return self.json
            case "pandas":
                return self.pandas
            case "url":
                return self.url


class Base:
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
    atributos : dict[str, list[str]]
        Dicionário de atributos e respectivos unpack_keys.
    verify : bool, default=True
        Defina como False em caso de falha na verificação do certificado SSL.

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
        endpoint: Literal["camara", "senado"],
        path: list[str],
        unpack_keys: list[str],
        error_key: str,
        atributos: dict[str, list[str]],
        verify: bool = True,
    ):
        self.dados = Get(
            endpoint=endpoint,
            path=path,
            unpack_keys=unpack_keys,
            verify=verify,
        ).json

        if error_key not in self.dados:
            raise DAB_InputError("Dados não encontrados.")

        for attr in atributos:
            self._set_attribute(attr, atributos)

    def _set_attribute(self, attr: str, attr_dict: dict) -> None:
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
