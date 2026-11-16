"""Modelos de saída do módulo `ibge`.

Localidades e frequências de nomes têm colunas que dependem da consulta
(nível territorial, nomes pesquisados). Para elas, o modelo é criado na hora
a partir dos campos da resposta, com tipos fixos por regra (`*id` → inteiro,
o resto texto), e guardado para as próximas consultas iguais.
"""

from functools import cache
from typing import Any

from pydantic import Field, create_model

from ..utils.modelos import Inteiro, Real, Registro, Texto


class Localidade(Registro):
    """Base das localidades (`localidades`).

    Os campos aninhados da API viram colunas `<pai>_<campo>`, como `UF_id` e
    `regiao_nome`; repetidos, vale o primeiro.
    """


class FrequenciaNomes(Registro):
    """Frequência de nascimentos por década (`nomes`): `periodo` e uma coluna por nome."""

    periodo: Texto = None


class NomeUF(Registro):
    """Frequência de um nome por UF (`nomes_uf`)."""

    localidade: Inteiro = None
    populacao: Inteiro = None
    frequencia: Inteiro = None
    proporcao: Real = None


class RankingNome(Registro):
    """Posição de um nome no ranking (`nomes_ranking`)."""

    nome: Texto = None
    frequencia: Inteiro = None
    ranking: Inteiro = None


def _achatar(registro: dict, prefixo: str = "") -> dict:
    achatado = {}
    for chave, valor in registro.items():
        nome = f"{prefixo}{chave}"
        if isinstance(valor, dict):
            achatado.update(_achatar(valor, f"{nome}."))
        else:
            achatado[nome] = valor
    return achatado


def _coluna(chave: str) -> str:
    partes = chave.replace("-", "_").split(".")
    return f"{partes[-2]}_{partes[-1]}" if len(partes) > 1 else partes[0]


def preparar_localidades(dados: Any) -> list[dict]:
    """Achata as localidades com os nomes de coluna do pacote."""
    if isinstance(dados, dict):
        dados = [dados]
    linhas = []
    for registro in dados:
        linha: dict = {}
        for chave, valor in _achatar(registro).items():
            linha.setdefault(_coluna(chave), valor)
        linhas.append(linha)
    return linhas


@cache
def _modelo(base: type[Registro], nome: str, campos: tuple[tuple[str, str], ...]) -> type[Registro]:
    tipos = {"int": Inteiro, "real": Real, "texto": Texto}
    definicoes = {campo: (tipos[tipo], Field(None)) for campo, tipo in campos}
    return create_model(nome, __base__=base, **definicoes)


def modelo_localidades(linhas: list[dict]) -> type[Localidade]:
    nomes: dict[str, None] = {}
    for linha in linhas:
        nomes.update(dict.fromkeys(linha))
    campos = tuple((nome, "int" if nome.endswith("id") else "texto") for nome in nomes)
    return _modelo(Localidade, "Localidade", campos)


def modelo_nomes(nomes: list[str]) -> type[FrequenciaNomes]:
    return _modelo(FrequenciaNomes, "FrequenciaNomes", tuple((nome, "int") for nome in nomes))


class Tabela(Registro):
    """Tabela do SIDRA (`lista_tabelas`)."""

    tabela_id: Inteiro = None
    tabela_nome: Texto = None
    pesquisa_id: Texto = None
    pesquisa_nome: Texto = None


class Pesquisa(Registro):
    """Pesquisa do SIDRA (`lista_pesquisas`)."""

    pesquisa_id: Texto = None
    pesquisa_nome: Texto = None


class ReferenciaSidra(Registro):
    """Código de referência do SIDRA (`referencias`)."""

    cod: Texto = Field(None, validation_alias="id")
    referencia: Texto = Field(None, validation_alias="literal")


class ValorSidra(Registro):
    """Base dos valores do SIDRA (`sidra`).

    As colunas são as do cabeçalho da resposta, como `"Nível Territorial"` e
    `"Valor"`, todas como texto (a API usa `"..."`, `"-"` e `"X"` para valores
    ausentes ou sigilosos).
    """


def modelo_sidra(cabecalho: dict[str, str]) -> type[ValorSidra]:
    definicoes = {nome: (Texto, Field(None, validation_alias=chave)) for chave, nome in cabecalho.items()}
    return create_model("ValorSidra", __base__=ValorSidra, **definicoes)


def preparar_tabelas(dados: list[dict]) -> list[dict]:
    return [
        {
            "tabela_id": agregado["id"],
            "tabela_nome": agregado["nome"],
            "pesquisa_id": pesquisa["id"],
            "pesquisa_nome": pesquisa["nome"],
        }
        for pesquisa in dados
        for agregado in pesquisa["agregados"]
    ]
