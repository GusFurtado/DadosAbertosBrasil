from pydantic import validate_call

from ..utils.requisicao import Requisicao
from ..utils.saida import consultar
from ..utils.typing import Formato, Saida
from . import modelos as m


@validate_call
def moedas(
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Obtém os nomes e símbolos das principais moedas internacionais.

    Parameters
    ----------
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
        Nomes e símbolos das principais moedas internacionais.

    See Also
    --------
    DadosAbertosBrasil.bacen.cambio
        Utilize a função `bacen.moedas` para identificar os argumentos da
        função `bacen.cambio`.

    Notes
    -----
    API original das cotações de câmbio
        https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3

    Moedas do tipo 'A':
        - Para calcular o valor equivalente em US$ (dólar americano), divida o
          montante na moeda consultada pela respectiva paridade.
        - Para obter o valor em R$ (reais), multiplique o montante na moeda
          consultada pela respectiva taxa.

    Moedas do tipo 'B':
        - Para calcular o valor equivalente em US$ (dólar americano),
          multiplique o montante na moeda consultada pela respectiva paridade.
        - Para obter o valor em R$ (reais), multiplique o montante na moeda
          consultada pela respectiva taxa.

    Examples
    --------
    >>> bacen.moedas()
      simbolo                      nome tipo
    0     AUD         Dólar australiano    B
    1     CAD           Dólar canadense    A
    2     CHF              Franco suíço    A
    3     DKK        Coroa dinamarquesa    A
    4     EUR                      Euro    B
    5     GBP           Libra Esterlina    B
    6     JPY                      Iene    A
    7     NOK          Coroa norueguesa    A
    8     SEK               Coroa sueca    A
    9     USD  Dólar dos Estados Unidos    A

    """

    return consultar(
        Requisicao("bacen", ["Moedas"], chaves=["value"], verificar_certificado=verificar_certificado, cacheavel=True),
        m.Moeda,
        formato,
        index_col=None,
    )
