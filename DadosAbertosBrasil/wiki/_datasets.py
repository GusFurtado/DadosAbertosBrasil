from collections.abc import Callable
from typing import Literal

from pydantic import Field, validate_call

from ..utils import repositorio
from ..utils.modelos import Params, Registro, SiglaUF, com_params, validar
from ..utils.saida import resolver_formato, tabela
from ..utils.typing import Formato, Saida
from . import modelos as m

Dataset = Literal["governadores", "prefeitos_capitais", "ministros", "tribunais", "partidos", "ufs", "municipios"]


def _metadados(envelope: dict) -> dict:
    return {chave: valor for chave, valor in envelope.items() if chave != "dados"}


def _consultar(
    dataset: str,
    modelo: type[Registro],
    formato: str | None,
    verificar_certificado: bool | None,
    filtro: Callable[[Registro], bool] | None = None,
) -> Saida:
    requisicao = repositorio.requisicao(f"{dataset}.json", verificar_certificado)
    formato = resolver_formato(formato)
    if formato == "url":
        return requisicao.url
    envelope = repositorio.conferir_envelope(requisicao.bruto(), dataset)
    if formato == "bruto":
        return envelope
    registros = validar(modelo, envelope["dados"])
    if filtro is not None:
        registros = [r for r in registros if filtro(r)]
    return tabela(registros, modelo, formato, metadados=_metadados(envelope))


class _ParamsUF(Params):
    uf: SiglaUF = Field(None, exclude=True)


def _filtro_uf(uf: str | None) -> Callable[[Registro], bool] | None:
    return None if uf is None else (lambda registro: registro.uf == uf)


@validate_call
def metadados(dataset: Dataset, verificar_certificado: bool | None = None) -> dict:
    """Metadados de um dataset: fontes, data de geração e licença.

    Parameters
    ----------
    dataset : str
        Nome do dataset, como o da função: `"governadores"`, `"ministros"`...

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    dict
        Envelope do arquivo sem os dados: `schema_version`, `dataset`,
        `descricao`, `licenca`, `gerado_em` e `fontes` (título, `revid` da
        revisão da Wikipedia ou a consulta SPARQL do Wikidata).

    Examples
    --------
    >>> wiki.metadados("governadores")["fontes"][0]["url"]
    'https://pt.wikipedia.org/w/index.php?oldid=73144165'

    """
    requisicao = repositorio.requisicao(f"{dataset}.json", verificar_certificado)
    return _metadados(repositorio.conferir_envelope(requisicao.bruto(), dataset))


@validate_call
@com_params(_ParamsUF)
def governadores(
    uf: str | None = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Governadores em exercício nas 27 unidades federativas.

    Fonte: *Lista de governadores das unidades federativas do Brasil*, na
    Wikipedia em português (CC BY-SA 4.0).

    Parameters
    ----------
    uf : str, optional
        Filtra por UF (nome, sigla ou código IBGE).

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": o arquivo inteiro, com o envelope de metadados;
        - "pydantic": lista de modelos Pydantic (`wiki.modelos`);
        - "pandas": DataFrame pandas, com os metadados em `DataFrame.attrs`;
        - "polars": DataFrame polars (metadados em `wiki.metadados`);
        - "url": endereço do arquivo.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[wiki.modelos.Governador] | pandas.DataFrame | polars.DataFrame | str | dict
        Um registro por UF.

    Examples
    --------
    >>> wiki.governadores(uf="SC", formato="json")[0]["nome"]

    """
    uf = _ParamsUF.de_locais(locals()).uf
    return _consultar("governadores", m.Governador, formato, verificar_certificado, _filtro_uf(uf))


@validate_call
@com_params(_ParamsUF)
def prefeitos_capitais(
    uf: str | None = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Prefeitos em exercício nas 26 capitais estaduais.

    Fonte: *Lista de prefeitos das capitais do Brasil*, na Wikipedia em
    português (CC BY-SA 4.0).

    Parameters
    ----------
    uf : str, optional
        Filtra pela UF da capital (nome, sigla ou código IBGE).

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": o arquivo inteiro, com o envelope de metadados;
        - "pydantic": lista de modelos Pydantic (`wiki.modelos`);
        - "pandas": DataFrame pandas, com os metadados em `DataFrame.attrs`;
        - "polars": DataFrame polars (metadados em `wiki.metadados`);
        - "url": endereço do arquivo.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[wiki.modelos.PrefeitoCapital] | pandas.DataFrame | polars.DataFrame | str | dict
        Um registro por capital.

    """
    uf = _ParamsUF.de_locais(locals()).uf
    return _consultar("prefeitos_capitais", m.PrefeitoCapital, formato, verificar_certificado, _filtro_uf(uf))


class _ParamsMinistros(Params):
    em_exercicio: bool | None = Field(None, exclude=True)


@validate_call
@com_params(_ParamsMinistros)
def ministros(
    em_exercicio: bool | None = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Gabinete do governo federal atual, com histórico.

    Fonte: lista de membros do gabinete do governo atual, na Wikipedia em
    português (CC BY-SA 4.0).

    Parameters
    ----------
    em_exercicio : bool, optional
        True para só os ministros em exercício; False para só os que já
        deixaram o cargo. Se omitido, retorna todos.

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": o arquivo inteiro, com o envelope de metadados;
        - "pydantic": lista de modelos Pydantic (`wiki.modelos`);
        - "pandas": DataFrame pandas, com os metadados em `DataFrame.attrs`;
        - "polars": DataFrame polars (metadados em `wiki.metadados`);
        - "url": endereço do arquivo.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[wiki.modelos.Ministro] | pandas.DataFrame | polars.DataFrame | str | dict
        Um registro por passagem de uma pessoa por um órgão.

    """
    filtro = None if em_exercicio is None else (lambda ministro: ministro.em_exercicio == em_exercicio)
    return _consultar("ministros", m.Ministro, formato, verificar_certificado, filtro)


class _ParamsTribunais(Params):
    tribunal: Literal["STF", "STJ", "TST", "STM", "TCU"] | None = Field(None, exclude=True)


@validate_call
@com_params(_ParamsTribunais)
def tribunais(
    tribunal: Literal["STF", "STJ", "TST", "STM", "TCU"] | None = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Composição atual do STF, STJ, TST, STM e TCU.

    Fonte: páginas de cada tribunal na Wikipedia em português (CC BY-SA 4.0).

    Parameters
    ----------
    tribunal : {"STF", "STJ", "TST", "STM", "TCU"}, optional
        Filtra por tribunal. Se omitido, retorna os cinco.

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": o arquivo inteiro, com o envelope de metadados;
        - "pydantic": lista de modelos Pydantic (`wiki.modelos`);
        - "pandas": DataFrame pandas, com os metadados em `DataFrame.attrs`;
        - "polars": DataFrame polars (metadados em `wiki.metadados`);
        - "url": endereço do arquivo.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[wiki.modelos.MinistroTribunal] | pandas.DataFrame | polars.DataFrame | str | dict
        Um registro por ministro em exercício.

    """
    filtro = None if tribunal is None else (lambda ministro: ministro.tribunal == tribunal)
    return _consultar("tribunais", m.MinistroTribunal, formato, verificar_certificado, filtro)


class _ParamsPartidos(Params):
    ativos: bool | None = Field(None, exclude=True)


@validate_call
@com_params(_ParamsPartidos)
def partidos(
    ativos: bool | None = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Partidos políticos em atividade e extintos desde o Império.

    Fonte: *Lista de partidos políticos do Brasil* e *Lista de partidos
    políticos brasileiros extintos*, na Wikipedia em português (CC BY-SA 4.0).

    Parameters
    ----------
    ativos : bool, optional
        True para só os partidos em atividade; False para só os extintos.
        Se omitido, retorna todos.

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": o arquivo inteiro, com o envelope de metadados;
        - "pydantic": lista de modelos Pydantic (`wiki.modelos`);
        - "pandas": DataFrame pandas, com os metadados em `DataFrame.attrs`;
        - "polars": DataFrame polars (metadados em `wiki.metadados`);
        - "url": endereço do arquivo.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[wiki.modelos.Partido] | pandas.DataFrame | polars.DataFrame | str | dict
        Um registro por partido.

    """
    filtro = None if ativos is None else (lambda partido: partido.ativo == ativos)
    return _consultar("partidos", m.Partido, formato, verificar_certificado, filtro)


@validate_call
def ufs(
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """As 27 unidades federativas: capital, área, coordenadas, gentílicos,
    lema, bandeira e brasão.

    Fonte: Wikidata (CC0), completado pela infobox de cada artigo na
    Wikipedia em português (CC BY-SA 4.0).

    Parameters
    ----------
    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": o arquivo inteiro, com o envelope de metadados;
        - "pydantic": lista de modelos Pydantic (`wiki.modelos`);
        - "pandas": DataFrame pandas, com os metadados em `DataFrame.attrs`;
        - "polars": DataFrame polars (metadados em `wiki.metadados`);
        - "url": endereço do arquivo.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[wiki.modelos.UF] | pandas.DataFrame | polars.DataFrame | str | dict
        Um registro por UF.

    """
    return _consultar("ufs", m.UF, formato, verificar_certificado)


@validate_call
@com_params(_ParamsUF)
def municipios(
    uf: str | None = None,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Os 5.570 municípios: gentílicos, fundação, aniversário, lema e coordenadas.

    Fonte: Wikidata (CC0), completado pela infobox de cada artigo na
    Wikipedia em português (CC BY-SA 4.0). As coordenadas são as do Wikidata
    (P625), um ponto por município.

    Parameters
    ----------
    uf : str, optional
        Filtra por UF (nome, sigla ou código IBGE).

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": o arquivo inteiro, com o envelope de metadados;
        - "pydantic": lista de modelos Pydantic (`wiki.modelos`);
        - "pandas": DataFrame pandas, com os metadados em `DataFrame.attrs`;
        - "polars": DataFrame polars (metadados em `wiki.metadados`);
        - "url": endereço do arquivo.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[wiki.modelos.Municipio] | pandas.DataFrame | polars.DataFrame | str | dict
        Um registro por município.

    """
    uf = _ParamsUF.de_locais(locals()).uf
    return _consultar("municipios", m.Municipio, formato, verificar_certificado, _filtro_uf(uf))
