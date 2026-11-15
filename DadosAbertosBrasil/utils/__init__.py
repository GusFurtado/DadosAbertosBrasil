"""Ferramentas internas do DadosAbertosBrasil.

Módulos
-------
- **errors**: exceções e avisos do pacote.
- **requisicao**: requisições HTTP às APIs.
- **modelos**: bases dos modelos Pydantic de entrada (`Params`) e saída (`Registro`).
- **saida**: entrega dos dados no formato pedido.
- **objeto**: base das classes de objeto (`camara.Partido(cod)`...).
- **parse**: padronização de UF, datas, localidades e moedas.

"""

from .typing import Expectativa, Formato, NivelTerritorial, Output, Saida
