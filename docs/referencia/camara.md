# camara

Deputados, partidos, frentes parlamentares, proposições, votações e outros dados legislativos da
API da Câmara dos Deputados.

## Mini-tutorial

1. Busque o código do objeto de estudo com as funções `lista_*`:

    ```python
    from DadosAbertosBrasil import camara

    camara.lista_deputados(...)
    ```

2. Instancie o objeto com o código encontrado. Os atributos trazem as informações básicas, e os
   métodos, as detalhadas:

    ```python
    dep = camara.Deputado(cod)
    dep.dados
    dep.despesas(...)
    ```

## API oficial

- [Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br/swagger/api.html)

## Referência

::: DadosAbertosBrasil.camara.Bloco

::: DadosAbertosBrasil.camara.lista_blocos

::: DadosAbertosBrasil.camara.Deputado

::: DadosAbertosBrasil.camara.lista_deputados

::: DadosAbertosBrasil.camara.Evento

::: DadosAbertosBrasil.camara.lista_eventos

::: DadosAbertosBrasil.camara.Frente

::: DadosAbertosBrasil.camara.lista_frentes

::: DadosAbertosBrasil.camara.Legislatura

::: DadosAbertosBrasil.camara.lista_legislaturas

::: DadosAbertosBrasil.camara.Orgao

::: DadosAbertosBrasil.camara.lista_orgaos

::: DadosAbertosBrasil.camara.Partido

::: DadosAbertosBrasil.camara.lista_partidos

::: DadosAbertosBrasil.camara.Proposicao

::: DadosAbertosBrasil.camara.lista_proposicoes

::: DadosAbertosBrasil.camara.referencias

::: DadosAbertosBrasil.camara.Votacao

::: DadosAbertosBrasil.camara.lista_votacoes
