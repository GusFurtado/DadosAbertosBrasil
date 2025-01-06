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


def test_Senador():
    senador = senado.Senador(5012)

    assert senador.__repr__()
    assert senador.__str__()

    df = senador.apartes()
    assert not df.empty

    df = senador.autorias()
    assert not df.empty

    df = senador.cargos()
    assert not df.empty

    df = senador.comissoes()
    assert not df.empty

    df = senador.cursos()
    assert not df.empty

    df = senador.discursos()
    assert not df.empty

    df = senador.filiacoes()
    assert not df.empty

    df = senador.historico()
    assert not df.empty

    df = senador.mandatos()
    assert not df.empty

    df = senador.liderancas()
    assert not df.empty

    df = senador.licencas()
    assert not df.empty

    df = senador.profissoes()
    assert not df.empty

    df = senador.relatorias()
    assert not df.empty

    df = senador.votacoes()
    assert not df.empty
