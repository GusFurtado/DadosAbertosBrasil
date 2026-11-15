import pytest
from DadosAbertosBrasil import ibge
from DadosAbertosBrasil.utils.errors import DABInputError, DABLocalidadeError
from DadosAbertosBrasil.utils.requisicao import Requisicao

pytestmark = pytest.mark.vcr


def test_Galeria():
    galeria = ibge.Galeria(35)
    assert galeria.fotografias


def test_Historia():
    historia = ibge.Historia(35)
    assert historia


def test_localidades():
    df = ibge.localidades("estados")
    assert not df.empty


def test_malha():
    malha = ibge.malha(localidade=35, qualidade="minima")
    assert malha["type"] == "FeatureCollection"


def test_malha_topojson_do_brasil():
    malha = ibge.malha(localidade="BR", nivel="paises", divisoes="uf", tipo="topojson")
    assert malha["type"] == "Topology"


def test_malha_svg():
    malha = ibge.malha(localidade=4209102, nivel="municipios", tipo="svg")
    assert isinstance(malha, str)
    assert "<svg" in malha


def test_malha_url():
    url = ibge.malha(localidade=53, tipo="svg", formato="url")
    assert url.startswith("https://servicodados.ibge.gov.br/api/v3/malhas/estados/53?")
    assert "formato=image%2Fsvg%2Bxml" in url


@pytest.mark.parametrize(
    "antigo, tipo",
    [("geojson", "application%2Fvnd.geo%2Bjson"), ("json", "application%2Fjson"), ("svg", "image%2Fsvg%2Bxml")],
)
def test_malha_formato_antigo(monkeypatch, antigo, tipo):
    """No 2.x, `formato` era o tipo de arquivo; `formato='svg'` retornava a URL."""
    urls = []
    monkeypatch.setattr(Requisicao, "bruto", lambda self: urls.append(self.url) or {"type": "Topology"})
    with pytest.warns(DeprecationWarning, match="tipo=") as avisos:
        resultado = ibge.malha(localidade=53, formato=antigo)
    assert avisos[0].filename == __file__
    url = resultado if antigo == "svg" else urls[0]
    assert f"formato={tipo}" in url


def test_malha_formato_antigo_conflita_com_tipo():
    with pytest.raises(DABInputError, match="conflita"):
        ibge.malha(localidade=53, tipo="svg", formato="json")


def test_malha_nivel_invalido():
    with pytest.raises(DABLocalidadeError):
        ibge.malha(localidade=53, nivel="bairros", formato="url")




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
    df = ibge.referencias(cod="assuntos")
    assert not df.empty


def test_sidra():
    df = ibge.sidra(1197)
    assert not df.empty
