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

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        Lista os tipos de uso da palavra.

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
