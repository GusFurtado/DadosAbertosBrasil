"""Os stubs (`.pyi`) com os overloads por `formato` acompanham o código.

Gerados por `scripts/gerar_stubs.py`: se um destes testes falhar depois de
mudar a interface de um módulo, rode o script de novo.
"""

import ast
import importlib.util
import inspect
import subprocess
import sys
import types
import typing
from pathlib import Path

import pytest

from DadosAbertosBrasil import bacen, camara, favoritos, ibge, ipea, senado, uf, wiki
from DadosAbertosBrasil.utils.typing import Formato

RAIZ = Path(__file__).parent.parent
PACOTE = RAIZ / "DadosAbertosBrasil"
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


def _valores_no_stub(anotacao: ast.expr) -> set:
    """O mesmo que `_valores`, lendo a anotação do stub."""
    if isinstance(anotacao, ast.Constant) and anotacao.value is None:
        return {None}
    if isinstance(anotacao, ast.BinOp):
        return _valores_no_stub(anotacao.left) | _valores_no_stub(anotacao.right)
    if isinstance(anotacao, ast.Subscript) and ast.unparse(anotacao.value) == "Literal":
        valores = ast.literal_eval(anotacao.slice)
        return set(valores) if isinstance(valores, tuple) else {valores}
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


def _definicoes(arquivo: Path, qualname: str) -> list[ast.FunctionDef]:
    corpo = ast.parse(arquivo.read_text()).body
    *classes, nome = qualname.split(".")
    for classe in classes:
        corpo = next(n for n in corpo if isinstance(n, ast.ClassDef) and n.name == classe).body
    return [n for n in corpo if isinstance(n, ast.FunctionDef) and n.name == nome]


def _implementacao_e_overloads(funcao) -> tuple[ast.FunctionDef, list[ast.FunctionDef]]:
    original = inspect.unwrap(funcao)
    arquivo = Path(inspect.getsourcefile(original))
    (implementacao,) = _definicoes(arquivo, original.__qualname__)
    stub = arquivo.with_suffix(".pyi")
    assert stub.exists(), f"{stub.name} não existe: rode scripts/gerar_stubs.py"
    overloads = [
        n
        for n in _definicoes(stub, original.__qualname__)
        if any(ast.unparse(d) == "overload" for d in n.decorator_list)
    ]
    return implementacao, overloads


def _parametros(funcao: ast.FunctionDef) -> list[tuple[str, str, bool]]:
    """(nome, anotação, tem default) de cada parâmetro, na ordem."""
    args = funcao.args
    sem_default = len(args.args) - len(args.defaults)
    posicionais = [(a, i >= sem_default) for i, a in enumerate(args.args)]
    nomeados = [(a, d is not None) for a, d in zip(args.kwonlyargs, args.kw_defaults, strict=True)]
    return [(a.arg, ast.unparse(a.annotation) if a.annotation else "", d) for a, d in posicionais + nomeados]


def _gerador():
    spec = importlib.util.spec_from_file_location("gerar_stubs", RAIZ / "scripts" / "gerar_stubs.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def test_ha_funcoes_de_dados():
    assert len(FUNCOES) >= 85


def test_stubs_em_dia():
    esperados = _gerador().gerar()
    assert set(PACOTE.rglob("*.pyi")) == set(esperados), "rode scripts/gerar_stubs.py"
    for stub, texto in esperados.items():
        assert stub.read_text() == texto, f"{stub.relative_to(RAIZ)} desatualizado: rode scripts/gerar_stubs.py"


@pytest.mark.parametrize("nome, funcao", FUNCOES)
def test_overloads_acompanham_a_assinatura(nome, funcao):
    implementacao, overloads = _implementacao_e_overloads(funcao)
    assert overloads, f"{nome} sem overloads: rode scripts/gerar_stubs.py"

    originais = _parametros(implementacao)
    aceitos = _valores(inspect.signature(funcao).parameters["formato"].annotation)
    cobertos = set()
    for sobrecarga in overloads:
        parametros = _parametros(sobrecarga)
        assert [p[0] for p in parametros] == [p[0] for p in originais], nome
        for parametro, original in zip(parametros, originais, strict=True):
            if parametro[0] == "formato":
                formato = next(a for a in sobrecarga.args.args + sobrecarga.args.kwonlyargs if a.arg == "formato")
                cobertos |= _valores_no_stub(formato.annotation)
                continue
            assert parametro == original, f"{nome}: {parametro[0]}"
    assert cobertos == aceitos | {None}, nome
    assert aceitos - {None} <= FORMATOS


@pytest.mark.parametrize("nome, funcao", FUNCOES)
def test_overload_sem_formato_retorna_any(nome, funcao):
    """Sem `formato`, o retorno depende de `config.formato`."""
    _, overloads = _implementacao_e_overloads(funcao)
    primeiro = overloads[0]
    formato = next(a for a in primeiro.args.args + primeiro.args.kwonlyargs if a.arg == "formato")
    assert None in _valores_no_stub(formato.annotation), nome
    assert ast.unparse(primeiro.returns) == "Any", nome


def _modulo(arquivo: Path) -> str:
    partes = arquivo.relative_to(RAIZ).with_suffix("").parts
    return ".".join(partes[:-1] if partes[-1] == "__init__" else partes)


@pytest.fixture(scope="module")
def config_mypy(tmp_path_factory) -> Path:
    """Checa os stubs; os módulos sem stub ainda têm erros de tipo antigos e ficam de fora."""
    sem_stub = sorted(_modulo(a) for a in PACOTE.rglob("*.py") if not a.with_suffix(".pyi").exists())
    config = tmp_path_factory.mktemp("mypy") / "mypy.ini"
    config.write_text(f"[mypy]\nignore_missing_imports = True\n\n[mypy-{','.join(sem_stub)}]\nignore_errors = True\n")
    return config


def _rodar(*argumentos: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-m", *argumentos], capture_output=True, text=True, cwd=RAIZ)


def test_stubtest(config_mypy):
    """Os stubs declaram o que existe em tempo de execução, com as mesmas assinaturas."""
    modulos = sorted(_modulo(a.with_suffix(".py")) for a in PACOTE.rglob("*.pyi"))
    allowlist = RAIZ / "tests" / "stubtest_allowlist.txt"
    saida = _rodar("mypy.stubtest", "--mypy-config-file", str(config_mypy), "--allowlist", str(allowlist), *modulos)
    assert saida.returncode == 0, saida.stdout + saida.stderr


@pytest.mark.skipif(importlib.util.find_spec("polars") is None, reason="o exemplo usa polars.DataFrame")
def test_tipos_no_mypy(config_mypy):
    """O mypy vê o tipo de retorno de cada `formato` (tests/tipos/uso.py)."""
    saida = _rodar(
        "mypy",
        "--config-file",
        str(config_mypy),
        "--enable-error-code",
        "deprecated",
        "--warn-unused-ignores",
        "tests/tipos/uso.py",
    )
    assert saida.returncode == 0, saida.stdout + saida.stderr
