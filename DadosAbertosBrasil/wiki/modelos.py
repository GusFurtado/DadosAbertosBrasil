"""Modelos de saída do módulo `wiki`.

Espelham os modelos do repositório de dados (`dab_wiki`). Como o formato é
nosso e versionado (`schema_version`), a validação é estrita: um valor fora
do modelo levanta erro em vez de aviso. Campos novos são ignorados, para que
o repositório possa ganhar campos sem quebrar versões instaladas.

"""

from datetime import date
from typing import Literal

from pydantic import ConfigDict, Field

from ..utils.modelos import Registro

Regiao = Literal["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
SiglaUF = Literal[
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA", "MG", "MS", "MT", "PA",
    "PB", "PE", "PI", "PR", "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO",
]  # fmt: skip

_ARTIGO = "Título do artigo na Wikipedia em português, quando existe."


class RegistroWiki(Registro):
    model_config = ConfigDict(extra="ignore", populate_by_name=True, strict=False)
    tolerante = False


class Governador(RegistroWiki):
    """Governador em exercício (`governadores`)."""

    uf: SiglaUF
    nome: str
    artigo: str | None = Field(description=_ARTIGO)
    interino: bool
    partido: str | None
    partido_sigla: str | None
    mandato_inicio: date
    mandato_fim: date | None = Field(description="Fim previsto do mandato.")
    ano_eleicao: int | None
    vice_governador: str | None


class PrefeitoCapital(RegistroWiki):
    """Prefeito em exercício de uma capital (`prefeitos_capitais`)."""

    uf: SiglaUF
    capital: str
    capital_artigo: str | None
    nome: str
    artigo: str | None = Field(description=_ARTIGO)
    partido: str | None
    partido_sigla: str | None
    vice_prefeito: str | None
    mandato_inicio: date | None
    mandato_fim: date | None


class Ministro(RegistroWiki):
    """Membro do gabinete do governo federal atual, com histórico (`ministros`)."""

    governo: str
    orgao: str
    orgao_artigo: str | None
    tipo: Literal["Ministério", "Órgão com status de ministério", "Secretaria com status de ministério"]
    nome: str
    artigo: str | None = Field(description=_ARTIGO)
    interino: bool
    partido_sigla: str | None
    uf_origem: SiglaUF | None
    posse: date
    saida: date | None
    em_exercicio: bool


class MinistroTribunal(RegistroWiki):
    """Ministro de STF, STJ, TST, STM ou TCU em exercício (`tribunais`)."""

    tribunal: Literal["STF", "STJ", "TST", "STM", "TCU"]
    nome: str
    artigo: str | None = Field(description=_ARTIGO)
    posse: date | None
    ano_aposentadoria_compulsoria: int | None
    indicado_por: str | None
    vaga: str | None
    uf_origem: SiglaUF | None


class Partido(RegistroWiki):
    """Partido político, em atividade ou extinto desde o Império (`partidos`)."""

    nome: str
    artigo: str | None = Field(description=_ARTIGO)
    sigla: str | None
    numero: int | None = Field(description="Número eleitoral.")
    ativo: bool
    periodo: str = Field(description="Período histórico do partido (ex.: Nova República).")
    ano_fundacao: int | None
    data_criacao: date | None
    data_registro: date | None
    ano_extincao: int | None
    situacao: str | None


class UF(RegistroWiki):
    """Unidade federativa (`ufs`)."""

    sigla: SiglaUF
    codigo_ibge: int
    nome: str
    regiao: Regiao
    wikidata: str = Field(description="Identificador do item no Wikidata (Q...).")
    artigo: str | None = Field(description=_ARTIGO)
    capital: str
    area_km2: float
    latitude: float
    longitude: float
    gentilicos: list[str]
    lema: str | None
    bandeira: str | None = Field(description="Nome do arquivo da bandeira no Wikimedia Commons.")
    brasao: str | None = Field(description="Nome do arquivo do brasão no Wikimedia Commons.")


class Municipio(RegistroWiki):
    """Município (`municipios`)."""

    codigo_ibge: int
    nome: str
    uf: SiglaUF
    regiao: Regiao
    wikidata: str = Field(description="Identificador do item no Wikidata (Q...).")
    artigo: str | None = Field(description=_ARTIGO)
    gentilicos: list[str]
    fundacao: date | None = Field(description="Data de fundação, quando conhecida até o dia.")
    ano_fundacao: int | None
    aniversario_dia: int | None
    aniversario_mes: int | None
    lema: str | None
    latitude: float | None = None
    longitude: float | None = None
