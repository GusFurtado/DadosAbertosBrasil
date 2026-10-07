import pandas as pd
import polars as pl
import pytest
import requests

import DadosAbertosBrasil as dab
from DadosAbertosBrasil import bacen, camara, ipea, senado


@pytest.fixture
def api(monkeypatch):
    """Faz a API devolver `resposta` em vez de consultar a rede."""

    def definir(resposta):
        class _Resposta:
            def raise_for_status(self):
                pass

            def json(self):
                return resposta

        monkeypatch.setattr(requests.Session, "get", lambda self, url, **kw: _Resposta())

    yield definir
    dab.config.formato = "pandas"


def _senador(cod, nome, completo, sexo, partido):
    return {
        "IdentificacaoParlamentar": {
            "CodigoParlamentar": str(cod),
            "NomeParlamentar": nome,
            "NomeCompletoParlamentar": completo,
            "SexoParlamentar": sexo,
            "SiglaPartidoParlamentar": partido,
        },
        "Mandato": {"UfParlamentar": "SP"},
    }


SENADORES = [
    _senador(1, "Ana", "Ana Silva", "Feminino", "AAA"),
    _senador(2, "Bia", "Beatriz Souza", "Feminino", "BBB"),
    _senador(3, "Caio", "Caio Silva", "Masculino", "AAA"),
]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_lista_senadores_filtros(api, formato):
    api(SENADORES)
    df = senado.lista_senadores(sexo="f", partido="aaa", formato=formato)
    codigos = df["codigo"].to_list() if formato == "polars" else list(df["codigo"])
    assert codigos == [1]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_lista_senadores_contendo_excluindo(api, formato):
    api(SENADORES)
    contendo = senado.lista_senadores(contendo="Silva", formato=formato)
    excluindo = senado.lista_senadores(excluindo="Silva", formato=formato)
    assert list(contendo["codigo"]) == [1, 3]
    assert list(excluindo["codigo"]) == [2]


def test_lista_senadores_formato_global_aplica_filtros(api):
    api(SENADORES)
    dab.config.formato = "polars"
    df = senado.lista_senadores(sexo="m")
    assert isinstance(df, pl.DataFrame)
    assert df["codigo"].to_list() == [3]


def test_lista_senadores_json_sem_filtro(api):
    api(SENADORES)
    assert senado.lista_senadores(sexo="m", formato="json") == SENADORES


EVENTOS = [
    {"id": 1, "dataHoraInicio": "2024-01-01T10:00", "orgaos": [{"id": 10}]},
    {"id": 2, "dataHoraInicio": "2024-01-02T10:00", "orgaos": [{"id": 10}, {"id": 20}]},
    {"id": 3, "dataHoraInicio": "2024-01-03T10:00", "orgaos": []},
]


def test_lista_eventos_orgaos_pandas(api):
    api({"dados": EVENTOS})
    df = camara.lista_eventos(formato="pandas")
    assert isinstance(df, pd.DataFrame)
    assert df["orgaos"].iloc[0] == 10
    assert df["orgaos"].iloc[1] == [10, 20]
    assert df["orgaos"].iloc[2] is None


def test_lista_eventos_orgaos_polars(api):
    api({"dados": EVENTOS})
    df = camara.lista_eventos(formato="polars")
    assert df["orgaos"].to_list() == [[10], [10, 20], []]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_moedas(api, formato):
    api({"value": [{"simbolo": "USD", "nomeFormatado": "Dólar", "tipoMoeda": "A"}]})
    df = bacen.moedas(formato=formato)
    assert list(df.columns) == ["simbolo", "nome", "tipo"]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_ipea_lista_temas_pai(api, formato):
    api({"value": [
        {"TEMCODIGO": 1, "TEMCODIGO_PAI": None, "TEMNOME": "A"},
        {"TEMCODIGO": 2, "TEMCODIGO_PAI": 1, "TEMNOME": "B"},
    ]})
    df = ipea.lista_temas(pai=1, formato=formato)
    assert list(df["codigo"]) == [2]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_lista_orcamentos_ano_materia(api, formato):
    api([
        {"AnoMateria": "2020", "SiglaTipoPlOrcamento": "LDO"},
        {"AnoMateria": "2021", "SiglaTipoPlOrcamento": "LOA"},
    ])
    df = senado.lista_orcamentos(ano_materia=2021, formato=formato)
    assert list(df["materia_ano"]) == [2021]


def test_temas_default_retorna_dataframe(api, monkeypatch):
    monkeypatch.setattr(camara.Proposicao, "__init__", lambda self, cod: setattr(self, "cod", cod) or setattr(self, "verify", None))
    api({"dados": [{"codTema": 1, "tema": "Saúde", "relevancia": 0}]})
    assert isinstance(camara.Proposicao(1).temas(), pd.DataFrame)
