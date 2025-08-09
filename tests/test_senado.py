import pandas as pd
from DadosAbertosBrasil import senado
from DadosAbertosBrasil.senado._senadores import lista_senadores


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

    # assert senador.__repr__()
    # assert senador.__str__()

    # df = senador.apartes()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.autorias()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.cargos()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.comissoes()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.cursos()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.discursos()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.filiacoes()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.historico()
    # assert isinstance(df, dict)

    # df = senador.mandatos()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.liderancas()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.licencas()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.profissoes()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.relatorias()
    # assert isinstance(df, pd.DataFrame)

    # df = senador.votacoes()
    # assert isinstance(df, pd.DataFrame)
