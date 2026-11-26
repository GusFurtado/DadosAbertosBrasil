# Sobre

## Licença

O DadosAbertosBrasil é distribuído sob a
[licença MIT](https://github.com/GusFurtado/DadosAbertosBrasil/blob/master/LICENSE.txt).

## Créditos

Os dados vêm das APIs públicas do IBGE, do Ipea, do Banco Central, da Câmara dos Deputados e do
Senado Federal, e dos dados abertos da Wikipedia em português (CC BY-SA) e do Wikidata (CC0),
publicados no repositório
[DadosAbertosBrasil-wiki](https://github.com/GusFurtado/DadosAbertosBrasil-wiki). Consulte os
termos de uso de cada fonte antes de redistribuir os dados.

O pacote usa [Requests](https://requests.readthedocs.io) e
[Pydantic](https://docs.pydantic.dev/), e opcionalmente o [pandas](https://pandas.pydata.org) e o
[polars](https://pola.rs).

## Como contribuir

O projeto usa o [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/GusFurtado/DadosAbertosBrasil
cd DadosAbertosBrasil
uv sync --extra pandas --extra polars
```

Antes de abrir um pull request, rode os mesmos testes da integração contínua:

```bash
uv run pytest -m "not online"    # testes sem acesso à rede
uv run ruff check DadosAbertosBrasil tests
```

Os testes marcados como `online` consultam as APIs de verdade; eles rodam toda semana numa
workflow separada (`uv run pytest -m "online or vcr" --disable-recording`).

Esta documentação usa o [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) e o
[mkdocstrings](https://mkdocstrings.github.io/); para visualizá-la localmente, rode
`uv run --group docs mkdocs serve`.

## História

O pacote começou em abril de 2020 e chegou à versão 1.0 em dezembro de 2022. A versão 3.0, de novembro de
2026, padronizou o retorno de todas as funções, tornou o pandas opcional e trouxe o módulo `wiki`;
veja a [migração do 2.x](migracao.md). Os dados auxiliares, que antes ficavam no repositório
`dab_assets`, agora estão no
[DadosAbertosBrasil-wiki](https://github.com/GusFurtado/DadosAbertosBrasil-wiki).
