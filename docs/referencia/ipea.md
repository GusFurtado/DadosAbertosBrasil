# ipea

Séries temporais de indicadores econômicos, sociais e demográficos do Instituto de Pesquisa
Econômica Aplicada (Ipea).

## Mini-tutorial

1. Busque o código da série com `lista_series`, filtrando por temas, países ou níveis territoriais:

    ```python
    from DadosAbertosBrasil import ipea

    ipea.lista_series(...)
    temas = ipea.lista_temas(...)
    paises = ipea.lista_paises(...)
    territorios = ipea.lista_territorios(...)
    niveis = ipea.lista_niveis(...)
    ```

2. Instancie um objeto `Serie` com o código encontrado e acesse valores e metadados:

    ```python
    serie = ipea.Serie(cod)
    serie.metadados
    serie.valores
    ```

3. Se precisar apenas dos valores, sem os metadados, a função `serie` é mais simples e rápida:

    ```python
    ipea.serie(cod)
    ```

## API oficial

- [IpeaData](http://www.ipeadata.gov.br/api/)

## Referência

::: DadosAbertosBrasil.ipea.lista_niveis

::: DadosAbertosBrasil.ipea.lista_paises

::: DadosAbertosBrasil.ipea.lista_temas

::: DadosAbertosBrasil.ipea.lista_territorios

::: DadosAbertosBrasil.ipea.Serie

::: DadosAbertosBrasil.ipea.lista_series

::: DadosAbertosBrasil.ipea.serie
