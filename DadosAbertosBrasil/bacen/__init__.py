"""Módulo para captura de dados das APIs do Banco Central do Brasil.

Este módulo permite o acesso a diversas informações econômicas disponibilizadas pelo Banco Central, incluindo:

- Histórico de câmbio das principais moedas do mundo;
- Expectativas do mercado para indicadores macroeconômicos do Brasil;
- Consulta a séries temporais do Sistema Gerenciador de Séries Temporais (SGS).

APIs Oficiais
-------------

- **SGS - Sistema Gerenciador de Séries Temporais:** `<https://www3.bcb.gov.br/sgspub/>`_
- **Cotação de Câmbio (PTAX):** `<https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/swagger-ui3>`_
- **Expectativas de Mercado:** `<https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/swagger-ui3#/>`_

"""

from ._cambio import cambio
from ._expectativas import expectativas
from ._moedas import moedas
from ._serie import serie
