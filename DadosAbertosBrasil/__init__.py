"""
Dados Abertos Brasil
====================

Dados Abertos Brasil é uma iniciativa para facilitar o acesso a dados abertos e APIs do governo brasileiro.

É um pacote open-source para Python e a forma mais simples de acessar dados de instituições como IBGE, IPEA, Banco Central, etc.

Módulos
-------
- ``DadosAbertosBrasil.ibge``
- ``DadosAbertosBrasil.ipea``
- ``DadosAbertosBrasil.camara``
- ``DadosAbertosBrasil.senado``
- ``DadosAbertosBrasil.bacen``
- ``DadosAbertosBrasil.favoritos``
- ``DadosAbertosBrasil.uf``
- ``DadosAbertosBrasil.wiki``

Sobre
-----
- **Página Oficial:** `<https://github.com/GusFurtado/DadosAbertosBrasil>`_
- **Documentação:** `<https://www.gustavofurtado.com/DadosAbertosBrasil/>`_

Instalação
----------
Para instalar, utilize o seguinte comando:

.. code-block:: bash

   pip install DadosAbertosBrasil

Dependências
------------
- `Python 3.11 ou superior <https://www.python.org/>`_
- `Pydantic <https://docs.pydantic.dev/latest/>`_
- `Requests <https://requests.readthedocs.io/en/master/>`_
- Opcionais: `pandas <https://pandas.pydata.org/>`_ (``[pandas]``) e `polars <https://pola.rs/>`_ (``[polars]``)

Licença
-------
- MIT


"""

from . import bacen, camara, ibge, ipea, senado, uf, wiki
from ._config import config
from .favoritos import (
    bandeira,
    brasao,
    catalogo,
    codigos_municipios,
    ipca,
    perfil_eleitorado,
    pib,
    rentabilidade_poupanca,
    reservas_internacionais,
    risco_brasil,
    salario_minimo,
    selic,
    taxa_referencial,
)
from .utils.errors import (
    DABDataError,
    DABError,
    DABFormatoWarning,
    DABFuncaoRemovidaError,
    DABInputError,
    DABLocalidadeError,
    DABMoedaError,
    DABUFError,
)
from .utils.errors import nome_antigo as _nome_antigo

__all__ = [
    "bacen",
    "camara",
    "ibge",
    "ipea",
    "senado",
    "uf",
    "wiki",
    "config",
    "bandeira",
    "brasao",
    "catalogo",
    "codigos_municipios",
    "ipca",
    "perfil_eleitorado",
    "pib",
    "rentabilidade_poupanca",
    "reservas_internacionais",
    "risco_brasil",
    "salario_minimo",
    "selic",
    "taxa_referencial",
    "DABDataError",
    "DABError",
    "DABFormatoWarning",
    "DABFuncaoRemovidaError",
    "DABInputError",
    "DABLocalidadeError",
    "DABMoedaError",
    "DABUFError",
]

__author__ = "Gustavo Furtado da Silva"
__version__ = "3.0.0"


def __getattr__(nome: str):
    # Nomes antigos das exceções (`DAB_UFError` etc.), com aviso.
    classe = _nome_antigo(nome)
    if classe is None:
        raise AttributeError(f"module {__name__!r} has no attribute {nome!r}")
    return classe
