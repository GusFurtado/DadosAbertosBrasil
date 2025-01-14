from datetime import date
from typing import Optional

from pydantic import validate_call, PositiveInt

from ..utils import Base, Get, parse, Formato, Output


class Evento(Base):
    """Retorna um conjunto detalhado de informações sobre o evento da Câmara.

    Parameters
    ----------
    cod : int
        Código numérico do evento do qual se deseja informações.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.

    cod : int
        Código numérico do evento.

    andar : str
        Andar do prédio onde ocorreu o evento.

    descricao : str
        Descrição do evento.

    descricao_tipo : str
        Tipo do evento.

    fases : str
        Fases do evento.

    fim : str
        Data e horário que o evento foi finalizado no formato `'AAAA-MM-DD'`.

    inicio : str
        Data e horário que o evento foi iniciado no formato `'AAAA-MM-DD'`.

    local : str
        Local onde ocorreu o evento.

    local_externo : str
        Local externo do evento.

    lista_orgaos : list of dict
        Lista de orgãos e informações sobre os mesmos.

    predio : str
        Prédio que ocorreu o evento.

    requerimentos : list of dict
        Requerimentos do evento.

    sala : str
        Sala do prédio onde ocorreu o evento.

    situacao : str
        Situação do evento.

    uri : str
        Endereço para coleta de dados direta pela API do evento.

    uri_convidados : str
        Endereço para coleta de dados direta pela API dos convidados.

    uri_deputados : str
        Endereço para coleta de dados direta pela API dos deputados.

    url_documento_pauta : str
        Endereço URL para visualizar a pauta do evento.

    url_registro : str
        Endereço URL onde o evento foi registrado.

    Methods
    -------
    deputados()
        Os deputados participantes do evento.

    orgaos()
        Lista de órgãos organizadores do evento.

    pauta()
        Lista de proposições que foram ou deverão ser avaliadas.

    votacoes()
        Informações detalhadas de votações sobre o evento.

    Examples
    --------
    Obter a URL para assistir ao evento #59265.
    >>> ev = camara.Evento(cod=59265)
    >>> ev.url_registro
    ... 'https://www.youtube.com/watch?v=8D2gjMrTnMA'

    """

    def __init__(self, cod: int, verificar_certificado: bool = True):
        self.cod = cod
        self.verify = verificar_certificado
        atributos = {
            "andar": ["localCamara", "andar"],
            "descricao": ["descricao"],
            "descricao_tipo": ["descricaoTipo"],
            "fases": ["fases"],
            "fim": ["dataHoraFim"],
            "inicio": ["dataHoraInicio"],
            "local": ["localCamara", "nome"],
            "local_externo": ["localExterno"],
            "lista_orgaos": ["orgaos"],
            "predio": ["localCamara", "predio"],
            "requerimentos": ["requerimentos"],
            "sala": ["localCamara", "sala"],
            "situacao": ["situacao"],
            "uri": ["uri"],
            "uri_convidados": ["uriConvidados"],
            "uri_deputados": ["uriDeputados"],
            "url_documento_pauta": ["urlDocumentoPauta"],
            "url_registro": ["urlRegistro"],
        }

        super().__init__(
            endpoint="camara",
            path=["eventos", str(cod)],
            unpack_keys=["dados"],
            error_key="localCamara",
            atributos=atributos,
            verify=self.verify,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Evento {self.descricao}"

    def __str__(self) -> str:
        return self.descricao

    def deputados(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Os deputados participantes do evento.

        Retorna uma lista de dados resumidos sobre deputados participantes do
        evento. Se o evento já ocorreu, a lista identifica os deputados que
        efetivamente registraram presença no evento. Se o evento ainda não
        ocorreu, a lista mostra os deputados que devem participar do evento,
        por serem convidados ou por serem membros do(s) órgão(s) responsável
        pelo evento.

        Parameters
        ----------
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.

        index : bool, default=False
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.

        formato : {"json", "pandas", "url"}, default="pandas"
            Formato do dado que será retornado:
            - "json": Dicionário com as chaves e valores originais da API;
            - "pandas": DataFrame formatado;
            - "url": Endereço da API que retorna o arquivo JSON.

        Returns
        -------
        pandas.core.frame.DataFrame | str | dict | list[dict]
            Os deputados participantes do evento.

        """

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
            path=["eventos", str(self.cod), "deputados"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri", "partido_uri", "foto", "email"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

    def orgaos(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Lista de órgãos organizadores do evento.

        Retorna uma lista em que cada item é um conjunto mínimo de dados sobre
        o(s) órgão(s) responsável(is) pelo evento.

        Parameters
        ----------
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.

        index : bool, default=False
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.

        formato : {"json", "pandas", "url"}, default="pandas"
            Formato do dado que será retornado:
            - "json": Dicionário com as chaves e valores originais da API;
            - "pandas": DataFrame formatado;
            - "url": Endereço da API que retorna o arquivo JSON.

        Returns
        -------
        pandas.core.frame.DataFrame | str | dict | list[dict]
            Lista de órgãos organizadores do evento.

        """

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
            path=["eventos", str(self.cod), "orgaos"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri", "partido_uri", "foto", "email"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

    def pauta(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Lista de proposições que foram ou deverão ser avaliadas em um evento
        de caráter deliberativo.

        Se o evento for de caráter deliberativo (uma reunião ordinária,
        por exemplo) este serviço retorna a lista de proposições previstas
        para avaliação pelos parlamentares. Cada item identifica, se as
        informações estiverem disponíveis, a proposição avaliada, o regime
        de preferência para avaliação, o relator e seu parecer, o resultado
        da apreciação e a votação realizada.

        Parameters
        ----------
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.

        index : bool, default=False
            Se True, define a coluna `ordem` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.

        formato : {"json", "pandas", "url"}, default="pandas"
            Formato do dado que será retornado:
            - "json": Dicionário com as chaves e valores originais da API;
            - "pandas": DataFrame formatado;
            - "url": Endereço da API que retorna o arquivo JSON.

        Returns
        -------
        pandas.core.frame.DataFrame | str | dict | list[dict]
            Lista de proposições.

        """

        cols_to_rename = {
            "ordem": "ordem",
            "topico": "topico",
            "regime": "regime",
            "codRegime": "regime_codigo",
            "titulo": "titulo",
            "proposicao_": "proposicao",
            "relator": "relator",
            "textoParecer": "parecer",
            "proposicaoRelacionada_": "proposicao_relacionada",
            "uriVotacao": "uri",
            "situacaoItem": "situacao",
        }

        return Get(
            endpoint="camara",
            path=["eventos", str(self.cod), "pauta"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri"],
            remover_url=not url,
            index_col="ordem",
            index=index,
            verify=self.verify,
        ).get(formato)

    def votacoes(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Informações detalhadas de votações sobre o evento.

        Retorna uma lista de dados básicos sobre votações que tenham sido
        realizadas no evento. Votações só ocorrem em eventos de caráter
        deliberativo. Dados complementares sobre cada votação listada podem
        ser obtidos no recurso.

        Parameters
        ----------
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.

        index : bool, default=False
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.

        formato : {"json", "pandas", "url"}, default="pandas"
            Formato do dado que será retornado:
            - "json": Dicionário com as chaves e valores originais da API;
            - "pandas": DataFrame formatado;
            - "url": Endereço da API que retorna o arquivo JSON.

        Returns
        -------
        pandas.core.frame.DataFrame | str | dict | list[dict]
            Informações detalhadas de votações sobre o evento.

        """

        cols_to_rename = {
            "id": "codigo",
            "uri": "uri",
            "data": "data",
            "dataHoraRegistro": "data_registro",
            "siglaOrgao": "orgao_sigla",
            "uriOrgao": "orgao_uri",
            "uriEvento": "evento_uri",
            "proposicaoObjeto": "proposicao",
            "uriProposicaoObjeto": "proposicao_uri",
            "descricao": "descricao",
            "aprovacao": "aprovacao",
        }

        return Get(
            endpoint="camara",
            path=["eventos", str(self.cod), "votacoes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data", "data_registro"],
            url_cols=["uri", "orgao_uri", "evento_uri", "proposicao_uri"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)


@validate_call
def lista_eventos(
    tipo_evento: Optional[PositiveInt] = None,
    situacao: Optional[PositiveInt] = None,
    tipo_orgao: Optional[PositiveInt] = None,
    orgao: Optional[PositiveInt] = None,
    inicio: date = None,
    fim: date = None,
    hora_inicio: Optional[str] = None,
    hora_fim: Optional[str] = None,
    pagina: PositiveInt = 1,
    itens: Optional[PositiveInt] = None,
    asc: bool = True,
    ordenar_por: str = "dataHoraInicio",
    url: bool = True,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Lista de eventos ocorridos ou previstos nos diversos órgãos da Câmara.

    Retorna uma lista cujos elementos trazem informações básicas sobre eventos
    dos órgãos legislativos da Câmara, previstos ou já ocorridos, em um certo
    intervalo de tempo. Esse intervalo pode ser configurado pelos parâmetros
    de data e hora listados abaixo. Se nenhum for passado, são listados
    eventos dos cinco dias anteriores, dos cinco dias seguintes e do próprio
    dia em que é feita a requisição.

    Parameters
    ----------
    tipo_evento : int, optional
        Identificador numérico do tipo de evento que se deseja obter.
        Os valores válidos podem ser obtidos pela função
        `camara.referencias('tiposEvento')`.

    situacao : int, optional
        Identificador numéricos do tipo de situação de evento.
        Valores válidos podem ser obtidos pela função
        `camara.referencias('situacoesEvento')`.

    tipo_orgao : int, optional
        Identificador numérico do tipo de órgão realizador dos eventos que se
        deseja obter. Os valores válidos podem ser obtidos pela função
        `camara.referencias('tiposOrgao').

    orgao : int, optional
        Identificador numérico do órgão. Os identificadores podem ser obtidos
        pela função `camara.lista_orgaos`.

    inicio : str, optional
        Data de início de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

    fim : str, optional
        Data de término de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

    hora_inicio : str, optional
        Hora inicial de um intervalo de tempo, no formato 'HH:MM', em horário
        de Brasília.

    hora_fim : str, optional
        Hora final de um intervalo de tempo, no formato 'HH:MM', em horário
        de Brasília.

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
        Se True, define a coluna `codigo` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        Lista de eventos ocorridos ou previstos nos diversos órgãos da Câmara.

    """

    params = {
        "pagina": pagina,
        "ordem": "asc" if asc else "desc",
        "ordenarPor": ordenar_por,
    }

    if tipo_evento is not None:
        params["codTipoEvento"] = tipo_evento
    if situacao is not None:
        params["codSituacao"] = situacao
    if tipo_orgao is not None:
        params["codTipoOrgao"] = tipo_orgao
    if orgao is not None:
        params["idOrgao"] = orgao
    if inicio is not None:
        params["dataInicio"] = parse.data(inicio, "camara")
    if fim is not None:
        params["dataFim"] = parse.data(fim, "camara")
    if hora_inicio is not None:
        params["horaInicio"] = hora_inicio
    if hora_fim is not None:
        params["horaFim"] = hora_fim
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
        "orgaos": "orgaos",
        "urlRegistro": "registro",
        "localExterno": "local_externo",
        "localCamara.nome": "local_nome",
        "localCamara.predio": "local_predio",
        "localCamara.sala": "local_sala",
        "localCamara.andar": "local_andar",
    }

    data = Get(
        endpoint="camara",
        path=["eventos"],
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_date=["data_inicio", "data_fim"],
        url_cols=["uri"],
        remover_url=not url,
        index=index,
        verify=verificar_certificado,
    ).get(formato)

    if formato == "dataframe":

        def get_orgaos(orgaos):
            cod = [orgao["id"] for orgao in orgaos]
            if len(cod) < 2:
                return cod[0]
            return cod

        data["orgaos"] = data["orgaos"].apply(get_orgaos)

    return data
