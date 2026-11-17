
from pydantic import Field, validate_call

from ..utils.modelos import com_params
from ..utils.typing import Formato, Saida
from . import modelos as m
from ._comum import ParamsSenado, consultar_senado


class _ParamsPartidos(ParamsSenado):
    inativos: bool = Field(False, exclude=True)

    def para_api(self) -> dict:
        return {"indAtivos": "N"} if self.inativos else {}


@validate_call
@com_params(_ParamsPartidos)
def lista_partidos(
    inativos: bool = False,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Lista os partidos políticos.

    Parameters
    ----------
    inativos : bool, default=False
        - True para incluir partidos inativos na lista.
        - False para listar apenas os partidos ativos.

    index : bool, default=False
        Se True, define a coluna `codigo` como index do DataFrame.
        Só se aplica ao formato 'pandas'; com 'polars', é ignorado com aviso.

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": JSON original da API, como veio;
        - "pydantic": lista de modelos Pydantic, um por registro;
        - "pandas": DataFrame pandas;
        - "polars": DataFrame polars;
        - "url": endereço da consulta.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
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

    return consultar_senado(
        ["senador", "partidos"],
        ["ListaPartidos", "Partidos", "Partido"],
        _ParamsPartidos.de_locais(locals()),
        m.Partido,
        formato,
        index=index,
        verificar_certificado=verificar_certificado,
        cacheavel=True,
    )
