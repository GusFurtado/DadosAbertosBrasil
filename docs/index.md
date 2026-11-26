<p align="center">
  <img class="hero" src="https://www.gustavofurtado.com/assets/img/projects/dab.png" alt="Dados Abertos Brasil" width="100%">
</p>

**A forma mais simples de acessar dados abertos e APIs do governo brasileiro com Python.**

Dados Abertos Brasil é um pacote open-source para Python que padroniza o acesso às APIs do IBGE,
do Ipea, do Banco Central, da Câmara dos Deputados e do Senado Federal, além de dados da Wikipedia e
do Wikidata. As consultas devolvem registros, modelos Pydantic ou DataFrames do pandas e do polars.

[![PyPI](https://img.shields.io/pypi/v/DadosAbertosBrasil)](https://pypi.org/project/DadosAbertosBrasil/)
[![Versões do Python](https://img.shields.io/pypi/pyversions/DadosAbertosBrasil)](https://pypi.org/project/DadosAbertosBrasil/)
[![Downloads](https://static.pepy.tech/badge/DadosAbertosBrasil/month)](https://pepy.tech/projects/DadosAbertosBrasil)
[![Testes](https://github.com/GusFurtado/DadosAbertosBrasil/actions/workflows/testes.yml/badge.svg)](https://github.com/GusFurtado/DadosAbertosBrasil/actions/workflows/testes.yml)
[![Licença](https://img.shields.io/pypi/l/DadosAbertosBrasil)](sobre.md#licenca)

## Recursos

- **Várias fontes, uma interface**: IBGE, Ipea, Banco Central, Câmara dos Deputados, Senado
  Federal, Wikipedia e Wikidata, com funções que seguem as mesmas convenções.
- **O formato que você preferir**: registros, modelos Pydantic, DataFrames do pandas ou do polars,
  ou o JSON original da API, escolhido em cada função ou para o pacote inteiro.
- **Atalhos para as consultas mais comuns**: IPCA, Selic, PIB e outras séries num só comando.
- **Um estado num só objeto**: a classe `UF` reúne os dados de uma unidade da federação.
- **Dados da Wikipedia com fonte**: cada arquivo traz a data de geração, a revisão de cada página
  e a consulta ao Wikidata.
- **Leve**: pandas e polars são extras opcionais.

## Exemplo

```python
import DadosAbertosBrasil as dab

dab.config.formato = "pandas"        # ou "polars", "json", "pydantic"

dab.ipca()                           # inflação mensal
dab.ibge.localidades("estados")      # as 27 UFs
dab.camara.lista_deputados(uf="SC")  # deputados federais de Santa Catarina
dab.wiki.governadores()              # governadores em exercício
```

## Por onde começar

- [Instalação](instalacao.md): o pacote, o extra do Polars e a configuração global
- [Migração do 2.x](migracao.md): o que muda na versão 3.0 e como adaptar o seu código
- [Referência](referencia/ibge.md): cada módulo, com um mini-tutorial e todas as funções e classes
- [Exemplos](https://github.com/GusFurtado/DadosAbertosBrasil-wiki/tree/2.x/exemplos): notebooks com casos de uso
- [Sobre](sobre.md): licença, créditos, como contribuir e a história do projeto

## Módulos

| Módulo | Fonte | Conteúdo |
|---|---|---|
| [`ibge`](referencia/ibge.md) | IBGE | Localidades, malhas, população, nomes e tabelas do SIDRA |
| [`ipea`](referencia/ipea.md) | Ipea | Séries temporais do IpeaData |
| [`bacen`](referencia/bacen.md) | Banco Central | Câmbio, expectativas de mercado e séries do SGS |
| [`camara`](referencia/camara.md) | Câmara dos Deputados | Deputados, partidos, proposições, votações e eventos |
| [`senado`](referencia/senado.md) | Senado Federal | Senadores, legislaturas, partidos e orçamentos |
| [`wiki`](referencia/wiki.md) | Wikipedia e Wikidata | Governadores, ministros, tribunais, partidos, UFs e municípios |
| [`favoritos`](referencia/favoritos.md) | Vários | Atalhos para as consultas mais comuns (IPCA, Selic, PIB...) |
| [`uf`](referencia/uf.md) | Vários | A classe `UF`, que reúne os dados de um estado num só objeto |
