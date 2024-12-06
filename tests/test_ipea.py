from DadosAbertosBrasil import ipea


def test_lista_series():
    df = ipea.lista_series()
    assert not df.empty
