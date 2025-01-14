from pydantic import validate_call

from ..utils import Get, Formato, Output


@validate_call
def lista_partidos(
    inativos: bool = False,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Lista os partidos políticos.

    Parameters
    ----------
    inativos : bool, default=False
        - True para incluir partidos inativos na lista.
        - False para listar apenas os partidos ativos.

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
        Lista os partidos políticos.

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

    return Get(
        endpoint="senado",
        path=["senador", "partidos"],
        params={"indAtivos": "N"} if inativos else {},
        unpack_keys=["ListaPartidos", "Partidos", "Partido"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo"],
        cols_to_date=["data_criacao", "data_extincao"],
        index=index,
        verify=verificar_certificado,
    ).get(formato)
