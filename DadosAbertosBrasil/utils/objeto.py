"""Base das classes de objeto (`camara.Partido(cod)`, `senado.Senador(cod)`...)."""

from typing import Any, ClassVar

from .errors import DABInputError
from .modelos import Registro, validar
from .requisicao import Requisicao


class Objeto:
    """Busca os dados no construtor e expõe os campos do modelo como atributos.

    Attributes
    ----------
    dados : dict
        Resposta JSON da API, como veio.
    registro : Registro
        Os mesmos dados validados pelo modelo de saída.

    """

    modelo: ClassVar[type[Registro]]
    chave_obrigatoria: ClassVar[str | None] = None

    dados: Any
    registro: Registro

    def _carregar(self, requisicao: Requisicao) -> None:
        self.dados = requisicao.json()
        if not isinstance(self.dados, dict) or (
            self.chave_obrigatoria is not None and self.chave_obrigatoria not in self.dados
        ):
            raise DABInputError("Dados não encontrados.")
        self.registro = validar(self.modelo, self.dados)[0]
        for nome in self.modelo.model_fields:
            setattr(self, nome, self.registro.__dict__.get(nome))
