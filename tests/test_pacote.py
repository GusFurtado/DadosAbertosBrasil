"""O pacote declara que traz tipos (PEP 561)."""

import tomllib
import types
from pathlib import Path

import pytest

from DadosAbertosBrasil import bacen, camara, favoritos, ibge, ipea, senado, uf, wiki

RAIZ = Path(__file__).parent.parent


def test_py_typed_existe_e_vai_no_wheel():
    """Sem `py.typed` no wheel, o mypy ignora os tipos e os overloads do pacote instalado."""
    assert (RAIZ / "DadosAbertosBrasil" / "py.typed").is_file()
    config = tomllib.loads((RAIZ / "pyproject.toml").read_text())
    assert "py.typed" in config["tool"]["setuptools"]["package-data"]["DadosAbertosBrasil"]


def test_stubs_vao_no_wheel():
    """Os `.pyi` com os overloads por `formato` (gerados por scripts/gerar_stubs.py)."""
    assert list((RAIZ / "DadosAbertosBrasil").rglob("*.pyi"))
    config = tomllib.loads((RAIZ / "pyproject.toml").read_text())
    assert "*.pyi" in config["tool"]["setuptools"]["package-data"]["*"]


@pytest.mark.parametrize("modulo", [bacen, camara, favoritos, ibge, ipea, senado, uf, wiki], ids=lambda m: m.__name__)
def test_reexportacoes_no_all(modulo):
    """Num pacote com `py.typed`, o pyright só considera públicos os nomes de `__all__`.

    Sem isso, `camara.lista_partidos` aparece como erro (`reportPrivateImportUsage`).
    """
    reexportados = {
        nome
        for nome, obj in vars(modulo).items()
        if not nome.startswith("_")
        and not isinstance(obj, types.ModuleType)
        and getattr(obj, "__module__", "").startswith(f"{modulo.__name__}.")
    }
    assert reexportados <= set(getattr(modulo, "__all__", ())), sorted(
        reexportados - set(getattr(modulo, "__all__", ()))
    )
