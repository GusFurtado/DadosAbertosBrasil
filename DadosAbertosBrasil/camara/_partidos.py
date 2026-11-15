from datetime import date
from typing import Any, Literal, overload

from pydantic import Field, PositiveInt, validate_call

from ..utils.modelos import com_params
from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars, Formato, Saida
from . import modelos as m
from ._comum import Ordenacao, Periodo, consultar_camara, requisicao


class _ParamsMembrosPartido(Ordenacao, Periodo):
    legislatura: PositiveInt | None = Field(None, serialization_alias="idLegislatura")


class _ParamsPartidos(Ordenacao, Periodo):
    legislatura: PositiveInt | None = Field(None, serialization_alias="idLegislatura")


class Partido(Objeto):
    """Informações detalhadas sobre um partido.

    Parameters
    ----------
    cod : int
        Código numérico do partido do qual se deseja informações.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

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

    Methods
    -------
    membros()
        Uma lista dos parlamentares de um partido durante um período.

    Examples
    --------
    Obter o nome completo do partido #36899.
    >>> p = camara.Partido(cod=36899)
    >>> p.nome
    ... 'Movimento Democrático Brasileiro'

    """

    modelo = m.PartidoDetalhes
    chave_obrigatoria = "status"

    def __init__(self, cod: int, verificar_certificado: bool | None = None):
        self.cod = cod
        self.verify = verificar_certificado
        self._carregar(requisicao(["partidos", cod], verificar_certificado=verificar_certificado))

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: {self.nome}"

    def __str__(self) -> str:
        return self.nome

    @overload
    def membros(
        self,
        inicio: date | None = ...,
        fim: date | None = ...,
        legislatura: PositiveInt | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        ordenar_por: str | None = ...,
        asc: bool = ...,
        url: bool = ...,
        index: bool = ...,
        formato: Literal["bruto"] | None = ...,
    ) -> Any: ...

    @overload
    def membros(
        self,
        inicio: date | None = ...,
        fim: date | None = ...,
        legislatura: PositiveInt | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        ordenar_por: str | None = ...,
        asc: bool = ...,
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
        legislatura: PositiveInt | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        ordenar_por: str | None = ...,
        asc: bool = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Deputado]: ...

    @overload
    def membros(
        self,
        inicio: date | None = ...,
        fim: date | None = ...,
        legislatura: PositiveInt | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        ordenar_por: str | None = ...,
        asc: bool = ...,
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
        legislatura: PositiveInt | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        ordenar_por: str | None = ...,
        asc: bool = ...,
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
        legislatura: PositiveInt | None = ...,
        pagina: PositiveInt = ...,
        itens: PositiveInt | None = ...,
        ordenar_por: str | None = ...,
        asc: bool = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["url"],
    ) -> str: ...

    @com_params(_ParamsMembrosPartido)
    def membros(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        legislatura: PositiveInt | None = None,
        pagina: PositiveInt = 1,
        itens: PositiveInt | None = None,
        ordenar_por: str | None = None,
        asc: bool = True,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
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
            Data de início de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

        fim : str, optional
            Data de término de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

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
            Lista dos parlamentares de um partido durante um período.

        """

        return consultar_camara(
            ["partidos", self.cod, "membros"],
            _ParamsMembrosPartido.de_locais(locals()),
            m.Deputado,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )


@overload
def lista_partidos(
    legislatura: PositiveInt | None = ...,
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
def lista_partidos(
    legislatura: PositiveInt | None = ...,
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
def lista_partidos(
    legislatura: PositiveInt | None = ...,
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
) -> list[m.Partido]: ...


@overload
def lista_partidos(
    legislatura: PositiveInt | None = ...,
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
def lista_partidos(
    legislatura: PositiveInt | None = ...,
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
def lista_partidos(
    legislatura: PositiveInt | None = ...,
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
@com_params(_ParamsPartidos)
def lista_partidos(
    legislatura: PositiveInt | None = None,
    inicio: date | None = None,
    fim: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "sigla",
    url: bool = True,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
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

    ordenar_por : str, default='sigla'
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
        Os partidos políticos que têm ou já tiveram parlamentares em exercício
        na Câmara.

    """

    return consultar_camara(
        ["partidos"],
        _ParamsPartidos.de_locais(locals()),
        m.Partido,
        formato,
        url=url,
        index=index,
        verificar_certificado=verificar_certificado,
    )
