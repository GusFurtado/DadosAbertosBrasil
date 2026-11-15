"""Os overloads por `formato` acompanham a assinatura de cada função.

Gerados por `scripts/gerar_overloads.py`: se este teste falhar depois de
mudar uma assinatura, rode o script de novo.
"""

import inspect
import types
import typing

import pytest

from DadosAbertosBrasil import bacen, camara, favoritos, ibge, ipea, senado, uf, wiki
from DadosAbertosBrasil.utils.typing import Formato

FORMATOS = set(typing.get_args(Formato))


def _valores(anotacao) -> set:
    """Valores de um `Literal[...]`, de um `Formato | None` ou de uniões deles."""
    if anotacao is None or anotacao is type(None):
        return {None}
    if typing.get_origin(anotacao) is typing.Literal:
        return set(typing.get_args(anotacao))
    if typing.get_origin(anotacao) in (typing.Union, types.UnionType):
        return set().union(*(_valores(a) for a in typing.get_args(anotacao)))
    return set()


def _funcoes_de_dados():
    for modulo in (bacen, camara, favoritos, ibge, ipea, senado, uf, wiki):
        for nome in dir(modulo):
            if nome.startswith("_"):
                continue
            obj = getattr(modulo, nome)
            candidatos = [(nome, obj)]
            if inspect.isclass(obj):
                candidatos = [(f"{nome}.{n}", getattr(obj, n)) for n in vars(obj) if not n.startswith("_")]
            for qualname, funcao in candidatos:
                if not inspect.isfunction(funcao):
                    continue
                parametro = inspect.signature(funcao).parameters.get("formato")
                if parametro is None or not _valores(parametro.annotation) & {"pandas"}:
                    continue
                yield f"{modulo.__name__.split('.')[-1]}.{qualname}", funcao


FUNCOES = sorted(dict(_funcoes_de_dados()).items())


def test_ha_funcoes_de_dados():
    assert len(FUNCOES) >= 85


@pytest.mark.parametrize("nome, funcao", FUNCOES)
def test_overloads_acompanham_a_assinatura(nome, funcao):
    overloads = typing.get_overloads(funcao)
    assert overloads, f"{nome} sem overloads: rode scripts/gerar_overloads.py"

    implementacao = inspect.signature(funcao)
    aceitos = _valores(implementacao.parameters["formato"].annotation)
    cobertos = set()
    for sobrecarga in overloads:
        assinatura = inspect.signature(sobrecarga)
        assert list(assinatura.parameters) == list(implementacao.parameters), nome
        for parametro, original in zip(assinatura.parameters.values(), implementacao.parameters.values()):
            if parametro.name == "formato":
                cobertos |= _valores(parametro.annotation)
                continue
            assert parametro.annotation == original.annotation, f"{nome}: {parametro.name}"
            assert (parametro.default is inspect.Parameter.empty) == (original.default is inspect.Parameter.empty)
    assert cobertos == aceitos | {None}, nome
    assert aceitos - {None} <= FORMATOS


@pytest.mark.parametrize("nome, funcao", FUNCOES)
def test_overload_sem_formato_retorna_any(nome, funcao):
    """Sem `formato`, o retorno depende de `config.formato`."""
    primeiro = typing.get_overloads(funcao)[0]
    assinatura = inspect.signature(primeiro)
    assert None in _valores(assinatura.parameters["formato"].annotation), nome
    assert assinatura.return_annotation is typing.Any, nome
