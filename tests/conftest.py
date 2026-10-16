import socket
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


def api_indisponivel(erro: BaseException) -> bool:
    """Indica se o erro vem da rede ou do serviço fora do ar.

    Erros 4xx (exceto 408 e 429), JSON inesperado e asserts continuam sendo
    falhas: são eles que os testes online existem para pegar.
    """

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
