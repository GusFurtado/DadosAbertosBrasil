# Dados Abertos Brasil

**A forma mais simples de acessar dados abertos e APIs do governo brasileiro com Python.**

[![PyPI](https://img.shields.io/pypi/v/DadosAbertosBrasil)](https://pypi.org/project/DadosAbertosBrasil/)
[![Versões do Python](https://img.shields.io/pypi/pyversions/DadosAbertosBrasil)](https://pypi.org/project/DadosAbertosBrasil/)
[![Downloads](https://static.pepy.tech/badge/DadosAbertosBrasil/month)](https://pepy.tech/projects/DadosAbertosBrasil)
[![Licença](https://img.shields.io/pypi/l/DadosAbertosBrasil)](https://github.com/GusFurtado/DadosAbertosBrasil/blob/master/LICENSE.txt)

Dados Abertos Brasil é um pacote open-source para Python que padroniza o acesso às APIs do IBGE,
do Ipea, do Banco Central, da Câmara dos Deputados e do Senado Federal. As consultas devolvem
DataFrames do Pandas (ou do Polars), prontos para análise.

```python
import DadosAbertosBrasil as dab

dab.ipca()                                # inflação mensal
dab.ibge.populacao(projecao="populacao")  # projeção da população brasileira
dab.camara.lista_deputados(uf="SC")       # deputados federais de Santa Catarina
```

## Por onde começar

- [Instalação](instalacao.md): o pacote, o extra do Polars e a configuração global
- [Referência](referencia/ibge.md): cada módulo, com um mini-tutorial e todas as funções e classes
- [Exemplos](https://github.com/GusFurtado/dab_assets/tree/main/exemplos): notebooks com casos de uso

## Módulos

| Módulo | Fonte | Conteúdo |
|---|---|---|
| [`ibge`](referencia/ibge.md) | IBGE | Localidades, malhas, população, nomes e tabelas do SIDRA |
| [`ipea`](referencia/ipea.md) | Ipea | Séries temporais do IpeaData |
| [`bacen`](referencia/bacen.md) | Banco Central | Câmbio, expectativas de mercado e séries do SGS |
| [`camara`](referencia/camara.md) | Câmara dos Deputados | Deputados, partidos, proposições, votações e eventos |
| [`senado`](referencia/senado.md) | Senado Federal | Senadores, legislaturas, partidos e orçamentos |
| [`favoritos`](referencia/favoritos.md) | Vários | Atalhos para as consultas mais comuns (IPCA, Selic, PIB...) |
| [`uf`](referencia/uf.md) | Vários | A classe `UF`, que reúne os dados de um estado num só objeto |
