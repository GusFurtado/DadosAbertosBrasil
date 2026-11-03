"""Dados da Wikipedia em português e do Wikidata.

Lê os datasets publicados no repositório
[DadosAbertosBrasil-wiki](https://github.com/GusFurtado/DadosAbertosBrasil-wiki), atualizados toda
semana a partir da Wikipedia e do Wikidata. Cada função corresponde a um dataset.

Licença e citação
-----------------
Os dados derivados da Wikipedia seguem a licença CC BY-SA 4.0; os do Wikidata
são CC0. Ao publicar algo feito com eles, cite a Wikipedia (e o Wikidata, nos
datasets `ufs` e `municipios`) como fonte. As revisões exatas das páginas
usadas e as consultas SPARQL estão nos metadados de cada dataset
(`wiki.metadados`, `DataFrame.attrs` em pandas ou o formato "bruto").

"""

from ._datasets import (
    governadores,
    metadados,
    ministros,
    municipios,
    partidos,
    prefeitos_capitais,
    tribunais,
    ufs,
)

__all__ = [
    "governadores",
    "metadados",
    "ministros",
    "municipios",
    "partidos",
    "prefeitos_capitais",
    "tribunais",
    "ufs",
]
