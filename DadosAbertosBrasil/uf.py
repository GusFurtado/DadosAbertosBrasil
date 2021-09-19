'''Objeto UF contendo informações das Unidades da Federação.

Este módulo é um protótipo e poderá passar por várias modificações.

Serve como um consolidador por UF de diversar funções do pacote
DadosAbertosBrasil.

'''
from ._utils.errors import DAB_UFError
from ._utils import parse
from ._ibge.misc import populacao, malha
from ._ibge.cidades import Historia, Galeria
from . import favoritos
from .camara import lista_deputados
from .senado import lista_atual



UF_INFO = {
    'BR': {
        'nome': 'Brasil',
        'cod': 1,
        'area': 8510295.914,
        'capital': 'Brasília',
        'extinto': False,
        'gentilico': {'brasileiro', 'brasileira'},
        'lema': 'Ordem e Progresso',
        'regiao': None,
        'governador': 'Jair Bolsonaro',
        'vice-governador': 'Hamilton Mourão' 
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
        'governador': 'Gladson Cameli',
        'vice-governador': 'Major Rocha' 
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
        'governador': 'Renan Filho',
        'vice-governador': None 
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
        'governador': 'Wilson Lima',
        'vice-governador': 'Carlos Almeida'
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
        'governador': 'Waldez Góes',
        'vice-governador': 'Jaime Nunes' 
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
        'governador': 'Rui Costa',
        'vice-governador': 'João Leão' 
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
        'governador': 'Camilo Santana',
        'vice-governador': 'Izolda Cela' 
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
        'governador': 'Ibaneis Rocha',
        'vice-governador': 'Paco Britto'
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
        'governador': 'Renato Casagrande',
        'vice-governador': 'Jacqueline Moraes'
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
        'governador': None,
        'vice-governador': None
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
        'governador': None,
        'vice-governador': None
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
        'governador': 'Ronaldo Caiado',
        'vice-governador': 'Lincoln Tejota'
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
        'governador': 'Flávio Dino',
        'vice-governador': 'Carlos Brandão'
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
        'governador': 'Romeu Zema',
        'vice-governador': 'Paulo Brant'
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
        'governador': 'Mauro Mendes',
        'vice-governador': 'Otaviano Pivetta'
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
        'governador': 'Azambuja',
        'vice-governador': 'Murilo Zauith'
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
        'governador': 'Helder Barbalho',
        'vice-governador': None
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
        'governador': 'João Azevêdo',
        'vice-governador': 'Lígia Feliciano'
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
        'governador': 'Paulo Câmara',
        'vice-governador': 'Luciana Santos'	 
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
        'governador': 'Wellington Dias',
        'vice-governador': 'Regina Sousa' 
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
        'governador': 'Ratinho Júnior',
        'vice-governador': 'Darci Piana'
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
        'governador': 'Cláudio Castro',
        'vice-governador': None
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
        'governador': 'Marcos Rocha',
        'vice-governador': 'Zé Jodan'	
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
        'governador': 'Fátima Bezerra',
        'vice-governador': 'Antenor Roberto'
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
        'governador': 'Antonio Denarium',
        'vice-governador': 'Frutuoso Lins'	
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
        'governador': 'Eduardo Leite',
        'vice-governador': 'Ranolfo Vieira Júnior'
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
        'governador': 'Carlos Moisés',
        'vice-governador': 'Daniela Reinehr'	
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
        'governador': 'Belivaldo Chagas',
        'vice-governador': 'Eliane Aquino'
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
        'governador': 'João Doria',
        'vice-governador': 'Rodrigo Garcia'
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
        'governador': 'Mauro Carlesse',
        'vice-governador': 'Wanderlei Barbosa'
    }
}



class UF:
    '''Consolidado de informações de uma Unidade Federativa.

    Este objeto ainda é um protótipo e poderá passar por várias modificações.

    Parâmetros
    ----------
    uf : str
        Nome, sigla ou código da UF desejada.

    Atributos
    ---------
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
    governador : str
        Nome do atual governador(a).
    vice-governador : str
        Nome do atual vice-governador(a).
    
    '''

    def __init__(self, uf:str):
        self.sigla = parse.uf(uf=uf, extintos=True)
        self.cod = UF_INFO[self.sigla]['cod']
        self.nome = UF_INFO[self.sigla]['nome']
        self.area = UF_INFO[self.sigla]['area']
        self.capital = UF_INFO[self.sigla]['capital']
        self.extinto = UF_INFO[self.sigla]['extinto']
        self.gentilico = UF_INFO[self.sigla]['gentilico']
        self.lema = UF_INFO[self.sigla]['lema']
        self.regiao = UF_INFO[self.sigla]['regiao']
        self.governador = UF_INFO[self.sigla]['governador']
        self.vice_governador = UF_INFO[self.sigla]['vice-governador']


    def __repr__(self):
        return f'<DadosAbertosBrasil.UF: {self.nome}>'


    def bandeira(self, tamanho:int=100):
        '''Gera a URL da WikiMedia para a bandeira do estado de um tamanho
        escolhido.

        Parâmetros
        ----------
        tamanho : int (default=100)
            Tamanho em pixels da bandeira.

        Retorna
        -------
        str
            URL da bandeira do estado no formato PNG.

        Ver Também
        ----------
        DadosAbertosBrasil.favoritos.bandeira
            Função original.

        Exemplos
        --------
        Gera o link para a imagem da bandeira de Santa Catarina de 200 pixels.

        >>> sc = UF('sc')
        >>> sc.bandeira(tamanho=200)
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/' ...

        '''

        return favoritos.bandeira(uf=self.sigla, tamanho=tamanho)


    def brasao(self, tamanho:int=100):
        '''Gera a URL da WikiMedia para o brasão do estado de um tamanho
        escolhido.

        Parâmetros
        ----------
        tamanho : int (default=100)
            Tamanho em pixels da bandeira.

        Retorna
        -------
        str
            URL da bandeira do estado no formato PNG.

        Ver Também
        ----------
        DadosAbertosBrasil.favoritos.brasao
            Função original.

        Exemplos
        --------
        Gera o link para a imagem do brasão de Santa Catarina de 200 pixels.

        >>> sc = UF('SC')
        >>> sc.brasao(tamanho=200)
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/' ...

        '''
        return favoritos.brasao(uf=self.sigla, tamanho=tamanho)


    def densidade(self):
        '''Densidade populacional (hab/km²) da UF.

        É a razão entre a população projetada pelo IBGE (habitantes) e a área
        territorial da UF (quilómetros quadrados).

        Retorna
        -------
        float
            Densidade populacional.

        Erros
        -----
        DAB_UFError
            Caso seja uma UF extinta.

        Ver Também
        ----------
        DadosAbertosBrasil.ibge.populacao
            Função utilizada para projetar a população da UF.

        Exemplos
        --------
        >>> am = UF('AM')
        >>> am.populacao()
        2.719286132694809
        
        '''

        if self.extinto:
            raise DAB_UFError('Método `densidade` indisponível para UFs extintas.')
        pop = populacao(projecao='populacao', localidade=self.cod)
        return pop / self.area


    def deputados(self):
        '''Lista dos deputados federais em exercício.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Tabela com informações básicas dos deputados federais.

        Erros
        -----
        DAB_UFError
            Caso seja uma UF extinta.

        Ver Também
        ----------
        DadosAbertosBrasil.camara.lista_deputados
            Função original.

        Exemplos
        --------
        >>> rj = UF('RJ')
        >>> rj.deputados()
        
        '''

        if self.extinto:
            raise DAB_UFError('Método `deputados` indisponível para UFs extintas.')
        return lista_deputados(uf=self.sigla)


    def galeria(self):
        '''Gera uma galeria de fotos da UF.

        Atributos
        ---------
        fotografias : lista de ibge._Fotografia
            Lista de fotografias da localidade.
        localidade : int
            Código IBGE da localidade.

        Ver também
        ----------
        DadosAbertosBrasil.ibge.Galeria
            Classe original.

        Exemplo
        -------
        Capturar a primeira fotografia da galeria do Espírito Santo.

        >>> es = dab.UF('ES')
        >>> galeria = es.galeria()
        >>> foto = galeria.fotografias[0]
        
        Gerar uma URL da fotografia com altura máxima de 500 pixels.

        >>> foto.url(altura=500)
        'https://servicodados.ibge.gov.br/api/v1/resize/image?maxwidth=600...'

        '''

        if self.extinto:
            raise DAB_UFError('Método `galeria` indisponível para UFs extintas.')
        return Galeria(self.cod)


    def geojson(self):
        '''Coordenadas dos municípios brasileiros em formato GeoJSON para
        criação de mapas.

        Retorna
        -------
        dict
            Coordenadas em formato GeoJSON.

        Erros
        -----
        DAB_UFError
            Caso seja uma UF extinta.

        Créditos
        --------
        https://github.com/tbrugz

        Ver Também
        ----------
        DadosAbertosBrasil.favoritos.geojson
            Função original.

        Exemplos
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

        '''

        if self.extinto:
            raise DAB_UFError('Método `geojson` indisponível para UFs extintas.')
        return favoritos.geojson(self.sigla)


    def historia(self):
        '''Objeto contendo a história da UF.

        Atributos
        ---------
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

        Ver também
        ----------
        DadosAbertosBrasil.ibge.Historia
            Classe original.

        Exemplos
        --------
        Capturar o texto da história de Minas Gerais.

        >>> mg = dab.UF('MG')
        >>> hist = mg.historia()
        >>> hist.historico
        "O Município de Wenceslau Braz tem sua origem praticamente desconh..."

        '''

        if self.sigla == 'GB':
            raise DAB_UFError('Método `historia` indisponível para a UF Guanabara.')
        elif self.sigla == 'FN':
            return Historia(localidade=260545)
        else:
            return Historia(localidade=self.cod)


    def malha(self):
        '''Obtém a URL para a malha referente à UF.

        Retorna
        -------
        str
            URL da malha da UF.

        Erros
        -----
        DAB_UFError
            Caso seja uma UF extinta.

        Ver Também
        ----------
        DadosAbertosBrasil.ibge.malha
            Função original.

        Exemplos
        --------
        >>> sp = UF('SP')
        >>> sp.malha()
        https://servicodados.ibge.gov.br/api/v2/malhas/35

        '''

        if self.extinto:
            raise DAB_UFError('Método `malha` indisponível para UFs extintas.')
        return malha(localidade=self.cod)        


    def municipios(self):
        '''Lista de municípios.

        Retorna
        -------
        list of str
            Lista de municípios.

        Erros
        -----
        DAB_UFError
            Caso seja uma UF extinta.

        Exemplos
        --------
        >>> ac = UF('AC')
        >>> ac.municipios()
        ['Acrelândia', 'Assis Brasil', 'Brasiléia', 'Bujari', ...]
        
        '''

        if self.extinto:
            raise DAB_UFError('Método `municipios` indisponível para UFs extintas.')
        js = favoritos.geojson(self.sigla)
        return [mun['properties']['name'] for mun in js['features']]


    def populacao(self):
        '''População projetada pelo IBGE.

        Retorna
        -------
        int
            População projetada.

        Erros
        -----
        DAB_UFError
            Caso seja uma UF extinta.

        Ver Também
        ----------
        DadosAbertosBrasil.ibge.populacao
            Função original.

        Exemplos
        --------
        >>> df = UF('DF')
        >>> df.populacao()
        3092244
        
        '''

        if self.extinto:
            raise DAB_UFError('Método `populacao` indisponível para UFs extintas.')
        return populacao(projecao='populacao', localidade=self.cod)


    def senadores(self):
        '''Lista dos três senadores em exercício.

        Retorna
        -------
        list of dict
            Lista de senadores.

        Erros
        -----
        DAB_UFError
            Caso seja uma UF extinta.

        Ver Também
        ----------
        DadosAbertosBrasil.senado.lista_atual
            Função original.

        Exemplos
        --------
        >>> rj = UF('RJ')
        >>> rj.senadores()
        
        '''
    
        if self.extinto:
            raise DAB_UFError('Método `senadores` indisponível para UFs extintas.')
        return lista_atual(uf=self.sigla)
