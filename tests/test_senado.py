from DadosAbertosBrasil import senado


def test_lista_senadores():
    df = senado.lista_senadores()
    assert not df.empty
