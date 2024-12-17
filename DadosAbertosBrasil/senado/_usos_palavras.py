from pydantic import validate_call

from ..utils import Get, Formato, Output


@validate_call
def lista_uso_palavra(
    ativos: bool = False,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Lista os tipos de uso da palavra.

    Parameters
    ----------
    ativos : bool, default=False
        Se True, retorna apenas os tipos de uso de palavra atualmente ativos.
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
        "Codigo": "codigo",
        "Sigla": "sigla",
        "Descricao": "descricao",
        "IndicadorAtivo": "ativo",
    }

    return Get(
        endpoint="senado",
        path=["senador", "lista", "tiposUsoPalavra"],
        params={"indAtivos": "S" if ativos else "N"},
        unpack_keys=["ListaTiposUsoPalavra", "TiposUsoPalavra", "TipoUsoPalavra"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo"],
        cols_to_bool=["ativo"],
        true_value="S",
        false_value="N",
        index=index,
        verify=verificar_certificado,
    ).get(formato)
