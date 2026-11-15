import sys
import warnings
from contextlib import AbstractContextManager
from datetime import timedelta
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
    """Avisa, uma vez por sessão, que o formato não foi escolhido."""
    global _formato_avisado
    if _formato_avisado:
        return
    # Import local: `utils` importa este módulo.
    from .utils.errors import DABFormatoWarning

    _formato_avisado = True
    warnings.warn(
        "Sem `formato`, as funções retornam 'json': uma lista de registros (dicionários). "
        'Para escolher o formato padrão e silenciar este aviso, defina `DadosAbertosBrasil.config.formato = "pandas"`, '
        '"polars" ou "json".',
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
    formato : {"json", "bruto", "pydantic", "pandas", "polars"}, optional
        Formato retornado pelas funções quando o argumento `formato` não é
        informado. Se não for definido, as funções retornam `"json"` e avisam
        uma vez por sessão (`DABFormatoWarning`); defini-lo, inclusive como
        `"json"`, silencia o aviso. `"pandas"` e `"polars"` exigem a biblioteca
        instalada (`pip install DadosAbertosBrasil[pandas]` ou `[polars]`).
    cache : bool, default=False
        Guarda localmente as respostas de dados que mudam pouco (localidades
        do IBGE, referências da Câmara, arquivos do módulo `wiki`...).
    cache_validade : datetime.timedelta, default=1 dia
        Por quanto tempo uma resposta guardada vale. Aceita segundos (`int`).
    cache_pasta : pathlib.Path, optional
        Pasta do cache. Se omitida, usa a pasta de cache do usuário
        (`~/.cache/DadosAbertosBrasil` ou `%LOCALAPPDATA%\\DadosAbertosBrasil`).

    Examples
    --------
    >>> import DadosAbertosBrasil as dab
    >>> dab.config.verificar_certificado = False
    >>> dab.config.formato = "polars"
    >>> dab.config.cache = True
    >>> with dab.config.sem_cache():
    ...     dab.ibge.localidades("estados")  # consulta a API mesmo com cache
    >>> dab.config.limpar_cache()

    """

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    verificar_certificado: bool = True
    formato: Literal["json", "bruto", "pydantic", "pandas", "polars"] | None = None
    cache: bool = False
    cache_validade: timedelta = timedelta(days=1)
    cache_pasta: Path | None = None

    def limpar_cache(self) -> int:
        """Apaga as respostas guardadas no cache e retorna quantas eram."""
        from .utils import cache

        return cache.limpar()

    def sem_cache(self) -> AbstractContextManager[None]:
        """Ignora o cache dentro de um bloco `with`."""
        from .utils import cache

        return cache.sem_cache()

    def resolver_certificado(self, valor: bool | None) -> bool:
        """Retorna `valor` se informado, ou a configuração global."""
        return self.verificar_certificado if valor is None else valor

    def resolver_formato(self, valor: str | None) -> str:
        """Retorna `valor` se informado, ou o formato global."""
        if valor is not None:
            return valor
        if self.formato is None:
            _avisar_formato()
            return "json"
        return self.formato


config = Config()
