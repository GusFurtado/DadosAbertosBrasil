'''
Dados Abertos Brasil é uma iniciativa para facilitar o acesso a dados abertos
e APIs do governo brasileiro.

É um pacote open-source para Python e Pandas e a forma mais simples de acessar
dados de instituições como IGBE, IPEA, etc.

Módulos em Desenvolvimento
--------------------------
    - DadosAbertosBrasil.API
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



import requests



ENDPOINTS = {
    'camara': 'https://dadosabertos.camara.leg.br/api/v2/',
    'ipea': 'http://www.ipeadata.gov.br/api/odata4/',
    'senado': 'http://legis.senado.gov.br/dadosabertos/',
}



class API:
    '''
    Classe para coleta direta dos dados brutos das API REST.

    Parâmetros
    ----------
    endpoint: str
        Qual API deseja se conectar:
        - 'camara': Acessar API da Câmara dos Deputados;
        - 'senado': Acessar API do Senado Federal.

    Exemplos
    --------
    >>> from DadosAbertosBrasil import API
    >>> api = API(endpoint='camara')
    >>> api.get(keys=['referencias', 'proposicoes', 'codTipoAutor'])

    >>> api = API(endpoint='senado')
    >>> api.get(keys='/autor/lista/atual')

    Documentação original
    ---------------------
    'camara'
        https://dadosabertos.camara.leg.br/swagger/api.html
    'senado'
        http://legis.senado.gov.br/dadosabertos/docs/ui/index.html#/

    --------------------------------------------------------------------------
    '''

    def __init__(self, endpoint:str):
        self.URL = ENDPOINTS[endpoint]

    def get(self, keys) -> dict:
        '''
        Coleta os dados requisitados.

        Parâmetros
        ----------
        keys: list ou str
            Caminho de parâmetros para acessar a função desejada.
            Pode ser uma string de parâmetros unidos por barras '/'.
            Ou pode ser uma lista de strings na ordem correta.
            Os dois métodos produzem o mesmo resultado.

        Exemplos
        --------
        Acessando usando uma string
        >>> api.get(keys='/autor/lista/atual')

        Acessando usando uma lista de string
        >>> api.get(keys=['autor', 'lista', 'atual'])

        ----------------------------------------------------------------------      
        '''
        
        if isinstance(keys, str):
            path = keys
        if isinstance(keys, list):
            path = '/'.join(keys)

        return requests.get(
            url = self.URL + path,
            headers = {'Accept':'application/json'}
        ).json()