from DadosAbertosBrasil import bacen
import pytest


def test_moedas():
    df = bacen.moedas()
    assert not df.empty


@pytest.mark.parametrize("cotacao", ["compra", "venda"])
def test_cambio(cotacao):
    df = bacen.cambio(index=True, cotacao=cotacao)
    assert not df.empty


def test_expectativas():
    df = bacen.expectativas("mensal", top=5)
    assert not df.empty


def test_serie():
    df = bacen.serie(432, ultimos=5)
    assert not df.empty
