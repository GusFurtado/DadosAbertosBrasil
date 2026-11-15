"""Objeto UF contendo informações das Unidades da Federação.

Serve como um consolidador por UF de diversar funções do pacote DadosAbertosBrasil.

"""

from datetime import datetime

from ..utils import parse
from ..utils.requisicao import Requisicao
from ..utils.errors import descontinuado


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
    nome_completo : str
    ano_eleicao : int
    mandato_inicio : datetime.date
    mandato_fim : datetime.date
    partido : str
    partido_sigla : str
    vice_governador : str

    """

    _UFS = {
        "AC": "Acre",
        "AL": "Alagoas",
        "AM": "Amazonas",
        "AP": "Amapá",
        "BA": "Bahia",
        "CE": "Ceará",
        "DF": "Distrito Federal",
        "ES": "Espírito Santo",
        "GO": "Goiás",
        "MA": "Maranhão",
        "MT": "Mato Grosso",
        "MS": "Mato Grosso do Sul",
        "MG": "Minas Gerais",
        "PA": "Pará",
        "PB": "Paraíba",
        "PR": "Paraná",
        "PE": "Pernambuco",
        "PI": "Piauí",
        "RJ": "Rio de Janeiro",
        "RN": "Rio Grande do Norte",
        "RS": "Rio Grande do Sul",
        "RO": "Rondônia",
        "RR": "Roraima",
        "SP": "São Paulo",
        "SC": "Santa Catarina",
        "SE": "Sergipe",
        "TO": "Tocantins",
    }

    def __init__(self, uf: str, verificar_certificado: bool | None = None):
        self.uf = parse.uf(uf)

        data = Requisicao("wiki", ["governadores.json"], verificar_certificado=verificar_certificado).json()
        data = data[self._UFS[self.uf]]

        # Criar atributos
        for key in data:
            setattr(self, "_nome_completo" if key == "nome_completo" else key, data[key])
        self.mandato_inicio = datetime.strptime(self.mandato_inicio, "%Y-%m-%d").date()
        self.mandato_fim = datetime.strptime(self.mandato_fim, "%Y-%m-%d").date()

    @property
    def nome_completo(self) -> str:
        """Nome completo do governador.

        Descontinuado: o atributo deixa de existir no DadosAbertosBrasil 3.0.
        """
        descontinuado(
            "`Governador.nome_completo` deixa de existir no DadosAbertosBrasil 3.0, "
            "cujos dados de governadores trazem `nome` e `artigo` (título do artigo "
            "na Wikipedia)."
        )
        return self._nome_completo

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.uf.Governador: {self.nome} ({self.uf})>"
