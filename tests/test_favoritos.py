import requests

from DadosAbertosBrasil import (
    bandeira,
    brasao,
    catalogo,
    codigos_municipios,
    ipca,
    perfil_eleitorado,
    pib,
    rentabilidade_poupanca,
    reservas_internacionais,
    risco_brasil,
    salario_minimo,
    selic,
    taxa_referencial,
)


def test_bandeira():
    url = bandeira(uf="SP", tamanho=120)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    assert response.status_code == 200


def test_brasao():
    url = brasao(uf="SP", tamanho=120)
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    assert response.status_code == 200, url


def test_catalogo():
    df = catalogo()
    assert not df.empty


def test_codigos_municipios():
    df = codigos_municipios()
    assert not df.empty


def test_ipca():
    df = ipca(ultimos=10, index=True)
    assert df.shape == (10, 1)

    df = ipca(inicio="2024-01-01", fim="2024-02-01")
    assert df.shape == (2, 2)


def test_perfil_eleitorado():
    df = perfil_eleitorado()
    assert not df.empty


def test_pib():
    df = pib(index=True)
    assert not df.empty


def test_rentabilidade_poupanca():
    df = rentabilidade_poupanca(ultimos=5)
    assert not df.empty


def test_reservas_internacionais():
    df = reservas_internacionais(ultimos=5)
    assert not df.empty


def test_risco_brasil():
    df = risco_brasil(index=True)
    assert not df.empty


def test_salario_minimo():
    df = salario_minimo(index=True)
    assert not df.empty


def test_selic():
    df = selic(ultimos=5)
    assert not df.empty


def test_taxa_referencial():
    df = taxa_referencial(ultimos=5, index=True)
    assert not df.empty
