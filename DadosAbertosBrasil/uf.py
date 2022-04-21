"""Objeto UF contendo informações das Unidades da Federação.

Este módulo é um protótipo e poderá passar por várias modificações.

Serve como um consolidador por UF de diversar funções do pacote
DadosAbertosBrasil.

"""

from datetime import datetime
import json
from typing import List, Optional, Union

from pandas import DataFrame
import requests

from . import ibge
from . import favoritos
from .camara import lista_deputados
from .senado import lista_senadores
from ._utils.errors import DAB_UFError
from ._utils import parse



_UF_INFO = {
    'BR': {
        'nome': 'Brasil',
        'cod': 1,
        'area': 8510295.914,
        'capital': 'Brasília',
        'extinto': False,
        'gentilico': {'brasileiro', 'brasileira'},
        'lema': 'Ordem e Progresso',
        'regiao': None,
    },
    'AC': {
        'nome': 'Acre',
        'cod': 12,
        'area': 164122.2,
        'capital': 'Rio Branco',
        'extinto': False,
        'gentilico': {'acriano', 'acriana', 'acreano', 'acreana'},
        'lema': 'Nec Luceo Pluribus Impar',
        'regiao': 'Norte',
    },
    'AL': {
        'nome': 'Alagoas',
        'cod': 27,
        'area': 27767.7,
        'capital': 'Maceió',
        'extinto': False,
        'gentilico': {'alagoano', 'alagoana'},
        'lema': 'Ad Bonum Et Prosperitatem',
        'regiao': 'Nordeste',
    },
    'AM': {
        'nome': 'Amazonas',
        'cod': 13,
        'area': 1570745.7,
        'capital': 'Manaus',
        'extinto': False,
        'gentilico': {'amazonense'},
        'lema': None,
        'regiao': 'Norte',
    },
    'AP': {
        'nome': 'Amapá',
        'cod': 16,
        'area': 142814.6,
        'capital': 'Macapá',
        'extinto': False,
        'gentilico': {'amapaense'},
        'lema': 'Aqui começa o Brasil',
        'regiao': 'Norte',
    },
    'BA': {
        'nome': 'Bahia',
        'cod': 29,
        'area': 564692.7,
        'capital': 'Salvador',
        'extinto': False,
        'gentilico': {'baiano, baiana'},
        'lema': 'Per Ardua Surgo',
        'regiao': 'Nordeste',
    },
    'CE': {
        'nome': 'Ceará',
        'cod': 23,
        'area': 148825.6,
        'capital': 'Fortaleza',
        'extinto': False,
        'gentilico': {'cearense'},
        'lema': 'Terra da Luz',
        'regiao': 'Nordeste',
    },
    'DF': {
        'nome': 'Distrito Federal',
        'cod': 53,
        'area': 5822.1,
        'capital': 'Brasília',
        'extinto': False,
        'gentilico': {'brasiliense', 'candango'},
        'lema': 'Ventvris Ventis',
        'regiao': 'Centro-Oeste',
    },
    'ES': {
        'nome': 'Espirito Santo',
        'cod': 32,
        'area': 46077.5,
        'capital': 'Vitória',
        'extinto': False,
        'gentilico': {'capixaba', 'espírito-santense'},
        'lema': 'Trabalha e Confia',
        'regiao': 'Sudeste',
    },
    'FN': {
        'nome': 'Fernando de Noronha',
        'cod': 20,
        'area': 18.609,
        'capital': 'Fernando de Noronha',
        'extinto': True,
        'gentilico': {'noronhense'},
        'lema': None,
        'regiao': 'Nordeste',
    },
    'GB': {
        'nome': 'Guanabara',
        'cod': 34,
        'area': 1356,
        'capital': 'Rio de Janeiro',
        'extinto': True,
        'gentilico': None,
        'lema': None,
        'regiao': 'Sudeste',
    },
    'GO': {
        'nome': 'Goiás',
        'cod': 52,
        'area': 340086.7,
        'capital': 'Goiânia',
        'extinto': False,
        'gentilico': {'goiano', 'goiana'},
        'lema': 'Terra Querida, Fruto da Vida',
        'regiao': 'Centro-Oeste',
    },
    'MA': {
        'nome': 'Maranhão',
        'cod': 21,
        'area': 331983.3,
        'capital': 'São Luís',
        'extinto': False,
        'gentilico': {'maranhense'},
        'lema': None,
        'regiao': 'Nordeste',
    },
    'MG': {
        'nome': 'Minas Gerais',
        'cod': 31,
        'area': 586528.3,
        'capital': 'Belo Horizonte',
        'extinto': False,
        'gentilico': {'mineiro', 'mineira'},
        'lema': 'Libertas Quæ Sera Tamen',
        'regiao': 'Sudeste',
    },
    'MT': {
        'nome': 'Mato Grosso',
        'cod': 51,
        'area': 903357.9,
        'capital': 'Cuiabá',
        'extinto': False,
        'gentilico': {'mato-grossense'},
        'lema': 'Virtute Plusquam Auro',
        'regiao': 'Centro-Oeste',
    },
    'MS': {
        'nome': 'Mato Grosso do Sul',
        'cod': 50,
        'area': 357125.0,
        'capital': 'Campo Grande',
        'extinto': False,
        'gentilico': {'sul-mato-grossense', 'mato-grossense-do-sul'},
        'lema': None,
        'regiao': 'Centro-Oeste',
    },
    'PA': {
        'nome': 'Pará',
        'cod': 15,
        'area': 1247689.5,
        'capital': 'Belém',
        'extinto': False,
        'gentilico': {'paraense'},
        'lema': None,
        'regiao': 'Norte',
    },
    'PB': {
        'nome': 'Paraíba',
        'cod': 25,
        'area': 56439.8,
        'capital': 'João Pessoa',
        'extinto': False,
        'gentilico': {'paraibano', 'paraibana'},
        'lema': None,
        'regiao': 'Nordeste',
    },
    'PE': {
        'nome': 'Pernambuco',
        'cod': 26,
        'area': 98311.6,
        'capital': 'Recife',
        'extinto': False,
        'gentilico': {'pernambucano', 'pernambucana'},
        'lema': 'Ego Sum Qui Fortissimum Et Leads',
        'regiao': 'Nordeste',
    },
    'PI': {
        'nome': 'Piauí',
        'cod': 22,
        'area': 251529.2,
        'capital': 'Teresina',
        'extinto': False,
        'gentilico': {'piauiense'},
        'lema': 'Impavidum Ferient Ruinae',
        'regiao': 'Nordeste',
    },
    'PR': {
        'nome': 'Paraná',
        'cod': 41,
        'area': 199314.9,
        'capital': 'Curitiba',
        'extinto': False,
        'gentilico': {'paranaense'},
        'lema': None,
        'regiao': 'Sul',
    },
    'RJ': {
        'nome': 'Rio de Janeiro',
        'cod': 33,
        'area': 43696.1,
        'capital': 'Rio de Janeiro',
        'extinto': False,
        'gentilico': {'fluminense'},
        'lema': 'Recete Rem Pvblicam Gerere',
        'regiao': 'Sudeste',
    },
    'RO': {
        'nome': 'Rondônia',
        'cod': 11,
        'area': 237576.2,
        'capital': 'Porto Velho',
        'extinto': False,
        'gentilico': {'rondoniense', 'rondoniano', 'rondoniana'},
        'lema': None,
        'regiao': 'Norte',
    },
    'RN': {
        'nome': 'Rio Grande do Norte',
        'cod': 24,
        'area': 52796.8,
        'capital': 'Natal',
        'extinto': False,
        'gentilico': {'potiguar', 'norte-rio-grandense', 'rio-grandense-do-norte'},
        'lema': None,
        'regiao': 'Nordeste',
    },
    'RR': {
        'nome': 'Roraima',
        'cod': 14,
        'area': 224299.0,
        'capital': 'Boa Vista',
        'extinto': False,
        'gentilico': {'roraimense'},
        'lema': 'Amazônia: Patrimônio dos Brasileiros',
        'regiao': 'Norte',
    },
    'RS': {
        'nome': 'Rio Grande do Sul',
        'cod': 43,
        'area': 281748.5,
        'capital': 'Porto Alegre',
        'extinto': False,
        'gentilico': {'gaúcho', 'gaúcha', 'sul-rio-grandense', 'rio-grandense-do-sul'},
        'lema': 'Liberdade, Igualdade, Humanidade',
        'regiao': 'Sul',
    },
    'SC': {
        'nome': 'Santa Catarina',
        'cod': 42,
        'area': 95346.2,
        'capital': 'Florianópolis',
        'extinto': False,
        'gentilico': {'catarinense', 'barriga-verde'},
        'lema': None,
        'regiao': 'Sul',
    },
    'SE': {
        'nome': 'Sergipe',
        'cod': 28,
        'area': 21910.3,
        'capital': 'Aracaju',
        'extinto': False,
        'gentilico': {'sergipano', 'sergipana', 'sergipense', 'serigy', 'aperipê'},
        'lema': 'Sub Lege Libertas',
        'regiao': 'Nordeste',
    },
    'SP': {
        'nome': 'São Paulo',
        'cod': 35,
        'area': 248209.4,
        'capital': 'São Paulo',
        'extinto': False,
        'gentilico': {'paulista'},
        'lema': 'Pro Brasilia Fiant Eximia',
        'regiao': 'Sudeste',
    },
    'TO': {
        'nome': 'Tocantins',
        'cod': 17,
        'area': 277620.9,
        'capital': 'Palmas',
        'extinto': False,
        'gentilico': {'tocantinense'},
        'lema': 'Co Yvy Ore Retama',
        'regiao': 'Norte',
    }
}



class _Governador:
    """Informações básicas do governador da UF.

    Attributes
    ----------
    uf : str
    nome : str
    nome_completo : str
    ano_eleicao : int
    mandato_inicio : datetime.date
    mandato_fim : datetime.date
    partido : str
    partido_sigla : str
    cargo_anterior : str
    vice_governador : str
    
    """

    def __init__(self, uf_nome:str, uf_sigla:str):

        # Baixar dados
        self._uf = uf_sigla
        URL = r'https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/data/governadores.json'
        r = requests.get(URL)
        data = json.loads(r.json())[uf_nome]

        # Criar atributos
        for key in data:
            setattr(self, key, data[key])
        self.mandato_inicio = datetime.strptime(self.mandato_inicio, '%Y-%m-%d').date()
        self.mandato_fim = datetime.strptime(self.mandato_fim, '%Y-%m-%d').date()

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f'<DadosAbertosBrasil.uf._Governador: {self.nome} ({self._uf})>'



class UF:
    """Consolidado de informações de uma Unidade Federativa.

    Parameters
    ----------
    uf : str
        Nome, sigla ou código da UF desejada.

    Attributes
    ----------
    sigla : str
        Sigla de duas letras maiúsculas.
    cod : int
        Código IBGE.
    nome : str
        Nome completo.
    area : float
        Área terrotorial em quilómetros quadrados.
    capital : str
        Cidade sede do governo estadual.
    extinto : bool
        True, caso UF tenha sido extinta (Fernando de Noronha ou Guanabara).
    gentilico : set
        Conjunto de gentílicos e variações.
    lema : str
        Lema da UF.
    regiao : str
        Grande região (Norte, Nordeste, Sudeste, Sul ou Centro-Oeste).

    Properties
    ----------
    densidade : float
        Densidade populacional (hab/km²) da UF.
    galeria : DadosAbertosBrasil.ibge.Galeria
        Gera uma galeria de fotos da UF.
    geojson : dict
        Coordenadas dos municípios brasileiros em formato GeoJSON.
    governador : DadosAbertosBrasil.uf._Governador
        Informações básico do governador da UF.
    historia : DadosAbertosBrasil.ibge.Historia
        Objeto contendo a história da UF.
    municipios : list[str]
        Lista de municípios.
    populacao : int
        População projetada pelo IBGE.

    Methods
    -------
    bandeira(tamanho=100)
        Gera a URL da WikiMedia para a bandeira do estado.
    brasao(tamanho=100)
        Gera a URL da WikiMedia para o brasão do estado.
    deputados(nome, legislatura, partido, sexo, inicio, fim, pagina, itens...)
        Lista dos deputados federais em exercício.
    malha(nivel, divisoes, periodo, formato, qualidade)
        Obtém a URL para a malha referente à UF.
    senadores(tipo, sexo, partido, contendo, excluindo, url, index, formato)
        Lista de senadores da república desta UF.

    """

    def __init__(self, uf:str):
        self.sigla = parse.uf(uf=uf, extintos=True)
        for attr in _UF_INFO[self.sigla]:
            setattr(self, attr, _UF_INFO[self.sigla][attr])


    def __repr__(self) -> str:
        return f'<DadosAbertosBrasil.UF: {self.nome}>'


    def __str__(self) -> str:
        return self.nome


    def bandeira(self, tamanho:int=100) -> str:
        """Gera a URL da WikiMedia para a bandeira do estado.

        Parameters
        ----------
        tamanho : int, default=100
            Tamanho em pixels da bandeira.

        Returns
        -------
        str
            URL da bandeira do estado no formato PNG.

        See Also
        --------
        DadosAbertosBrasil.favoritos.bandeira
            Função original.

        Examples
        --------
        Gera o link para a imagem da bandeira de Santa Catarina de 200 pixels.

        >>> sc = UF('sc')
        >>> sc.bandeira(tamanho=200)
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/' ...

        """

        return favoritos.bandeira(uf=self.sigla, tamanho=tamanho)


    def brasao(self, tamanho:int=100) -> str:
        """Gera a URL da WikiMedia para o brasão do estado.

        Parameters
        ----------
        tamanho : int, default=100
            Tamanho em pixels da bandeira.

        Returns
        -------
        str
            URL da bandeira do estado no formato PNG.

        See Also
        --------
        DadosAbertosBrasil.favoritos.brasao
            Função original.

        Examples
        --------
        Gera o link para a imagem do brasão de Santa Catarina de 200 pixels.

        >>> sc = UF('SC')
        >>> sc.brasao(tamanho=200)
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/' ...

        """
        return favoritos.brasao(uf=self.sigla, tamanho=tamanho)


    @property
    def densidade(self) -> float:
        """Densidade populacional (hab/km²) da UF.

        É a razão entre a população projetada pelo IBGE (habitantes) e a área
        territorial da UF (quilómetros quadrados).

        Returns
        -------
        float
            Densidade populacional.

        Raises
        ------
        DAB_UFError
            Caso seja uma UF extinta.

        See Also
        --------
        DadosAbertosBrasil.ibge.populacao
            Função utilizada para projetar a população da UF.

        Examples
        --------
        >>> am = UF('AM')
        >>> am.populacao()
        2.719286132694809
        
        """

        if self.extinto:
            raise DAB_UFError('Método `densidade` indisponível para UFs extintas.')
        pop = ibge.populacao(projecao='populacao', localidade=self.cod)
        return pop / self.area


    def deputados(
            self,
            nome: Optional[str] = None,
            legislatura: Optional[int] = None,
            partido: Optional[str] = None,
            sexo: Optional[str] = None,
            inicio: Union[datetime, str, None] = None,
            fim: Union[datetime, str, None] = None,
            pagina: int = 1,
            itens: Optional[int] = None,
            asc: bool = True,
            ordenar_por: str = 'nome',
            url: bool = True,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> DataFrame:
        """Lista dos deputados federais da UF em exercício.

        Retorna uma lista de dados básicos sobre deputados que estiveram em
        exercício parlamentar em algum intervalo de tempo. Se não for passado um
        parâmetro de tempo, como `legislatura` ou `inicio`, a lista enumerará
        somente os deputados em exercício no momento da requisição.

        Parameters
        ----------
        nome : str, optional
            Parte do nome dos parlamentares.
        legislatura : int, optional
            Número da legislatura a qual os dados buscados devem corresponder.
        partido : str, optional
            Sigla do partido ao qual sejam filiados os deputados.
            Para obter as siglas válidas, consulte a função `camara.lista_partidos`.
            Atenção: partidos diferentes podem usar a mesma sigla em diferentes
            legislaturas.
        sexo : {'M', 'F'}, optional
            Letra que designe o gênero dos parlamentares que se deseja buscar,
            - 'M': Masculino;
            - 'F': Feminino.
        inicio : str, optional
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim : str, optional
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        pagina : int, default=1
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido
            pelo parâmetro `itens`. Se omitido, assume o valor 1.
        itens : int, optional
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        asc : bool, default=True
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por : str, default='nome'
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        index : bool, default=False
            Se True, define a coluna `id` como index do DataFrame.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Obs.: Alguns filtros não serão aplicados no formato 'json'.

        Returns
        -------
        pandas.core.frame.DataFrame
            Tabela com informações básicas dos deputados federais.

        Raises
        ------
        DAB_UFError
            Caso seja uma UF extinta.

        See Also
        --------
        DadosAbertosBrasil.camara.lista_deputados
            Função original.

        Examples
        --------
        >>> rj = UF('RJ')
        >>> rj.deputados()
        
        """

        if self.extinto:
            raise DAB_UFError('Método `deputados` indisponível para UFs extintas.')
        return lista_deputados(
            nome = nome,
            legislatura = legislatura,
            uf = self.sigla,
            partido = partido,
            sexo = sexo,
            inicio = inicio,
            fim = fim,
            pagina = pagina,
            itens = itens,
            asc = asc,
            ordenar_por = ordenar_por,
            url = url,
            index = index,
            formato = formato
        )


    @property
    def galeria(self) -> ibge.Galeria:
        """Gera uma galeria de fotos da UF.

        Returns
        -------
        DadosAbertosBrasil._ibge.cidades.Galeria
            Objeto `Galeria` contendo uma lista de Fotografias.

        See Also
        --------
        DadosAbertosBrasil.ibge.Galeria
            Classe original.

        Examples
        --------
        Capturar a primeira fotografia da galeria do Espírito Santo.

        >>> es = dab.UF('ES')
        >>> galeria = es.galeria()
        >>> foto = galeria.fotografias[0]
        
        Gerar uma URL da fotografia com altura máxima de 500 pixels.

        >>> foto.url(altura=500)
        'https://servicodados.ibge.gov.br/api/v1/resize/image?maxwidth=600...'

        """

        if self.extinto:
            raise DAB_UFError('Método `galeria` indisponível para UFs extintas.')
        return ibge.Galeria(self.cod)


    @property
    def geojson(self) -> dict:
        """Coordenadas dos municípios brasileiros em formato GeoJSON.

        Returns
        -------
        dict
            Coordenadas em formato GeoJSON.

        Raises
        ------
        DAB_UFError
            Caso seja uma UF extinta.

        References
        ----------
        .. [1] https://github.com/tbrugz

        See Also
        --------
        DadosAbertosBrasil.favoritos.geojson
            Função original.

        Examples
        --------
        >>> sc = UF('SC')
        >>> sc.geojson()
        {
            'type': 'FeatureCollection',
            'features': [{
                'type': 'Feature',
                'properties': {
                    'id': '4200051',
                    'name': 'Abdon Batista',
                    'description': 'Abdon Batista'
                },
                'geometry': {
                    'type': 'Polygon',
                    'coordinates': [[
                        [-51.0378352721, -27.5044338231],
                        [-51.0307859254, -27.5196681175],
                        [-51.0175689993, -27.5309862449],
                        [-50.9902859975, -27.5334223314],
                        [-50.9858971419, -27.5302011257],
                        ...

        """

        if self.extinto:
            raise DAB_UFError('Método `geojson` indisponível para UFs extintas.')
        return favoritos.geojson(self.sigla)


    @property
    def governador(self) -> _Governador:
        """Informações básicas do governador da UF.

        Attributes
        ----------
        uf : str
        nome : str
        nome_completo : str
        ano_eleicao : int
        mandato_inicio : datetime.date
        mandato_fim : datetime.date
        partido : str
        partido_sigla : str
        cargo_anterior : str
        vice_governador : str
        
        Raises
        ------
        DAB_UFError
            Caso seja uma UF extinta.

        """

        if self.cod == 1:
            raise DAB_UFError("Propriedade `governador` indisponível para 'Brasil'.")
        if self.extinto:
            raise DAB_UFError('Propriedade `governador` indisponível para UFs extintas.')

        return _Governador(self.nome, self.sigla)


    @property
    def historia(self) -> ibge.Historia:
        """Objeto contendo a história da UF.

        Returns
        -------
        DadosAbertosBrasil._ibge.cidades.Historia
            Objeto `Historia` da API IBGE Cidades.

        See Also
        --------
        DadosAbertosBrasil.ibge.Historia
            Classe original.

        Examples
        --------
        Capturar o texto da história de Minas Gerais.

        >>> mg = dab.UF('MG')
        >>> hist = mg.historia()
        >>> hist.historico
        "O Município de Wenceslau Braz tem sua origem praticamente desconh..."

        """

        if self.sigla == 'GB':
            raise DAB_UFError('Método `historia` indisponível para a UF Guanabara.')
        elif self.sigla == 'FN':
            return ibge.Historia(localidade=260545)
        else:
            return ibge.Historia(localidade=self.cod)


    def malha(
            self,
            nivel: str = 'estados',
            divisoes: Optional[str] = None,
            periodo: int = 2020,
            formato: str = 'svg',
            qualidade: str = 'minima'
        ) -> Union[str, dict]:
        """Obtém a malha referente à UF.

        Parameters
        ----------
        nivel : str, default='estados'
            Nível geográfico dos dados.
        divisoes : str, optional
            Subdiviões intrarregionais do nível.
            Se None, apresenta a malha sem subdivisões.
        periodo : int, default=2020
            Ano da revisão da malha.
        formato : {'svg', 'json', 'geojson'}, default='svg'
            Formato dos dados da malha.
        qualidade : {'minima', 'intermediaria', 'maxima'}, default='minima'
            Qualidade de imagem da malha.

        Returns
        -------
        str
            Se formato='svg', retorna a URL da malha da localidade desejada.
        dict
            Se formato='json', retorna a malha em formato TopoJSON.
        dict
            Se formato='geojson', retorna a malha em formato GeoJSON.

        Raises
        ------
        DAB_LocalidadeError
            Caso o nível geográfico seja inválido.

        References
        ----------
        .. [1] https://servicodados.ibge.gov.br/api/docs/malhas?versao=3

        See also
        --------
        DadosAbertosBrasil.ibge.malha
            Função original

        Examples
        --------
        Captura a malha do Distrito Federal (localidade=53) em formato GeoJSON.

        >>> df = dab.UF('DF')
        >>> df.malha(formato='geojson')
        {'type': 'FeatureCollection',
            'features': [{'type': 'Feature',
                'geometry': {'type': 'Polygon',
                    'coordinates': [[[-47.31, -16.0363], ...

        Captura a malha de Alagoas em formato SVG com qualidade mínima com
        subdivisões municipais.

        >>> al = dab.UF('alagoas')
        >>> al.malha(
        ...     nivel = 'municipios',
        ...     formato = 'svg',
        ...     qualidade = 'minima'
        ... )
        'https://servicodados.ibge.gov.br/api/v3/malhas/...'

        """

        if self.extinto:
            raise DAB_UFError('Método `malha` indisponível para UFs extintas.')
        return ibge.malha(
            localidade = self.cod,
            nivel = nivel,
            divisoes = divisoes,
            periodo = periodo,
            formato = formato,
            qualidade = qualidade
        )


    @property
    def municipios(self) -> List[str]:
        """Lista de municípios.

        Returns
        -------
        list of str
            Lista de municípios.

        Raises
        ------
        DAB_UFError
            Caso seja uma UF extinta.

        Examples
        --------
        >>> ac = UF('AC')
        >>> ac.municipios()
        ['Acrelândia', 'Assis Brasil', 'Brasiléia', 'Bujari', ...]
        
        """

        if self.extinto:
            raise DAB_UFError('Método `municipios` indisponível para UFs extintas.')
        js = favoritos.geojson(self.sigla)
        return [mun['properties']['name'] for mun in js['features']]


    @property
    def populacao(self) -> int:
        """População projetada pelo IBGE.

        Returns
        -------
        int
            População projetada.

        Raises
        ------
        DAB_UFError
            Caso seja uma UF extinta.

        See Also
        --------
        DadosAbertosBrasil.ibge.populacao
            Função original.

        Examples
        --------
        >>> df = UF('DF')
        >>> df.populacao()
        3092244
        
        """

        if self.extinto:
            raise DAB_UFError('Método `populacao` indisponível para UFs extintas.')
        return ibge.populacao(projecao='populacao', localidade=self.cod)


    def senadores(
            self,
            tipo: str = 'atual',
            sexo: Optional[str] = None,
            partido: Optional[str] = None,
            contendo: Optional[str] = None,
            excluindo: Optional[str] = None,
            url: bool = True,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[DataFrame, dict]:
        """Lista de senadores da república desta UF.

        Parameters
        ----------
        tipo : {'atual', 'titulares', 'suplentes', 'afastados'}, default='atual'
            - 'atual': Todos os senadores em exercício;
            - 'titulares': Apenas senadores que iniciaram o mandato como titulares;
            - 'suplentes': Apenas senadores que iniciaram o mandato como suplentes;
            - 'afastados': Todos os senadores afastados.
        sexo : str, optional
            Filtro de sexo dos senadores.
        partido : str, optional
            Filtro de partido dos senadores.
        contendo : str, optional
            Captura apenas senadores contendo esse texto no nome.
        excluindo : str, optional
            Exclui da consulta senadores contendo esse texto no nome.
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        index : bool, default=False
            Se True, define a coluna `codigo` como index do DataFrame.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Obs.: Alguns filtros não serão aplicados no formato 'json'.

        Returns
        -------
        pandas.core.frame.DataFrame
            Tabela com informações básicas dos senadores consultados.
        dict
            Dados brutos em formato json.

        See Also
        --------
        DadosAbertosBrasil.senado.lista_senadores
            Função original.
        
        Examples
        --------
        Lista senadores do partido PL do Rio de Janeiro.

        >>> rj = UF('rj')
        >>> rj.senadores(partido='PL')
        codigo nome_parlamentar              nome_completo       sexo \
        0   5936  Carlos Portinho  Carlos Francisco Portinho  Masculino
        1   5322          Romário     Romario de Souza Faria  Masculino
        
        """
    
        if self.extinto:
            raise DAB_UFError('Método `senadores` indisponível para UFs extintas.')

        return lista_senadores(
            uf = self.sigla,
            tipo = tipo,
            sexo = sexo,
            partido = partido,
            contendo = contendo,
            excluindo = excluindo,
            url = url,
            index = index,
            formato = formato
        )
