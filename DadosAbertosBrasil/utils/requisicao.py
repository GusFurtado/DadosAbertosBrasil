"""Requisições HTTP às APIs, separadas da transformação dos dados."""

import json
from urllib.parse import quote, urlencode
from dataclasses import dataclass, field
from functools import cache
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .._config import config
from .endpoints import ENDPOINTS
from .errors import DABInputError


@cache
def sessao() -> requests.Session:
    """Sessão HTTP compartilhada, com novas tentativas em erros temporários."""
    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers.update({"Accept": "application/json"})
    return session


@dataclass
class Requisicao:
    """Uma consulta a uma API.

    Parameters
    ----------
    endpoint : str
        Chave de `ENDPOINTS` ou URL base.
    path : list
        Partes do caminho a partir do endpoint.
    params : dict, optional
        Parâmetros da query string, já com os nomes e valores da API.
    chaves : list of str, optional
        Chaves do JSON até os dados relevantes. Chaves ausentes são ignoradas.
    verificar_certificado : bool, optional
        Se omitido, usa `config.verificar_certificado`.
    cacheavel : bool, default=False
        Se a resposta pode ser guardada no cache local (`config.cache`).
        Só para dados que mudam pouco.
    timeout : int, default=30
        Timeout em segundos.

    """

    endpoint: str
    path: list = field(default_factory=list)
    params: dict | None = None
    chaves: list[str] = field(default_factory=list)
    verificar_certificado: bool | None = None
    cacheavel: bool = False
    timeout: int = 30

    @property
    def url(self) -> str:
        """Endereço completo da consulta, com a query string."""
        base = ENDPOINTS.get(self.endpoint, self.endpoint)
        url = base + "/".join(str(p) for p in self.path)
        if not self.params:
            return url
        # `quote` codifica espaços como %20: as APIs OData recusam `+`.
        return f"{url}?{urlencode(self.params, doseq=True, quote_via=quote)}"

    def texto(self) -> str:
        """Corpo da resposta, do cache local quando possível (`config.cache`)."""
        from . import cache

        url = self.url
        if self.cacheavel:
            guardado = cache.ler(url)
            if guardado is not None:
                return guardado
        texto = self._baixar(url)
        if self.cacheavel:
            cache.gravar(url, texto)
        return texto

    def _baixar(self, url: str) -> str:
        response = sessao().get(
            url=url,
            verify=config.resolver_certificado(self.verificar_certificado),
            timeout=self.timeout,
        )
        response.raise_for_status()
        # Sem charset declarado, JSON é UTF-8 (o requests assumiria ISO-8859-1
        # para `text/*`).
        if "charset" in response.headers.get("Content-Type", "").lower():
            return response.text
        return response.content.decode("utf-8-sig")

    def bruto(self) -> Any:
        """Resposta JSON original da API, sem as chaves de `chaves`."""
        data = json.loads(self.texto())
        # Algumas APIs devolvem o JSON serializado dentro de uma string.
        if isinstance(data, str):
            data = json.loads(data)
        return data

    def json(self) -> Any:
        """Resposta JSON, já dentro das chaves de `chaves`."""
        return self.desembrulhar(self.bruto())

    def desembrulhar(self, data: Any) -> Any:
        """Entra nas chaves de `chaves` do JSON original."""
        for chave in self.chaves:
            if isinstance(data, dict) and chave in data:
                data = data[chave]
        if data is None:
            raise DABInputError("Nenhum dado encontrado. Verifique os parâmetros da consulta.")
        return data
