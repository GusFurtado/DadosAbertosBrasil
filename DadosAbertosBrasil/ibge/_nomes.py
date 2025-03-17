from typing import Literal, Optional

import pandas as pd
from pydantic import validate_call, PositiveInt
import requests

from ..utils import parse, Formato, Output


@validate_call
def nomes(
    nomes: list[str] | str,
    sexo: Optional[Literal["f", "m"]] = None,
    localidade: Optional[PositiveInt] = None,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
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
        Frequência de nascimentos por década para os nomes consultados.

    Raises
    ------
    DAB_LocalidadeError
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

    if isinstance(nomes, list):
        nomes = "|".join(nomes)

    params = {}
    if sexo is not None:
        params["sexo"] = sexo
    if localidade is not None:
        params["localidade"] = parse.localidade(localidade)

    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nomes}"
    if formato == "url":
        return url

    data = requests.get(url, params=params, verify=verificar_certificado).json()
    if formato == "json":
        return data

    json = pd.DataFrame(data)
    dfs = [pd.DataFrame(json.res[i]).set_index("periodo") for i in json.index]
    df = pd.concat(dfs, axis=1)
    df.columns = json.nome

    return df


@validate_call
def nomes_uf(
    nome: str,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Obtém a frequência de nascimentos por UF para o nome consultado.

    Parameters
    ----------
    nome : str
        Nome que se deseja pesquisar.

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

    if formato == "json":
        raise NotImplementedError(
            "Formato `json` temporariamente indisponível. Escolha formato `url` ou `pandas`."
        )

    url = f"https://servicodados.ibge.gov.br/api/v2/censos/nomes/{nome}?groupBy=UF"
    if formato == "url":
        return url

    json = pd.read_json(url)
    df = pd.DataFrame(
        [json[json.localidade == i].res.values[0][0] for i in json.localidade]
    )

    df.index = json.localidade
    df.sort_index(inplace=True)

    return df


@validate_call
def nomes_ranking(
    decada: Optional[PositiveInt] = None,
    sexo: Optional[Literal["f", "m"]] = None,
    localidade: Optional[PositiveInt] = None,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
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
        Nomes mais populadores dentro do universo de parâmetros pesquisados.

    Raises
    ------
    DAB_LocalidadeError
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

    query = "https://servicodados.ibge.gov.br/api/v2/censos/nomes/ranking"
    params = []

    if decada is not None:
        decada_error = "O argumento 'decada' deve ser um número inteiro multiplo de 10."
        if isinstance(decada, int):
            if decada % 10 == 0:
                params.append(f"decada={decada}")
            else:
                raise ValueError(decada_error)
        else:
            raise TypeError(decada_error)

    if localidade is not None:
        params.append(f"localidade={parse.localidade(localidade)}")

    if sexo is not None:
        if sexo in ["M", "m", "F", "f"]:
            params.append(f"sexo={sexo.upper()}")
        else:
            raise ValueError(
                "O argumento 'sexo' deve ser um tipo 'string' igual a 'M' para masculino ou 'F' para feminino."
            )

    params = "&".join(params)
    if params != "":
        query += f"?{params}"

    match formato:
        case "url":
            return query
        case "json":
            raise NotImplementedError(
                "Formato `json` temporariamente indisponível. Escolha formato `url` ou `pandas`."
            )
        case "pandas":
            return pd.DataFrame(pd.read_json(query).res[0]).set_index("ranking")
