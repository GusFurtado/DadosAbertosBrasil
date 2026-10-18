# Instalação

```bash
pip install DadosAbertosBrasil
```

Requer Python 3.10 ou superior. As dependências são [Pandas](https://pandas.pydata.org/),
[Pydantic](https://docs.pydantic.dev/latest/) e [Requests](https://requests.readthedocs.io/).

## Polars

Para obter os resultados como DataFrames do [Polars](https://pola.rs/), instale o extra opcional:

```bash
pip install "DadosAbertosBrasil[polars]"
```

E escolha o formato em cada função, com o argumento `formato`, ou para o pacote inteiro:

```python
import DadosAbertosBrasil as dab

dab.config.formato = "polars"
```

!!! warning "Pandas como extra opcional"
    Atualmente o Pandas é uma dependência obrigatória e o formato padrão dos resultados. Em uma
    versão futura, ele deixará de ser obrigatório e passará a ser instalado apenas como extra
    opcional. Para não depender do formato padrão, defina `dab.config.formato` ou use o argumento
    `formato` nas funções.

Veja as outras opções em [Configuração e erros](referencia/configuracao.md).
