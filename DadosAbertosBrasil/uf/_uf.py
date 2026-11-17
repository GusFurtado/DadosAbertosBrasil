"""Objeto UF contendo informações das Unidades da Federação.

Serve como um consolidador por UF de diversar funções do pacote DadosAbertosBrasil.

"""

from datetime import date
from typing import Any, Literal

from .. import favoritos, ibge, wiki
from ..camara import lista_deputados
from ..senado import lista_senadores
from ..utils import parse
from ..utils.errors import DABUFError
from ..utils.typing import Formato, Saida
from ._governador import Governador

# O Brasil e as UFs extintas não estão em `wiki.ufs()`.
_FORA_DO_WIKI = {
    "BR": {
        "nome": "Brasil",
        "cod": 1,
        "area": 8510295.914,
        "capital": "Brasília",
        "extinto": False,
        "gentilico": ["brasileiro", "brasileira"],
        "lema": "Ordem e Progresso",
        "regiao": None,
        "coordenadas": None,
    },
    "FN": {
        "nome": "Fernando de Noronha",
        "cod": 20,
        "area": 18.609,
        "capital": "Fernando de Noronha",
        "extinto": True,
        "gentilico": ["noronhense"],
        "lema": None,
        "regiao": "Nordeste",
        "coordenadas": None,
    },
    "GB": {
        "nome": "Guanabara",
        "cod": 34,
        "area": 1356,
        "capital": "Rio de Janeiro",
        "extinto": True,
        "gentilico": None,
        "lema": None,
        "regiao": "Sudeste",
        "coordenadas": None,
    },
}


class UF:
    """Consolidado de informações de uma Unidade Federativa.

    Parameters
    ----------
    uf : str
        Nome, sigla ou código da UF desejada.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

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

    gentilico : list[str]
        Gentílicos e variações.

    lema : str
        Lema da UF.

    regiao : str
        Grande região (Norte, Nordeste, Sudeste, Sul ou Centro-Oeste).

    coordenadas : dict[str, float]
        Dicionário contendo latitude e longitude.

    wikidata : str
        Identificador do item no Wikidata (só para as 27 UFs atuais).

    artigo : str
        Título do artigo na Wikipedia (só para as 27 UFs atuais).

    registro : DadosAbertosBrasil.wiki.modelos.UF | None
        Registro completo de `wiki.ufs()`; None para o Brasil e as UFs extintas.

    Properties
    ----------
    densidade : float
        Densidade populacional (hab/km²) da UF.

    galeria : DadosAbertosBrasil.ibge.Galeria
        Gera uma galeria de fotos da UF.

    governador : DadosAbertosBrasil.uf.Governador
        Informações básico do governador da UF.

    historia : DadosAbertosBrasil.ibge.Historia
        Objeto contendo a história da UF.

    municipios : list[str]
        Lista de municípios.

    populacao : int
        População residente estimada pelo IBGE (tabela 6579 do SIDRA).

    prefeito : DadosAbertosBrasil.wiki.modelos.PrefeitoCapital
        Prefeito em exercício da capital.

    Methods
    -------
    bandeira(tamanho=100)
        Gera a URL da WikiMedia para a bandeira do estado.

    brasao(tamanho=100)
        Gera a URL da WikiMedia para o brasão do estado.

    deputados(nome, legislatura, partido, sexo, inicio, fim, pagina, itens...)
        Lista dos deputados federais em exercício.

    malha(nivel, divisoes, periodo, tipo, qualidade, formato)
        Obtém a URL para a malha referente à UF.

    senadores(tipo, sexo, partido, contendo, excluindo, url, index, formato)
        Lista de senadores da república desta UF.

    """

    sigla: str
    verify: bool | None
    registro: wiki.modelos.UF | None

    def __init__(self, uf: str, verificar_certificado: bool | None = None):
        self.sigla = parse.uf(uf=uf, extintos=True)
        self.verify = verificar_certificado
        self.registro = None
        data = self._get_data()
        for attr in data:
            setattr(self, attr, data[attr])

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.UF: {self.nome}>"

    def __str__(self) -> str:
        return self.nome

    def _get_data(self) -> dict:
        """Buscar dados de UFs no DadosAbertosBrasil-wiki."""

        if self.sigla in _FORA_DO_WIKI:
            return dict(_FORA_DO_WIKI[self.sigla])
        registros = wiki.ufs(formato="pydantic", verificar_certificado=self.verify)
        self.registro = next(r for r in registros if r.sigla == self.sigla)
        r = self.registro
        return {
            "nome": r.nome,
            "cod": r.codigo_ibge,
            "area": r.area_km2,
            "capital": r.capital,
            "extinto": False,
            "gentilico": r.gentilicos,
            "lema": r.lema,
            "regiao": r.regiao,
            "coordenadas": {"latitude": r.latitude, "longitude": r.longitude},
            "wikidata": r.wikidata,
            "artigo": r.artigo,
        }

    def bandeira(self, tamanho: int = 100) -> str:
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

        >>> sc = UF("sc")
        >>> sc.bandeira(tamanho=200)
        'https://upload.wikimedia.org/wikipedia/commons/thumb/1/1a/' ...

        """

        return favoritos.bandeira(uf=self.sigla, tamanho=tamanho)

    def brasao(self, tamanho: int = 100) -> str:
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

        É a razão entre a população estimada pelo IBGE (habitantes) e a área
        territorial da UF (quilómetros quadrados).

        Returns
        -------
        float
            Densidade populacional.

        Raises
        ------
        DABUFError
            Caso seja uma UF extinta.

        See Also
        --------
        UF.populacao
            População estimada da UF.

        Examples
        --------
        >>> am = UF('AM')
        >>> am.populacao()
        2.719286132694809

        """

        if self.extinto:
            raise DABUFError("Método `densidade` indisponível para UFs extintas.")
        return self.populacao / self.area

    def deputados(
        self,
        nome: str | None = None,
        legislatura: int | None = None,
        partido: str | None = None,
        sexo: str | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: int = 1,
        itens: int | None = None,
        asc: bool = True,
        ordenar_por: str = "nome",
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
        verificar_certificado: bool | None = None,
    ) -> Saida:
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

        sexo : {'f', 'm'}, optional
            Letra que designe o gênero dos parlamentares que se deseja buscar:
            - 'f': Feminino;
            - 'm': Masculino.

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

        url : bool, default=True
            Se False, remove as colunas contendo URI, URL e e-mails.
            Vale para os formatos 'json', 'pandas' e 'polars'.

        index : bool, default=False
            Se True, define a coluna `id` como index do DataFrame.
            Só se aplica ao formato 'pandas'; com 'polars', é ignorado com aviso.

        formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
            Formato do dado que será retornado:
            - "json": lista de registros (`list[dict]`), com os mesmos campos e
              tipos das colunas do DataFrame;
            - "bruto": JSON original da API, como veio;
            - "pydantic": lista de modelos Pydantic, um por registro;
            - "pandas": DataFrame pandas;
            - "polars": DataFrame polars;
            - "url": endereço da consulta.
            Se omitido, usa `DadosAbertosBrasil.config.formato`.

        verificar_certificado : bool, optional
            Defina como `False` em caso de falha na verificação do certificado
            SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

        Returns
        -------
        list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
            Tabela com informações básicas dos deputados federais.

        Raises
        ------
        DABUFError
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
            raise DABUFError("Método `deputados` indisponível para UFs extintas.")

        return lista_deputados(
            nome=nome,
            legislatura=legislatura,
            uf=self.sigla,
            partido=partido,
            sexo=sexo,
            inicio=inicio,
            fim=fim,
            pagina=pagina,
            itens=itens,
            asc=asc,
            ordenar_por=ordenar_por,
            url=url,
            index=index,
            formato=formato,
            verificar_certificado=verificar_certificado,
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
            raise DABUFError("Método `galeria` indisponível para UFs extintas.")
        return ibge.Galeria(self.cod)

    @property
    def governador(self) -> Governador:
        """Informações básicas do governador da UF.

        Returns
        -------
        DadosAbertosBrasil.uf.Governador
            Governador em exercício, a partir de `wiki.governadores()`.

        Raises
        ------
        DABUFError
            Caso seja uma UF extinta.

        """

        if self.cod == 1:
            raise DABUFError("Propriedade `governador` indisponível para 'Brasil'.")
        if self.extinto:
            raise DABUFError("Propriedade `governador` indisponível para UFs extintas.")
        return Governador(self.sigla, verificar_certificado=self.verify)

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

        if self.sigla == "GB":
            raise DABUFError("Método `historia` indisponível para a UF Guanabara.")
        elif self.sigla == "FN":
            return ibge.Historia(localidade=260545)
        else:
            return ibge.Historia(localidade=self.cod)

    def malha(
        self,
        nivel: str = "estados",
        divisoes: str | None = None,
        periodo: int = 2020,
        tipo: Literal["geojson", "topojson", "svg"] = "geojson",
        qualidade: Literal["minima", "intermediaria", "maxima"] = "minima",
        formato: Literal["bruto", "url", "svg", "json", "geojson"] = "bruto",
    ) -> dict[str, Any] | str:
        """Malha territorial da UF, em GeoJSON, TopoJSON ou SVG.

        Parameters
        ----------
        nivel : str, default='estados'
            Nível geográfico dos dados.

        divisoes : str, optional
            Subdivisões intrarregionais da malha, como 'municipio' ou
            'microrregiao'. Se None, apresenta a malha sem subdivisões.

        periodo : int, default=2020
            Ano da revisão da malha.

        tipo : {'geojson', 'topojson', 'svg'}, default='geojson'
            Tipo de arquivo da malha.

        qualidade : {'minima', 'intermediaria', 'maxima'}, default='minima'
            Qualidade (nível de detalhe) da malha.

        formato : {'bruto', 'url'}, default='bruto'
            - "bruto": o conteúdo da malha: `dict` para GeoJSON e TopoJSON,
              `str` com o SVG;
            - "url": endereço da malha.
            Os valores antigos 'geojson', 'json' e 'svg' continuam funcionando
            com `DeprecationWarning`; use `tipo`.

        Returns
        -------
        dict
            Malha em GeoJSON ou TopoJSON, com `formato='bruto'`.
        str
            SVG da malha, com `tipo='svg'`, ou endereço da malha, com
            `formato='url'`.

        Raises
        ------
        DABUFError
            Caso seja uma UF extinta.
        DABLocalidadeError
            Caso o nível geográfico ou a subdivisão sejam inválidos.

        Notes
        -----
        https://servicodados.ibge.gov.br/api/docs/malhas?versao=3

        See also
        --------
        DadosAbertosBrasil.ibge.malha
            Função original

        Examples
        --------
        Malha do Distrito Federal em GeoJSON.

        >>> df = dab.UF('DF')
        >>> df.malha()
        {'type': 'FeatureCollection',
            'features': [{'type': 'Feature',
                'geometry': {'type': 'Polygon',
                    'coordinates': [[[-47.31, -16.0363], ...

        SVG de Alagoas com as divisas dos municípios.

        >>> al = dab.UF('alagoas')
        >>> al.malha(divisoes='municipio', tipo='svg')
        '<?xml version="1.0"?><svg xmlns="http://www.w3.org/2000/svg" ...'

        """

        if self.extinto:
            raise DABUFError("Método `malha` indisponível para UFs extintas.")
        return ibge.malha(
            localidade=self.cod,
            nivel=nivel,
            divisoes=divisoes,
            periodo=periodo,
            tipo=tipo,
            qualidade=qualidade,
            formato=formato,
        )

    @property
    def municipios(self) -> int | str:
        """Lista de municípios.

        Returns
        -------
        dict[int, str]
            Dicionário onde a chave é o código IBGE do município e o valor é
            seu respectivo nome.

        Raises
        ------
        DABUFError
            Caso seja uma UF extinta.

        Examples
        --------
        >>> ac = UF('AC')
        >>> ac.municipios()
        {1200013: 'Acrelândia', 1200054: 'Assis Brasil', 1200104: 'Brasiléia', ...

        """

        if self.extinto:
            raise DABUFError("Método `municipios` indisponível para UFs extintas.")
        municipios = ibge.localidades("estados", divisoes="municipios", localidade=self.cod, formato="pydantic")
        return {municipio.id: municipio.nome for municipio in municipios}

    @property
    def populacao(self) -> int:
        """População residente estimada pelo IBGE.

        Usa a estimativa mais recente da tabela 6579 do SIDRA. A API de
        projeções populacionais do IBGE, usada até o 2.x, saiu do ar.

        Returns
        -------
        int
            População residente estimada.

        Raises
        ------
        DABUFError
            Caso seja uma UF extinta.

        See Also
        --------
        DadosAbertosBrasil.ibge.sidra
            Função usada, com a tabela 6579.

        Examples
        --------
        >>> df = UF('DF')
        >>> df.populacao()
        3092244

        """

        if self.extinto:
            raise DABUFError("Método `populacao` indisponível para UFs extintas.")
        nivel = {1: "all"} if self.cod == 1 else {3: self.cod}
        estimativa = ibge.sidra(6579, variaveis=9324, localidades=nivel, formato="bruto",
                                verificar_certificado=self.verify)
        return int(estimativa[1]["V"])

    @property
    def prefeito(self) -> wiki.modelos.PrefeitoCapital:
        """Prefeito em exercício da capital da UF.

        Returns
        -------
        DadosAbertosBrasil.wiki.modelos.PrefeitoCapital
            Registro de `wiki.prefeitos_capitais()`.

        Raises
        ------
        DABUFError
            Caso seja o Brasil, o Distrito Federal (sem prefeitura) ou uma UF
            extinta.

        Examples
        --------
        >>> UF("SC").prefeito.nome

        """

        if self.registro is None or self.sigla == "DF":
            raise DABUFError("Propriedade `prefeito` indisponível para esta UF.")
        prefeitos = wiki.prefeitos_capitais(uf=self.sigla, formato="pydantic", verificar_certificado=self.verify)
        return prefeitos[0]

    def senadores(
        self,
        tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
        sexo: str | None = None,
        partido: str | None = None,
        contendo: str | None = None,
        excluindo: str | None = None,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
        verificar_certificado: bool | None = None,
    ) -> Saida:
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

        url : bool, default=True
            Se False, remove as colunas contendo URI, URL e e-mails.
            Vale para os formatos 'json', 'pandas' e 'polars'.

        index : bool, default=False
            Se True, define a coluna `codigo` como index do DataFrame.
            Só se aplica ao formato 'pandas'; com 'polars', é ignorado com aviso.

        formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
            Formato do dado que será retornado:
            - "json": lista de registros (`list[dict]`), com os mesmos campos e
              tipos das colunas do DataFrame;
            - "bruto": JSON original da API, como veio;
            - "pydantic": lista de modelos Pydantic, um por registro;
            - "pandas": DataFrame pandas;
            - "polars": DataFrame polars;
            - "url": endereço da consulta.
            Se omitido, usa `DadosAbertosBrasil.config.formato`.

        verificar_certificado : bool, optional
            Defina como `False` em caso de falha na verificação do certificado
            SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

        Returns
        -------
        list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
            Lista de senadores.

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
            raise DABUFError("Método `senadores` indisponível para UFs extintas.")

        return lista_senadores(
            uf=self.sigla,
            tipo=tipo,
            sexo=sexo,
            partido=partido,
            contendo=contendo,
            excluindo=excluindo,
            url=url,
            index=index,
            formato=formato,
            verificar_certificado=verificar_certificado,
        )
