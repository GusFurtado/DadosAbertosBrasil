"""Módulo wiki, com os arquivos publicados no DadosAbertosBrasil-wiki como fixtures."""

import pytest
from pydantic import ValidationError

from DadosAbertosBrasil import wiki
from DadosAbertosBrasil.utils.errors import DABDadosWarning

from .conftest import FIXTURES_WIKI, envelope_wiki as _envelope

DATASETS = sorted(p.stem for p in FIXTURES_WIKI.glob("*.json"))


@pytest.mark.parametrize("dataset", DATASETS)
def test_dataset_valida_contra_o_modelo(repositorio, dataset):
    registros = getattr(wiki, dataset)(formato="pydantic")
    assert len(registros) == len(_envelope(dataset)["dados"])


@pytest.mark.parametrize("dataset", DATASETS)
def test_json_tem_os_campos_do_arquivo(repositorio, dataset):
    registros = getattr(wiki, dataset)(formato="json")
    assert set(registros[0]) == set(_envelope(dataset)["dados"][0])


def test_bruto_e_o_envelope(repositorio):
    envelope = wiki.governadores(formato="bruto")
    assert envelope == _envelope("governadores")
    assert envelope["schema_version"] == 1


def test_url():
    assert wiki.ufs(formato="url").endswith("/DadosAbertosBrasil-wiki/main/data/ufs.json")


def test_metadados(repositorio):
    meta = wiki.metadados("governadores")
    assert "dados" not in meta
    assert meta["licenca"].startswith("CC BY-SA")
    assert meta["fontes"][0]["revid"]


def test_metadados_em_attrs_no_pandas(repositorio):
    pytest.importorskip("pandas")
    df = wiki.governadores(formato="pandas")
    assert df.attrs["dataset"] == "governadores"
    assert df.attrs["fontes"] == _envelope("governadores")["fontes"]


@pytest.mark.parametrize("formato", ["pandas", "polars"])
def test_dataframes(repositorio, formato):
    pytest.importorskip(formato)
    df = wiki.ufs(formato=formato)
    assert len(df) == 27
    assert list(df.columns) == list(wiki.modelos.UF.model_fields)


def test_filtro_por_uf_aceita_nome(repositorio):
    registros = wiki.governadores(uf="santa catarina", formato="json")
    assert [r["uf"] for r in registros] == ["SC"]


def test_filtros(repositorio):
    assert {r["tribunal"] for r in wiki.tribunais(tribunal="STF", formato="json")} == {"STF"}
    assert all(r["ativo"] for r in wiki.partidos(ativos=True, formato="json"))
    assert all(r["em_exercicio"] for r in wiki.ministros(em_exercicio=True, formato="json"))


def test_schema_mais_novo_avisa(api):
    envelope = _envelope("ufs") | {"schema_version": 2}
    api(envelope)
    with pytest.warns(DABDadosWarning, match="Atualize"):
        wiki.ufs(formato="json")


def test_validacao_estrita(api):
    envelope = _envelope("ufs")
    envelope["dados"][0]["area_km2"] = "muito grande"
    api(envelope)
    with pytest.raises(ValidationError):
        wiki.ufs(formato="json")


def test_campo_novo_no_repositorio_nao_quebra(api):
    envelope = _envelope("ufs")
    for registro in envelope["dados"]:
        registro["campo_novo"] = 1
    api(envelope)
    assert "campo_novo" not in wiki.ufs(formato="json")[0]
