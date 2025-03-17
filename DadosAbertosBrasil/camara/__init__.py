"""Módulo para captura de dados abertos da Câmara dos Deputados do Brasil.

Este módulo permite acessar informações detalhadas sobre deputados, partidos, 
frentes parlamentares, proposições, votações e outros dados legislativos 
disponibilizados pela API da Câmara dos Deputados.

Mini-Tutorial
-------------

1. Importe o módulo `camara`:

.. code-block:: python

	from DadosAbertosBrasil import camara

2. Busque o código do objeto de estudo utilizando as funções `lista`:

.. code-block:: python

	camara.lista_deputados(...)

3. Instancie o objeto de estudo utilizando o código encontrado:

.. code-block:: python

	dep = camara.Deputado(cod)

4. Utilize os atributos da classe para obter informações básicas do objeto:

.. code-block:: python
	
    dep.dados

5. Utilize os métodos da classe para obter informações detalhadas do objeto:

.. code-block:: python

	dep.despesas(...)

API Oficial
-----------

- **Dados Abertos da Câmara dos Deputados:** `<https://dadosabertos.camara.leg.br/swagger/api.html>`_

"""

from ._blocos import Bloco, lista_blocos
from ._deputados import Deputado, lista_deputados
from ._eventos import Evento, lista_eventos
from ._frentes import Frente, lista_frentes
from ._legislaturas import Legislatura, lista_legislaturas
from ._orgaos import Orgao, lista_orgaos
from ._partidos import Partido, lista_partidos
from ._proposicoes import Proposicao, lista_proposicoes
from ._referencias import referencias
from ._votacoes import Votacao, lista_votacoes
