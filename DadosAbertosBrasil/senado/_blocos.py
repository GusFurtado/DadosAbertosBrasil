from pydantic import validate_call

from ..utils import Get, Formato, Output


@validate_call
def lista_blocos(
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Obtém a lista e a composição dos Blocos Parlamentares no
    Congresso Nacional.

    Parameters
    ----------
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
        Lista de Blocos Parlamentares no Congresso Nacional.

    """

    cols_to_rename = {
        "CodigoBloco": "codigo",
        "NomeBloco": "nome",
        "NomeApelido": "apelido",
        "SiglaBloco": "sigla",
        "DataCriacao": "data_criacao",
    }

    return Get(
        endpoint="senado",
        path=["blocoParlamentar", "lista"],
        unpack_keys=["ListaBlocoParlamentar", "Blocos", "Bloco"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo"],
        cols_to_date=["data_criacao"],
        index=index,
        verify=verificar_certificado,
    ).get(formato)
