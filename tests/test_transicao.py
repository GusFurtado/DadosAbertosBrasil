"""Avisos da versão de transição 2.3 para o 3.0."""

import sys
import warnings

import pytest
import requests

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


class _SemRedeError(Exception):
    pass


@pytest.mark.parametrize("funcao", ["camara.lista_partidos", "bacen.moedas"])
def test_aviso_formato_aponta_para_quem_chama(monkeypatch, funcao):
    """O aviso indica a linha do usuário, não a do pacote ou do `validate_call`."""
    # Os módulos guardam a própria referência a `config`: troca em todos.
    antiga, nova = _config.config, _config.Config()
    for modulo in list(sys.modules.values()):
        if modulo.__name__.startswith("DadosAbertosBrasil") and getattr(modulo, "config", None) is antiga:
            monkeypatch.setattr(modulo, "config", nova)
    monkeypatch.setattr(_config, "_formato_avisado", False)

    def sem_rede(*args, **kwargs):
        raise _SemRedeError

    monkeypatch.setattr(requests.Session, "get", sem_rede)
    modulo, nome = funcao.split(".")
    with pytest.warns(dab.DABFormatoWarning) as avisos, pytest.raises(_SemRedeError):
        getattr(getattr(dab, modulo), nome)()
    assert avisos[0].filename == __file__


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


def test_dab_deprecation_error_removido():
    with pytest.raises(AttributeError):
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
    with pytest.warns(DeprecationWarning, match=novo) as avisos:
        url = antigo(**({"inicio": 56} if novo == "lista_legislaturas" else {}), formato="url")
    assert avisos[0].filename == __file__
    assert url.startswith("https://") or url.startswith("http://")


@pytest.mark.parametrize("funcao", [favoritos.perfil_eleitorado, ibge.coordenadas])
def test_funcoes_removidas_viram_stubs(funcao):
    with pytest.raises(dab.DABFuncaoRemovidaError, match="migracao"):
        funcao(formato="pandas")
    assert issubclass(dab.DABFuncaoRemovidaError, NotImplementedError)
