"""Módulo para captura dos dados abertos das APIs do IBGE.

Serviços Disponíveis
--------------------
- IBGE Cidades
- Nomes 2.0
- Agregados 3.0 (SIDRA)
- Malhas Geográficas 2.0
- Projeções 1.0
- Localidades 1.0

Mini-Tutorial de SIDRA
----------------------
1. Importe o módulo `ibge`.
>>> from DadosAbertosBrasil import ibge

2. Utilize a função `lista_tabelas` com os filtros necessários para encontrar
a tabela desejada.
>>> ibge.lista_tabelas( ... )

3. Utilize as funções `lista_pesquisas` e `referencias` para facilitar a busca.
>>> pesquisas = ibge.lista_pesquisas( ... )
>>> referencias = ibge.referencias( ... )

4. Após obter o código numérico da tabela, insira-o como argumento de um
objeto `Metadados`.
>>> dados = ibge.Metadados(tabela)

5. Pelos atributos do objeto `Metadados`, veja quais são os valores
disponíveis para consulta desta tabela.
>>> print(dados.periodos)
>>> print(dados.variaveis)
>>> print(dados.localidades)
>>> print(dados.classificacoes)

6. Utilize os valores encontrados nos metadados da tabela para alimentar a
função `sidra`.
>>> ibge.sidra( ... )

References
----------
.. [1] IBGE Cidades
    https://cidades.ibge.gov.br/
.. [2] Serviços
    https://servicodados.ibge.gov.br/api/docs
.. [3] SIDRA
    http://api.sidra.ibge.gov.br/

"""

from ._ibge.cidades import Galeria, Historia
from ._ibge.misc import coordenadas, localidades, malha, populacao
from ._ibge.nomes import nomes, nomes_ranking, nomes_uf
from ._ibge.sidra import Metadados, lista_pesquisas, lista_tabelas, referencias, sidra
