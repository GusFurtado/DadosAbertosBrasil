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
    - DadosAbertosBrasil.favoritos

Sobre
-----
    - Página Oficial: https://www.gustavofurtado.com/dab.html
    - Documentação: https://www.gustavofurtado.com/doc.html

Instalação
----------
    - pip install DadosAbertosBrasil

Dependências
------------
    - pandas
    - requests

Licença
-------
    - MIT

Próximos Passos
---------------
    - Conclusão do módulo senado;
    - Substituição das funções do módulo camara por classes.
      Atualmente as funções capturam apenas dados dos últimos
      seis meses e da última legislatura;
    - Expansão das funções de filtro e busca de séries,
      para facilitar encontrar a série desejada;
    - Padronização dos nomes das colunas dos DataFrame para
      melhor interpretação do usuário e integração entre módulos;
    - Adição constante de novas funções no módulo favoritos.
'''



__version__ = '0.1.3'
__author__ = 'Gustavo Furtado da Silva'