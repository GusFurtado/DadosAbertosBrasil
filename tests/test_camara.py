from DadosAbertosBrasil import camara


def test_lista_deputados():
    df = camara.lista_deputados()
    assert not df.empty
