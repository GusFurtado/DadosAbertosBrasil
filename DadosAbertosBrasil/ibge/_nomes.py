from typing import Literal, Optional

from pydantic import Field, PositiveInt, computed_field, field_validator, validate_call

from ..utils.modelos import Maiusculo, Params, com_params, validar
from ..utils.requisicao import Requisicao
from ..utils.saida import resolver_formato, tabela
from ..utils.typing import Formato, Saida
from . import modelos as m


class _ParamsNomes(Params):
    nomes: list[str] | str = Field(exclude=True)
    sexo: Literal["f", "m"] | None = None
    localidade: PositiveInt | None = None


class _ParamsNomesUF(Params):
    nome: str = Field(exclude=True)

    @computed_field
    @property
    def groupBy(self) -> str:  # noqa: N802
        return "UF"


class _ParamsRanking(Params):
    decada: PositiveInt | None = None
    sexo: Maiusculo = None
    localidade: PositiveInt | None = None

    @field_validator("decada")
    @classmethod
    def _decada(cls, decada: int | None) -> int | None:
        if decada is not None and decada % 10 != 0:
            raise ValueError("O argumento 'decada' deve ser um número inteiro múltiplo de 10.")
        return decada


def _entregar(requisicao: Requisicao, formato: str | None, montar, index_col: str) -> Saida:
    """Consulta com tabela montada por `montar(bruto) -> (modelo, linhas)`."""
    formato = resolver_formato(formato)
    if formato == "url":
        return requisicao.url
    bruto = requisicao.bruto()
    if formato == "bruto":
        return bruto
    modelo, linhas = montar(bruto)
    return tabela(validar(modelo, linhas), modelo, formato, index=formato == "pandas", index_col=index_col)


@validate_call
@com_params(_ParamsNomes)
def nomes(
    nomes: list[str] | str,
    sexo: Optional[Literal["f", "m"]] = None,
    localidade: Optional[PositiveInt] = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Obtém a frequência de nascimentos por década dos nomes consultados.

    Defina o campo `nomes` com um string ou uma lista de string.
    Use os argumentos opcionais para definir sexo e localidade dos nomes.

    Parameters
    ----------
    nomes : list or str
        Nome ou lista de nomes a ser consultado.

    sexo : {'f', 'm'}, optional
        - 'F' para consultar apenas o nome de pessoas do sexo feminino;
        - 'M' para consultar apenas o nome de pessoas do sexo masculino;
        - None para consultar ambos.

    localidade : int, optional
        Caso deseje obter a frequência referente a uma dada localidade,
        informe o parâmetro localidade. Por padrão, assume o valor BR,
        mas pode ser o identificador de um município ou de uma UF.
        Utilize a função `ibge.localidade` para encontrar a localidade
        desejada.

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
        Frequência de nascimentos por década para os nomes consultados.

    Raises
    ------
    DABLocalidadeError
        Caso o código da localidade seja inválido.

    Examples
    --------
    Forma mais simples da função.

    >>> ibge.nomes('Joao')
    nome           JOAO
    periodo
    1930[         60155
    [1930,1940[  141772
    [1940,1950[  256001
    [1950,1960[  396438
    [1960,1970[  429148
    [1970,1980[  279975
    [1980,1990[  273960
    [1990,2000[  352552
    [2000,2010[  794118

    Quantidade de nascimento de "João" no Rio de Janeiro (localidade 33)
    e do sexo masculino ('M').

    >>> ibge.nomes('Joao', sexo='M', localidade=33)
    nome          JOAO
    periodo
    1930[         3592
    [1930,1940[   9207
    [1940,1950[  16860
    [1950,1960[  25221
    [1960,1970[  25839
    [1970,1980[  15477
    [1980,1990[  16114
    [1990,2000[  26862
    [2000,2010[  68741

    """

    params = _ParamsNomes.de_locais(locals())
    if isinstance(nomes, list):
        nomes = "|".join(nomes)
    requisicao = Requisicao(
        "https://servicodados.ibge.gov.br/api/v2/",
        ["censos", "nomes", nomes],
        params.para_api(),
        verificar_certificado=verificar_certificado,
    )

    def montar(bruto):
        colunas = [item["nome"] for item in bruto]
        linhas: dict[str, dict] = {}
        for item in bruto:
            for valor in item["res"]:
                linhas.setdefault(valor["periodo"], {"periodo": valor["periodo"]})[item["nome"]] = valor["frequencia"]
        return m.modelo_nomes(colunas), list(linhas.values())

    return _entregar(requisicao, formato, montar, "periodo")


@validate_call
@com_params(_ParamsNomesUF)
def nomes_uf(
    nome: str,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Obtém a frequência de nascimentos por UF para o nome consultado.

    Parameters
    ----------
    nome : str
        Nome que se deseja pesquisar.

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
        Frequência de nascimentos do nome pesquisado, agrupado por Unidade da Federação.

    Examples
    --------
    >>> ibge.nomes_uf('Joao')

                populacao  frequencia  proporcao
    localidade
    11            1562409       23366    1495.51
    12             733559       10383    1415.43
    13            3483985       41234    1183.53
    14             450479        5664    1257.33
    ..                ...         ...        ...

    """

    requisicao = Requisicao(
        "https://servicodados.ibge.gov.br/api/v2/",
        ["censos", "nomes", nome],
        _ParamsNomesUF.de_locais(locals()).para_api(),
        verificar_certificado=verificar_certificado,
    )

    def montar(bruto):
        linhas = [{"localidade": item["localidade"], **item["res"][0]} for item in bruto]
        return m.NomeUF, sorted(linhas, key=lambda linha: int(linha["localidade"]))

    return _entregar(requisicao, formato, montar, "localidade")


@validate_call
@com_params(_ParamsRanking)
def nomes_ranking(
    decada: Optional[PositiveInt] = None,
    sexo: Optional[Literal["f", "m"]] = None,
    localidade: Optional[PositiveInt] = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Obtém o ranking dos nomes segundo a frequência de nascimentos por década.

    Parameters
    ----------
    decada : int, optional
        Deve ser um número múltiplo de 10 no formato AAAA.

    sexo : {'f', 'm'}, optional
        - 'F' para consultar apenas o nome de pessoas do sexo feminino;
        - 'M' para consultar apenas o nome de pessoas do sexo masculino;
        - None para consultar ambos.

    localidade : int, optional
        Caso deseje obter o ranking de nomes referente a uma dada localidade,
        informe o parâmetro localidade. Por padrão, assume o valor BR,
        mas pode ser o identificador de um município ou de uma UF.
        Utilize a função `ibge.localidade` para encontrar a localidade
        desejada.

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
        Nomes mais populadores dentro do universo de parâmetros pesquisados.

    Raises
    ------
    DABLocalidadeError
        Caso o código da localidade seja inválido.

    Examples
    --------
    Forma mais simples da função.

    >>> ibge.nomes_ranking()
                nome  frequencia
    ranking
    1            MARIA    11734129
    2             JOSE     5754529
    3              ANA     3089858
    4             JOAO     2984119
    ..             ...         ...

    Ranking de nomes femininos no Rio de Janeiro na decada de 1990.

    >>> ibge.nomes_ranking(decada=1990, localidade=33, sexo='F')
                nome  frequencia
    ranking
    1              ANA       44284
    2            MARIA       27944
    3            ALINE       26084
    4          VANESSA       24225
    ..             ...         ...

    """

    requisicao = Requisicao(
        "https://servicodados.ibge.gov.br/api/v2/",
        ["censos", "nomes", "ranking"],
        _ParamsRanking.de_locais(locals()).para_api(),
        verificar_certificado=verificar_certificado,
    )
    return _entregar(requisicao, formato, lambda bruto: (m.RankingNome, bruto[0]["res"]), "ranking")
