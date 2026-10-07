import pytest
import requests
from pydantic import ValidationError

import DadosAbertosBrasil as dab
from DadosAbertosBrasil.utils import Get


class _Resposta:
    def raise_for_status(self):
        pass

    def json(self):
        return [{"codigo": 1}]


@pytest.fixture
def verify_usado(monkeypatch):
    usados = []

    def get(self, url, **kwargs):
        usados.append(kwargs["verify"])
        return _Resposta()

    monkeypatch.setattr(requests.Session, "get", get)
    yield usados
    dab.config.verificar_certificado = True


def _consultar(**kwargs):
    return Get(endpoint="camara", path=["x"], **kwargs).json


def test_padrao_verifica_certificado(verify_usado):
    _consultar()
    assert verify_usado == [True]


def test_config_global_desativa_verificacao(verify_usado):
    dab.config.verificar_certificado = False
    _consultar()
    assert verify_usado == [False]


def test_argumento_sobrescreve_config(verify_usado):
    dab.config.verificar_certificado = False
    _consultar(verify=True)
    dab.config.verificar_certificado = True
    _consultar(verify=False)
    assert verify_usado == [True, False]


def test_config_valida_atribuicao():
    with pytest.raises(ValidationError):
        dab.config.verificar_certificado = "talvez"
    with pytest.raises(ValidationError):
        dab.config.inexistente = 1
