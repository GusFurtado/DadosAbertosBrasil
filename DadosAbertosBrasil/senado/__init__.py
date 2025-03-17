"""Módulo para captura de dados abertos do Senado Brasileiro.

Este módulo permite acessar informações sobre senadores, legislaturas, partidos,
orçamentos e outros dados legislativos disponibilizados pelo Senado Federal.

Mini-Tutorial
-------------

1. Importe o módulo `senado`:

.. code-block:: python

    from DadosAbertosBrasil import senado

2. Utilize as funções `lista` para obter códigos necessários:

.. code-block:: python

    senado.lista_senadores(...)
	senado.lista_legislatura(...)

Instancie um objeto `Senador` para acessar informações do parlamentar:

.. code-block:: python

    sen = senado.Senador(cod)

Utilize os métodos da classe `Senador` para obter mais detalhes:

.. code-block:: python

    sen.cargos(...)
	sen.votacoes(...)

API Original
------------ 
  
- **Dados Abertos do Senado:** `<http://legis.senado.gov.br/dadosabertos/docs/>`_

"""

from ._blocos import lista_blocos
from ._legislaturas import lista_legislatura
from ._orcamentos import lista_orcamentos
from ._partidos import lista_partidos
from ._senadores import Senador, lista_senadores
from ._usos_palavras import lista_uso_palavra
