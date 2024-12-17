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


def test_lista_proposicoes():
    df = camara.lista_proposicoes()
    assert not df.empty


def test_lista_votacoes():
    df = camara.lista_votacoes(itens=5, asc=True)
    assert not df.empty


def test_referencias():
    df = camara.referencias("ufs")
    return not df.empty


def test_Bloco():
    obj = camara.Bloco(586)
    assert obj.dados


def test_Deputado():
    obj = camara.Deputado(220593)
    assert obj.dados


def test_Evento():
    obj = camara.Evento(74519)
    assert obj.dados


def test_Frente():
    obj = camara.Frente(55660)
    assert obj.dados


def test_Legislatura():
    obj = camara.Legislatura(56)
    assert obj.dados


def test_Orgao():
    obj = camara.Orgao(4)
    assert obj.dados


def test_Partido():
    obj = camara.Partido(13)
    assert obj.dados


def test_Proposicao():
    obj = camara.Proposicao(15151)
    assert obj.dados


def test_Votacao():
    obj = camara.Votacao("2430143-148")
    assert obj.dados
