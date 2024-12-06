from DadosAbertosBrasil import bacen


def test_moedas():
    df = bacen.moedas()
    assert not df.empty
