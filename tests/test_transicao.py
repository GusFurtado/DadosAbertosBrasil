"""Avisos da versão de transição 2.3 para o 3.0."""

import warnings

import pytest

import DadosAbertosBrasil as dab
from DadosAbertosBrasil import _config, favoritos, ibge, senado
from DadosAbertosBrasil.utils import errors


@pytest.fixture
def config_limpa(monkeypatch):
    """Config sem `formato` definido e aviso ainda não emitido."""
    monkeypatch.setattr(_config, "config", _config.Config())
    monkeypatch.setattr(_config, "_formato_avisado", False)
    return _config.config


def test_aviso_formato_uma_vez_por_sessao(config_limpa):
    with pytest.warns(dab.DABFormatoWarning, match="json"):
        assert config_limpa.resolver_formato(None) == "pandas"
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert config_limpa.resolver_formato(None) == "pandas"


def test_definir_formato_silencia_aviso(config_limpa):
    config_limpa.formato = "pandas"
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert config_limpa.resolver_formato(None) == "pandas"


def test_formato_explicito_nao_avisa(config_limpa):
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        assert config_limpa.resolver_formato("polars") == "polars"


def test_aviso_formato_filtravel():
    assert issubclass(dab.DABFormatoWarning, Warning)


@pytest.mark.parametrize("antigo, novo", errors.NOMES_ANTIGOS.items())
def test_nomes_antigos_das_excecoes(antigo, novo):
    with pytest.warns(DeprecationWarning, match=novo):
        classe = getattr(dab, antigo)
    assert classe is getattr(dab, novo)
    with pytest.warns(DeprecationWarning):
        assert getattr(errors, antigo) is classe


def test_excecoes_tem_base_comum():
    for nome in errors.NOMES_ANTIGOS.values():
        assert issubclass(getattr(dab, nome), dab.DABError)
    assert issubclass(dab.DABUFError, ValueError)
    assert issubclass(dab.DABDataError, TypeError)


def test_dab_deprecation_error_avisa():
    with pytest.warns(DeprecationWarning, match="removido"):
        dab.DAB_DeprecationError  # noqa: B018


def test_nome_inexistente():
    with pytest.raises(AttributeError):
        dab.NaoExiste  # noqa: B018


@pytest.mark.parametrize(
    "antigo, novo",
    [
        (senado.lista_legislatura, "lista_legislaturas"),
        (senado.lista_uso_palavra, "lista_tipos_uso_palavra"),
    ],
)
def test_funcoes_renomeadas_do_senado(antigo, novo):
    with pytest.warns(DeprecationWarning, match=novo):
        url = antigo(**({"inicio": 56} if novo == "lista_legislaturas" else {}), formato="url")
    assert url.startswith("https://") or url.startswith("http://")


@pytest.mark.parametrize(
    "funcao, arquivo",
    [(favoritos.perfil_eleitorado, "eleitorado.csv"), (ibge.coordenadas, "coordenadas.csv")],
)
def test_funcoes_removidas_no_3_0_avisam(funcao, arquivo):
    with pytest.warns(DeprecationWarning, match="3.0"):
        url = funcao(formato="url")
    assert url == f"https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil-wiki/2.x/data/{arquivo}"
