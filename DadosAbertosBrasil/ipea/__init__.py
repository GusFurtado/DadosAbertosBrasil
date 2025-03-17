"""Módulo para captura de dados abertos da API do IpeaData.

Este módulo permite acessar séries temporais de indicadores econômicos, sociais e
demográficos disponibilizados pelo Instituto de Pesquisa Econômica Aplicada (Ipea).

Mini-Tutorial
-------------

1. Importe o módulo `ipea`:

.. code-block:: python

    from DadosAbertosBrasil import ipea

2. Busque o código alfanumérico da série desejada usando `lista_series`:

.. code-block:: python

    ipea.lista_series(...)

3. Facilite a busca filtrando temas, países ou níveis territoriais:

.. code-block:: python

    temas = ipea.lista_temas(...)
    paises = ipea.lista_paises(...)
    territorios = ipea.lista_territorios(...)
    niveis = ipea.lista_niveis(...)

4. Instancie um objeto `Serie` utilizando o código encontrado:

.. code-block:: python

	serie = ipea.Serie(cod)

5. Acesse os atributos para visualizar valores e metadados da série:

.. code-block:: python

	serie.metadados
	serie.valores

6. Use a função `ipea.serie` para coletar apenas os valores da série.
Se precisar apenas dos dados, sem os metadados, esta é uma forma mais simples e rápida:

.. code-block:: python

	ipea.serie(cod)

API Original
------------

- **IpeaData:** `<http://www.ipeadata.gov.br/api/>`_

"""

from ._referencias import lista_niveis, lista_paises, lista_temas, lista_territorios
from ._serie import Serie, lista_series, serie
