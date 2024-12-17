from pydantic import validate_call

from ..utils import Get, Formato, Output


@validate_call
def referencias(
    lista: str,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Listas de valores válidos para as funções deste módulo.

    Parameters
    ----------
    lista : str
        Referências que serão listadas. Deve ser uma destas opções:
            - 'autores'
            - 'temas'
            - 'eventos'
            - 'orgaos'
            - 'proposicoes'
            - 'tramitacoes'
            - 'ufs'
            - 'situacoes_deputados'
            - 'situacoes_eventos'
            - 'situacoes_orgaos'
            - 'situacoes_proposicoes'
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

    referencia = {
        "autores": "proposicoes/codTipoAutor",
        "temas": "proposicoes/codTema",
        "eventos": "tiposEvento",
        "orgaos": "tiposOrgao",
        "proposicoes": "tiposProposicao",
        "tramitacoes": "tiposTramitacao",
        "ufs": "uf",
        "situacoes_deputados": "situacoesDeputado",
        "situacoes_eventos": "situacoesEvento",
        "situacoes_orgaos": "situacoesOrgao",
        "situacoes_proposicoes": "situacoesProposicao",
    }

    if lista not in referencia.keys():
        raise TypeError(
            "Referência inválida. Insira um dos seguintes valores para `lista`: "
            + ", ".join(list(referencia.keys()))
        )

    cols_to_rename = {
        "cod": "codigo",
        "sigla": "sigla",
        "nome": "nome",
        "descricao": "descricao",
    }

    return Get(
        endpoint="camara",
        path=["referencias", referencia[lista]],
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        index=index,
        verify=verificar_certificado,
    ).get(formato)
