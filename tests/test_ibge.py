from DadosAbertosBrasil import ibge


def test_Galeria():
    galeria = ibge.Galeria(35)
    assert galeria.fotografias


def test_Historia():
    historia = ibge.Historia(35)
    assert historia


def test_coordenadas():
    df = ibge.coordenadas()
    assert not df.empty


def test_localidades():
    df = ibge.localidades()
    assert not df.empty


def test_malha():
    malha = ibge.malha(localidade=35, qualidade="minima")
    assert malha


# API aparentemente descontinuada
# def test_populacao():
#     pop = ibge.populacao()
#     assert pop


def test_nomes():
    df = ibge.nomes(nomes="Gustavo", sexo="m", localidade=35)
    assert not df.empty


def test_nomes_ranking():
    df = ibge.nomes_ranking(decada=1990, sexo="f", localidade=35)
    assert not df.empty


def test_nomes_uf():
    df = ibge.nomes_uf(nome="Camila")
    assert not df.empty


def test_Metadados():
    metadados = ibge.Metadados(905)
    assert metadados.dados


def test_lista_pesquisas():
    df = ibge.lista_pesquisas(index=True)
    assert not df.empty


def test_lista_tabelas():
    df = ibge.lista_tabelas(contendo="PIB")
    assert not df.empty


def test_referencias():
    df = ibge.referencias(cod="A")
    assert not df.empty


def test_sidra():
    df = ibge.sidra(1197)
    assert not df.empty
