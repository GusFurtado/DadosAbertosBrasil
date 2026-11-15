"""Erros e avisos específicos dos módulos do DadosAbertosBrasil.

Todas as exceções herdam de `DABError`, então `except DABError` captura
qualquer erro do pacote. Cada uma também herda da exceção nativa
correspondente (`ValueError` ou `TypeError`).

"""

import warnings

from .._config import nivel_fora_do_pacote

GUIA_MIGRACAO = "https://www.gustavofurtado.com/DadosAbertosBrasil/migracao/"
"""Endereço do guia de migração do 2.x para o 3.0."""


class DABError(Exception):
    """Base de todos os erros do DadosAbertosBrasil."""


class DABDataError(DABError, TypeError):
    """Erro gerado quando o usuário insere um valor inválido para a data."""


class DABInputError(DABError, ValueError):
    """Erro gerado quando o usuário insere um valor inválido para um argumento."""


class DABLocalidadeError(DABError, TypeError):
    """Erro gerado quando o usuário insere um valor inválido para a localidade."""


class DABMoedaError(DABError, ValueError):
    """Erro gerado quando o usuário insere um valor inválido para uma moeda."""


class DABUFError(DABError, ValueError):
    """Erro gerado quando o usuário insere um valor inválido para a UF."""


class DABFormatoWarning(FutureWarning):
    """Aviso de que o formato padrão de retorno muda no DadosAbertosBrasil 3.0.

    Para silenciar, defina `DadosAbertosBrasil.config.formato`.
    """


class DABValidacaoWarning(UserWarning):
    """Aviso de um valor da API que não corresponde ao modelo de saída.

    Quase sempre indica que a API mudou. O valor é mantido como veio.
    """


class _DABDeprecationError(DeprecationWarning):
    """Erro gerado quando o usuário chama uma função depreciada."""


def descontinuado(mensagem: str, stacklevel: int | None = None) -> None:
    """Emite um `DeprecationWarning` com o link do guia de migração.

    Se `stacklevel` for omitido, o aviso aponta para a primeira linha fora do
    pacote, mesmo com `@validate_call` no meio.
    """
    warnings.warn(
        f"{mensagem} Veja o guia de migração: {GUIA_MIGRACAO}",
        DeprecationWarning,
        stacklevel=stacklevel or nivel_fora_do_pacote(),
    )


NOMES_ANTIGOS = {
    "DAB_DataError": "DABDataError",
    "DAB_InputError": "DABInputError",
    "DAB_LocalidadeError": "DABLocalidadeError",
    "DAB_MoedaError": "DABMoedaError",
    "DAB_UFError": "DABUFError",
}


def nome_antigo(nome: str):
    """Resolve um nome antigo de exceção, avisando da mudança.

    Retorna `None` se `nome` não for um nome antigo.
    """
    if nome in NOMES_ANTIGOS:
        novo = NOMES_ANTIGOS[nome]
        descontinuado(
            f"`{nome}` foi renomeado para `{novo}` e o nome antigo deixa de "
            "existir em uma versão futura do 3.x.",
            stacklevel=4,
        )
        return globals()[novo]
    if nome == "DAB_DeprecationError":
        descontinuado(
            "`DAB_DeprecationError` não é usado pelo pacote e será removido no 3.0.",
            stacklevel=4,
        )
        return _DABDeprecationError
    return None


def __getattr__(nome: str):
    classe = nome_antigo(nome)
    if classe is None:
        raise AttributeError(f"module {__name__!r} has no attribute {nome!r}")
    return classe
