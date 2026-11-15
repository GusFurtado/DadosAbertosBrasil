import pytest

from DadosAbertosBrasil.utils import repositorio
from DadosAbertosBrasil.utils.errors import DABDadosWarning


def test_url_fixa_na_main_do_repositorio_renomeado():
    url = repositorio.requisicao("ufs.json").url
    assert url == "https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil-wiki/main/data/ufs.json"


def test_envelope_suportado_nao_avisa(recwarn):
    envelope = {"schema_version": repositorio.SCHEMA_VERSION, "dados": []}
    assert repositorio.conferir_envelope(envelope, "ufs") is envelope
    assert not [w for w in recwarn if issubclass(w.category, DABDadosWarning)]


def test_schema_mais_novo_avisa_para_atualizar():
    with pytest.warns(DABDadosWarning, match="pip install -U"):
        repositorio.conferir_envelope({"schema_version": 99, "dados": []}, "ufs")


def test_formato_antigo_levanta_erro_claro():
    with pytest.raises(ValueError, match="pip install -U"):
        repositorio.conferir_envelope({"SC": {"nome": "Santa Catarina"}}, "ufs")
