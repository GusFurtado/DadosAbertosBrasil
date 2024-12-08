from datetime import date
from typing import Literal, Optional

import pandas as pd
from pydantic import validate_call, PositiveInt

from .._utils import parse
from .._utils.get_data import DAB_Base, get_and_format


class Legislatura(DAB_Base):
    """Informações extras sobre uma determinada legislatura da Câmara.

    Parameters
    ----------
    cod : int
        Código numérico da legislatura da qual se deseja informações.

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

    Examples
    --------
    Obter o primeiro e último dia da legislatura #56.
    >>> leg = camara.Legislatura(cod=54)
    >>> leg.inicio
    ... '2011-02-01'
    >>> leg.fim
    ... '2015-01-31'

    """

    def __init__(self, cod: int):
        self.cod = cod
        atributos = {"fim": ["dataFim"], "inicio": ["dataInicio"], "uri": ["uri"]}

        super().__init__(
            api="camara",
            path=["legislaturas", str(cod)],
            unpack_keys=["dados"],
            error_key="dataInicio",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Legislatura {self.cod}"

    def __str__(self) -> str:
        return f"Legislatura {self.cod}"

    def mesa(
        self,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        url: bool = True,
        index: bool = False,
        formato: Literal["dataframe", "json"] = "dataframe",
    ) -> dict | pd.DataFrame:
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
            composição da Mesa, no formato 'AAAA-MM-DD'.
        fim : str, optional
            Data de término do intervalo de tempo do qual se deseja saber a
            composição da Mesa, no formato 'AAAA-MM-DD'.
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

        params = {}
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")

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

        return get_and_format(
            api="camara",
            path=["legislaturas", self.cod, "mesa"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["titulo_codigo"],
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "partido_uri", "foto", "email"],
            url=url,
            index=index,
            formato=formato,
        )


@validate_call
def lista_legislaturas(
    data: Optional[date] = None,
    pagina: PositiveInt = 1,
    itens: Optional[PositiveInt] = None,
    asc: bool = False,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    formato: Literal["dataframe", "json"] = "dataframe",
) -> dict | pd.DataFrame:
    """Os períodos de mandatos e atividades parlamentares da Câmara.

    Legislatura é o nome dado ao período de trabalhos parlamentares entre uma
    eleição e outra. Esta função retorna uma lista em que cada item contém as
    informações básicas sobre um desses períodos. Os números que identificam
    as legislaturas são sequenciais, desde a primeira que ocorreu.

    Parameters
    ----------
    data : str, optional
        Data no formato 'AAAA-MM-DD'. Se este parâmetro estiver presente, a
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
    if data is not None:
        params["data"] = data
    if itens is not None:
        params["itens"] = itens

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "dataInicio": "data_inicio",
        "dataFim": "data_fim",
    }

    return get_and_format(
        api="camara",
        path="legislaturas",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_date=["data_inicio", "data_fim"],
        url_cols=["uri"],
        url=url,
        index=index,
        formato=formato,
    )
