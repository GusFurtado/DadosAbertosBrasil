"""O pacote declara que traz tipos (PEP 561)."""

import tomllib
from pathlib import Path

RAIZ = Path(__file__).parent.parent


def test_py_typed_existe_e_vai_no_wheel():
    """Sem `py.typed` no wheel, o mypy ignora os tipos e os overloads do pacote instalado."""
    assert (RAIZ / "DadosAbertosBrasil" / "py.typed").is_file()
    config = tomllib.loads((RAIZ / "pyproject.toml").read_text())
    assert "py.typed" in config["tool"]["setuptools"]["package-data"]["DadosAbertosBrasil"]
