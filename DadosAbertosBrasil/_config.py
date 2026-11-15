import sys
import warnings
from pathlib import Path
from typing import Literal

import pydantic
from pydantic import BaseModel, ConfigDict

_formato_avisado = False
_PACOTE = str(Path(__file__).parent)
# Frames do pydantic aparecem entre o usuário e o pacote (`@validate_call`).
_INTERNOS = (_PACOTE, str(Path(pydantic.__file__).parent))


def nivel_fora_do_pacote() -> int:
    """`stacklevel` que aponta para o primeiro frame fora do DadosAbertosBrasil (e do pydantic)."""
    frame = sys._getframe(1)
    nivel = 1
    while frame is not None and frame.f_code.co_filename.startswith(_INTERNOS):
        frame = frame.f_back
        nivel += 1
    return nivel


def _avisar_formato() -> None:
    """Avisa, uma vez por sessão, que o formato padrão muda no 3.0."""
    global _formato_avisado
    if _formato_avisado:
        return
    # Import local: `utils` importa este módulo.
    from .utils.errors import GUIA_MIGRACAO, DABFormatoWarning

    _formato_avisado = True
    warnings.warn(
        "No DadosAbertosBrasil 3.0, as funções chamadas sem `formato` passam a "
        "retornar 'json' (lista de registros) em vez de um DataFrame pandas, e o "
        "pandas vira dependência opcional (`pip install DadosAbertosBrasil[pandas]`). "
        'Defina `DadosAbertosBrasil.config.formato = "pandas"` (ou "polars") para '
        f"manter o retorno atual e silenciar este aviso. Guia de migração: {GUIA_MIGRACAO}",
        DABFormatoWarning,
        stacklevel=nivel_fora_do_pacote(),
    )


class Config(BaseModel):
    """Configurações globais do pacote.

    Os valores podem ser alterados por atribuição direta e são validados na
    hora. Argumentos passados diretamente às funções têm precedência sobre
    estas configurações.

    Attributes
    ----------
    verificar_certificado : bool, default=True
        Verifica o certificado SSL das requisições. Defina como `False` em caso
        de falha na verificação do certificado.
    formato : {"pandas", "polars"}, default="pandas"
        Biblioteca usada nos DataFrames retornados pelas funções quando o
        argumento `formato` não é informado. Requer `polars` instalado para
        `"polars"` (`pip install DadosAbertosBrasil[polars]`). Enquanto não for
        definido, as funções avisam (uma vez por sessão, com
        `DABFormatoWarning`) que o padrão muda para `"json"` no 3.0.

    Examples
    --------
    >>> import DadosAbertosBrasil as dab
    >>> dab.config.verificar_certificado = False
    >>> dab.config.formato = "polars"

    """

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    verificar_certificado: bool = True
    formato: Literal["pandas", "polars"] = "pandas"

    def resolver_certificado(self, valor: bool | None) -> bool:
        """Retorna `valor` se informado, ou a configuração global."""
        return self.verificar_certificado if valor is None else valor

    def resolver_formato(self, valor: str | None) -> str:
        """Retorna `valor` se informado, ou o formato global."""
        if valor is not None:
            return valor
        if "formato" not in self.model_fields_set:
            _avisar_formato()
        return self.formato


config = Config()
