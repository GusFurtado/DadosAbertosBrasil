"""Módulo para captura de dados abertos das APIs do IBGE.

Este módulo fornece acesso a diversas informações do Instituto Brasileiro de Geografia e Estatística (IBGE), 
incluindo dados geográficos, demográficos e estatísticos.

Serviços Disponíveis
--------------------

- **IBGE Cidades**: Informações sobre municípios brasileiros.
- **Nomes 2.0**: Estatísticas sobre nomes mais comuns no Brasil.
- **Agregados 3.0 (SIDRA)**: Dados de séries temporais e tabelas estatísticas.
- **Malhas Geográficas 2.0**: Arquivos geoespaciais do Brasil.
- **Projeções 1.0**: Projeções populacionais e estatísticas futuras.
- **Localidades 1.0**: Informações detalhadas sobre unidades territoriais.

Mini-Tutorial de SIDRA
----------------------

1. Importe o módulo `ibge`:

.. code-block:: python

	from DadosAbertosBrasil import ibge

2. Utilize `lista_tabelas` para encontrar a tabela desejada:

.. code-block:: python

	ibge.lista_tabelas(...)

3. Use `lista_pesquisas` e `referencias` para facilitar a busca:

.. code-block:: python

	pesquisas = ibge.lista_pesquisas(...)
	referencias = ibge.referencias(...)

4. Após obter o código numérico da tabela, instancie um objeto `Metadados`:

.. code-block:: python

	dados = ibge.Metadados(tabela)

5. Verifique os valores disponíveis para consulta na tabela:

.. code-block:: python

	print(dados.periodos)
	print(dados.variaveis)
	print(dados.localidades)
	print(dados.classificacoes)

6. Use os valores dos metadados para alimentar a função `sidra`:

.. code-block:: python

	ibge.sidra(...)

APIs Originais
--------------

- **IBGE Cidades:** `<https://cidades.ibge.gov.br/>`_
- **Serviços IBGE:** `<https://servicodados.ibge.gov.br/api/docs>`_
- **SIDRA:** `<http://api.sidra.ibge.gov.br/>`_

"""

from ._cidades import Galeria, Historia
from ._misc import coordenadas, localidades, malha, populacao
from ._nomes import nomes, nomes_ranking, nomes_uf
from ._sidra import Metadados, lista_pesquisas, lista_tabelas, referencias, sidra
