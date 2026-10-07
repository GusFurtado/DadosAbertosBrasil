import sys

import pandas as pd
import polars as pl
import pytest
import requests
from pydantic import ValidationError

import DadosAbertosBrasil as dab
from DadosAbertosBrasil import camara
from DadosAbertosBrasil.utils import Get

REGISTROS = [
    {"id": "1", "nome": "A", "ativo": "Sim", "data": "2024-01-02T03:04:05", "uri": "http://x/1", "sub": {"k": 7}},
    {"id": "2", "nome": "B", "ativo": "Não", "data": "2024-02-03T04:05:06", "uri": "http://x/2", "sub": {"k": 8}},
]


class _Resposta:
    def raise_for_status(self):
        pass

    def json(self):
        return {"dados": REGISTROS}


@pytest.fixture(autouse=True)
def api_falsa(monkeypatch):
    monkeypatch.setattr(requests.Session, "get", lambda self, url, **kw: _Resposta())
    yield
    dab.config.formato = "pandas"


def _get(**kwargs):
    base = dict(
        endpoint="camara",
        path=["x"],
        unpack_keys=["dados"],
        cols_to_rename={"id": "codigo", "nome": "nome", "ativo": "ativo", "data": "data", "sub.k": "k", "uri": "uri"},
        cols_to_int=["codigo"],
        cols_to_date=["data"],
        cols_to_bool=["ativo"],
        true_value="Sim",
        false_value="Não",
        remover_url=True,
        url_cols=["uri"],
    )
    base.update(kwargs)
    return Get(**base)


def test_polars_equivale_ao_pandas():
    pdf = _get().pandas
    plf = _get().polars
    assert isinstance(plf, pl.DataFrame)
    assert set(plf.columns) == set(pdf.columns)
    assert "uri" not in plf.columns
    assert plf["codigo"].to_list() == [1, 2]
    assert plf["ativo"].to_list() == [True, False]
    assert plf["k"].to_list() == [7, 8]
    assert plf["data"].dtype == pl.Datetime
    assert plf["data"].to_list() == list(pd.to_datetime(pdf["data"]))


def test_get_formato_polars():
    assert isinstance(_get().get("polars"), pl.DataFrame)
    assert isinstance(_get().get("pandas"), pd.DataFrame)


def test_config_formato_global_e_argumento():
    dab.config.formato = "polars"
    assert isinstance(_get().get(), pl.DataFrame)
    assert isinstance(_get().get("pandas"), pd.DataFrame)


def test_config_formato_invalido():
    with pytest.raises(ValidationError):
        dab.config.formato = "numpy"


def test_index_ignorado_com_aviso():
    with pytest.warns(UserWarning, match="polars"):
        plf = _get(index=True).polars
    assert isinstance(plf, pl.DataFrame)


def test_funcao_publica_aceita_polars(monkeypatch):
    blocos = [{"id": 1, "uri": "http://x/1", "nome": "A", "idLegislatura": 57}]

    class _Blocos(_Resposta):
        def json(self):
            return {"dados": blocos}

    monkeypatch.setattr(requests.Session, "get", lambda self, url, **kw: _Blocos())
    df = camara.lista_blocos(formato="polars")
    assert isinstance(df, pl.DataFrame)
    assert {"codigo", "nome", "legislatura"} <= set(df.columns)


def test_polars_ausente(monkeypatch):
    monkeypatch.setitem(sys.modules, "polars", None)
    with pytest.raises(ImportError, match="DadosAbertosBrasil\\[polars\\]"):
        _ = _get().polars
