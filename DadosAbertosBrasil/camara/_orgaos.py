from datetime import date
from typing import Optional

from pydantic import validate_call, PositiveInt

from ..utils import Base, Get, parse, Formato, Output


class Orgao(Base):
    """Informações detalhadas sobre um órgão da Câmara.

    Parameters
    ----------
    cod : int
        Código numérico do órgão do qual se deseja informações.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.
    cod : int
        Código numérico do órgão.
    apelido : str
        Apelido do órgão.
    casa : str
        Casa do órgão.
    cod_tipo : int
        Código do tipo do órgão.
    fim : str
        Data final do órgão.
    inicio : str
        Data inicial do órgão.
    instalacao : str
        Data de instalação do órgão.
    nome : str
        Nome do órgão.
    nome_publicacao : str
        Nome de publicação.
    sala : str
        Sala do órgão.
    sigla : str
        Sigla do órgão.
    tipo : str
        Tipo do órgão.
    uri : str
        Endereço para coleta de dados direta pela API do órgão.
    urlWebsite : str
        URL para acessar o website do órgão.

    Examples
    --------
    Obter o apelido do órgão #4.
    >>> org = camara.Orgao(cod=4)
    >>> org.apelido
    ... 'Mesa Diretora'

    """

    def __init__(self, cod: int, verificar_certificado: bool = True):
        self.cod = cod
        self.verify = verificar_certificado
        atributos = {
            "apelido": ["apelido"],
            "casa": ["casa"],
            "cod_tipo": ["codTipoOrgao"],
            "fim": ["dataFim"],
            "inicio": ["dataInicio"],
            "instalacao": ["dataInstalacao"],
            "nome": ["nome"],
            "nome_publicacao": ["nomePublicacao"],
            "sala": ["sala"],
            "sigla": ["sigla"],
            "tipo": ["tipoOrgao"],
            "uri": ["uri"],
            "urlWebsite": ["urlWebsite"],
        }

        super().__init__(
            endpoint="camara",
            path=["orgaos", str(cod)],
            unpack_keys=["dados"],
            error_key="nome",
            atributos=atributos,
            verify=self.verify,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Órgão {self.nome}"

    def __str__(self) -> str:
        return f"Órgão {self.nome}"

    def eventos(
        self,
        tipo_evento: Optional[str] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Os eventos ocorridos ou previstos em um órgão legislativo.

        Retorna uma lista de informações resumidas dos eventos realizados
        (ou a realizar) pelo órgão legislativo. Por padrão, são retornados
        eventos em andamento ou previstos para o mesmo dia, dois dias antes
        e dois dias depois da requisição. Parâmetros podem ser passados para
        alterar esse período, bem como os tipos de eventos.

        Parameters
        ----------
        tipo_evento : str, optional
            Identificador numérico do tipo de evento que se deseja obter.
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
        ordenar_por : str, default='dataHoraInicio'
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        index : bool, default=False
            Se True, define a coluna `id` como index do DataFrame.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.


        Returns
        -------
        pandas.core.frame.DataFrame
            Lista de discursos feitos por um deputado em eventos diversos.

        """

        params = {
            "pagina": pagina,
            "ordem": "asc" if asc else "desc",
            "ordenarPor": ordenar_por,
        }
        if tipo_evento is not None:
            params["idTipoEvento"] = tipo_evento
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")
        if itens is not None:
            params["itens"] = itens

        cols_to_rename = {
            "id": "codigo",
            "uri": "uri",
            "dataHoraInicio": "data_inicio",
            "dataHoraFim": "data_fim",
            "situacao": "situacao",
            "descricaoTipo": "descricao_tipo",
            "descricao": "descricao",
            "localExterno": "local_externo",
            "orgaos": "orgaos",
            "localCamara": "local_camara",
            "urlRegistro": "url",
        }

        return Get(
            endpoint="camara",
            path=["orgaos", str(self.cod), "eventos"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "url"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

    def membros(
        self,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        pagina: PositiveInt = 1,
        itens: Optional[PositiveInt] = None,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Lista de cargos de um órgão e parlamentares que os ocupam.

        Retorna uma lista de dados resumidos que identificam cada parlamentar
        e o cargo ou posição que ocupa ou ocupou no órgão parlamentar durante
        um certo período de tempo. Se não forem passados parâmetros que
        delimitem esse período, o serviço retorna os membros do órgão no
        momento da requisição. Se o órgão não existir mais ou não estiver
        instalado, é retornada uma lista vazia.

        Parameters
        ----------
        inicio : str, optional
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim : str, optional
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        pagina : int, default=1
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido
            pelo parâmetro `itens`. Se omitido, assume o valor 1.
        itens : int, optional
            Número máximo de itens na “página” que se deseja obter com esta
            requisição.
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

        params = {"pagina": pagina}
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")
        if itens is not None:
            params["itens"] = itens

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
            "dataInicio": "data_inicio",
            "dataFim": "data_fim",
            "titulo": "titulo",
            "codTitulo": "titulo_codigo",
        }

        return Get(
            endpoint="camara",
            path=["orgaos", str(self.cod), "membros"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["titulo_codigo"],
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "partido_uri", "foto", "email"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

    def votacoes(
        self,
        proposicao: Optional[int] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Uma lista de eventos com a participação do parlamentar.

        Retorna uma lista de dados básicos de votações que tenham sido
        realizadas em eventos realizados no órgão. Se este for um órgão
        permanente da Câmara, são retornados, por padrão, dados sobre as
        votações realizadas pelo órgão nos últimos 30 dias. Esse período pode
        ser alterado com o uso dos parâmetros `inicio` e/ou `fim`, que por
        enquanto são limitados a selecionar somente votações ocorridas em um
        mesmo ano.
        Caso este seja um órgão temporário, como uma comissão especial, são
        listadas por padrão todas as votações ocorridas no órgão, em qualquer
        período de tempo.
        Dados complementares sobre cada votação listada podem ser obtidos com
        o objeto `camara.Votacao`.

        Parameters
        ----------
        proposicao : int, optional
            Código numérico da proposição, que podem ser obtidos por meio da
            função `camara.lista_proposicoes`. Se presente, listará as
            votações que tiveram a proposição como objeto de votação ou que
            afetaram as proposições listadas.
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
        asc : bool, default=False
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por : str, default='dataHoraRegistro'
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
        if proposicao is not None:
            params["idProposicao"] = proposicao
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")
        if itens is not None:
            params["itens"] = itens

        cols_to_rename = {
            "aprovacao": "aprovacao",
            "data": "data",
            "dataHoraRegistro": "data_registro",
            "descricao": "descricao",
            "id": "codigo",
            "proposicaoObjeto": "proposicao",
            "siglaOrgao": "orgao",
            "uri": "uri",
            "uriEvento": "evento_uri",
            "uriOrgao": "orgao_uri",
            "uriProposicaoObjeto": "proposicao_uri",
        }

        return Get(
            endpoint="camara",
            path=["orgaos", str(self.cod), "votacoes"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data", "data_registro"],
            url_cols=["uri", "evento_uri", "orgao_uri", "proposicao_uri"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)


@validate_call
def lista_orgaos(
    sigla: Optional[str] = None,
    tipo: Optional[PositiveInt] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    pagina: PositiveInt = 1,
    itens: Optional[PositiveInt] = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Lista das comissões e outros órgãos legislativos da Câmara.

    Retorna uma lista de informações básicas sobre os órgãos legislativos e
    seus identificadores, tipos e descrições. É possível filtrar a lista por
    identificadores, tipos de órgãos, sigla, situação do órgão ou período de
    tempo em que os órgãos estiveram ativos, se aplicável.

    Parameters
    ----------
    sigla : str, optional
        Sigla oficialmente usadas para designar o órgão da câmara.
    tipo : int, optional
        Código numérico do tipo de órgãos que se deseja buscar dados. Pode ser
        obtido pela função `camara.referencias`.
    inicio : str, optional
        Data de início, no formato 'AAAA-MM-DD', de um intervalo de tempo no
        qual os órgãos buscados devem ter estado em atividade.
    fim : str, optional
        Data de término, no formato 'AAAA-MM-DD', de um intervalo de tempo no
        qual os órgãos buscados devem ter estado em atividade.
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
    ordenar_por : str, default='id'
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
    if sigla is not None:
        params["sigla"] = sigla
    if tipo is not None:
        params["codTipoOrgao"] = tipo
    if inicio is not None:
        params["dataInicio"] = parse.data(inicio, "camara")
    if fim is not None:
        params["dataFim"] = parse.data(fim, "camara")
    if itens is not None:
        params["itens"] = itens

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "sigla": "sigla",
        "nome": "nome",
        "apelido": "apelido",
        "codTipoOrgao": "orgao_tipo_codigo",
        "tipoOrgao": "orgao_tipo",
        "nomePublicacao": "nome_publicacao",
    }

    return Get(
        endpoint="camara",
        path=["orgaos"],
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        url_cols=["uri"],
        remover_url=not url,
        index=index,
        verify=verificar_certificado,
    ).get(formato)
