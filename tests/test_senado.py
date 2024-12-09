from DadosAbertosBrasil import senado


def test_lista_blocos():
    df = senado.lista_blocos(index=True)
    assert not df.empty


def test_lista_legislatura():
    df = senado.lista_legislatura(inicio=56)
    assert not df.empty


def test_lista_orcamentos():
    df = senado.lista_orcamentos()
    assert not df.empty


def test_lista_partidos():
    df = senado.lista_partidos()
    assert not df.empty


def test_lista_senadores():
    df = senado.lista_senadores(uf="sc", sexo="f")
    assert not df.empty


def test_lista_uso_palavra():
    df = senado.lista_uso_palavra(ativos=True)
    assert not df.empty
