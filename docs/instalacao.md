# Instalação

```bash
pip install DadosAbertosBrasil
```

Requer Python 3.11 ou superior. A instalação básica traz só [Pydantic](https://docs.pydantic.dev/latest/)
e [Requests](https://requests.readthedocs.io/), sem nenhuma biblioteca de DataFrame.

## Formatos e DataFrames

Sem o argumento `formato`, as funções retornam `"json"`: uma lista de registros (dicionários), com os
mesmos campos e tipos das colunas dos DataFrames. Para receber DataFrames, instale o extra da biblioteca
que você usa:

```bash
pip install "DadosAbertosBrasil[pandas]"
pip install "DadosAbertosBrasil[polars]"
pip install "DadosAbertosBrasil[pandas,polars]"  # os dois, se precisar
```

E escolha o formato em cada função, com o argumento `formato`, ou para o pacote inteiro:

```python
import DadosAbertosBrasil as dab

dab.config.formato = "pandas"
```

Enquanto `dab.config.formato` não for definido, a primeira função chamada sem `formato` emite um
`DABFormatoWarning` (uma vez por sessão). Definir o formato, inclusive como `"json"`, silencia o aviso.

| Formato | Retorno |
|---|---|
| `"json"` | `list[dict]` com os registros normalizados |
| `"pydantic"` | lista de modelos Pydantic (por exemplo, `camara.modelos.Deputado`) |
| `"pandas"` | `pandas.DataFrame` |
| `"polars"` | `polars.DataFrame` |
| `"bruto"` | JSON original da API, como veio |
| `"url"` | endereço da consulta |

Veja as outras opções em [Configuração e erros](referencia/configuracao.md).
