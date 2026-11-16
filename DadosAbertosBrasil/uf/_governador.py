"""Governador de uma UF, a partir de `wiki.governadores()`."""

from .. import wiki
from ..utils import parse


class Governador:
    """Informações básicas do governador da UF.

    Parameters
    ----------
    uf: str
        Nome, sigla ou código da UF desejada.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Attributes
    ----------
    uf : str
    nome : str
    artigo : str | None
        Título do artigo sobre o governador na Wikipedia.
    interino : bool
    partido : str | None
    partido_sigla : str | None
    mandato_inicio : datetime.date
    mandato_fim : datetime.date | None
    ano_eleicao : int | None
    vice_governador : str | None
    registro : DadosAbertosBrasil.wiki.modelos.Governador
        Registro completo de `wiki.governadores()`.

    Notes
    -----
    Fonte: Wikipedia em português (CC BY-SA 4.0), via `wiki.governadores()`.
    O atributo `nome_completo`, do 2.x, não existe mais.

    """

    def __init__(self, uf: str, verificar_certificado: bool | None = None):
        self.uf = parse.uf(uf)
        registros = wiki.governadores(uf=self.uf, formato="pydantic", verificar_certificado=verificar_certificado)
        self.registro = registros[0]
        for campo in wiki.modelos.Governador.model_fields:
            setattr(self, campo, getattr(self.registro, campo))

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.uf.Governador: {self.nome} ({self.uf})>"
