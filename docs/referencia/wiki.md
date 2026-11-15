# wiki

Dados da Wikipedia em português e do Wikidata: governadores, prefeitos das capitais, ministros,
tribunais superiores, partidos, UFs e municípios.

Os arquivos vêm do repositório [DadosAbertosBrasil-wiki](https://github.com/GusFurtado/DadosAbertosBrasil-wiki),
atualizado toda semana. Cada arquivo traz a data de geração e as fontes exatas: o `revid` da
revisão de cada página da Wikipedia e a consulta SPARQL do Wikidata.

```python
from DadosAbertosBrasil import wiki

wiki.governadores(uf="SC", formato="json")
wiki.municipios(formato="pandas")       # gentílicos, fundação, coordenadas...
wiki.metadados("ministros")["gerado_em"]
```

## Licença e citação

- Dados derivados da Wikipedia: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.pt-br).
  Quem redistribui os dados, ou algo derivado deles, deve atribuir a fonte e manter a mesma licença.
- Dados do Wikidata (`ufs` e `municipios`, em parte): [CC0](https://creativecommons.org/publicdomain/zero/1.0/deed.pt-br).

Para citar, use os metadados do dataset:

```python
meta = wiki.metadados("governadores")
fonte = meta["fontes"][0]
print(f"Wikipedia, \"{fonte['titulo']}\", revisão {fonte['revid']} ({fonte['url']}), "
      f"via DadosAbertosBrasil, dados de {meta['gerado_em']}. Licença {meta['licenca']}.")
```

Os metadados também estão em `DataFrame.attrs` (pandas) e no formato `"bruto"`, que devolve o
arquivo inteiro. Polars não tem `attrs`: use `wiki.metadados`.

## Referência

::: DadosAbertosBrasil.wiki.governadores

::: DadosAbertosBrasil.wiki.prefeitos_capitais

::: DadosAbertosBrasil.wiki.ministros

::: DadosAbertosBrasil.wiki.tribunais

::: DadosAbertosBrasil.wiki.partidos

::: DadosAbertosBrasil.wiki.ufs

::: DadosAbertosBrasil.wiki.municipios

::: DadosAbertosBrasil.wiki.metadados

## Modelos

::: DadosAbertosBrasil.wiki.modelos
    options:
      show_root_heading: false
      show_root_toc_entry: false
      filters: ["!^_", "!^RegistroWiki$", "!^Regiao$", "!^SiglaUF$"]
