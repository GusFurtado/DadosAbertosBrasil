# ibge

Dados das APIs do Instituto Brasileiro de Geografia e Estatística (IBGE): informações geográficas,
demográficas e estatísticas.

| Serviço | Conteúdo |
|---|---|
| IBGE Cidades | Informações sobre municípios brasileiros |
| Nomes 2.0 | Frequência e ranking de nomes no Brasil |
| Agregados 3.0 (SIDRA) | Séries temporais e tabelas estatísticas |
| Malhas Geográficas 2.0 | Arquivos geoespaciais do Brasil |
| Projeções 1.0 | Projeções populacionais |
| Localidades 1.0 | Unidades territoriais |

## Mini-tutorial do SIDRA

1. Encontre a tabela desejada com `lista_tabelas`, usando `lista_pesquisas` e `referencias` para
   filtrar a busca:

    ```python
    from DadosAbertosBrasil import ibge

    ibge.lista_tabelas(...)
    pesquisas = ibge.lista_pesquisas(...)
    referencias = ibge.referencias(...)
    ```

2. Com o código numérico da tabela, consulte os metadados para ver os valores disponíveis:

    ```python
    dados = ibge.Metadados(tabela)
    dados.periodos
    dados.variaveis
    dados.localidades
    dados.classificacoes
    ```

3. Use esses valores na função `sidra`:

    ```python
    ibge.sidra(...)
    ```

## APIs oficiais

- [IBGE Cidades](https://cidades.ibge.gov.br/)
- [Serviços IBGE](https://servicodados.ibge.gov.br/api/docs)
- [SIDRA](http://api.sidra.ibge.gov.br/)

## Referência

::: DadosAbertosBrasil.ibge.Galeria

::: DadosAbertosBrasil.ibge.Historia

::: DadosAbertosBrasil.ibge.coordenadas

::: DadosAbertosBrasil.ibge.localidades

::: DadosAbertosBrasil.ibge.malha

::: DadosAbertosBrasil.ibge.populacao

::: DadosAbertosBrasil.ibge.nomes

::: DadosAbertosBrasil.ibge.nomes_ranking

::: DadosAbertosBrasil.ibge.nomes_uf

::: DadosAbertosBrasil.ibge.Metadados

::: DadosAbertosBrasil.ibge.lista_pesquisas

::: DadosAbertosBrasil.ibge.lista_tabelas

::: DadosAbertosBrasil.ibge.referencias

::: DadosAbertosBrasil.ibge.sidra
