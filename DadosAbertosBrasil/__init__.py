"""
Dados Abertos Brasil
====================

Dados Abertos Brasil é uma iniciativa para facilitar o acesso a dados abertos e APIs do governo brasileiro.

É um pacote open-source para Python e Pandas e a forma mais simples de acessar dados de instituições como IBGE, IPEA, Banco Central, etc.

Módulos
-------

- ``DadosAbertosBrasil.ibge``
- ``DadosAbertosBrasil.ipea``
- ``DadosAbertosBrasil.camara``
- ``DadosAbertosBrasil.senado``
- ``DadosAbertosBrasil.bacen``
- ``DadosAbertosBrasil.favoritos``
- ``DadosAbertosBrasil.uf``

Sobre
-----

- **Página Oficial:** `<https://www.gustavofurtado.com/dab.html>`_
- **Documentação:** `<https://www.gustavofurtado.com/DadosAbertosBrasil>`_

Instalação
----------

Para instalar, utilize o seguinte comando:

.. code-block:: bash

   pip install DadosAbertosBrasil

Dependências
------------

- `Python 3.10 ou superior <https://www.python.org/>`_
- `Pandas <https://pandas.pydata.org/>`_
- `Pydantic <https://docs.pydantic.dev/latest/>`_
- `Requests <https://requests.readthedocs.io/en/master/>`_

Licença
-------

- MIT


"""

from . import bacen
from . import camara
from . import ibge
from . import ipea
from . import senado
from . import uf
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
    DAB_DataError,
    DAB_InputError,
    DAB_LocalidadeError,
    DAB_MoedaError,
    DAB_UFError,
    DAB_DeprecationError,
)


__all__ = [
    "bacen",
    "camara",
    "ibge",
    "ipea",
    "senado",
    "uf",
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
    "DAB_DataError",
    "DAB_InputError",
    "DAB_LocalidadeError",
    "DAB_MoedaError",
    "DAB_UFError",
    "DAB_DeprecationError",
]

__author__ = "Gustavo Furtado da Silva"
