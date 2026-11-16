"""Gera os `@overload` por `formato` das funções públicas.

O tipo de retorno de cada função depende do `formato` pedido. Os overloads
deixam isso visível para type checkers e IDEs:

- sem `formato` (depende de `config.formato`) ou "bruto": `Any`;
- "json": `list[dict[str, Any]]`;
- "pydantic": `list[<modelo da função>]`;
- "pandas" / "polars": o DataFrame correspondente;
- "url": `str`.

Os overloads são gerados a partir da assinatura da implementação e
substituem os anteriores: rode o script depois de mudar a assinatura de uma
função com `formato`. O teste `test_overloads` acusa quando ficam fora de
sincronia.

    uv run python scripts/gerar_overloads.py
"""

import ast
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PACOTE = RAIZ / "DadosAbertosBrasil"

TODOS = ("json", "bruto", "pydantic", "pandas", "polars", "url")

# Funções cujo modelo não é o argumento passado antes de `formato`: modelos
# montados conforme a consulta (o tipo é a base deles) ou chamadas a outras
# funções. Valor: (expressão do modelo, import necessário ou None).
MODELOS = {
    "bacen/_cambio.py:cambio": ("m.Cotacao", None),
    "bacen/_expectativas.py:expectativas": ("Registro", "from ..utils.modelos import Registro"),
    "ibge/_misc.py:localidades": ("m.Localidade", None),
    "ibge/_nomes.py:nomes": ("m.FrequenciaNomes", None),
    "ibge/_nomes.py:nomes_uf": ("m.NomeUF", None),
    "ibge/_nomes.py:nomes_ranking": ("m.RankingNome", None),
    "ibge/_sidra.py:sidra": ("m.ValorSidra", None),
    "favoritos/__init__.py:ipca": ("ValorSerie", "from ..bacen.modelos import ValorSerie"),
    "favoritos/__init__.py:rentabilidade_poupanca": ("ValorSerie", "from ..bacen.modelos import ValorSerie"),
    "favoritos/__init__.py:reservas_internacionais": ("ValorSerie", "from ..bacen.modelos import ValorSerie"),
    "favoritos/__init__.py:selic": ("ValorSerie", "from ..bacen.modelos import ValorSerie"),
    "favoritos/__init__.py:taxa_referencial": ("ValorSerie", "from ..bacen.modelos import ValorSerie"),
    "favoritos/__init__.py:pib": ("m.ValorIpea", None),
    "favoritos/__init__.py:risco_brasil": ("m.ValorIpea", None),
    "favoritos/__init__.py:salario_minimo": ("m.ValorIpea", None),
    "uf/_uf.py:UF.deputados": ("Deputado", "from ..camara.modelos import Deputado"),
    "uf/_uf.py:UF.senadores": ("Senador", "from ..senado.modelos import Senador"),
}

IMPORTS = (
    "from typing import Any, Literal, overload",
    "from ..utils.typing import DataFramePandas, DataFramePolars",
)


def formatos(anotacao: ast.expr) -> tuple[str, ...] | None:
    """Formatos aceitos pela implementação, ou None se não for uma função de dados."""
    texto = ast.unparse(anotacao)
    if "Formato" in texto:
        return TODOS
    if texto.startswith("Literal["):
        literal = anotacao.left if isinstance(anotacao, ast.BinOp) else anotacao
        valores = tuple(ast.literal_eval(ast.unparse(literal.slice)))
        if set(valores) <= set(TODOS) and "pandas" in valores:
            return valores
    return None


def modelo_passado(funcao: ast.FunctionDef) -> str | None:
    """Argumento passado logo antes de `formato` na chamada que monta a saída."""
    for no in ast.walk(funcao):
        if isinstance(no, ast.Call):
            for i, arg in enumerate(no.args):
                if isinstance(arg, ast.Name) and arg.id == "formato" and i > 0:
                    anterior = ast.unparse(no.args[i - 1])
                    if anterior.startswith("m."):
                        return anterior
    return None


def eh_overload(no: ast.stmt) -> bool:
    return isinstance(no, ast.FunctionDef) and any(
        ast.unparse(d) in ("overload", "typing.overload") for d in no.decorator_list
    )


def overload(funcao: ast.FunctionDef, formato: str, retorno: str, obrigatorio: bool) -> str:
    """Um overload com a assinatura da implementação e `formato` trocado.

    Com `obrigatorio`, `formato` vira keyword-only e sem default: senão o
    overload também casaria com chamadas sem `formato` (sobreposição).
    """
    args = ast.parse(ast.unparse(funcao.args).join(("def f(", "): ..."))).body[0].args
    args.defaults = [ast.Constant(...) for _ in args.defaults]
    args.kw_defaults = [None if d is None else ast.Constant(...) for d in args.kw_defaults]
    nomes = [a.arg for a in args.args]
    if obrigatorio and "formato" in nomes:
        if args.vararg:
            sys.exit(f"{funcao.name}: *args impede tornar `formato` keyword-only.")
        i = nomes.index("formato")
        sem_default = len(args.args) - len(args.defaults)
        depois = args.args[i:]
        args.args = args.args[:i]
        args.defaults = args.defaults[: max(0, i - sem_default)]
        args.kwonlyargs = depois + args.kwonlyargs
        args.kw_defaults = [ast.Constant(...) for _ in depois] + args.kw_defaults
    alvo = next(a for a in args.args + args.kwonlyargs if a.arg == "formato")
    alvo.annotation = ast.parse(formato, mode="eval").body
    if obrigatorio:
        args.kw_defaults[[a.arg for a in args.kwonlyargs].index("formato")] = None
    nova = ast.FunctionDef(
        name=funcao.name,
        args=args,
        body=[ast.Expr(ast.Constant(...))],
        decorator_list=[ast.Name("overload")],
        returns=ast.parse(retorno, mode="eval").body,
        type_params=[],
    )
    return ast.unparse(ast.fix_missing_locations(nova))


def formatar(codigo: str, recuo: int) -> str:
    """Formata só o trecho gerado: o resto do arquivo fica como está."""
    saida = subprocess.run(
        ["ruff", "format", "--line-length", str(120 - recuo), "--stdin-filename", "overloads.py", "-"],
        input=codigo,
        capture_output=True,
        text=True,
        check=True,
        cwd=RAIZ,
    )
    return saida.stdout


def assinaturas(aceitos: tuple[str, ...], modelo: str) -> list[tuple[str, str]]:
    """Pares (anotação de `formato`, retorno), começando pelo caso sem `formato`."""
    padrao = 'Literal["bruto"] | None' if "bruto" in aceitos else "None"
    pares = [(padrao, "Any")]
    retornos = {
        "json": "list[dict[str, Any]]",
        "pydantic": f"list[{modelo}]",
        "pandas": "DataFramePandas",
        "polars": "DataFramePolars",
        "url": "str",
    }
    pares += [(f'Literal["{f}"]', r) for f, r in retornos.items() if f in aceitos]
    return pares


def processar(arquivo: Path) -> bool:
    fonte = arquivo.read_text()
    linhas = fonte.splitlines(keepends=True)
    arvore = ast.parse(fonte)
    relativo = arquivo.relative_to(PACOTE).as_posix()

    alvos = []  # (corpo onde está, função, qualname)
    for no in arvore.body:
        if isinstance(no, ast.FunctionDef):
            alvos.append((arvore.body, no, no.name))
        elif isinstance(no, ast.ClassDef):
            alvos += [(no.body, f, f"{no.name}.{f.name}") for f in no.body if isinstance(f, ast.FunctionDef)]

    trocas = []  # (início, fim, texto) em índices de linha (0-based, fim exclusivo)
    imports = set()
    for corpo, funcao, qualname in alvos:
        if eh_overload(funcao) or funcao.name.startswith("_"):
            continue
        parametro = next((a for a in funcao.args.args + funcao.args.kwonlyargs if a.arg == "formato"), None)
        if parametro is None or parametro.annotation is None:
            continue
        if not (funcao.returns and ast.unparse(funcao.returns) == "Saida"):
            continue
        aceitos = formatos(parametro.annotation)
        if aceitos is None:
            continue
        chave = f"{relativo}:{qualname}"
        if chave in MODELOS:
            modelo, extra = MODELOS[chave]
            if extra:
                imports.add(extra)
        else:
            modelo = modelo_passado(funcao)
            if modelo is None:
                sys.exit(f"{chave}: modelo não identificado; acrescente em MODELOS.")

        for antigo in (n for n in corpo if eh_overload(n) and n.name == funcao.name):
            inicio, fim = min(d.lineno for d in antigo.decorator_list) - 1, antigo.end_lineno
            while fim < len(linhas) and not linhas[fim].strip():
                fim += 1  # as linhas em branco depois do overload saem junto
            trocas.append((inicio, fim, ""))

        recuo = " " * funcao.col_offset
        bloco = formatar(
            "\n\n".join(overload(funcao, f, r, i > 0) for i, (f, r) in enumerate(assinaturas(aceitos, modelo))),
            len(recuo),
        )
        if recuo:
            bloco = bloco.replace("\n\n\n", "\n\n")  # métodos: uma linha em branco entre eles
        texto = "".join(recuo + linha if linha.strip() else linha for linha in bloco.splitlines(keepends=True))
        texto += "\n" if recuo else "\n\n"
        inicio = min([d.lineno for d in funcao.decorator_list] + [funcao.lineno]) - 1
        trocas.append((inicio, inicio, texto))

    if not trocas:
        return False

    for inicio, fim, texto in sorted(trocas, key=lambda t: (t[0], t[1]), reverse=True):
        linhas[inicio:fim] = [texto]

    ultimo_import = max(n.end_lineno for n in arvore.body if isinstance(n, (ast.Import, ast.ImportFrom)))
    novos = "".join(f"{i}\n" for i in sorted(set(IMPORTS) | imports))
    # As trocas acima ficam todas depois dos imports: o índice continua válido.
    linhas.insert(ultimo_import, novos)
    arquivo.write_text("".join(linhas))
    return True


def main():
    alterados = [str(a) for a in sorted(PACOTE.rglob("*.py")) if processar(a)]
    if alterados:
        subprocess.run(["ruff", "check", "--fix", "--select", "I", "--quiet", *alterados], check=False)
    print(f"{len(alterados)} arquivos com overloads.")


if __name__ == "__main__":
    main()
