from DadosAbertosBrasil.uf import UF, Governador


def test_uf_attributes():
    uf = UF("RS")

    assert uf.sigla is not None
    assert uf.cod is not None
    assert uf.nome is not None
    assert uf.area is not None
    assert uf.capital is not None
    assert uf.extinto is not None
    assert uf.gentilico is not None
    assert uf.lema is not None
    assert uf.regiao is not None


def test_uf_properties():
    uf = UF("SC")

    assert uf.densidade is not None
    assert uf.galeria is not None
    assert uf.governador is not None
    assert uf.historia is not None
    assert uf.municipios is not None
    assert uf.populacao is not None


def test_governador():
    governador = Governador("PR")

    assert governador.uf is not None
    assert governador.nome is not None
    assert governador.nome_completo is not None
    assert governador.ano_eleicao is not None
    assert governador.mandato_inicio is not None
    assert governador.mandato_fim is not None
    assert governador.partido is not None
    assert governador.partido_sigla is not None
    assert governador.vice_governador is not None
