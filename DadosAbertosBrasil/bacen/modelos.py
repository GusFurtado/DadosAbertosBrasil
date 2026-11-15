"""Modelos de saída do módulo `bacen`.

As expectativas de mercado mantêm os nomes de campo da API do Banco Central
(`Indicador`, `Data`, `Media`...), como nas colunas dos DataFrames do 2.x.

"""

from pydantic import Field, create_model

from ..utils.modelos import Data, Inteiro, Real, Registro, Texto

DataTipo = Data


class Moeda(Registro):
    """Moeda (`moedas`)."""

    simbolo: Texto = None
    nome: Texto = Field(None, validation_alias="nomeFormatado")
    tipo: Texto = Field(None, validation_alias="tipoMoeda")


class ValorSerie(Registro):
    """Valor de uma série temporal do SGS (`serie`)."""

    data: Data = None
    datafim: Data = Field(None, validation_alias="dataFim")
    valor: Real = None


_ESTATISTICAS = {campo: (Real, None) for campo in ("Media", "Mediana", "DesvioPadrao", "Minimo", "Maximo")}
_RESPONDENTES = {"numeroRespondentes": (Inteiro, None), "baseCalculo": (Inteiro, None)}


def _expectativa(nome: str, doc: str, antes: dict, depois: dict) -> type[Registro]:
    campos = {"Indicador": (Texto, None), **antes, **_ESTATISTICAS, **depois}
    return create_model(nome, __base__=Registro, __doc__=doc, **campos)


ExpectativaAnual = _expectativa(
    "ExpectativaAnual",
    'Expectativa anual (`expectativas("anual")`).',
    {"IndicadorDetalhe": (Texto, None), "Data": (DataTipo, None), "DataReferencia": (Texto, None)},
    _RESPONDENTES,
)
ExpectativaInflacao = _expectativa(
    "ExpectativaInflacao",
    'Expectativa de inflação em 12 meses (`expectativas("inflacao")`).',
    {"Data": (DataTipo, None), "Suavizada": (Texto, None)},
    _RESPONDENTES,
)
ExpectativaMensal = _expectativa(
    "ExpectativaMensal",
    'Expectativa mensal (`expectativas("mensal")`).',
    {"Data": (DataTipo, None), "DataReferencia": (Texto, None)},
    _RESPONDENTES,
)
ExpectativaSelic = _expectativa(
    "ExpectativaSelic",
    'Expectativa da Selic por reunião do Copom (`expectativas("selic")`).',
    {"Data": (DataTipo, None), "Reuniao": (Texto, None)},
    _RESPONDENTES,
)
ExpectativaTop5 = _expectativa(
    "ExpectativaTop5",
    'Expectativa Top 5 (`expectativas("top5anual")` e `expectativas("top5mensal")`).',
    {"Data": (DataTipo, None), "DataReferencia": (Texto, None), "tipoCalculo": (Texto, None)},
    {},
)
ExpectativaTrimestral = _expectativa(
    "ExpectativaTrimestral",
    'Expectativa trimestral (`expectativas("trimestral")`).',
    {"Data": (DataTipo, None), "DataReferencia": (Texto, None)},
    _RESPONDENTES,
)


class Cotacao(Registro):
    """Cotação de uma moeda numa data (`cambio`).

    A tabela de `cambio` tem a coluna `data` e uma coluna por moeda; o modelo
    de cada consulta é criado com `modelo_cambio`.
    """

    data: Data = None


def modelo_cambio(moedas: list[str]) -> type[Cotacao]:
    """Modelo com a coluna `data` e uma coluna `Real` por moeda."""
    return create_model("Cotacao", __base__=Cotacao, **{moeda: (Real, None) for moeda in moedas})
