import json
import socket
from pathlib import Path
import urllib.error

import pytest
import requests

# Respostas HTTP que indicam indisponibilidade temporária do serviço, e não um
# erro da biblioteca ou uma mudança na API.
STATUS_INDISPONIVEL = {408, 429, 500, 502, 503, 504}


def _status(erro: BaseException) -> int | None:
    if isinstance(erro, requests.HTTPError) and erro.response is not None:
        return erro.response.status_code
    if isinstance(erro, urllib.error.HTTPError):
        return erro.code
    return None


def api_indisponivel(erro: BaseException | None) -> bool:
    """Indica se o erro vem da rede ou do serviço fora do ar.

    Erros 4xx (exceto 408 e 429), JSON inesperado e asserts continuam sendo
    falhas: são eles que os testes online existem para pegar.

    Segue a cadeia de exceções porque o pandas embrulha o erro de rede: o
    `pd.read_json(url)` relança um `URLError` como `FileNotFoundError`.
    """

    while erro is not None:
        if _erro_de_rede(erro):
            return True
        erro = erro.__cause__ or erro.__context__
    return False


def _erro_de_rede(erro: BaseException) -> bool:
    status = _status(erro)
    if status is not None:
        return status in STATUS_INDISPONIVEL
    return isinstance(
        erro,
        (
            requests.ConnectionError,
            requests.Timeout,
            requests.exceptions.RetryError,
            urllib.error.URLError,
            socket.timeout,
            TimeoutError,
            ConnectionError,
        ),
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Transforma em `skip` os testes online que falharam por indisponibilidade.

    Com `--reruns`, só a última tentativa vira `skip`; as anteriores continuam
    falhando para que o pytest-rerunfailures repita o teste.
    """

    outcome = yield
    report = outcome.get_result()

    if (
        report.when != "call"
        or not report.failed
        or item.get_closest_marker("online") is None
        or call.excinfo is None
        or not api_indisponivel(call.excinfo.value)
    ):
        return

    reruns = item.config.getoption("reruns", 0) or 0
    if getattr(item, "execution_count", 1) <= reruns:
        return

    report.outcome = "skipped"
    report.longrepr = (
        str(item.path),
        item.location[1],
        f"API indisponível: {type(call.excinfo.value).__name__}: {call.excinfo.value}",
    )


class RespostaFalsa:
    """Resposta HTTP mínima para testes offline (`requests.Session.get`)."""

    headers = {"Content-Type": "application/json"}

    def __init__(self, conteudo, texto: str | None = None):
        self.conteudo = conteudo
        self.text = texto if texto is not None else json.dumps(conteudo)
        self.content = self.text.encode()

    def raise_for_status(self):
        pass

    def json(self):
        return self.conteudo


@pytest.fixture
def api(monkeypatch):
    """Faz as consultas devolverem `resposta` (ou `resposta(url)`) sem rede."""
    import DadosAbertosBrasil as dab

    def definir(resposta):
        def get(self, url, **kwargs):
            return RespostaFalsa(resposta(url) if callable(resposta) else resposta)

        monkeypatch.setattr(requests.Session, "get", get)

    formato = dab.config.formato
    yield definir
    dab.config.formato = formato


@pytest.fixture(autouse=True)
def formato_pandas_nos_testes_online(request, monkeypatch):
    """Os testes online verificam DataFrames pandas (`df.empty`)."""
    if request.node.get_closest_marker("online") is not None:
        pytest.importorskip("pandas")
        import DadosAbertosBrasil as dab

        monkeypatch.setattr(dab.config, "formato", "pandas")


FIXTURES_WIKI = Path(__file__).parent / "fixtures" / "wiki"


def envelope_wiki(dataset: str) -> dict:
    return json.loads((FIXTURES_WIKI / f"{dataset}.json").read_text())


def servir_wiki(url: str):
    """Arquivo de tests/fixtures/wiki correspondente à URL do repositório de dados."""
    if "DadosAbertosBrasil-wiki" in url:
        return envelope_wiki(url.rsplit("/", 1)[-1].removesuffix(".json"))
    return None


@pytest.fixture
def repositorio(api):
    """Serve os arquivos de tests/fixtures/wiki no lugar do GitHub."""
    api(servir_wiki)
