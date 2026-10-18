# senado

Senadores, legislaturas, partidos, orçamentos e outros dados legislativos do Senado Federal.

## Mini-tutorial

1. Use as funções `lista_*` para obter os códigos necessários:

    ```python
    from DadosAbertosBrasil import senado

    senado.lista_senadores(...)
    senado.lista_legislatura(...)
    ```

2. Instancie um objeto `Senador` e use os métodos da classe para obter mais detalhes:

    ```python
    sen = senado.Senador(cod)
    sen.cargos(...)
    sen.votacoes(...)
    ```

## API oficial

- [Dados Abertos do Senado](http://legis.senado.gov.br/dadosabertos/docs/)

## Referência

::: DadosAbertosBrasil.senado.lista_blocos

::: DadosAbertosBrasil.senado.lista_legislatura

::: DadosAbertosBrasil.senado.lista_orcamentos

::: DadosAbertosBrasil.senado.lista_partidos

::: DadosAbertosBrasil.senado.Senador

::: DadosAbertosBrasil.senado.lista_senadores

::: DadosAbertosBrasil.senado.lista_uso_palavra
