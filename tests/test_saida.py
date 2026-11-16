"""Núcleo do 3.0: modelos de entrada e saída e entrega nos formatos."""

import datetime as dt
import inspect
import sys
import warnings

import pytest
from pydantic import AliasPath, Field, ValidationError

import DadosAbertosBrasil as dab
from DadosAbertosBrasil import bacen, camara, favoritos, ibge, ipea, senado
from DadosAbertosBrasil.utils.errors import DABInputError, DABValidacaoWarning
from DadosAbertosBrasil.utils.modelos import Bool, Data, DataHora, Inteiro, Params, Real, Registro, Texto, Url, validar
from DadosAbertosBrasil.utils.requisicao import Requisicao
from DadosAbertosBrasil.utils.saida import consultar, tabela


class Modelo(Registro):
    codigo: Inteiro = Field(None, validation_alias="id")
    nome: Texto = None
    ativo: Bool = None
    data: DataHora = None
    dia: Data = None
    k: Real = Field(None, validation_alias=AliasPath("sub", "k"))
    uri: Url = None


BRUTO = {
    "dados": [
        {"id": "1", "nome": "A", "ativo": "Sim", "data": "2024-01-02T03:04:05", "dia": "02/01/2024", "uri": "http://x/1", "sub": {"k": 7}},
        {"id": "2", "nome": "B", "ativo": "Não", "data": "2024-02-03T04:05:06", "dia": "", "uri": "http://x/2", "sub": {"k": "8,5"}},
    ]
}


def _requer(*formatos):
    """Pula o teste se a biblioteca de algum formato não estiver instalada."""
    for formato in formatos:
        if formato in ("pandas", "polars"):
            pytest.importorskip(formato)


@pytest.fixture
def requisicao(api):
    api(BRUTO)
    return Requisicao("camara", ["x"], {"pagina": 1}, chaves=["dados"])


def test_url_tem_parametros(requisicao):
    assert requisicao.url == "https://dadosabertos.camara.leg.br/api/v2/x?pagina=1"
    assert consultar(requisicao, Modelo, "url") == requisicao.url


def test_bruto_e_o_json_da_api(requisicao):
    assert consultar(requisicao, Modelo, "bruto") == BRUTO


def test_json_normalizado(requisicao):
    registros = consultar(requisicao, Modelo, "json")
    assert registros[0] == {
        "codigo": 1,
        "nome": "A",
        "ativo": True,
        "data": dt.datetime(2024, 1, 2, 3, 4, 5),
        "dia": dt.date(2024, 1, 2),
        "k": 7.0,
        "uri": "http://x/1",
    }
    assert registros[1]["dia"] is None
    assert registros[1]["k"] == 8.5


def test_pydantic(requisicao):
    registros = consultar(requisicao, Modelo, "pydantic")
    assert all(isinstance(r, Modelo) for r in registros)
    assert registros[1].ativo is False


@pytest.mark.parametrize("formato", ["json", "pandas", "polars"])
def test_url_false_remove_colunas_de_url(requisicao, formato):
    _requer(formato)
    dados = consultar(requisicao, Modelo, formato, url=False)
    colunas = list(dados[0]) if formato == "json" else list(dados.columns)
    assert colunas == ["codigo", "nome", "ativo", "data", "dia", "k"]


def test_pandas_e_polars_tem_os_mesmos_dados(requisicao):
    pd = pytest.importorskip("pandas")  # noqa: F841
    pl = pytest.importorskip("polars")
    pdf = consultar(requisicao, Modelo, "pandas")
    plf = consultar(requisicao, Modelo, "polars")
    assert list(pdf.columns) == plf.columns
    assert str(pdf["codigo"].dtype) == "Int64"
    assert str(pdf["ativo"].dtype) == "boolean"
    assert plf.schema["codigo"] == pl.Int64
    assert plf.schema["dia"] == pl.Date
    assert plf.schema["data"] == pl.Datetime
    assert plf["k"].to_list() == list(pdf["k"])


def test_tabela_vazia_tem_colunas_e_tipos():
    pd = pytest.importorskip("pandas")  # noqa: F841
    pl = pytest.importorskip("polars")
    pdf = tabela([], Modelo, "pandas")
    plf = tabela([], Modelo, "polars")
    assert list(pdf.columns) == list(Modelo.model_fields)
    assert plf.columns == list(Modelo.model_fields)
    assert plf.schema["codigo"] == pl.Int64


def test_index_pandas_e_aviso_no_polars(requisicao):
    pd = pytest.importorskip("pandas")  # noqa: F841
    pl = pytest.importorskip("polars")
    assert list(consultar(requisicao, Modelo, "pandas", index=True).index) == [1, 2]
    with pytest.warns(UserWarning, match="polars"):
        consultar(requisicao, Modelo, "polars", index=True)


def test_filtro(requisicao):
    registros = consultar(requisicao, Modelo, "json", filtro=lambda r: r.ativo)
    assert [r["codigo"] for r in registros] == [1]


def test_formato_invalido(requisicao):
    with pytest.raises(DABInputError):
        consultar(requisicao, Modelo, "numpy")


def test_config_formato_global(requisicao):
    pd = pytest.importorskip("pandas")  # noqa: F841
    pl = pytest.importorskip("polars")
    antes = dab.config.formato
    try:
        dab.config.formato = "polars"
        assert isinstance(consultar(requisicao, Modelo, None), pl.DataFrame)
        assert isinstance(consultar(requisicao, Modelo, "pandas"), pd.DataFrame)
    finally:
        dab.config.formato = antes


def test_config_formato_invalido():
    with pytest.raises(ValidationError):
        dab.config.formato = "numpy"


def test_sem_pandas_e_polars_json_funciona(requisicao, monkeypatch):
    monkeypatch.setitem(sys.modules, "pandas", None)
    monkeypatch.setitem(sys.modules, "polars", None)
    assert consultar(requisicao, Modelo, "json")[0]["codigo"] == 1
    with pytest.raises(ImportError, match="DadosAbertosBrasil\\[pandas\\]"):
        consultar(requisicao, Modelo, "pandas")


def test_polars_ausente(requisicao, monkeypatch):
    monkeypatch.setitem(sys.modules, "polars", None)
    with pytest.raises(ImportError, match="DadosAbertosBrasil\\[polars\\]"):
        consultar(requisicao, Modelo, "polars")


def test_valor_inesperado_avisa_e_mantem_o_bruto():
    with pytest.warns(DABValidacaoWarning, match="Modelo.codigo"):
        registros = validar(Modelo, [{"id": "abc", "nome": "A"}, {"id": "2"}])
    assert registros[0].codigo == "abc"
    assert registros[0].nome == "A"
    assert registros[1].codigo == 2


def test_modelo_estrito_levanta_erro():
    class Estrito(Modelo):
        tolerante = False

    with pytest.raises(ValidationError):
        validar(Estrito, [{"id": "abc"}])


def test_campo_novo_na_api_e_ignorado():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert validar(Modelo, [{"id": 1, "novo": "x"}])[0].codigo == 1


def test_params_traduz_nomes_e_datas():
    class P(Params):
        formato_data = "%Y%m%d"
        verdadeiro = "S"
        inicio: dt.date | None = Field(None, serialization_alias="dataInicio")
        ativos: bool = Field(False, serialization_alias="indAtivos")
        interno: str | None = Field(None, exclude=True)

    p = P.de_locais({"inicio": "2024-01-02", "ativos": True, "interno": "x", "outro": 1})
    assert p.para_api() == {"dataInicio": "20240102", "indAtivos": "S"}


def test_params_uf_invalida_levanta_erro_do_pacote(api):
    api({"dados": []})
    with pytest.raises(dab.DABUFError):
        camara.lista_deputados(uf="xx", formato="json")


ARGUMENTOS_COMUNS = {"self", "url", "index", "formato", "verificar_certificado"}


def _funcoes_com_params():
    for modulo in (bacen, camara, favoritos, ibge, ipea, senado):
        for nome in dir(modulo):
            obj = getattr(modulo, nome)
            candidatos = [obj]
            if inspect.isclass(obj):
                candidatos = [getattr(obj, n) for n in dir(obj) if not n.startswith("_")]
            for funcao in candidatos:
                if callable(funcao) and hasattr(funcao, "__dab_params__"):
                    yield f"{modulo.__name__.split('.')[-1]}.{getattr(funcao, '__qualname__', nome)}", funcao


@pytest.mark.parametrize("nome, funcao", sorted(dict(_funcoes_com_params()).items()))
def test_assinatura_igual_ao_modelo_de_entrada(nome, funcao):
    """Argumentos da função e campos do modelo de entrada não podem divergir."""
    argumentos = set(inspect.signature(funcao).parameters) - ARGUMENTOS_COMUNS
    campos = set(funcao.__dab_params__.model_fields)
    assert argumentos == campos, nome


def test_ha_funcoes_com_modelo_de_entrada():
    assert len(dict(_funcoes_com_params())) >= 45
