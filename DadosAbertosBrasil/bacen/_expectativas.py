from typing import Optional

from pydantic import validate_call, PositiveInt

from ..utils import Get, Expectativa, Formato, Output


@validate_call
def expectativas(
    expectativa: Expectativa,
    indicador: Optional[str] = None,
    top: Optional[PositiveInt] = None,
    ordenar_por: str = "Data",
    asc: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Expectativas de mercado para os principais indicadores macroeconômicos.

    Parameters
    ----------
    expectativa : str
        - "mensal": Expectativas de Mercado Mensal
        - "selic": Expectativas de Mercado Selic
        - "trimestral": Expectativas de Mercado Trimestral
        - "anual": Expectativas de Mercado com referência anual
        - "inflacao": Expectativas de mercado para inflação nos próximos 12 meses
        - "top5mensal": Expectativas mensais de mercado para os indicadores do Top 5
        - "top5anual": Expectativas de mercado anuais para os indicadores do Top 5
        - "instituicoes": Expectativas de mercado informadas pelas instituições credenciadas

    indicador : str, optional
        Capturar apenas o indicador desejado. Deve ser um dos seguintes
        indicadores, desde que esteja de acordo com a `expectativa` escolhida.
        Caso o valor seja `None`, retorna todos os indicadores disponíveis:
        - "Balança Comercial",
        - "Câmbio",
        - "Conta corrente",
        - "Dívida bruta do governo geral",
        - "Dívida líquida do setor público",
        - "IGP-DI",
        - "IGP-M",
        - "INPC",
        - "Investimento direto no país",
        - "IPA-DI",
        - "IPA-M",
        - "IPCA",
        - "IPCA Administrados",
        - "IPCA Alimentação no domicílio",
        - "IPCA Bens industrializados",
        - "IPCA Livres",
        - "IPCA Serviços",
        - "IPCA-15",
        - "IPC-FIPE",
        - "PIB Agropecuária",
        - "PIB Despesa de consumo da administração pública",
        - "PIB despesa de consumo das famílias",
        - "PIB Exportação de bens e serviços",
        - "PIB Formação Bruta de Capital Fixo",
        - "PIB Importação de bens e serviços",
        - "PIB Indústria",
        - "PIB Serviços",
        - "PIB Total",
        - "Produção industrial",
        - "Resultado nominal",
        - "Resultado primário",
        - "Selic",
        - "Taxa de desocupação".

    top : int, optional
        Número máximo de registros que será retornado.

    ordenar_por : str, default='Data'
        Por qual coluna da tabela os registros serão ordenados.

    asc : bool, default=False
        - Se True, ordena os registros pela coluna selecionada no argumento
          `ordenar_por` em ordem crescente (A-Z ou 0-9);
        - Se False, ordena em ordem descrescente (Z-A ou 9-0).

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
        Breve estatística descritiva da expectativa de mercado de cada
        indicador por período de referência.

    Raises
    ------
    ValueError
        Em caso de parâmetros inválidos.

    Notes
    -----
    API original de expectativas de mercado
        https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/swagger-ui3#/

    Base de Cálculo 0:
        Uso das expectativas mais recentes informadas pelas instituições
        participantes a partir do 30º dia anterior à data de cálculo das
        estatísticas.

    Base de Cálculo 1:
        Uso das expectativas mais recentes informadas pelas instituições
        participantes a partir do 4º dia útil anterior à data de cálculo
        das estatísticas.

    Examples
    --------
    >>> bacen.expectativa(expectativa='mensal', indicador='IGP-M')
          Indicador        Data DataReferencia  Media  Mediana  DesvioPadrao  ...
    0         IGP-M  2021-06-25        07/2022   0.31     0.30          0.21  ...
    1         IGP-M  2021-06-25        07/2021   0.64     0.61          0.42  ...
    2         IGP-M  2021-06-25        06/2021   1.25     1.10          0.58  ...
    3         IGP-M  2021-06-25        11/2022   0.47     0.47          0.16  ...
    4         IGP-M  2021-06-25        11/2021   0.50     0.50          0.24  ...
    ..          ...         ...            ...    ...      ...           ...  ...

    >>> bacen.expectativa(
    ...     expectativa = 'trimestral',
    ...     indicador = 'PIB Total',
    ...     top = 3,
    ...     ordenar_por = 'Media',
    ...     asc = True
    ... )
       Indicador        Data DataReferencia  Media  Mediana  DesvioPadrao  ...
    0  PIB Total  2020-06-02         2/2020 -14.00    -14.0          3.92  ...
    1  PIB Total  2020-06-09         2/2020 -14.00    -13.4          3.55  ...
    2  PIB Total  2020-06-01         2/2020 -13.99    -14.0          3.91  ...

    """

    order_by = f'&%24orderby={ordenar_por}%20{"asc" if asc else "desc"}'
    top_n = "" if top is None else f"&%24top={top}"

    match expectativa:
        case "anual":
            expec = "ExpectativasMercadoAnuais"
            KPIS = (
                "Balança Comercial",
                "Câmbio",
                "Conta corrente",
                "Dívida bruta do governo geral",
                "Dívida líquida do setor público",
                "IGP-DI",
                "IGP-M",
                "INPC",
                "Investimento direto no país",
                "IPA-DI",
                "IPA-M",
                "IPCA",
                "IPCA Administrados",
                "IPCA Alimentação no domicílio",
                "IPCA Bens industrializados",
                "IPCA Livres",
                "IPCA Serviços",
                "IPCA-15",
                "IPC-FIPE",
                "PIB Agropecuária",
                "PIB Despesa de consumo da administração pública",
                "PIB despesa de consumo das famílias",
                "PIB Exportação de bens e serviços",
                "PIB Formação Bruta de Capital Fixo",
                "PIB Importação de bens e serviços",
                "PIB Indústria",
                "PIB Serviços",
                "PIB Total",
                "Produção industrial",
                "Resultado nominal",
                "Resultado primário",
                "Selic",
                "Taxa de desocupação",
            )

        case "inflacao":
            expec = "ExpectativasMercadoInflacao12Meses"
            KPIS = (
                "IGP-DI",
                "IGP-M",
                "INPC",
                "IPA-DI",
                "IPA-M",
                "IPCA",
                "IPCA Administrados",
                "IPCA Alimentação no domicílio",
                "IPCA Bens industrializados",
                "IPCA Livres",
                "IPCA Serviços",
                "IPCA-15",
                "IPC-FIPE",
            )

        case "instituicoes":
            expec = "ExpectativasMercadoInstituicoes"
            KPIS = (
                "Balança Comercial",
                "Câmbio",
                "Conta corrente",
                "Dívida bruta do governo geral",
                "Dívida líquida do setor público",
                "IGP-DI",
                "IGP-M",
                "INPC",
                "Investimento direto no país",
                "IPA-DI",
                "IPA-M",
                "IPCA",
                "IPCA Administrados",
                "IPCA Alimentação no domicílio",
                "IPCA Bens industrializados",
                "IPCA Livres",
                "IPCA Serviços",
                "IPCA-15",
                "IPC-FIPE",
                "PIB Agropecuária",
                "PIB Despesa de consumo da administração pública",
                "PIB despesa de consumo das famílias",
                "PIB Exportação de bens e serviços",
                "PIB Formação Bruta de Capital Fixo",
                "PIB Importação de bens e serviços",
                "PIB Indústria",
                "PIB Serviços",
                "PIB Total",
                "Produção industrial",
                "Resultado nominal",
                "Resultado primário",
                "Selic",
                "Taxa de desocupação",
            )

        case "mensal":
            expec = "ExpectativaMercadoMensais"
            KPIS = (
                "Câmbio",
                "IGP-DI",
                "IGP-M",
                "INPC",
                "IPA-DI",
                "IPA-M",
                "IPCA",
                "IPCA Administrados",
                "IPCA Alimentação no domicílio",
                "IPCA Bens industrializados",
                "IPCA Livres",
                "IPCA Serviços",
                "IPCA-15",
                "IPC-Fipe",
                "Produção industrial",
                "Selic",
                "Taxa de desocupação",
            )

        case "selic":
            expec = "ExpectativasMercadoSelic"
            KPIS = ("Selic",)

        case "top5anual":
            expec = "ExpectativasMercadoTop5Anuais"
            KPIS = ("Câmbio", "IGP-DI", "IGP-M", "IPCA", "Selic")

        case "top5mensal":
            expec = "ExpectativasMercadoTop5Mensais"
            KPIS = ("Câmbio", "IGP-DI", "IGP-M", "IPCA", "Selic")

        case "trimestral":
            expec = "ExpectativasMercadoTrimestrais"
            KPIS = (
                "Câmbio",
                "IPCA",
                "IPCA Administrados",
                "IPCA Alimentação no domicílio",
                "IPCA Bens industrializados",
                "IPCA Livres",
                "IPCA Serviços",
                "PIB Agropecuária",
                "PIB Indústria",
                "PIB Serviços",
                "PIB Total",
                "Taxa de desocupação",
            )

    if indicador is None:
        kpi = ""
    elif indicador in KPIS:
        kpi = f"&%24filter=Indicador%20eq%20'{indicador}'"
    else:
        raise ValueError(
            f"""'{indicador}' é um indicador inválido para expectativa '{expectativa.title()}'. Insira um dos seguintes valores:
        - {", ".join(KPIS)}."""
        )

    data = Get(
        endpoint="expectativas",
        path=[f"{expec}?%24format=json{order_by}{kpi}{top_n}"],
        unpack_keys=["value"],
        verify=verificar_certificado,
    )
    return data.get(formato)
