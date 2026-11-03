from datetime import date
from typing import Literal, Optional

from pydantic import Field, validate_call

from ..utils import parse
from ..utils.errors import DABInputError
from ..utils.modelos import Params, com_params, validar
from ..utils.requisicao import Requisicao
from ..utils.saida import resolver_formato, tabela
from ..utils.typing import Formato, Saida
from . import modelos as m

_COTACAO = "CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"


class _ParamsCambio(Params):
    formato_data = "'%m-%d-%Y'"

    moedas: list[str] | str = Field(exclude=True)
    inicio: date = Field(serialization_alias="@dataInicial")
    fim: date = Field(serialization_alias="@dataFinalCotacao")
    cotacao: Literal["compra", "venda"] = Field(exclude=True)
    boletim: Literal["abertura", "fechamento", "intermediário"] = Field(exclude=True)

    def da_moeda(self, moeda: str) -> dict:
        return {
            "@moeda": f"'{moeda}'",
            **self.para_api(),
            "$filter": f"contains(tipoBoletim,'{self.boletim.title()}')",
            "$select": f"cotacao{self.cotacao.title()},dataHoraCotacao",
            "$format": "json",
        }


@validate_call
@com_params(_ParamsCambio)
def cambio(
    moedas: list[str] | str = ["USD"],
    inicio: date = date(2000, 1, 1),
    fim: Optional[date] = Field(default_factory=date.today),
    cotacao: Literal["compra", "venda"] = "compra",
    boletim: Literal["abertura", "fechamento", "intermediário"] = "fechamento",
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Taxa de câmbio das principais moedas internacionais.

    É possível escolher várias moedas inserindo uma lista no campo `moeda`.
    Defina o período da consulta pelos campos `inicio` e `fim`.

    Parameters
    ----------
    moedas : str or list of str, default="USD"
        Sigla da moeda ou lista de siglas de moedas que serão pesquisadas no
        formato `"MMM"` (três letras). Utilize a função `bacen.moedas` para
        obter a lista de moedas válidas.

    inicio : date, default="2000-01-01"
        String no formato de data `"AAAA-MM-DD"` que representa o primeiro dia
        da pesquisa.

    fim : date, optional
        String no formato de data `"AAAA-MM-DD"` que representa o último dia da
        pesquisa. Caso este campo seja None, será considerada a data de hoje.

    cotacao : {"compra", "venda"}, default="compra"
        Tipo de cotação.

    boletim : {"abertura", "intermediário", "fechamento"}, default="fechamento"
        Tipo de boletim.

    index : bool, default=False
        Define se a coluna "Data" será o index do DataFrame.
        Ignorado com aviso se `formato` for 'polars'.

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
        Cotações diárias das moedas selecionadas.

    Raises
    ------
    DABDataError
        Caso seja inserida uma data inválida.

    DABMoedaError
        Caso seja inserida uma moeda inválida.

    See Also
    --------
    DadosAbertosBrasil.bacen.moedas
        Utilize a função `bacen.moedas` para identificar as moedas que serão
        usadas no argumento da função `bacen.cambio`.

    Notes
    -----
    API original das cotações de câmbio
        https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3

    Examples
    --------
    Retornar uma moeda usando argumentos padrões.

    >>> bacen.cambio(moedas="EUR")
                Data      EUR
    0    2000-01-03  1.84601
    1    2000-01-04  1.88695
    2    2000-01-05  1.91121
    3    2000-01-06  1.90357
    4    2000-01-07  1.87790
    ..          ...      ...

    Retornar várias moedas, alterando argumentos.

    >>> bacen.cambio(
    ...     moedas = ["USD", "CAD"],
    ...     inicio = "2021-01-01",
    ...     fim = "2021-01-10",
    ...     cotacao = "venda",
    ...     boletim = "abertura",
    ...     index = True
    ... )
                    USD     CAD
    Data
    2021-01-04  5.1402  4.0500
    2021-01-05  5.3405  4.1890
    2021-01-06  5.3013  4.1798
    2021-01-07  5.3174  4.1833
    2021-01-08  5.3612  4.2237

    """

    params = _ParamsCambio.de_locais(locals())
    moedas = parse.moeda(moedas)
    requisicoes = {
        moeda: Requisicao("bacen", [_COTACAO], params.da_moeda(moeda), ["value"], verificar_certificado)
        for moeda in moedas
    }

    formato = resolver_formato(formato)
    if formato == "url":
        return [r.url for r in requisicoes.values()]
    brutos = {moeda: r.bruto() for moeda, r in requisicoes.items()}
    if formato == "bruto":
        return list(brutos.values())

    # Uma linha por dia, com a última cotação do dia de cada moeda.
    campo = f"cotacao{cotacao.title()}"
    linhas: dict[str, dict] = {}
    for moeda, bruto in brutos.items():
        for item in requisicoes[moeda].desembrulhar(bruto):
            dia = item["dataHoraCotacao"][:10]
            linhas.setdefault(dia, {"data": dia})[moeda] = item.get(campo)
    if not linhas:
        raise DABInputError("Nenhum dado encontrado. Verifique os argumentos da função.")

    modelo = m.modelo_cambio(moedas)
    registros = validar(modelo, [linhas[dia] for dia in sorted(linhas)])
    return tabela(registros, modelo, formato, index=index, index_col="data")
