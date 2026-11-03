# uf

A classe `UF` reúne num único objeto os dados de uma Unidade Federativa disponíveis no pacote:
os dados da UF e do governador vêm do módulo [`wiki`](wiki.md), e os métodos chamam as funções de
`ibge`, `camara`, `senado` e `favoritos` com a UF já preenchida.

```python
from DadosAbertosBrasil.uf import UF

sc = UF("SC")
sc.capital, sc.gentilico, sc.coordenadas
sc.governador.nome
sc.prefeito.nome          # prefeito da capital
sc.populacao              # estimativa do IBGE (SIDRA, tabela 6579)
sc.deputados(formato="pandas")
```

O Brasil (`UF("BR")`) e as UFs extintas (`"FN"` e `"GB"`) têm os atributos básicos, mas não os
métodos que dependem de dados atuais.

## Referência

::: DadosAbertosBrasil.uf.UF

::: DadosAbertosBrasil.uf.Governador
