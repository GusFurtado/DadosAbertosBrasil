from datetime import date
from typing import Any, Literal, overload

from pydantic import Field, PositiveInt, validate_call

from ..utils.errors import alias_descontinuado
from ..utils.modelos import com_params
from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars, Formato, Saida
from . import modelos as m
from ._comum import Ordenacao, Paginacao, Periodo, consultar_camara, requisicao


class _ParamsEventosOrgao(Ordenacao, Periodo):
    tipo_evento: str | None = Field(None, serialization_alias="idTipoEvento")


class _ParamsMembrosOrgao(Paginacao, Periodo):
    pass


class _ParamsVotacoesOrgao(Ordenacao, Periodo):
    proposicao: int | None = Field(None, serialization_alias="idProposicao")


class _ParamsOrgaos(Ordenacao, Periodo):
    sigla: str | None = None
    tipo: PositiveInt | None = Field(None, serialization_alias="codTipoOrgao")


class Orgao(Objeto):
    """Informações detalhadas sobre um órgão da Câmara.

    Parameters
    ----------
    cod : int
        Código numérico do órgão do qual se deseja informações.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

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

    website : str
        URL para acessar o website do órgão.

    Methods
    -------
    eventos()
        Os eventos ocorridos ou previstos em um órgão legislativo.

    membros()
        Lista de cargos de um órgão e parlamentares que os ocupam.

    votacoes()
        Uma lista de eventos com a participação do parlamentar.

    Examples
    --------
    Obter o apelido do órgão #4.
    >>> org = camara.Orgao(cod=4)
    >>> org.apelido
    ... 'Mesa Diretora'

    """

    modelo = m.OrgaoDetalhes
    chave_obrigatoria = "nome"

    def __init__(self, cod: int, verificar_certificado: bool | None = None):
        self.cod = cod
        self.verify = verificar_certificado
        self._carregar(requisicao(["orgaos", cod], verificar_certificado=verificar_certificado))

    urlWebsite = alias_descontinuado("urlWebsite", "website")

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Órgão {self.nome}"

    def __str__(self) -> str:
        return f"Órgão {self.nome}"

    @overload
    def eventos(
        self,
        tipo_evento: str | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        formato: Literal["bruto"] | None = ...,
    ) -> Any: ...

    @overload
    def eventos(
        self,
        tipo_evento: str | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...

    @overload
    def eventos(
        self,
        tipo_evento: str | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.EventoOrgao]: ...

    @overload
    def eventos(
        self,
        tipo_evento: str | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...

    @overload
    def eventos(
        self,
        tipo_evento: str | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...

    @overload
    def eventos(
        self,
        tipo_evento: str | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["url"],
    ) -> str: ...

    @com_params(_ParamsEventosOrgao)
    def eventos(
        self,
        tipo_evento: str | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: int = 1,
        itens: int | None = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
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
            Data de início de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

        fim : str, optional
            Data de término de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

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

        Returns
        -------
        list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
            Lista de discursos feitos por um deputado em eventos diversos.

        """

        return consultar_camara(
            ["orgaos", self.cod, "eventos"],
            _ParamsEventosOrgao.de_locais(locals()),
            m.EventoOrgao,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    @overload
    def membros(
        self,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        url: bool = ...,
        index: bool = ...,
        formato: Literal["bruto"] | None = ...,
    ) -> Any: ...

    @overload
    def membros(
        self,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...

    @overload
    def membros(
        self,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Membro]: ...

    @overload
    def membros(
        self,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...

    @overload
    def membros(
        self,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...

    @overload
    def membros(
        self,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["url"],
    ) -> str: ...

    @com_params(_ParamsMembrosOrgao)
    def membros(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
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
            Data de início de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

        fim : str, optional
            Data de término de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

        pagina : int, default=1
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido
            pelo parâmetro `itens`. Se omitido, assume o valor 1.

        itens : int, optional
            Número máximo de itens na “página” que se deseja obter com esta
            requisição.

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
            Lista de cargos de um órgão e parlamentares que os ocupam.

        """

        return consultar_camara(
            ["orgaos", self.cod, "membros"],
            _ParamsMembrosOrgao.de_locais(locals()),
            m.Membro,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    @overload
    def votacoes(
        self,
        proposicao: int | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        formato: Literal["bruto"] | None = ...,
    ) -> Any: ...

    @overload
    def votacoes(
        self,
        proposicao: int | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...

    @overload
    def votacoes(
        self,
        proposicao: int | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Votacao]: ...

    @overload
    def votacoes(
        self,
        proposicao: int | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...

    @overload
    def votacoes(
        self,
        proposicao: int | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...

    @overload
    def votacoes(
        self,
        proposicao: int | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        pagina: int = ...,
        itens: int | None = ...,
        asc: bool = ...,
        ordenar_por: str = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["url"],
    ) -> str: ...

    @com_params(_ParamsVotacoesOrgao)
    def votacoes(
        self,
        proposicao: int | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        pagina: int = 1,
        itens: int | None = None,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
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
            Data de início de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

        fim : str, optional
            Data de término de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

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
            Uma lista de eventos com a participação do parlamentar.

        """

        return consultar_camara(
            ["orgaos", self.cod, "votacoes"],
            _ParamsVotacoesOrgao.de_locais(locals()),
            m.Votacao,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )


@overload
def lista_orgaos(
    sigla: str | None = ...,
    tipo: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    pagina: PositiveInt = ...,
    itens: PositiveInt | None = ...,
    asc: bool = ...,
    ordenar_por: str = ...,
    url: bool = ...,
    index: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def lista_orgaos(
    sigla: str | None = ...,
    tipo: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    pagina: PositiveInt = ...,
    itens: PositiveInt | None = ...,
    asc: bool = ...,
    ordenar_por: str = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def lista_orgaos(
    sigla: str | None = ...,
    tipo: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    pagina: PositiveInt = ...,
    itens: PositiveInt | None = ...,
    asc: bool = ...,
    ordenar_por: str = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.Orgao]: ...


@overload
def lista_orgaos(
    sigla: str | None = ...,
    tipo: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    pagina: PositiveInt = ...,
    itens: PositiveInt | None = ...,
    asc: bool = ...,
    ordenar_por: str = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def lista_orgaos(
    sigla: str | None = ...,
    tipo: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    pagina: PositiveInt = ...,
    itens: PositiveInt | None = ...,
    asc: bool = ...,
    ordenar_por: str = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def lista_orgaos(
    sigla: str | None = ...,
    tipo: PositiveInt | None = ...,
    inicio: date | None = ...,
    fim: date | None = ...,
    pagina: PositiveInt = ...,
    itens: PositiveInt | None = ...,
    asc: bool = ...,
    ordenar_por: str = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsOrgaos)
def lista_orgaos(
    sigla: str | None = None,
    tipo: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
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
        Data de início, no formato `'AAAA-MM-DD'`, de um intervalo de tempo no
        qual os órgãos buscados devem ter estado em atividade.

    fim : str, optional
        Data de término, no formato `'AAAA-MM-DD'`, de um intervalo de tempo no
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
        Lista das comissões e outros órgãos legislativos da Câmara.

    """

    return consultar_camara(
        ["orgaos"],
        _ParamsOrgaos.de_locais(locals()),
        m.Orgao,
        formato,
        url=url,
        index=index,
        verificar_certificado=verificar_certificado,
    )
