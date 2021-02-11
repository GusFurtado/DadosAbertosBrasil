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
    - Desenvolvimento do módulo `_errors` como suporte aos módulos principais;
    - Converter strings em formato de data em objetos `datetime`;
    - Adicionar novos exemplos à documentação;
    - Adição constante de novas funções no módulo `favoritos`.
'''



__version__ = '0.2.0'
__author__ = 'Gustavo Furtado da Silva'



from typing import Union

import requests



ENDPOINTS = {
    'camara': 'https://dadosabertos.camara.leg.br/api/v2/',
    'ipea': 'http://www.ipeadata.gov.br/api/odata4/',
    'senado': 'http://legis.senado.gov.br/dadosabertos/',
    'sidra': 'https://servicodados.ibge.gov.br/api/v3/agregados/'
}



class API:
    '''
    Classe para coleta direta dos dados brutos das API REST.

    Parâmetros
    ----------
    endpoint: str
        Qual API deseja se conectar:
        - 'camara': Acessar API da Câmara dos Deputados;
        - 'ipea': Acessar API do IPEA Data;
        - 'senado': Acessar API do Senado Federal;
        - 'sidra': Acessar API do SIDRA - IBGE.

    Exemplos
    --------
    >>> from DadosAbertosBrasil import API
    >>> api = API(endpoint='camara')
    >>> api.get(path=['referencias', 'proposicoes', 'codTipoAutor'])

    >>> api = API(endpoint='senado')
    >>> api.get(path='/autor/lista/atual')

    Documentação original
    ---------------------
    'camara'
        https://dadosabertos.camara.leg.br/swagger/api.html
    'ipea'
        http://www.ipeadata.gov.br/api/
    'senado'
        http://legis.senado.gov.br/dadosabertos/docs/ui/index.html#/
    'sidra'
        http://api.sidra.ibge.gov.br/

    --------------------------------------------------------------------------
    '''

    def __init__(self, endpoint:str):
        self.URL = ENDPOINTS[endpoint]

    def get(
            self,
            path: Union[str, list],
            params: dict = None
        ) -> dict:
        '''
        Coleta os dados requisitados.

        Parâmetros
        ----------
        path: list ou str
            Caminho de parâmetros para acessar a função desejada.
            Pode ser uma string de parâmetros unidos por barras '/'.
            Ou pode ser uma lista de strings na ordem correta.
            Os dois métodos produzem o mesmo resultado.
        params: dict (default=None)
            Dicionário de parâmetros de busca que serão enviados
            para o request.

        Retorna
        -------
        dict
            Dados brutos coletados da API.

        Exemplos
        --------
        Acessando usando uma string
        >>> api.get(path='/autor/lista/atual')

        Acessando usando uma lista de string
        >>> api.get(path=['autor', 'lista', 'atual'])

        ----------------------------------------------------------------------      
        '''
        
        if isinstance(path, list):
            path = '/'.join(path)

        return requests.get(
            url = self.URL + path,
            headers = {'Accept':'application/json'},
            params = params
        ).json()