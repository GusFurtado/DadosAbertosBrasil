from typing import Literal

import pandas as pd
from pydantic import validate_call

from .._utils.get_data import get_and_format


@validate_call
def lista_blocos(
    index: bool = False,
    formato: Literal["dataframe", "json"] = "dataframe",
) -> pd.DataFrame | list[dict]:
    """Obtém a lista e a composição dos Blocos Parlamentares no
    Congresso Nacional.

    Parameters
    ----------
    index : bool, default=False
        Se True, define a coluna `codigo` como index do DataFrame.
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

    """

    cols_to_rename = {
        "CodigoBloco": "codigo",
        "NomeBloco": "nome",
        "NomeApelido": "apelido",
        "SiglaBloco": "sigla",
        "DataCriacao": "data_criacao",
    }

    return get_and_format(
        api="senado",
        path=["blocoParlamentar", "lista"],
        unpack_keys=["ListaBlocoParlamentar", "Blocos", "Bloco"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo"],
        cols_to_date=["data_criacao"],
        index=index,
        formato=formato,
    )
