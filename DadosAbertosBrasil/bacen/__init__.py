"""Módulo de captura de dados das APIs do Banco Central do Brasil.

Notes
-----
SGS - Sistema Gerenciador de Séries Temporais
    https://www3.bcb.gov.br/sgspub/

Cotação do Câmbio
    https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3
    
Expectativas de Mercado
    https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/swagger-ui3#/

"""

from ._cambio import cambio
from ._expectativas import expectativas
from ._moedas import moedas
from ._serie import serie
