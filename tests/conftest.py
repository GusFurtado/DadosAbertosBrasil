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


def _usa_rede(item) -> bool:
    """Teste que consulta a API real: `online`, ou `vcr` com a gravação desligada."""
    if item.get_closest_marker("online") is not None:
        return True
    gravacao_desligada = item.config.getoption("--disable-recording", False)
    return item.get_closest_marker("vcr") is not None and gravacao_desligada


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
        or not _usa_rede(item)
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
    """Os testes dos módulos (gravados ou online) verificam DataFrames pandas (`df.empty`)."""
    no = request.node
    if no.get_closest_marker("online") is not None or no.get_closest_marker("vcr") is not None:
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


# Respostas gravadas (pytest-recording / VCR.py) ----------------------------
#
# Os testes marcados com `vcr` usam as respostas de tests/cassettes/, sem rede.
# Para regravar depois de uma mudança na API:
#     uv run pytest -m vcr --record-mode=rewrite tests/test_camara.py
# Para conferir contra as APIs reais, sem gravar (job testes-online.yml):
#     uv run pytest -m vcr --disable-recording


class _PersisterGzip:
    """Guarda as gravações em YAML comprimido (`.yaml.gz`)."""

    @staticmethod
    def _caminho(cassette_path) -> Path:
        caminho = Path(cassette_path)
        return caminho if caminho.suffix == ".gz" else caminho.with_name(caminho.name + ".gz")

    @classmethod
    def load_cassette(cls, cassette_path, serializer):
        import gzip

        from vcr.serialize import deserialize

        caminho = cls._caminho(cassette_path)
        if not caminho.exists():
            from vcr.persisters.filesystem import CassetteNotFoundError

            raise CassetteNotFoundError()
        return deserialize(gzip.decompress(caminho.read_bytes()).decode(), serializer)

    @classmethod
    def save_cassette(cls, cassette_path, cassette_dict, serializer):
        import gzip

        from vcr.serialize import serialize

        caminho = cls._caminho(cassette_path)
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_bytes(gzip.compress(serialize(cassette_dict, serializer).encode(), mtime=0))


def pytest_recording_configure(config, vcr):
    vcr.register_persister(_PersisterGzip)


def _sem_cookies(response):
    """Remove os cookies que as APIs mandam na resposta (`filter_headers` só vale para a requisição)."""
    headers = response.get("headers", {})
    for nome in [n for n in headers if n.lower() == "set-cookie"]:
        del headers[nome]
    return response


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "decode_compressed_response": True,
        "filter_headers": ["User-Agent", "Cookie", "Authorization"],
        "before_record_response": _sem_cookies,
        "match_on": ["method", "scheme", "host", "port", "path", "query"],
    }
