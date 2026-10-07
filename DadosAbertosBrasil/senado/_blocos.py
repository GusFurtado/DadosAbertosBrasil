from pydantic import validate_call

from ..utils import Get, Formato, Output


@validate_call
def lista_blocos(
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Output:
    """Obtém a lista e a composição dos Blocos Parlamentares no
    Congresso Nacional.

    Parameters
    ----------
    index : bool, default=False
        Se True, define a coluna `codigo` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'; com 'polars',
        é ignorado com aviso.

    formato : {"json", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado (pandas);
        - "polars": DataFrame formatado (polars);
        - "url": Endereço da API que retorna o arquivo JSON.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    pandas.core.frame.DataFrame | polars.DataFrame | str | dict | list[dict]
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
