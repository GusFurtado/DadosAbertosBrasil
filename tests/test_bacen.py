from DadosAbertosBrasil import bacen


def test_moedas():
    df = bacen.moedas()
    assert not df.empty


def test_cambio():
    df = bacen.cambio(index=True)
    assert not df.empty


def test_expectativas():
    df = bacen.expectativas("mensal", top=5)
    assert not df.empty


def test_serie():
    df = bacen.serie(432, ultimos=5)
    assert not df.empty
