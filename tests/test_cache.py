import os
import time

import pytest

import DadosAbertosBrasil as dab
from DadosAbertosBrasil.utils import cache
from DadosAbertosBrasil.utils.requisicao import Requisicao


@pytest.fixture
def contador(api, tmp_path, monkeypatch):
    chamadas = []

    def resposta(url):
        chamadas.append(url)
        return {"dados": [{"n": len(chamadas)}]}

    api(resposta)
    monkeypatch.setattr(dab.config, "cache", True)
    monkeypatch.setattr(dab.config, "cache_pasta", tmp_path)
    return chamadas


def _req(cacheavel=True):
    return Requisicao("camara", ["referencias", "uf"], chaves=["dados"], cacheavel=cacheavel)


def test_desligado_por_padrao():
    assert dab.config.cache is False


def test_segunda_consulta_vem_do_cache(contador):
    assert _req().json() == [{"n": 1}]
    assert _req().json() == [{"n": 1}]
    assert len(contador) == 1


def test_so_requisicoes_cacheaveis(contador):
    _req(cacheavel=False).json()
    _req(cacheavel=False).json()
    assert len(contador) == 2


def test_validade(contador):
    _req().json()
    arquivo = next(cache.pasta().glob("*.cache"))
    antigo = time.time() - dab.config.cache_validade.total_seconds() - 1
    os.utime(arquivo, (antigo, antigo))
    assert _req().json() == [{"n": 2}]


def test_sem_cache(contador):
    _req().json()
    with dab.config.sem_cache():
        assert _req().json() == [{"n": 2}]
    assert _req().json() == [{"n": 1}]


def test_limpar(contador):
    _req().json()
    assert dab.config.limpar_cache() == 1
    assert _req().json() == [{"n": 2}]


def test_cache_desligado_nao_grava(contador, monkeypatch):
    monkeypatch.setattr(dab.config, "cache", False)
    _req().json()
    assert not list(cache.pasta().glob("*.cache"))


def test_validade_aceita_segundos(monkeypatch):
    monkeypatch.setattr(dab.config, "cache_validade", 60)
    assert dab.config.cache_validade.total_seconds() == 60
