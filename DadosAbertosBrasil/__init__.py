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
    - Expandir módulo `bacen` com coleta de dados de expectativas de mercado;
    - Adicionar novos exemplos à documentação;
    - Adição constante de novas funções no módulo `favoritos`.
'''



__version__ = '0.2.2'
__author__ = 'Gustavo Furtado da Silva'



from typing import Union

import requests



def get_data(
        endpoint: str,
        path: Union[str, list],
        params: dict = None
    ) -> dict:
    '''
    Coleta os dados requisitados das APIs REST.

    Parâmetros
    ----------
    endpoint : str
        Diretório base da API desejada.
    path : list ou str
        Caminho de parâmetros para acessar a função desejada.
        Pode ser uma string de parâmetros unidos por barras '/' ou pode ser
        uma lista de strings na ordem correta. Os dois métodos produzem o
        mesmo resultado.
    params : dict (default=None)
        Dicionário de parâmetros de busca que serão enviados para o request.

    Retorna
    -------
    dict
        Dados brutos coletados da API.

    --------------------------------------------------------------------------   
    '''

    if isinstance(path, list):
        path = '/'.join(path)

    return requests.get(
        url = endpoint + path,
        headers = {'Accept':'application/json'},
        params = params
    ).json()