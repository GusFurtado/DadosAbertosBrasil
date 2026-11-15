"""Leitura dos arquivos do repositório de dados DadosAbertosBrasil-wiki.

Cada versão maior do pacote lê de um ponto fixo do repositório: o 3.x lê da
`main`. Se o formato mudar de forma incompatível, o repositório congela um
branch `3.x` antes da mudança e o pacote passa a ler dele.
"""

import warnings
from typing import Any

from .endpoints import ENDPOINTS
from .errors import DABDadosWarning
from .requisicao import Requisicao

SCHEMA_VERSION = 1
"""Maior `schema_version` do envelope que esta versão do pacote entende."""


def requisicao(arquivo: str, verificar_certificado: bool | None = None) -> Requisicao:
    """Requisição de um arquivo de `data/` do repositório de dados."""
    return Requisicao("wiki", [arquivo], verificar_certificado=verificar_certificado, cacheavel=True)


def conferir_envelope(envelope: Any, dataset: str) -> dict:
    """Confere o envelope (`schema_version`, `dados`) de um arquivo de dados.

    Um `schema_version` maior que o suportado gera `DABDadosWarning` pedindo
    para atualizar o pacote; a leitura continua e pode falhar adiante.
    """
    if not isinstance(envelope, dict) or "dados" not in envelope:
        raise ValueError(
            f"O arquivo do dataset '{dataset}' não está no formato esperado (envelope com `dados`). "
            "Atualize o DadosAbertosBrasil: `pip install -U DadosAbertosBrasil`."
        )
    versao = envelope.get("schema_version")
    if not isinstance(versao, int) or versao > SCHEMA_VERSION:
        warnings.warn(
            f"O dataset '{dataset}' usa o formato de dados {versao!r}, mais novo que o suportado por esta "
            f"versão do DadosAbertosBrasil ({SCHEMA_VERSION}). Atualize o pacote com "
            "`pip install -U DadosAbertosBrasil`.",
            DABDadosWarning,
            stacklevel=4,
        )
    return envelope
