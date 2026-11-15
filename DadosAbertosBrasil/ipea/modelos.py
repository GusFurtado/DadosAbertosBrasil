"""Modelos de saída do módulo `ipea`."""

from typing import Annotated

from pydantic import BeforeValidator, Field

from ..utils.modelos import Bool, Data, DataHora, Inteiro, Real, Registro, Texto, Url


def _ativo(valor):
    return {"A": True, "I": False}.get(valor, valor)


Ativo = Annotated[Bool, BeforeValidator(_ativo)]
"""Situação da série: `"A"` (ativa) vira True, `"I"` (inativa) vira False."""


class ValorSerie(Registro):
    """Valor de uma série do IPEA (`serie`, `Serie.valores`)."""

    codigo: Texto = Field(None, validation_alias="SERCODIGO")
    data: Data = Field(None, validation_alias="VALDATA")
    valor: Real = Field(None, validation_alias="VALVALOR")
    nivel: Texto = Field(None, validation_alias="NIVNOME")
    territorio: Texto = Field(None, validation_alias="TERCODIGO")


class Metadados(Registro):
    """Metadados de uma série do IPEA (`lista_series`, `Serie.metadados`)."""

    codigo: Texto = Field(None, validation_alias="SERCODIGO")
    nome: Texto = Field(None, validation_alias="SERNOME")
    comentario: Texto = Field(None, validation_alias="SERCOMENTARIO")
    ultima_atualizacao: DataHora = Field(None, validation_alias="SERATUALIZACAO")
    base: Texto = Field(None, validation_alias="BASNOME")
    fonte_sigla: Texto = Field(None, validation_alias="FNTSIGLA")
    fonte_nome: Texto = Field(None, validation_alias="FNTNOME")
    fonte_url: Url = Field(None, validation_alias="FNTURL")
    periodo: Texto = Field(None, validation_alias="PERNOME")
    unidade: Texto = Field(None, validation_alias="UNINOME")
    multiplicador: Texto = Field(None, validation_alias="MULNOME")
    ativo: Ativo = Field(None, validation_alias="SERSTATUS")
    tema: Inteiro = Field(None, validation_alias="TEMCODIGO")
    codigo_pai: Texto = Field(None, validation_alias="PAICODIGO")
    numerica: Bool = Field(None, validation_alias="SERNUMERICA")


class Tema(Registro):
    """Tema (`lista_temas`)."""

    codigo: Inteiro = Field(None, validation_alias="TEMCODIGO")
    pai: Inteiro = Field(None, validation_alias="TEMCODIGO_PAI")
    nome: Texto = Field(None, validation_alias="TEMNOME")


class Pais(Registro):
    """País (`lista_paises`)."""

    codigo: Texto = Field(None, validation_alias="PAICODIGO")
    nome: Texto = Field(None, validation_alias="PAINOME")


class Territorio(Registro):
    """Território (`lista_territorios`)."""

    nivel: Texto = Field(None, validation_alias="NIVNOME")
    codigo: Texto = Field(None, validation_alias="TERCODIGO")
    nome: Texto = Field(None, validation_alias="TERNOME")
    nome_padrao: Texto = Field(None, validation_alias="TERNOMEPADRAO")
    capital: Bool = Field(None, validation_alias="TERCAPITAL")
    area: Real = Field(None, validation_alias="TERAREA")
    amc: Bool = Field(None, validation_alias="NIVAMC")
