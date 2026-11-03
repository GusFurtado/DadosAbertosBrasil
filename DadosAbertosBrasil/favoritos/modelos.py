"""Modelos de saída do módulo `favoritos`."""

from pydantic import Field

from ..utils.modelos import Bool, Data, Inteiro, Real, Registro, Texto, Url


class Catalogo(Registro):
    """Iniciativa de dados abertos (`catalogo`), com as colunas do CSV original."""

    titulo: Texto = Field(None, validation_alias="Título")
    url: Url = Field(None, validation_alias="URL")
    municipio: Texto = Field(None, validation_alias="Município")
    uf: Texto = Field(None, validation_alias="UF")
    esfera: Texto = Field(None, validation_alias="Esfera")
    poder: Texto = Field(None, validation_alias="Poder")
    solucao: Texto = Field(None, validation_alias="Solução")


class CodigoMunicipio(Registro):
    """Códigos de um município no IBGE e no TSE (`codigos_municipios`)."""

    codigo_tse: Inteiro = None
    codigo_ibge: Inteiro = None
    nome_municipio: Texto = None
    uf: Texto = None
    capital: Bool = None


class ValorIpea(Registro):
    """Valor de uma série do IPEA sem as colunas de território (`pib`, `risco_brasil`, `salario_minimo`)."""

    data: Data = Field(None, validation_alias="VALDATA")
    valor: Real = Field(None, validation_alias="VALVALOR")
