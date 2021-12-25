"""Submódulo IBGE contendo os wrappers das APIs do IBGE Cidades.

Este submódulo é importado automaticamente com o módulo `ibge`.

>>> from DadosAbertosBrasil import ibge

References
----------
.. [1] https://cidades.ibge.gov.br/

"""

from typing import Iterator, Optional, Union

from DadosAbertosBrasil._utils import parse
from DadosAbertosBrasil._utils.get_data import get_data



class _Fotografia:
    """Metadados de uma fotografia da bblioteca do IBGE.

    Attributes
    ----------
    ano : str
        Ano que a fotografia foi tirada.
    autor : str
        Autor(a) da fotografia.
    codigo_municipal : str
        Código IBGE da localidade.
    id : str
        Código da fotografia.
    link : str
        Nome do arquivo na biblioteca do IBGE.
    titulo : str
        Título da fotografia.

    Methods
    -------
    __call__(altura:int=None, largura:int=None) -> str
        Gera a URL da fotografia.

    Examples
    --------
    Instanciar a galeria de fotos de Fortaleza.

    >>> fortaleza = ibge.Galeria(2304400)

    Visualizar lista de fotografias dentro da galeria.

    >>> fortaleza.fotografias

    Selecionar primeira fotografia da galeria.

    >>> foto = fortaleza[0]
    
    Gerar uma URL da fotografia com altura máxima de 500 pixels.

    >>> foto(altura=500)
    'https://servicodados.ibge.gov.br/api/v1/resize/image?maxwidth=600&max...'

    References
    ----------
    .. [1] https://cidades.ibge.gov.br/

    """

    def __init__(self, dados):
        for k in dados:
            self.__setattr__(k.lower(), dados[k])


    def __repr__(self) -> str:
        return f'<DadosAbertosBrasil.ibge: Fotografia {self.id}>'


    def __str__(self) -> str:
        return f'Fotografia {self.id}'

    
    def __call__(
            self,
            altura: Optional[int] = None,
            largura: Optional[int] = None
        ) -> str:
        """Gera a URL da foto.

        Parameters
        ----------
        altura : int, optional
            Altura máxima da fotografia em pixels.
        largura : int, optional
            Largura máxima da fotografia em pixels.
        
        Returns
        -------
        str
            URL da fotografia.

        """
        
        if altura is None and largura is None:
            altura, largura = 600, 600
        elif altura is None:
            altura = largura
        elif largura is None:
            largura = altura
        return f'https://servicodados.ibge.gov.br/api/v1/resize/image?maxwidth={largura}&maxheight={altura}&caminho=biblioteca.ibge.gov.br/visualizacao/fotografias/GEBIS%20-%20RJ/{self.link}'



class Galeria:
    """Gera uma galeria de fotos da localidade desejada.
    
    Parameters
    ----------
    localidade : int
        Código IBGE da localidade.
        O código pode ser obtido com auxílio da função `ibge.localidades`.

    Attributes
    ----------
    fotografias : list of ibge._Fotografia
        Lista de fotografias da localidade.
    localidade : int
        Código IBGE da localidade.
    
    Examples
    --------
    Instanciar a galeria de fotos de Fortaleza.

    >>> fortaleza = ibge.Galeria(2304400)

    Visualizar lista de fotografias dentro da galeria.

    >>> fortaleza.fotografias

    Selecionar primeira fotografia da galeria.

    >>> foto = fortaleza[0]
    
    Gerar uma URL da fotografia com altura máxima de 500 pixels.

    >>> foto(altura=500)
    'https://servicodados.ibge.gov.br/api/v1/resize/image?maxwidth=600&max...'

    References
    ----------
    .. [1] https://cidades.ibge.gov.br/

    """

    def __init__(self, localidade:Union[str,int]):
        self.localidade = parse.localidade(localidade)
        galeria = self._get_photos()
        self.fotografias = [_Fotografia(galeria[foto]) for foto in galeria]


    def __iter__(self) -> Iterator:
        return iter(self.fotografias)


    def __len__(self) -> int:
        return len(self.fotografias)


    def __getitem__(self, slice):
        return self.fotografias[slice]


    def __repr__(self) -> str:
        return f'<DadosAbertosBrasil.ibge: Galeria de fotos da localidade {self.localidade}>'


    def __reversed__(self) -> list:
        return reversed(self.fotografias)


    def __str__(self) -> str:
        return f'Galeria {self.localidade}'


    def _get_photos(self) -> dict:
        return get_data(
            endpoint = 'https://servicodados.ibge.gov.br/api/v1/',
            path = 'biblioteca',
            params = {
                'codmun': self.localidade,
                'aspas': '3',
                'fotografias': '1',
                'serie': 'Acervo dos Trabalhos Geográficos de Campo|Acervo dos Municípios brasileiros'
            }
        )



class Historia:
    """Histórico de uma localidade.

    Parameters
    ----------
    localidade : int or str
        Código da localidade.
        Este código pode ser obtido com auxílio da função `ìbge.localidades`.

    Attributes
    ----------
    ano : int
        Ano da publicação do histórico.
    estado : str
        Nome do estado no formato 'Estado - UF'.
    estado1 : str
        Nome do estado sem a sigla.
    formacao_administrativa : str
        Descrição da formação administrativa da localidade.
    gentilico : str
        Gentílico dos naturais desta localidade.
    historico : str
        Texto descrevendo a história da localidade.
    historico_fonte : str
        Fonte do texto do atributo `historico`.
    localidade : int
        Código da localidade.
    municipio : str
        Nome do município.

    Raises
    ------
    DAB_LocalidadeError
        Caso o código da localidade seja inválido.

    Examples
    --------
    Capturar o histórico de Belo Horizonte e a fonte do texto.

    >>> bh = ibge.Historia(localidade=310620)
    >>> bh.historico
    'Foi à procura de ouro que, no distante 1701, o bandeirante João Leite...'

    >>> bh.historico_fonte
    'Belo Horizonte (MG). Prefeitura. 2014. Disponível em: ...'

    Capturar o histórico do estado de Minas Gerais
    >>> mg = ibge.Historia(52)

    References
    ----------
    .. [1] https://cidades.ibge.gov.br/

    """

    def __init__(self, localidade:Union[int,str]):
        self.localidade = parse.localidade(localidade)
        d = self._get_historia()
        self._set_attribs(d)


    def __repr__(self) -> str:
        return f'<DadosAbertosBrasil.ibge: História da localidade {self.localidade}>'


    def __str__(self) -> str:
        return f'História ({self.localidade})'


    def _get_historia(self) -> dict:
        return get_data(
            endpoint = 'https://servicodados.ibge.gov.br/api/v1/',
            path = 'biblioteca',
            params = {
                'aspas': '3',
                'codmun': self.localidade
            })


    def _set_attribs(self, d:dict) -> None:
        for attribs in d:
            for k in d[attribs]:
                self.__setattr__(k.lower(), d[attribs][k])
