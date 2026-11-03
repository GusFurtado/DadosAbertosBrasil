from typing import Optional

from pydantic import Field, PositiveInt, validate_call

from ..utils.errors import DABInputError
from ..utils.modelos import Params, com_params
from ..utils.requisicao import Requisicao
from ..utils.saida import consultar
from ..utils.typing import Expectativa, Formato, Saida
from . import modelos as m

_COMUNS = (
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
)

_ANUAIS = (
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

# expectativa: (conjunto de dados na API, modelo, indicadores válidos)
_EXPECTATIVAS = {
    "anual": ("ExpectativasMercadoAnuais", m.ExpectativaAnual, _ANUAIS),
    "inflacao": ("ExpectativasMercadoInflacao12Meses", m.ExpectativaInflacao, _COMUNS[1:] + ("IPC-FIPE",)),
    "mensal": (
        "ExpectativaMercadoMensais",
        m.ExpectativaMensal,
        _COMUNS + ("IPC-Fipe", "Produção industrial", "Selic", "Taxa de desocupação"),
    ),
    "selic": ("ExpectativasMercadoSelic", m.ExpectativaSelic, ("Selic",)),
    "top5anual": ("ExpectativasMercadoTop5Anuais", m.ExpectativaTop5, ("Câmbio", "IGP-DI", "IGP-M", "IPCA", "Selic")),
    "top5mensal": ("ExpectativasMercadoTop5Mensais", m.ExpectativaTop5, ("Câmbio", "IGP-DI", "IGP-M", "IPCA", "Selic")),
    "trimestral": (
        "ExpectativasMercadoTrimestrais",
        m.ExpectativaTrimestral,
        (
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
        ),
    ),
}


class _ParamsExpectativas(Params):
    expectativa: Expectativa = Field(exclude=True)
    indicador: str | None = Field(None, exclude=True)
    top: PositiveInt | None = Field(None, serialization_alias="$top")
    ordenar_por: str = Field("Data", exclude=True)
    asc: bool = Field(False, exclude=True)

    def para_api(self) -> dict:
        params = {"$format": "json", "$orderby": f"{self.ordenar_por} {'asc' if self.asc else 'desc'}"}
        if self.indicador is not None:
            params["$filter"] = f"Indicador eq '{self.indicador}'"
        return params | super().para_api()


@validate_call
@com_params(_ParamsExpectativas)
def expectativas(
    expectativa: Expectativa,
    indicador: Optional[str] = None,
    top: Optional[PositiveInt] = None,
    ordenar_por: str = "Data",
    asc: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
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

    conjunto, modelo, indicadores = _EXPECTATIVAS[expectativa]
    if indicador is not None and indicador not in indicadores:
        raise DABInputError(
            f"'{indicador}' é um indicador inválido para a expectativa '{expectativa}'. "
            f"Insira um dos seguintes valores: {', '.join(indicadores)}."
        )
    return consultar(
        Requisicao(
            "expectativas",
            [conjunto],
            _ParamsExpectativas.de_locais(locals()).para_api(),
            chaves=["value"],
            verificar_certificado=verificar_certificado,
        ),
        modelo,
        formato,
        index_col=None,
    )
