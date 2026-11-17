from datetime import date

from pydantic import PositiveInt, validate_call

from ..utils.modelos import com_params
from ..utils.objeto import Objeto
from ..utils.typing import Formato, Saida
from . import modelos as m
from ._comum import Ordenacao, Periodo, consultar_camara, requisicao


class _ParamsMesa(Periodo):
    pass


class _ParamsLegislaturas(Ordenacao):
    data: date | None = None


class Legislatura(Objeto):
    """Informações extras sobre uma determinada legislatura da Câmara.

    Parameters
    ----------
    cod : int
        Código numérico da legislatura da qual se deseja informações.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.

    cod : int
        Código numérico da legislatura.

    inicio : str
        Primeiro dia da legislatura.

    fim : str
        Último dia da legislatura.

    uri : str
        Endereço para coleta de dados direta pela API da legislatura.

    Methods
    -------
    mesa()
        Quais deputados fizeram parte da Mesa Diretora em uma legislatura.

    Examples
    --------
    Obter o primeiro e último dia da legislatura #56.
    >>> leg = camara.Legislatura(cod=54)
    >>> leg.inicio
    ... '2011-02-01'
    >>> leg.fim
    ... '2015-01-31'

    """

    modelo = m.LegislaturaDetalhes
    chave_obrigatoria = "dataInicio"

    def __init__(self, cod: int, verificar_certificado: bool | None = None):
        self.cod = cod
        self.verify = verificar_certificado
        self._carregar(requisicao(["legislaturas", cod], verificar_certificado=verificar_certificado))

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Legislatura {self.cod}"

    def __str__(self) -> str:
        return f"Legislatura {self.cod}"

    @com_params(_ParamsMesa)
    def mesa(
        self,
        inicio: date | None = None,
        fim: date | None = None,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Quais deputados fizeram parte da Mesa Diretora em uma legislatura.

        Retorna uma lista com dados básicos sobre todos os deputados que
        ocuparam algum posto na Mesa Diretora da Câmara em algum período de
        tempo dentro da legislatura. Normalmente, cada legislatura tem duas
        Mesas Diretoras, com presidente, dois vice-presidentes, quatro
        secretários parlamentares e os suplentes dos secretários.

        Parameters
        ----------
        inicio : str, optional
            Dia de início do intervalo de tempo do qual se deseja saber a
            composição da Mesa, no formato `'AAAA-MM-DD'`.

        fim : str, optional
            Data de término do intervalo de tempo do qual se deseja saber a
            composição da Mesa, no formato `'AAAA-MM-DD'`.

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
            Quais deputados fizeram parte da Mesa Diretora em uma legislatura.

        """

        return consultar_camara(
            ["legislaturas", self.cod, "mesa"],
            _ParamsMesa.de_locais(locals()),
            m.Membro,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )


@validate_call
@com_params(_ParamsLegislaturas)
def lista_legislaturas(
    data: date | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = False,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Os períodos de mandatos e atividades parlamentares da Câmara.

    Legislatura é o nome dado ao período de trabalhos parlamentares entre uma
    eleição e outra. Esta função retorna uma lista em que cada item contém as
    informações básicas sobre um desses períodos. Os números que identificam
    as legislaturas são sequenciais, desde a primeira que ocorreu.

    Parameters
    ----------
    data : str, optional
        Data no formato `'AAAA-MM-DD'`. Se este parâmetro estiver presente, a
        função retornará as informações básicas sobre a legislatura que estava
        em curso na data informada.

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
        Os períodos de mandatos e atividades parlamentares da Câmara.

    """

    return consultar_camara(
        ["legislaturas"],
        _ParamsLegislaturas.de_locais(locals()),
        m.Legislatura,
        formato,
        url=url,
        index=index,
        verificar_certificado=verificar_certificado,
    )
