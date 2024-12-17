from datetime import date
from typing import Optional

from pydantic import validate_call, PositiveInt

from ..utils import Base, Get, parse, Formato, Output


class Partido(Base):
    """Informações detalhadas sobre um partido.

    Parameters
    ----------
    cod : int
        Código numérico do partido do qual se deseja informações.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.
    cod : int
        Código numérico do partido.
    facebook : str
        URL da página no Facebook do partido.
    legislatura : str
        Código numérico da última legislatura.
    lider : dict
        Informações sobre o líder do partido.
    logo : str
        URL da logo do partido.
    nome : str
        Nome completo do partido.
    numero : int
        Número eleitoral do partido.
    sigla : str
        Sigla do partido.
    situacao : str
        Situação do partido.
    total_membros : str
        Total de membros do partido.
    total_posse : str
        Total de posse do partido.
    ultima_atualizacao : str
        Última atualização das informações sobre o partido.
    uri : str
        Endereço para coleta de dados direta pela API do partido.
    uri_membros : str
        Endereço para coleta de dados direta pela API dos membros do partido.
    website : str
        URL do website do partido.


    Examples
    --------
    Obter o nome completo do partido #36899.
    >>> p = camara.Partido(cod=36899)
    >>> p.nome
    ... 'Movimento Democrático Brasileiro'

    """

    def __init__(self, cod: int, verificar_certificado: bool = True):
        self.cod = cod
        self.verify = verificar_certificado
        atributos = {
            "facebook": ["urlFacebook"],
            "legislatura": ["status", "idLegislatura"],
            "lider": ["status", "lider"],
            "logo": ["urlLogo"],
            "nome": ["nome"],
            "numero": ["numeroEleitoral"],
            "sigla": ["sigla"],
            "situacao": ["status", "situacao"],
            "total_membros": ["status", "totalMembros"],
            "total_posse": ["status", "totalPosse"],
            "ultima_atualizacao": ["status", "data"],
            "uri": ["uri"],
            "uri_membros": ["status", "uriMembros"],
            "website": ["urlWebSite"],
        }

        super().__init__(
            endpoint="camara",
            path=["partidos", str(cod)],
            unpack_keys=["dados"],
            error_key="status",
            atributos=atributos,
            verify=self.verify,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: {self.nome}"

    def __str__(self) -> str:
        return self.nome

    def membros(
        self,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        legislatura: Optional[PositiveInt] = None,
        pagina: PositiveInt = 1,
        itens: Optional[PositiveInt] = None,
        ordenar_por: Optional[str] = None,
        asc: bool = True,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Uma lista dos parlamentares de um partido durante um período.

        Retorna uma lista de deputados que estão ou estiveram em exercício
        pelo partido. Opcionalmente, pode-se usar os parâmetros `inicio`,
        `fim` ou `legislatura` para se obter uma lista de deputados filiados
        ao partido num certo intervalo de tempo. Isso é equivalente à função
        `lista_deputados` com filtro por partido, mas é melhor para obter
        informações sobre membros de partidos já extintos.

        Parameters
        ----------
        inicio : str, optional
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim : str, optional
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        legislatura : int, optional
            Número da legislatura, à qual os dados buscados devem corresponder.
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
        ordenar_por : str, optional
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        index : bool, default=False
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Returns
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list of dict
            Se formato = 'json', retorna os dados brutos no formato json.

        """

        params = {"pagina": pagina, "ordem": "asc" if asc else "desc"}
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")
        if legislatura is not None:
            params["idLegislatura"] = legislatura
        if itens is not None:
            params["itens"] = itens
        if ordenar_por is not None:
            params["ordenarPor"] = ordenar_por

        cols_to_rename = {
            "id": "codigo",
            "uri": "uri",
            "nome": "nome",
            "siglaPartido": "partido",
            "uriPartido": "partido_uri",
            "siglaUf": "uf",
            "idLegislatura": "legislatura",
            "urlFoto": "foto",
            "email": "email",
        }

        return Get(
            endpoint="camara",
            path=["partidos", str(self.cod), "membros"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri", "partido_uri", "foto", "email"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)


@validate_call
def lista_partidos(
    legislatura: Optional[PositiveInt] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    pagina: PositiveInt = 1,
    itens: Optional[PositiveInt] = None,
    asc: bool = True,
    ordenar_por: str = "sigla",
    url: bool = True,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Os partidos políticos que têm ou já tiveram parlamentares em exercício
    na Câmara.

    Retorna uma lista de dados básicos sobre os partidos políticos que têm ou
    já tiveram deputados na Câmara. Se não forem passados parâmetros, a função
    retorna os partidos que têm deputados em exercício no momento da
    requisição. É possível obter uma lista de partidos representados na Câmara
    em um certo intervalo de datas ou de legislaturas.

    Parameters
    ----------
    legislatura : int, optional
        Número da legislatura a qual os dados buscados devem corresponder.
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
    ordenar_por : str, default='sigla'
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.
    url : bool, default=False
        Se False, remove as colunas contendo URI, URL e e-mails.
        Esse argumento é ignorado se `formato` for igual a 'json'.
    index : bool, default=False
        Se True, define a coluna `codigo` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'.
    formato : {'dataframe', 'json'}, default='dataframe'
        Formato do dado que será retornado.
        Os dados no formato 'json' são mais completos, porém alguns filtros
        podem não ser aplicados.

    Returns
    -------
    pandas.core.frame.DataFrame
        Se formato = 'dataframe', retorna os dados formatados em uma tabela.
    list of dict
        Se formato = 'json', retorna os dados brutos no formato json.

    """

    params = {
        "pagina": pagina,
        "ordem": "asc" if asc else "desc",
        "ordenarPor": ordenar_por,
    }
    if legislatura is not None:
        params["idLegislatura"] = legislatura
    if inicio is not None:
        params["dataInicio"] = parse.data(inicio, "camara")
    if fim is not None:
        params["dataFim"] = parse.data(fim, "camara")
    if itens is not None:
        params["itens"] = itens

    cols_to_rename = {"id": "codigo", "sigla": "sigla", "nome": "nome", "uri": "uri"}

    return Get(
        endpoint="camara",
        path=["partidos"],
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        url_cols=["uri"],
        remover_url=not url,
        index=index,
        verify=verificar_certificado,
    ).get(formato)
