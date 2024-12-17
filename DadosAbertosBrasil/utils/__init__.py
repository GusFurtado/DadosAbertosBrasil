"""O subpacote `_utils` contém ferramentas de auxílio às funções do pacote.

Módulos
-------
errors
    Pacote de `Exceptions` exclusivas para as funções do `DadosAbertosBrasil`
get
    Pacote contendo a função para captura de dados em formato JSON.
parse
    Pacote para padronização de inputs das funções do `DadosAbertosBrasil`

"""

from .get import Base, Get
from .typing import Formato, Expectativa, NivelTerritorial, Output
