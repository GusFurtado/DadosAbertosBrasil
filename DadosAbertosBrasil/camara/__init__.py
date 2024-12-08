"""Módulo para captura dos dados abertos da Câmara dos Deputados do Brasil.

Mini-Tutorial
-------------
1. Importe o módulo `camara`.
>>> from DadosAbertosBrasil import camara

2. Busque o código do objeto de estudo utilizando as funções `lista`.
>>> camara.lista_deputados( ... )

3. Instancie o objeto de estudo utilizando o código encontrado.
>>> dep = camara.Deputado(cod)

4. Utilize os atributos da classe para obter informações básicas do objeto.
>>> dep.dados

5. Utilize os métodos da classe para obter informações detalhadas do objeto.
>>> dep.despesas( ... )

References
----------
.. [1] https://dadosabertos.camara.leg.br/swagger/api.html

"""

from ._blocos import Bloco, lista_blocos
from ._deputados import Deputado, lista_deputados
from ._eventos import Evento, lista_eventos
from ._frentes import Frente, lista_frentes
from ._legislaturas import Legislatura, lista_legislaturas
from ._orgaos import Orgao, lista_orgaos
from ._partidos import Partido, lista_partidos
from ._referencias import referencias
from ._votacoes import Votacao, lista_votacoes
