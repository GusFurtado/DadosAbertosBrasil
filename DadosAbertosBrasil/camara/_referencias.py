from typing import Literal

from pydantic import validate_call

from ..utils.typing import Formato, Saida
from . import modelos as m
from ._comum import consultar_camara

_REFERENCIAS = {
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


@validate_call
def referencias(
    lista: Literal[
        "autores",
        "temas",
        "eventos",
        "orgaos",
        "proposicoes",
        "tramitacoes",
        "ufs",
        "situacoes_deputados",
        "situacoes_eventos",
        "situacoes_orgaos",
        "situacoes_proposicoes",
    ],
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Listas de valores válidos para as funções deste módulo.

    Parameters
    ----------
    lista : str
        Referências que serão listadas. Deve ser uma destas opções:
        - "autores"
        - "temas"
        - "eventos"
        - "orgaos"
        - "proposicoes"
        - "tramitacoes"
        - "ufs"
        - "situacoes_deputados"
        - "situacoes_eventos"
        - "situacoes_orgaos"
        - "situacoes_proposicoes"

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
        Listas de valores válidos para as funções deste módulo.

    """

    return consultar_camara(
        ["referencias", _REFERENCIAS[lista]],
        None,
        m.Referencia,
        formato,
        index=index,
        verificar_certificado=verificar_certificado,
        cacheavel=True,
    )
