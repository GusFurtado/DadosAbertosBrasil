"""Módulo para captura dos dados abertos da API do IpeaData.

Mini-Tutorial
-------------
1. Importe o módulo `ipea`.
>>> from DadosAbertosBrasil import ipea

2. Busque o código alfanumérico da série desejada com a função
`ipea.lista_series`.
>>> ipea.lista_series( ... )

3. Para facilitar a busca, filtre temas, países ou níveis territoriais com
as outras funções `lista`.
>>> temas = ipea.lista_temas( ... )
>>> paises = ipea.lista_paises( ... )
>>> territorios = ipea.lista_territorios( ... )
>>> niveis = ipea.lista_niveis( ... )

4. Instancie o objeto `Serie` utilizando o código encontrado.
>>> serie = ipea.Serie(cod)

5. Utilize os atributos para visualizar valores e metadados do série.
>>> serie.metadados
>>> serie.valores

6. Alternativamente, utilize a função `ipea.serie` para coletar apenas os
valores da série, sem os metadados. Está é uma forma simplificada e mais
rápida de obter os dados de uma série.

References
----------
.. [1] http://www.ipeadata.gov.br/api/

"""

from ._referencias import lista_niveis, lista_paises, lista_temas, lista_territorios
from ._serie import Serie, lista_series, serie
