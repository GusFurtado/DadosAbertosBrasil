"""Objeto `UF` contendo informações das Unidades da Federação.

Este módulo consolida dados estaduais disponíveis no pacote DadosAbertosBrasil, 
incluindo informações sobre governadores e outras estatísticas por estado.

"""

from ._governador import Governador
from ._uf import UF

__all__ = [
    "Governador",
    "UF",
]
