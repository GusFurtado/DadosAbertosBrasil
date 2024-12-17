from datetime import date
from typing import Optional

from pydantic import validate_call, PositiveInt

from ..utils import Base, Get, parse, Formato, Output


class Votacao(Base):
    """Informações detalhadas sobre uma votação da Câmara.

    Retorna um conjunto detalhado de dados sobre a votação, tais como as
    proposições que podem ter sido o objeto da votação e os efeitos de
    tramitação de outras proposições que eventualmente tenham sido cadastrados
    em consequência desta votação.

    Parameters
    ----------
    cod : str
        Código alfa-numérico da votação da qual se deseja informações.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.
    cod : str
        Código alfa-numérico da votação.
    aprovacao : int
        Aprovação da votação.
    data : str
        Data da votação.
    data_regitro : str
        Data e horário de registro da votação.
    data_ultima_abertura : str
        Data e horário da última abertura da votação.
    descricao : str
        Descrição da votação.
    efeitos_registrados : list
        Lista de efeitos registrados.
    evento : int
        Código numérico do evento da votação.
    orgao : int
        Código numérico do órgão da votação.
    objetos_possiveis : list of dict
        Lista de objetos possíveis.
    proposicoes_afetadas : str
        Proposições afetadas.
    sigla_orgao : str
        Sigla do órgão.
    ultima_apresentacao_proposicao : dict
        Última apresentação da proposição.
    uri : str
        Endereço para coleta de dados direta pela API da votação.
    uri_evento : str
        Endereço para coleta de dados direta pela API do evento.
    uri_orgao : str
        Endereço para coleta de dados direta pela API do órgão.

    Examples
    --------
    Obter a data da votação #2265603-43.
    >>> vot = camara.Votacao(cod='2265603-43')
    >>> vot.data
    ... '2020-12-22'

    """

    def __init__(self, cod: str, verificar_certificado: bool = True):
        self.cod = cod
        self.verify = verificar_certificado
        atributos = {
            "aprovacao": ["aprovacao"],
            "data": ["data"],
            "data_regitro": ["dataHoraRegistro"],
            "data_ultima_abertura": ["dataHoraUltimaAberturaVotacao"],
            "descricao": ["descricao"],
            "efeitos_registrados": ["efeitosRegistrados"],
            "evento": ["idEvento"],
            "orgao": ["idOrgao"],
            "objetos_possiveis": ["objetosPossiveis"],
            "proposicoes_afetadas": ["proposicoesAfetadas"],
            "sigla_orgao": ["siglaOrgao"],
            "ultima_apresentacao_proposicao": ["ultimaApresentacaoProposicao"],
            "uri": ["uri"],
            "uri_evento": ["uriEvento"],
            "uri_orgao": ["uriOrgao"],
        }

        super().__init__(
            endpoint="camara",
            path=["votacoes", str(cod)],
            unpack_keys=["dados"],
            error_key="descricao",
            atributos=atributos,
            verify=self.verify,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Votação {self.cod}"

    def __str__(self) -> str:
        return f"Votação {self.cod}"

    def orientacoes(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """O voto recomendado pelas lideranças aos seus deputados na votação.

        Em muitas votações, os líderes de partidos e blocos – as bancadas –
        fazem recomendações de voto para seus parlamentares. Essas orientações
        de uma votação também são feitas pelas lideranças de Governo, Minoria
        e as mais recentes Maioria e Oposição. Uma liderança também pode
        liberar a bancada para que cada deputado vote como quiser, ou entrar
        em obstrução, para que seus parlamentares não sejam contados para o
        quórum da votação.
        Se a votação teve orientações, este recurso retorna uma lista em que
        cada item contém os identificadores de um partido, bloco ou liderança,
        e o posicionamento ou voto que foi recomendado aos seus parlamentares.
        Até o momento, só estão disponíveis dados sobre orientações dadas em
        votações no Plenário.

        Parameters
        ----------
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

        cols_to_rename = {
            "orientacaoVoto": "orientacao",
            "codTipoLideranca": "lideranca",
            "siglaPartidoBloco": "bloco",
            "codPartidoBloco": "bloco_codigo",
            "uriPartidoBloco": "bloco_uri",
        }

        return Get(
            endpoint="camara",
            path=["votacoes", str(self.cod), "orientacoes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["bloco_uri"],
            remover_url=not url,
            index_col="bloco_codigo",
            index=index,
            verify=self.verify,
        ).get(formato)

    def votos(
        self,
        url: bool = True,
        formato: Formato = "pandas",
    ) -> Output:
        """Como cada parlamentar votou em uma votação nominal e aberta.

        Se a votação da Câmara é nominal e não foi secreta, retorna uma lista
        em que cada item contém os identificadores básicos de um deputado e o
        voto ou posicionamento que ele registrou.
        O resultado é uma lista vazia se a votação foi uma votação simbólica,
        em que os votos individuais não são contabilizados. Mas há algumas
        votações simbólicas que também têm registros de "votos": nesses casos,
        normalmente se trata de parlamentares que pediram expressamente que
        seus posicionamentos fossem registrados.
        Não são listados parlamentares ausentes à votação.

        Parameters
        ----------
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
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

        cols_to_rename = {
            "tipoVoto": "voto",
            "dataRegistroVoto": "data",
            "deputado_.id": "deputado_codigo",
            "deputado_.uri": "deputado_uri",
            "deputado_.nome": "deputado_nome",
            "deputado_.siglaPartido": "deputado_partido",
            "deputado_.uriPartido": "deputado_partido_uri",
            "deputado_.siglaUf": "deputado_uf",
            "deputado_.idLegislatura": "deputado_legislatura",
            "deputado_.urlFoto": "deputado_foto",
            "deputado_.email": "deputado_email",
        }

        return Get(
            endpoint="camara",
            path=["votacoes", str(self.cod), "votos"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data"],
            url_cols=[
                "deputado_uri",
                "deputado_partido_uri",
                "deputado_foto",
                "deputado_email",
            ],
            remover_url=not url,
            verify=self.verify,
        ).get(formato)


@validate_call
def lista_votacoes(
    proposicao: Optional[int] = None,
    evento: Optional[int] = None,
    orgao: Optional[int] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    pagina: PositiveInt = 1,
    itens: Optional[PositiveInt] = None,
    asc: bool = False,
    ordenar_por: str = "dataHoraRegistro",
    url: bool = True,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Lista de votações na Câmara.

    Retorna uma lista de informações básicas sobre as votações ocorridas em
    eventos dos diversos órgãos da Câmara. Se não forem passados parâmetros
    que delimitem o intervalo de tempo da pesquisa, são retornados dados sobre
    todas as votações ocorridas nos últimos 30 dias, em eventos de todos os
    órgãos.

    Os parâmetros de data permitem estender o período, mas por enquanto é
    necessário que as duas datas sejam de um mesmo ano. Quando apenas uma
    delas está presente, são retornadas somente as votações ocorridas no mesmo
    ano, antes de `fim` ou após `inicio`.

    Parameters
    ----------
    proposicao : int, optional
        Código numérico da proposição, que podem ser obtidos pela função
        `camara.lista_proposições`. Se presente, listará as votações que
        tiveram a proposição como objeto de votação ou que afetaram as
        proposições listadas.
    evento : int, optional
        Código numérico do evento realizado na Câmara, no qual tenham sido
        realizadas as votações a serem listadas. Os códigos podem ser obtidos
        pela função `camara.lista_eventos`. Somente os eventos deliberativos
        podem ter votações. Os eventos podem ter ocorrido fora do intervalo de
        tempo padrão ou definido por `inicio` e/ou `fim`.
    orgao : int, optional
        Código numérico do órgão da Câmara. Se presente, serão retornadas
        somente votações do órgão enumerado. Os códigos existentes podem ser
        obtidos pela função `camara.lista_orgaos`.
    inicio : str, optional
        Data em formato 'AAAA-MM-DD' para início do intervalo de tempo no qual
        tenham sido realizadas as votações a serem listadas. Se usado sozinho,
        esse parâmetro faz com que sejam retornadas votações ocorridas dessa
        data até o fim do mesmo ano. Se usado com `fim`, as duas datas devem
        ser de um mesmo ano.
    fim : str, optional
        Data em formato 'AAAA-MM-DD' que define o fim do intervalo de tempo no
        qual tenham sido realizadas as votações a serem listadas. Se usado
        sozinho, esse parâmetro faz com que sejam retornadas todas as votações
        ocorridas desde 1º de janeiro do mesmo ano até esta data. Se usado com
        `inicio`, é preciso que as duas datas sejam de um mesmo ano.
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
    if evento is not None:
        params["idEvento"] = evento
    if orgao is not None:
        params["idOrgao"] = orgao
    if inicio is not None:
        params["dataInicio"] = parse.data(inicio, "camara")
    if fim is not None:
        params["dataFim"] = parse.data(fim, "camara")
    if itens is not None:
        params["itens"] = itens

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "data": "data",
        "dataHoraRegistro": "data_registro",
        "siglaOrgao": "orgao",
        "uriOrgao": "orgao_uri",
        "uriEvento": "evento_uri",
        "proposicaoObjeto": "proposicao",
        "uriProposicaoObjeto": "proposicao_uri",
        "descricao": "descricao",
        "aprovacao": "aprovacao",
    }

    return Get(
        endpoint="camara",
        path=["votacoes"],
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_date=["data", "data_registro"],
        url_cols=["uri", "orgao_uri", "evento_uri", "proposicao_uri"],
        remover_url=not url,
        index=index,
        verify=verificar_certificado,
    ).get(formato)
