from pydantic import validate_call

from ..utils import Get, Formato, Output


@validate_call
def moedas(
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Obtém os nomes e símbolos das principais moedas internacionais.

    Parameters
    ----------
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

    data = Get(
        endpoint="bacen",
        path=["Moedas"],
        unpack_keys=["value"],
        verify=verificar_certificado,
    ).get(formato)

    if formato == "pandas":
        data.columns = ["simbolo", "nome", "tipo"]

    return data
