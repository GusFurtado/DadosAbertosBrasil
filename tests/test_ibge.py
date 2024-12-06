from DadosAbertosBrasil import ibge


def test_lista_tabelas():
    df = ibge.lista_tabelas()
    assert not df.empty
