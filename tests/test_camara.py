from DadosAbertosBrasil import camara


def test_lista_blocos():
    df = camara.lista_blocos(legislatura=56, itens=5)
    assert not df.empty


def test_lista_deputados():
    df = camara.lista_deputados(uf="sc", sexo="f")
    assert not df.empty


def test_lista_eventos():
    eventos = camara.lista_eventos(itens=5, index=True, formato="json")
    assert eventos


def test_lista_frentes():
    df = camara.lista_frentes(pagina=2)
    assert not df.empty


def test_lista_legislaturas():
    df = camara.lista_legislaturas(itens=5, url=False, index=True)
    assert not df.empty


def test_lista_orgaos():
    df = camara.lista_orgaos(inicio="2024-01-01", itens=5)
    assert not df.empty


def test_lista_partidos():
    df = camara.lista_partidos(url=False)
    assert not df.empty


def test_lista_votacoes():
    df = camara.lista_votacoes(itens=5, asc=True)
    assert not df.empty
