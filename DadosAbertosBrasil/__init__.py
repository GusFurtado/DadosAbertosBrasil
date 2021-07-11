'''
Dados Abertos Brasil é uma iniciativa para facilitar o acesso a dados abertos
e APIs do governo brasileiro.

É um pacote open-source para Python e Pandas e a forma mais simples de acessar
dados de instituições como IGBE, IPEA, etc.

Módulos em Desenvolvimento
--------------------------
    - DadosAbertosBrasil.ibge
    - DadosAbertosBrasil.ipea
    - DadosAbertosBrasil.camara
    - DadosAbertosBrasil.senado
    - DadosAbertosBrasil.bacen
    - DadosAbertosBrasil.favoritos

Sobre
-----
    - Página Oficial: https://www.gustavofurtado.com/dab.html
    - Documentação: https://www.gustavofurtado.com/DadosAbertosBrasil/index.html

Instalação
----------
    - pip install DadosAbertosBrasil

Dependências
------------
    - Python 3.6 ou superior
    - pandas
    - requests

Licença
-------
    - MIT

Próximos Passos
---------------
    - Conclusão do módulo `senado`;
    - Desenvolvimento do módulo `transparencia` para coleta de dados do
      Portal da Transparência do Governo Federal;
    - Adicionar novos exemplos à documentação;
    - Adição constante de novas funções no módulo `favoritos`.
'''



__version__ = '0.2.4'
__author__ = 'Gustavo Furtado da Silva'



from . import bacen
from . import camara
from . import ibge
from . import ipea
from . import senado
from .favoritos import *
from .uf import UF