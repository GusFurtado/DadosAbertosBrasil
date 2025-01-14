"""Módulo para captura dos dados abertos da Senado Brasileiro.

Mini-Tutorial
-------------
1. Importe o módulo `senado`
>>> from DadosAbertosBrasil import senado

2. Utilize as funções `lista` para identificar o código do Senado desejado.
>>> senado.lista_senadores( ... )
>>> senado.lista_legislatura( ... )

3. Utilize a class `Senador` para obter as informações do(a) parlamentar.
>>> sen = senado.Senador(cod)

4. Após a class `Senador` ser instanciada, utilize seus métodos para buscas
outros tipos de informação sobre ele(a).
>>> sen.cargos( ... )
>>> sen.votacoes( ... )
>>> ... 

Notes
-----
http://legis.senado.gov.br/dadosabertos/docs/

"""

from ._blocos import lista_blocos
from ._legislaturas import lista_legislatura
from ._orcamentos import lista_orcamentos
from ._partidos import lista_partidos
from ._senadores import Senador, lista_senadores
from ._usos_palavras import lista_uso_palavra
