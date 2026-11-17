"""O que um usuário vê no type checker: conferido pelo mypy em `tests/test_stubs.py`.

Não é executado: só o mypy lê este arquivo.
"""

from datetime import datetime
from typing import Any, assert_type

import polars as pl

from DadosAbertosBrasil import camara, favoritos, ibge, ipea, senado, uf, wiki
from DadosAbertosBrasil.bacen.modelos import ValorSerie
from DadosAbertosBrasil.camara import modelos as modelos_camara
from DadosAbertosBrasil.senado import modelos as modelos_senado
from DadosAbertosBrasil.wiki import modelos as modelos_wiki

# Funções: o retorno acompanha o `formato`.
assert_type(camara.lista_partidos(), Any)
assert_type(camara.lista_partidos(formato="bruto"), Any)
assert_type(camara.lista_partidos(formato="json"), list[dict[str, Any]])
assert_type(camara.lista_partidos(formato="pydantic"), list[modelos_camara.Partido])
assert_type(camara.lista_partidos(formato="polars"), pl.DataFrame)
assert_type(camara.lista_partidos(formato="url"), str)
assert_type(wiki.governadores(formato="pydantic"), list[modelos_wiki.Governador])
assert_type(favoritos.selic(formato="pydantic"), list[ValorSerie])

# Métodos das classes de objeto.
assert_type(camara.Partido(36899).membros(formato="pydantic"), list[modelos_camara.Deputado])
assert_type(uf.UF("SP").senadores(formato="pydantic"), list[modelos_senado.Senador])

# Atributos.
assert_type(camara.Partido(36899).cod, int)
assert_type(uf.UF("SP").sigla, str)
assert_type(ipea.Serie("PRECOS12_IPCA12").ultima_atualizacao, datetime | None)
assert_type(ibge.Metadados(1301).nome, str)

# Nomes antigos e funções removidas aparecem como descontinuados.
assert_type(senado.lista_legislatura(56, formato="url"), str)  # type: ignore[deprecated]
favoritos.perfil_eleitorado()  # type: ignore[deprecated]
