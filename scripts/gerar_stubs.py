"""Gera os stubs (`.pyi`) com os `@overload` por `formato` das funções públicas.

O tipo de retorno de cada função depende do `formato` pedido. Os overloads
deixam isso visível para type checkers e IDEs:

- sem `formato` (depende de `config.formato`) ou "bruto": `Any`;
- "json": `list[dict[str, Any]]`;
- "pydantic": `list[<modelo da função>]`;
- "pandas" / "polars": o DataFrame correspondente;
- "url": `str`.

Os overloads ficam num `.pyi` ao lado de cada módulo com funções de dados, e o
`.py` fica só com a implementação. Quando existe um `.pyi`, o type checker lê só
ele: por isso o stub repete a interface pública inteira do módulo (classes,
métodos, atributos e constantes), sem as implementações. As docstrings ficam no
`.py`, de onde o editor e o mkdocstrings continuam lendo.

Os stubs são gerados a partir do código e substituem os anteriores: rode o
script depois de mudar a interface pública de um desses módulos. O teste
`test_stubs` acusa quando ficam fora de sincronia.

    uv run python scripts/gerar_stubs.py
"""

import ast
import copy
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
PACOTE = RAIZ / "DadosAbertosBrasil"

CABECALHO = "# Gerado por scripts/gerar_stubs.py. Não edite: mude o .py e rode o script de novo.\n"

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
    "from typing_extensions import deprecated",
    "from ..utils.typing import DataFramePandas, DataFramePolars",
)

# Decoradores que mudam a interface e por isso vão para o stub. Os demais
# (`validate_call`, `com_params`...) mantêm a assinatura e ficam só no `.py`.
DECORADORES = {"property", "staticmethod", "classmethod", "cached_property", "functools.cached_property"}


def privado(nome: str) -> bool:
    return nome.startswith("_") and not (nome.startswith("__") and nome.endswith("__"))


def deprecated(mensagem: str) -> ast.expr:
    """`@deprecated`: o editor risca o nome e o type checker avisa."""
    return ast.Call(ast.Name("deprecated"), [ast.Constant(mensagem)], [])


def alvo_do_wraps(funcao: ast.FunctionDef) -> str | None:
    """Nome da função embrulhada por `@functools.wraps(...)` (nomes antigos)."""
    for decorador in funcao.decorator_list:
        if (
            isinstance(decorador, ast.Call)
            and ast.unparse(decorador.func) in ("functools.wraps", "wraps")
            and isinstance(decorador.args[0], ast.Name)
        ):
            return decorador.args[0].id
    return None


def removida(funcao: ast.FunctionDef) -> bool:
    """Função removida no 3.0, que só levanta `DABFuncaoRemovidaError`."""
    return any(
        isinstance(no, ast.Raise) and isinstance(no.exc, ast.Call) and ast.unparse(no.exc.func) == "removida"
        for no in ast.walk(funcao)
    )


def nome_declarado(stub: ast.stmt) -> str:
    if isinstance(stub, ast.FunctionDef):
        return stub.name
    return ast.unparse(stub.targets[0] if isinstance(stub, ast.Assign) else stub.target)


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


def formatos_de_dados(funcao: ast.FunctionDef) -> tuple[str, ...] | None:
    """Formatos aceitos, se `funcao` for uma função de dados pública."""
    if privado(funcao.name):
        return None
    parametro = next((a for a in funcao.args.args + funcao.args.kwonlyargs if a.arg == "formato"), None)
    if parametro is None or parametro.annotation is None:
        return None
    if not (funcao.returns and ast.unparse(funcao.returns) == "Saida"):
        return None
    return formatos(parametro.annotation)


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


def default(valor: ast.expr) -> ast.expr:
    """Valores simples aparecem no stub (e no editor); os demais viram `...`."""
    try:
        literal = ast.literal_eval(valor)
    except ValueError:
        return ast.Constant(...)
    if literal is None or isinstance(literal, bool | int | float) or (isinstance(literal, str) and len(literal) <= 40):
        return valor
    return ast.Constant(...)


def argumentos(funcao: ast.FunctionDef) -> ast.arguments:
    args = copy.deepcopy(funcao.args)
    if args.posonlyargs:
        sys.exit(f"{funcao.name}: argumentos só posicionais não são suportados.")
    args.defaults = [default(d) for d in args.defaults]
    args.kw_defaults = [None if d is None else default(d) for d in args.kw_defaults]
    return args


def stub_funcao(funcao: ast.FunctionDef) -> ast.FunctionDef:
    decoradores = [
        d
        for d in funcao.decorator_list
        if ast.unparse(d) in DECORADORES or ast.unparse(d).endswith((".setter", ".deleter", ".getter"))
    ]
    retorno = funcao.returns
    if retorno is None and funcao.name == "__init__":
        retorno = ast.Constant(None)
    return ast.FunctionDef(
        name=funcao.name,
        args=argumentos(funcao),
        body=[ast.Expr(ast.Constant(...))],
        decorator_list=decoradores,
        returns=retorno,
        type_params=[],
    )


def overload(funcao: ast.FunctionDef, formato: str, retorno: str, obrigatorio: bool) -> ast.FunctionDef:
    """Um overload com a assinatura da implementação e `formato` trocado.

    Com `obrigatorio`, `formato` vira keyword-only e sem default: senão o
    overload também casaria com chamadas sem `formato` (sobreposição).
    """
    args = argumentos(funcao)
    nomes = [a.arg for a in args.args]
    if obrigatorio and "formato" in nomes:
        if args.vararg:
            sys.exit(f"{funcao.name}: *args impede tornar `formato` keyword-only.")
        i = nomes.index("formato")
        sem_default = len(args.args) - len(args.defaults)
        por_argumento = [None] * sem_default + args.defaults
        args.kwonlyargs = args.args[i:] + args.kwonlyargs
        args.kw_defaults = por_argumento[i:] + args.kw_defaults
        args.args = args.args[:i]
        args.defaults = por_argumento[sem_default:i]
    alvo = next(a for a in args.args + args.kwonlyargs if a.arg == "formato")
    alvo.annotation = ast.parse(formato, mode="eval").body
    if obrigatorio:
        args.kw_defaults[[a.arg for a in args.kwonlyargs].index("formato")] = None
    return ast.FunctionDef(
        name=funcao.name,
        args=args,
        body=[ast.Expr(ast.Constant(...))],
        decorator_list=[ast.Name("overload")],
        returns=ast.parse(retorno, mode="eval").body,
        type_params=[],
    )


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


class Modulo:
    """Monta o stub de um módulo."""

    def __init__(self, arquivo: Path):
        self.relativo = arquivo.relative_to(PACOTE).as_posix()
        self.arvore = ast.parse(arquivo.read_text())
        self.imports = set()  # imports extras dos overloads
        self.omitidos = set()  # nomes privados que ficaram de fora do stub
        self.publico = self.relativo.split("/")[0]  # `senado`, `camara`...
        self.definicoes = {n.name: n for n in self.arvore.body if isinstance(n, ast.FunctionDef)}

    def funcoes(self, funcao: ast.FunctionDef, qualname: str) -> list[ast.FunctionDef]:
        """O stub da função, ou os overloads se for uma função de dados."""
        alvo = alvo_do_wraps(funcao)
        if alvo is not None:  # nome antigo: a mesma interface do novo, descontinuada
            stubs = self.funcoes(self.definicoes[alvo], alvo)
            for stub in stubs:
                stub.name = funcao.name
                stub.decorator_list.append(deprecated(f"Renomeada para `{self.publico}.{alvo}`."))
            return stubs
        aceitos = formatos_de_dados(funcao)
        if aceitos is None:
            stub = stub_funcao(funcao)
            if removida(funcao):
                stub.decorator_list.append(deprecated("Removida no 3.0: levanta `DABFuncaoRemovidaError`."))
            return [stub]
        chave = f"{self.relativo}:{qualname}"
        if chave in MODELOS:
            modelo, extra = MODELOS[chave]
            if extra:
                self.imports.add(extra)
        else:
            modelo = modelo_passado(funcao)
            if modelo is None:
                sys.exit(f"{chave}: modelo não identificado; acrescente em MODELOS.")
        return [overload(funcao, f, r, i > 0) for i, (f, r) in enumerate(assinaturas(aceitos, modelo))]

    def atribuicao(self, no: ast.Assign | ast.AnnAssign, onde: str) -> ast.stmt | None:
        """Constantes, aliases de tipo e atributos de classe."""
        if isinstance(no, ast.AnnAssign):
            if not isinstance(no.target, ast.Name):
                sys.exit(f"{self.relativo}:{no.lineno}: atribuição não suportada em {onde}.")
            if privado(no.target.id):
                self.omitidos.add(no.target.id)
                return None
            valor = no.value if ast.unparse(no.annotation).endswith("TypeAlias") else None
            if no.value is not None and valor is None:
                valor = ast.Constant(...)
            return ast.AnnAssign(target=no.target, annotation=no.annotation, value=valor, simple=1)
        if len(no.targets) != 1 or not isinstance(no.targets[0], ast.Name):
            sys.exit(f"{self.relativo}:{no.lineno}: atribuição não suportada em {onde}.")
        nome = no.targets[0].id
        if privado(nome):
            self.omitidos.add(nome)
            return None
        if isinstance(no.value, ast.Constant | ast.Name | ast.Attribute | ast.Subscript | ast.BinOp):
            return no  # constante simples ou alias de tipo, como `Dataset = Literal[...]`
        if isinstance(no.value, ast.Call) and ast.unparse(no.value.func) == "alias_descontinuado":
            novo = ast.literal_eval(no.value.args[1])
            return ast.FunctionDef(
                name=nome,
                args=ast.arguments(posonlyargs=[], args=[ast.arg("self")], kwonlyargs=[], kw_defaults=[], defaults=[]),
                body=[ast.Expr(ast.Constant(...))],
                decorator_list=[ast.Name("property"), deprecated(f"Renomeado para `{novo}`.")],
                returns=ast.Name("Any"),
                type_params=[],
            )
        return ast.AnnAssign(target=ast.Name(nome), annotation=ast.Name("Any"), value=None, simple=1)

    def classe(self, classe: ast.ClassDef) -> ast.ClassDef:
        atributos, metodos, declarados = [], [], set()
        for no in classe.body:
            if isinstance(no, ast.Expr | ast.Pass):
                continue  # docstring
            if isinstance(no, ast.Assign | ast.AnnAssign):
                stub = self.atribuicao(no, f"`{classe.name}`")
                if stub is not None:
                    atributos.append(stub)
                    declarados.add(nome_declarado(stub))
            elif isinstance(no, ast.FunctionDef):
                if not privado(no.name):
                    metodos += self.funcoes(no, f"{classe.name}.{no.name}")
                    declarados.add(no.name)
            else:
                sys.exit(f"{self.relativo}:{no.lineno}: {type(no).__name__} não suportado em `{classe.name}`.")

        # Atributos de instância (`self.x = ...`): o tipo vem da anotação ou do
        # parâmetro atribuído; os demais precisam de anotação na classe.
        instancia = {}
        for metodo in (n for n in classe.body if isinstance(n, ast.FunctionDef)):
            parametros = {a.arg: a.annotation for a in metodo.args.args + metodo.args.kwonlyargs}
            for no in ast.walk(metodo):
                if isinstance(no, ast.AnnAssign):
                    alvos, anotacao = [no.target], no.annotation
                elif isinstance(no, ast.Assign):
                    alvos = no.targets
                    anotacao = parametros.get(no.value.id) if isinstance(no.value, ast.Name) else None
                else:
                    continue
                for alvo in alvos:
                    if not (isinstance(alvo, ast.Attribute) and ast.unparse(alvo.value) == "self"):
                        continue
                    if privado(alvo.attr) or alvo.attr in declarados:
                        continue
                    if instancia.get(alvo.attr) is None:
                        instancia[alvo.attr] = anotacao
        faltando = sorted(n for n, a in instancia.items() if a is None)
        if faltando:
            sys.exit(f"{self.relativo}: anote na classe `{classe.name}` o tipo de {', '.join(faltando)}.")
        atributos += [
            ast.AnnAssign(target=ast.Name(n), annotation=a, value=None, simple=1) for n, a in instancia.items()
        ]

        return ast.ClassDef(
            name=classe.name,
            bases=classe.bases,
            keywords=classe.keywords,
            body=atributos + metodos or [ast.Expr(ast.Constant(...))],
            decorator_list=[],
            type_params=[],
        )

    def stub(self) -> str | None:
        """Texto do stub, ou None se o módulo não tiver funções de dados."""
        if not any(isinstance(n, ast.FunctionDef) and formatos_de_dados(n) for n in ast.walk(self.arvore)):
            return None
        corpo = []
        for no in self.arvore.body:
            if isinstance(no, ast.Import | ast.ImportFrom):
                corpo.append(no)
            elif isinstance(no, ast.Expr):
                continue  # docstring
            elif isinstance(no, ast.Assign | ast.AnnAssign):
                stub = self.atribuicao(no, "módulo")
                if stub is not None:
                    corpo.append(stub)
            elif isinstance(no, ast.ClassDef):
                if privado(no.name):
                    self.omitidos.add(no.name)
                else:
                    corpo.append(self.classe(no))
            elif isinstance(no, ast.FunctionDef):
                if privado(no.name):
                    self.omitidos.add(no.name)
                else:
                    corpo += self.funcoes(no, no.name)
            elif isinstance(no, ast.If) and ast.unparse(no.test) in ("TYPE_CHECKING", "typing.TYPE_CHECKING"):
                corpo.append(no)
            else:
                sys.exit(f"{self.relativo}:{no.lineno}: {type(no).__name__} não suportado no módulo.")

        modulo = ast.fix_missing_locations(ast.Module(body=corpo, type_ignores=[]))
        usados = {n.id for n in ast.walk(modulo) if isinstance(n, ast.Name)}
        if usados & self.omitidos:
            sys.exit(
                f"{self.relativo}: o stub usa nomes privados omitidos: {', '.join(sorted(usados & self.omitidos))}."
            )
        imports = "".join(f"{i}\n" for i in sorted(set(IMPORTS) | self.imports))
        return CABECALHO + imports + ast.unparse(modulo) + "\n"


def ruff(argumentos: list[str], codigo: str, arquivo: Path) -> str:
    saida = subprocess.run(
        ["ruff", *argumentos, "--stdin-filename", str(arquivo), "-"],
        input=codigo,
        capture_output=True,
        text=True,
        cwd=RAIZ,
    )
    if not saida.stdout:
        sys.exit(f"ruff falhou em {arquivo}:\n{saida.stderr}")
    return saida.stdout


def nome_do_modulo(arquivo: Path) -> str:
    partes = arquivo.relative_to(RAIZ).with_suffix("").parts
    return ".".join(partes[:-1] if partes[-1] == "__init__" else partes)


def conferir_importacoes(stubs: dict[Path, str]) -> None:
    """Quem importa de um módulo com stub só pode importar o que o stub declara.

    Num stub, `from x import y` não reexporta `y`: um nome que o `.py` só
    importa de outro lugar não existe para quem lê o stub.
    """
    declarados = {}
    for pyi, texto in stubs.items():
        nomes = set()
        for no in ast.parse(texto).body:
            if isinstance(no, ast.ClassDef | ast.FunctionDef | ast.AnnAssign | ast.Assign):
                nomes.add(nome_declarado(no) if not isinstance(no, ast.ClassDef) else no.name)
            elif isinstance(no, ast.ImportFrom):
                nomes |= {a.asname for a in no.names if a.asname == a.name}
        declarados[nome_do_modulo(pyi.with_suffix(".py"))] = nomes

    for arquivo in sorted(PACOTE.rglob("*.py")):
        pacote = nome_do_modulo(arquivo).split(".")
        if arquivo.name != "__init__.py":
            pacote = pacote[:-1]
        for no in ast.walk(ast.parse(arquivo.read_text())):
            if not isinstance(no, ast.ImportFrom) or no.module is None:
                continue
            if no.level:
                base = pacote[: len(pacote) - no.level + 1]
                origem = ".".join([*base, no.module])
            else:
                origem = no.module
            if origem not in declarados:
                continue
            for alias in no.names:
                if alias.name not in declarados[origem]:
                    sys.exit(
                        f"{arquivo.relative_to(RAIZ)}: importa `{alias.name}` de {origem}, que o stub não declara."
                    )


def gerar() -> dict[Path, str]:
    """Os stubs esperados, por caminho do `.pyi`."""
    stubs = {}
    for arquivo in sorted(PACOTE.rglob("*.py")):
        texto = Modulo(arquivo).stub()
        if texto is None:
            continue
        pyi = arquivo.with_suffix(".pyi")
        texto = ruff(["check", "--fix-only", "--select", "F401,I", "--quiet"], texto, pyi)
        stubs[pyi] = ruff(["format"], texto, pyi)
    conferir_importacoes(stubs)
    return stubs


def main():
    stubs = gerar()
    for antigo in sorted(set(PACOTE.rglob("*.pyi")) - set(stubs)):
        if not antigo.read_text().startswith(CABECALHO):
            sys.exit(f"{antigo.relative_to(RAIZ)} não foi gerado por este script; remova à mão se for o caso.")
        antigo.unlink()
        print(f"removido: {antigo.relative_to(RAIZ)}")
    for pyi, texto in stubs.items():
        pyi.write_text(texto)
    print(f"{len(stubs)} stubs gerados.")


if __name__ == "__main__":
    main()
