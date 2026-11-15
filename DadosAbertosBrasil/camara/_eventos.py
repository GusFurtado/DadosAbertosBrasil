from datetime import date
from typing import Optional

from pydantic import Field, PositiveInt, validate_call

from ..utils.modelos import com_params
from ..utils.objeto import Objeto
from ..utils.typing import Formato, Saida
from . import modelos as m
from ._comum import Ordenacao, Periodo, consultar_camara, requisicao


class _ParamsEventos(Ordenacao, Periodo):
    tipo_evento: PositiveInt | None = Field(None, serialization_alias="codTipoEvento")
    situacao: PositiveInt | None = Field(None, serialization_alias="codSituacao")
    tipo_orgao: PositiveInt | None = Field(None, serialization_alias="codTipoOrgao")
    orgao: PositiveInt | None = Field(None, serialization_alias="idOrgao")
    hora_inicio: str | None = Field(None, serialization_alias="horaInicio")
    hora_fim: str | None = Field(None, serialization_alias="horaFim")


class Evento(Objeto):
    """Retorna um conjunto detalhado de informações sobre o evento da Câmara.

    Parameters
    ----------
    cod : int
        Código numérico do evento do qual se deseja informações.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

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

    modelo = m.EventoDetalhes
    chave_obrigatoria = "localCamara"

    def __init__(self, cod: int, verificar_certificado: bool | None = None):
        self.cod = cod
        self.verify = verificar_certificado
        self._carregar(requisicao(["eventos", cod], verificar_certificado=verificar_certificado))

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Evento {self.descricao}"

    def __str__(self) -> str:
        return self.descricao

    def deputados(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Os deputados participantes do evento.

        Retorna uma lista de dados resumidos sobre deputados participantes do
        evento. Se o evento já ocorreu, a lista identifica os deputados que
        efetivamente registraram presença no evento. Se o evento ainda não
        ocorreu, a lista mostra os deputados que devem participar do evento,
        por serem convidados ou por serem membros do(s) órgão(s) responsável
        pelo evento.

        Parameters
        ----------
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

        Returns
        -------
        list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
            Os deputados participantes do evento.

        """

        return consultar_camara(
            ["eventos", self.cod, "deputados"],
            None,
            m.Deputado,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    def orgaos(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Lista de órgãos organizadores do evento.

        Retorna uma lista em que cada item é um conjunto mínimo de dados sobre
        o(s) órgão(s) responsável(is) pelo evento.

        Parameters
        ----------
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

        Returns
        -------
        list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
            Lista de órgãos organizadores do evento.

        """

        return consultar_camara(
            ["eventos", self.cod, "orgaos"],
            None,
            m.Orgao,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    def pauta(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
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
        url : bool, default=True
            Se False, remove as colunas contendo URI, URL e e-mails.
            Vale para os formatos 'json', 'pandas' e 'polars'.

        index : bool, default=False
            Se True, define a coluna `ordem` como index do DataFrame.
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

        Returns
        -------
        list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
            Lista de proposições.

        """

        return consultar_camara(
            ["eventos", self.cod, "pauta"],
            None,
            m.ItemPauta,
            formato,
            url=url,
            index=index,
            index_col="ordem",
            verificar_certificado=self.verify,
        )

    def votacoes(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Informações detalhadas de votações sobre o evento.

        Retorna uma lista de dados básicos sobre votações que tenham sido
        realizadas no evento. Votações só ocorrem em eventos de caráter
        deliberativo. Dados complementares sobre cada votação listada podem
        ser obtidos no recurso.

        Parameters
        ----------
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

        Returns
        -------
        list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
            Informações detalhadas de votações sobre o evento.

        """

        return consultar_camara(
            ["eventos", self.cod, "votacoes"],
            None,
            m.VotacaoEvento,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )


@validate_call
@com_params(_ParamsEventos)
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
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
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
        Lista de eventos ocorridos ou previstos nos diversos órgãos da Câmara.

    """

    return consultar_camara(
        ["eventos"],
        _ParamsEventos.de_locais(locals()),
        m.Evento,
        formato,
        url=url,
        index=index,
        verificar_certificado=verificar_certificado,
    )
