"""Dados Abertos Brasil é uma iniciativa para facilitar o acesso a dados
abertos e APIs do governo brasileiro.

É um pacote open-source para Python e Pandas e a forma mais simples de acessar
dados de instituições como IGBE, IPEA, Banco Central, etc.

Módulos
-------
- DadosAbertosBrasil.ibge
- DadosAbertosBrasil.ipea
- DadosAbertosBrasil.camara
- DadosAbertosBrasil.senado
- DadosAbertosBrasil.bacen
- DadosAbertosBrasil.favoritos
- DadosAbertosBrasil.UF

Sobre
-----
- Página Oficial: https://www.gustavofurtado.com/dab.html
- Documentação: https://www.gustavofurtado.com/DadosAbertosBrasil

Instalação
----------
- `pip install DadosAbertosBrasil`

Dependências
------------
- Python 3.6 ou superior
- pandas
- requests

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
from .favoritos import *
from .utils.errors import *


__version__ = "2.0.0-alpha"
__author__ = "Gustavo Furtado da Silva"
