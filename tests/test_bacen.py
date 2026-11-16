from DadosAbertosBrasil import bacen
import pytest

pytestmark = pytest.mark.vcr


def test_moedas():
    df = bacen.moedas()
    assert not df.empty


@pytest.mark.parametrize("cotacao", ["compra", "venda"])
def test_cambio(cotacao):
    df = bacen.cambio(inicio="2024-01-01", fim="2024-03-01", index=True, cotacao=cotacao)
    assert not df.empty


def test_expectativas():
    df = bacen.expectativas("mensal", top=5)
    assert not df.empty


def test_serie():
    df = bacen.serie(432, ultimos=5)
    assert not df.empty
