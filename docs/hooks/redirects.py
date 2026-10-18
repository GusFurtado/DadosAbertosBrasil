"""Redireciona as URLs da antiga documentação em Sphinx para as páginas do MkDocs.

Links antigos (como DadosAbertosBrasil.camara.html ou _modules/.../_deputados.html) continuam
funcionando, inclusive os de gustavofurtado.com/dab/, que apontam para cá.
"""

from pathlib import Path

MODULOS = ["bacen", "camara", "favoritos", "ibge", "ipea", "senado", "uf"]

# Páginas de código-fonte geradas pelo sphinx.ext.viewcode, por módulo.
CODIGO_FONTE = {
    "bacen": ["_cambio", "_expectativas", "_moedas", "_serie"],
    "camara": [
        "_blocos", "_deputados", "_eventos", "_frentes", "_legislaturas",
        "_orgaos", "_partidos", "_proposicoes", "_referencias", "_votacoes",
    ],
    "ibge": ["_cidades", "_misc", "_nomes", "_sidra"],
    "ipea": ["_referencias", "_serie"],
    "senado": ["_blocos", "_legislaturas", "_orcamentos", "_partidos", "_senadores", "_usos_palavras"],
    "uf": ["_governador", "_uf"],
    "utils": ["errors", "get", "parse"],
}

PAGINA = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<title>Redirecionando...</title>
<link rel="canonical" href="{destino}">
<script>location.replace("{destino}" + location.hash)</script>
<meta http-equiv="refresh" content="0; url={destino}">
</head>
<body><a href="{destino}">{destino}</a></body>
</html>
"""


def _pagina(modulo):
    return "referencia/configuracao/" if modulo == "utils" else f"referencia/{modulo}/"


def _redirecionamentos():
    mapa = {f"DadosAbertosBrasil.{m}.html": _pagina(m) for m in MODULOS + ["utils"]}
    for antigo in ["DadosAbertosBrasil.html", "modules.html", "genindex.html", "py-modindex.html",
                   "search.html", "_modules/index.html", "_modules/functools.html"]:
        mapa[antigo] = ""
    mapa["_modules/DadosAbertosBrasil/favoritos.html"] = _pagina("favoritos")
    for modulo, arquivos in CODIGO_FONTE.items():
        for arquivo in arquivos:
            mapa[f"_modules/DadosAbertosBrasil/{modulo}/{arquivo}.html"] = _pagina(modulo)
    return mapa


def on_post_build(config, **kwargs):
    site = Path(config["site_dir"])
    for antigo, destino in _redirecionamentos().items():
        # Caminho relativo, para funcionar em qualquer prefixo (o Pages serve em /DadosAbertosBrasil/).
        relativo = "../" * antigo.count("/") + destino or "./"
        caminho = site / antigo
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(PAGINA.format(destino=relativo), encoding="utf-8")
