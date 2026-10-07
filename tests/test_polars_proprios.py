import datetime as dt

import pandas as pd
import polars as pl
import pytest
import requests

import DadosAbertosBrasil as dab
from DadosAbertosBrasil import bacen, favoritos, ibge, ipea
from DadosAbertosBrasil.utils import converter


class _Resposta:
    def __init__(self, conteudo):
        self.conteudo = conteudo

    def raise_for_status(self):
        pass

    def json(self):
        return self.conteudo


@pytest.fixture
def api(monkeypatch):
    """Faz `Get` e `requests.get` devolverem `resposta(url)` sem acessar a rede."""

    def definir(resposta):
        monkeypatch.setattr(
            requests.Session, "get", lambda self, url, **kw: _Resposta(resposta(url))
        )
        monkeypatch.setattr(requests, "get", lambda url, **kw: _Resposta(resposta(url)))

    yield definir
    dab.config.formato = "pandas"


# converter


def test_converter_pandas_aplica_index():
    df = pd.DataFrame({"codigo": [1, 2], "nome": ["a", "b"]})
    assert list(converter(df, "pandas", True, "codigo").index) == [1, 2]
    assert isinstance(converter(df, "pandas").index, pd.RangeIndex)


def test_converter_polars_sem_pyarrow_e_index_vira_coluna():
    df = pd.DataFrame(
        {"nome": ["a", None], "data": [dt.date(2020, 1, 1), None], "v": [1.5, float("nan")]},
        index=pd.Index([10, 20], name="periodo"),
    )
    plf = converter(df, "polars")
    assert plf.columns == ["periodo", "nome", "data", "v"]
    assert plf["nome"].to_list() == ["a", None]
    assert plf["data"].dtype == pl.Date
    assert plf["v"].to_list() == [1.5, None]


def test_converter_polars_ignora_index_sem_nome():
    df = pd.DataFrame({"a": [1, 2, 3]})
    assert converter(df[df["a"] > 1], "polars").columns == ["a"]


def test_converter_polars_avisa_index():
    with pytest.warns(UserWarning, match="polars"):
        converter(pd.DataFrame({"a": [1]}), "polars", True, "a")


# bacen


SGS = [{"data": "01/01/2020", "valor": "1.5"}, {"data": "01/02/2020", "valor": "2.0"}]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_bacen_serie(api, formato):
    api(lambda url: SGS)
    df = bacen.serie(432, formato=formato)
    datas = df["data"].to_list() if formato == "polars" else list(df["data"])
    assert [d.date() for d in datas] == [dt.date(2020, 1, 1), dt.date(2020, 2, 1)]


def test_bacen_serie_formato_global(api):
    api(lambda url: SGS)
    dab.config.formato = "polars"
    assert isinstance(bacen.serie(432), pl.DataFrame)
    assert bacen.serie(432, formato="json") == SGS


def test_bacen_cambio_polars(api):
    def resposta(url):
        if "'USD'" in url:
            return {"value": [{"cotacaoCompra": 5.0, "dataHoraCotacao": "2021-01-04 13:00:00.0"}]}
        return {"value": [
            {"cotacaoCompra": 4.0, "dataHoraCotacao": "2021-01-04 13:00:00.0"},
            {"cotacaoCompra": 4.1, "dataHoraCotacao": "2021-01-05 13:00:00.0"},
        ]}

    api(resposta)
    df = bacen.cambio(["USD", "CAD"], inicio="2021-01-01", fim="2021-01-10", formato="polars")
    assert df.columns == ["data", "USD", "CAD"]
    assert df["USD"].to_list() == [5.0, None]
    assert df["CAD"].to_list() == [4.0, 4.1]


# ipea


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_ipea_serie(api, formato):
    api(lambda url: {"value": [
        {"SERCODIGO": "X", "VALDATA": "1996-01-01T00:00:00-02:00", "VALVALOR": 1.0},
    ]})
    df = ipea.serie("X", formato=formato)
    assert list(df["data"]) == [dt.date(1996, 1, 1)]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_ipea_lista_series_filtros(api, formato):
    api(lambda url: {"value": [
        {"SERCODIGO": "A", "SERNOME": "PIB", "SERCOMENTARIO": "", "SERSTATUS": "A"},
        {"SERCODIGO": "B", "SERNOME": "IPCA", "SERCOMENTARIO": "", "SERSTATUS": "I"},
    ]})
    df = ipea.lista_series(contendo="pib", formato=formato)
    assert list(df["codigo"]) == ["A"]
    assert list(df["ativo"]) == [True]


# ibge


def test_ibge_nomes_polars(api):
    api(lambda url: [
        {"nome": "ANA", "res": [{"periodo": "1930[", "frequencia": 10}, {"periodo": "[1930,1940[", "frequencia": 20}]},
        {"nome": "BIA", "res": [{"periodo": "1930[", "frequencia": 1}, {"periodo": "[1930,1940[", "frequencia": 2}]},
    ])
    df = ibge.nomes(["ana", "bia"], formato="polars")
    assert df.columns == ["periodo", "ANA", "BIA"]
    assert df["ANA"].to_list() == [10, 20]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_ibge_localidades(api, formato):
    api(lambda url: [{"id": 1, "nome": "X", "municipio": {"id": 9, "nome": "M"}}])
    df = ibge.localidades(formato=formato)
    assert list(df.columns) == ["id", "nome", "municipio_id", "municipio_nome"]


def test_ibge_sidra_polars(api):
    api(lambda url: [{"V": "Valor", "D1N": "Brasil"}, {"V": "10", "D1N": "Brasil"}])
    df = ibge.sidra(1419, formato="polars")
    assert df.columns == ["Valor", "Brasil"]


def test_ibge_referencias_index(api):
    api(lambda url: [{"id": 148, "literal": "Água"}])
    df = ibge.referencias("assuntos", index=True, formato="pandas")
    assert df.index.name == "cod"


AGREGADOS = [
    {"id": "CD", "nome": "Censo", "agregados": [
        {"id": "1", "nome": "População residente"},
        {"id": "2", "nome": "Domicílios"},
    ]},
]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_ibge_lista_tabelas_excluindo(api, formato):
    api(lambda url: AGREGADOS)
    df = ibge.lista_tabelas(excluindo="domic", formato=formato)
    assert list(df["tabela_id"]) == [1]


def test_ibge_lista_pesquisas_polars(api):
    api(lambda url: AGREGADOS)
    df = ibge.lista_pesquisas(formato="polars")
    assert df.rows() == [("CD", "Censo")]


# favoritos


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_favoritos_pib(api, formato):
    api(lambda url: {"value": [{
        "SERCODIGO": "X", "VALDATA": "1996-01-01T00:00:00-02:00", "VALVALOR": 1.0,
        "NIVNOME": "", "TERCODIGO": "",
    }]})
    df = favoritos.pib(formato=formato)
    assert list(df.columns) == ["data", "valor"]


def test_favoritos_catalogo_polars(monkeypatch):
    monkeypatch.setattr(pd, "read_csv", lambda url, **kw: pd.DataFrame({"Título": ["X"]}))
    df = favoritos.catalogo(formato="polars")
    assert isinstance(df, pl.DataFrame)
    assert favoritos.catalogo(formato="url").startswith("https://")
