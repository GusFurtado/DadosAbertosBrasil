<p align="center">
  <a href="https://www.gustavofurtado.com/DadosAbertosBrasil/"><img src="https://www.gustavofurtado.com/assets/img/projects/dab.png" alt="Dados Abertos Brasil" width="640"></a>
</p>

<p align="center">
  <b>A forma mais simples de acessar dados abertos e APIs do governo brasileiro com Python.</b>
</p>

<p align="center">
  <a href="https://pypi.org/project/DadosAbertosBrasil/"><img src="https://img.shields.io/pypi/v/DadosAbertosBrasil" alt="PyPI"></a>
  <a href="https://pypi.org/project/DadosAbertosBrasil/"><img src="https://img.shields.io/pypi/pyversions/DadosAbertosBrasil" alt="Versões do Python"></a>
  <a href="https://pepy.tech/projects/DadosAbertosBrasil"><img src="https://static.pepy.tech/badge/DadosAbertosBrasil/month" alt="Downloads"></a>
  <a href="https://github.com/GusFurtado/DadosAbertosBrasil/actions/workflows/testes.yml"><img src="https://github.com/GusFurtado/DadosAbertosBrasil/actions/workflows/testes.yml/badge.svg" alt="Testes"></a>
  <a href="https://github.com/GusFurtado/DadosAbertosBrasil/blob/master/LICENSE.txt"><img src="https://img.shields.io/pypi/l/DadosAbertosBrasil" alt="Licença"></a>
</p>

<p align="center">
  <b><a href="https://www.gustavofurtado.com/DadosAbertosBrasil/">Documentação</a></b>
</p>

Pacote open-source que padroniza o acesso às APIs do IBGE, do Ipea, do Banco Central, da Câmara
dos Deputados e do Senado Federal, além de dados da Wikipedia e do Wikidata. As consultas devolvem
registros (`json`), modelos Pydantic ou DataFrames do pandas e do polars.

## Instalação

```sh
pip install DadosAbertosBrasil

# Para resultados em DataFrames
pip install "DadosAbertosBrasil[pandas]"   # ou [polars]
```

## Módulos

- **`ibge`**: localidades, malhas, população, nomes e tabelas do SIDRA.
- **`ipea`**: séries temporais do IpeaData.
- **`bacen`**: câmbio, expectativas de mercado e séries do SGS do Banco Central.
- **`camara`**: deputados, partidos, proposições, votações e eventos da Câmara.
- **`senado`**: senadores, legislaturas, partidos e orçamentos do Senado.
- **`favoritos`**: atalhos para as consultas mais comuns, como IPCA, Selic e PIB.
- **`wiki`**: governadores, ministros, tribunais, partidos, UFs e municípios, da Wikipedia e do Wikidata.
- **`uf`**: a classe `UF`, que reúne os dados de um estado num só objeto.

Veja a [referência](https://www.gustavofurtado.com/DadosAbertosBrasil/referencia/ibge/) de cada
módulo e os [exemplos](https://github.com/GusFurtado/DadosAbertosBrasil-wiki/tree/2.x/exemplos).
