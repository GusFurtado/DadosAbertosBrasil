from typing import Any

from .typing import Output


def filtrar(data: Output, formato: str, coluna: str, valor: Any) -> Output:
    """Mantém as linhas em que `coluna` é igual a `valor`.

    Para os formatos 'json' e 'url', retorna `data` sem alteração.
    """
    match formato:
        case "pandas":
            return data[data[coluna] == valor]
        case "polars":
            import polars as pl

            return data.filter(pl.col(coluna) == valor)
    return data


def filtrar_nome(
    data: Output,
    formato: str,
    colunas: list[str],
    contendo: str | None = None,
    excluindo: str | None = None,
) -> Output:
    """Filtra linhas pelo texto (regex) presente nas colunas de nome.

    `contendo` mantém as linhas em que alguma coluna contém o padrão.
    `excluindo` remove as linhas em que todas as colunas contêm o padrão.
    Para os formatos 'json' e 'url', retorna `data` sem alteração.
    """
    match formato:
        case "pandas":
            if contendo is not None:
                mascara = data[colunas[0]].str.contains(contendo)
                for coluna in colunas[1:]:
                    mascara |= data[coluna].str.contains(contendo)
                data = data[mascara]
            if excluindo is not None:
                mascara = ~data[colunas[0]].str.contains(excluindo)
                for coluna in colunas[1:]:
                    mascara |= ~data[coluna].str.contains(excluindo)
                data = data[mascara]
        case "polars":
            import polars as pl

            if contendo is not None:
                data = data.filter(
                    pl.any_horizontal(pl.col(c).str.contains(contendo) for c in colunas)
                )
            if excluindo is not None:
                data = data.filter(
                    ~pl.all_horizontal(pl.col(c).str.contains(excluindo) for c in colunas)
                )
    return data


def codigos_orgaos(data: Output, formato: str) -> Output:
    """Substitui a coluna `orgaos` pelos códigos dos órgãos.

    Em pandas, um órgão vira um `int` e vários viram uma lista. Em polars,
    a coluna é sempre uma lista de códigos. Para 'json' e 'url', retorna
    `data` sem alteração.
    """
    match formato:
        case "pandas":

            def extrair(orgaos):
                cod = [orgao["id"] for orgao in orgaos]
                if not cod:
                    return None
                if len(cod) < 2:
                    return cod[0]
                return cod

            data["orgaos"] = data["orgaos"].apply(extrair)
        case "polars":
            import polars as pl

            data = data.with_columns(
                pl.col("orgaos").list.eval(pl.element().struct.field("id"))
            )
    return data
