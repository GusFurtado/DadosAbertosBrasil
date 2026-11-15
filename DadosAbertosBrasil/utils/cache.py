"""Cache local opcional para dados que mudam pouco.

Só as requisições marcadas como `cacheavel` (localidades do IBGE, referências
da Câmara e do Senado, listas do IPEA, arquivos do módulo `wiki`...) passam
por aqui, e só com `config.cache = True`. Cada resposta é um arquivo na pasta
do cache, com nome derivado da URL, válido por `config.cache_validade`.
"""

import hashlib
import os
import time
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from pathlib import Path

from .._config import config

_ignorar: ContextVar[bool] = ContextVar("ignorar_cache", default=False)


def pasta() -> Path:
    """Pasta do cache: `config.cache_pasta` ou a pasta de cache do usuário."""
    if config.cache_pasta is not None:
        return Path(config.cache_pasta)
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    else:
        base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "DadosAbertosBrasil"


def _arquivo(url: str) -> Path:
    return pasta() / f"{hashlib.sha256(url.encode()).hexdigest()}.cache"


def ativo() -> bool:
    return config.cache and not _ignorar.get()


def ler(url: str) -> str | None:
    """Resposta guardada para `url`, se o cache estiver ativo e ela for válida."""
    if not ativo():
        return None
    arquivo = _arquivo(url)
    try:
        idade = time.time() - arquivo.stat().st_mtime
        if idade > config.cache_validade.total_seconds():
            return None
        return arquivo.read_text(encoding="utf-8")
    except OSError:
        return None


def gravar(url: str, texto: str) -> None:
    """Guarda a resposta de `url`. Falhas de escrita são ignoradas."""
    if not ativo():
        return
    arquivo = _arquivo(url)
    try:
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        temporario = arquivo.with_suffix(".tmp")
        temporario.write_text(texto, encoding="utf-8")
        temporario.replace(arquivo)
    except OSError:
        pass


def limpar() -> int:
    """Apaga as respostas guardadas e retorna quantas foram apagadas."""
    removidos = 0
    for arquivo in pasta().glob("*.cache"):
        try:
            arquivo.unlink()
            removidos += 1
        except OSError:
            continue
    return removidos


@contextmanager
def sem_cache() -> Iterator[None]:
    """Ignora o cache (leitura e escrita) dentro do bloco `with`."""
    token = _ignorar.set(True)
    try:
        yield
    finally:
        _ignorar.reset(token)
