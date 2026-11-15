# Configuração e erros

## Configuração global

O objeto `config` guarda as configurações que valem para todas as funções do pacote. Argumentos
passados diretamente às funções têm precedência sobre ele.

```python
import DadosAbertosBrasil as dab

dab.config.formato = "polars"
dab.config.verificar_certificado = False
```

::: DadosAbertosBrasil._config.Config
    options:
      show_root_full_path: false

## Erros

As exceções do pacote podem ser importadas direto de `DadosAbertosBrasil`, como
`from DadosAbertosBrasil import DABUFError`. Todas herdam de `DABError`.

Na versão 2.3, as exceções ganharam nomes no padrão do PEP 8. Os nomes antigos (`DAB_UFError`,
`DAB_InputError` etc.) continuam funcionando, com `DeprecationWarning`, e deixam de existir em uma
versão futura do 3.x.

::: DadosAbertosBrasil.utils.errors
    options:
      show_root_heading: false
      show_root_toc_entry: false
      members:
        - DABError
        - DABDataError
        - DABInputError
        - DABLocalidadeError
        - DABMoedaError
        - DABUFError
        - DABFuncaoRemovidaError
        - DABValidacaoWarning
        - DABFormatoWarning
