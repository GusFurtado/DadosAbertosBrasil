"""Subpacote `_utils` — Ferramentas auxiliares do pacote DadosAbertosBrasil.

Módulos
-------

- **errors**: Exceções personalizadas para as funções do pacote.
- **get**: Função para captura de dados em formato JSON.
- **parse**: Padronização de inputs das funções do pacote.

"""

from .get import Base, Get
from .typing import Formato, Expectativa, NivelTerritorial, Output
