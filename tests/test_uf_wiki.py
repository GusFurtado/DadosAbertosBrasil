"""Classe UF sobre o módulo wiki, sem rede."""

import pytest

import DadosAbertosBrasil as dab
from DadosAbertosBrasil.uf import UF, Governador

from .conftest import envelope_wiki, servir_wiki

SIDRA_6579 = [
    {"NC": "Nível Territorial (Código)", "V": "Valor"},
    {"NC": "3", "V": "8312759"},
]


@pytest.fixture
def rede(api):
    api(lambda url: SIDRA_6579 if "apisidra" in url else servir_wiki(url))


def test_atributos_da_uf(rede):
    sc = UF("santa catarina")
    registro = next(r for r in envelope_wiki("ufs")["dados"] if r["sigla"] == "SC")
    assert (sc.sigla, sc.cod, sc.nome, sc.capital) == ("SC", 42, "Santa Catarina", registro["capital"])
    assert sc.area == registro["area_km2"]
    assert sc.gentilico == registro["gentilicos"]
    assert sc.coordenadas == {"latitude": registro["latitude"], "longitude": registro["longitude"]}
    assert sc.extinto is False
    assert sc.registro.wikidata == registro["wikidata"]


@pytest.mark.parametrize("sigla, extinto", [("BR", False), ("GB", True), ("FN", True)])
def test_brasil_e_ufs_extintas_sem_rede(sigla, extinto):
    uf = UF(sigla)
    assert uf.extinto is extinto
    assert uf.registro is None


def test_governador(rede):
    governador = UF("SC").governador
    assert isinstance(governador, Governador)
    assert governador.uf == "SC"
    assert governador.nome == next(r["nome"] for r in envelope_wiki("governadores")["dados"] if r["uf"] == "SC")
    assert not hasattr(governador, "nome_completo")


def test_governador_indisponivel_para_extintas():
    with pytest.raises(dab.DABUFError):
        UF("GB").governador  # noqa: B018


def test_prefeito(rede):
    prefeito = UF("SC").prefeito
    assert prefeito.uf == "SC"
    with pytest.raises(dab.DABUFError):
        UF("DF").prefeito  # noqa: B018


def test_populacao_e_densidade(rede):
    sc = UF("SC")
    assert sc.populacao == 8312759
    assert sc.densidade == pytest.approx(8312759 / sc.area)
