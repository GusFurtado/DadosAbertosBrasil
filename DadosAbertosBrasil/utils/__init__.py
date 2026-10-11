"""Subpacote `_utils` — Ferramentas auxiliares do pacote DadosAbertosBrasil.

Módulos
-------

- **errors**: Exceções personalizadas para as funções do pacote.
- **get**: Função para captura de dados em formato JSON.
- **parse**: Padronização de inputs das funções do pacote.

"""

from .filtros import codigos_orgaos, filtrar, filtrar_nome
from .get import Base, Get, converter
from .typing import Formato, Expectativa, NivelTerritorial, Output
