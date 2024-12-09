from typing import Literal

import pandas as pd
from pydantic import validate_call

from .._utils.get_data import get_and_format


@validate_call
def lista_partidos(
    inativos: bool = False,
    index: bool = False,
    formato: Literal["dataframe", "json"] = "dataframe",
) -> pd.DataFrame | list[dict]:
    """Lista os partidos políticos.

    Parameters
    ----------
    inativos : bool, default=False
        - True para incluir partidos inativos na lista.
        - False para listar apenas os partidos ativos.
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

    See Also
    --------
    DadosAbertosBrasil.camara.lista_partidos
        Função semelhante do módulo `camara`.

    Examples
    --------
    Capturar todos os partidos, incluindo inativos.
    
    >>> senado.lista_partido(inativos=True)
       codigo          sigla                          nome data_criacao \
    0     525            ANL  Aliança Nacional Libertadora   1935-01-01   
    1     238          ARENA   Aliança Renovadora Nacional   1965-11-24   
    2     578         AVANTE                        AVANTE   2017-09-12

    """

    cols_to_rename = {
        "Codigo": "codigo",
        "Sigla": "sigla",
        "Nome": "nome",
        "DataCriacao": "data_criacao",
        "DataExtincao": "data_extincao",
    }

    return get_and_format(
        api="senado",
        path=["senador", "partidos"],
        params={"indAtivos": "N"} if inativos else {},
        unpack_keys=["ListaPartidos", "Partidos", "Partido"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo"],
        cols_to_date=["data_criacao", "data_extincao"],
        index=index,
        formato=formato,
    )
