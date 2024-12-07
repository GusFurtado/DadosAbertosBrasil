from DadosAbertosBrasil import ipea


def test_lista_niveis():
    niveis = ipea.lista_niveis()
    assert isinstance(niveis, list)


def test_lista_paises():
    df = ipea.lista_paises()
    assert not df.empty


def test_lista_temas():
    df = ipea.lista_temas(index=True)
    assert not df.empty


def test_lista_territorios():
    df = ipea.lista_territorios()
    assert not df.empty


def test_Serie():
    s = ipea.Serie("ABATE_ABPEAV")

    assert s.dados is not None
    assert s.cod is not None
    assert s.metadados is not None
    assert s.base is not None
    assert s.fonte_nome is not None
    assert s.fonte_sigla is not None
    assert s.fonte_url is not None
    assert s.multiplicador is not None
    assert s.periodo is not None
    assert s.ultima_atualizacao is not None
    assert s.comentario is not None
    assert s.nome is not None
    assert s.unidade is not None
    assert s.ativo is not None
    assert s.tema is not None
    assert s.pais is not None
    assert s.numerica is not None


def test_lista_series():
    df = ipea.lista_series(ativo=True, index=True)
    assert not df.empty


def test_serie():
    df = ipea.serie("PNAD_IAGRV")
    assert not df.empty
