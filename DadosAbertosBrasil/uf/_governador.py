"""Objeto UF contendo informações das Unidades da Federação.

Serve como um consolidador por UF de diversar funções do pacote DadosAbertosBrasil.

"""

from datetime import datetime

from ..utils import Get, parse


class Governador:
    """Informações básicas do governador da UF.

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

    def __init__(self, uf: str, verificar_certificado: bool = True):
        self.uf = parse.uf(uf)

        data = Get(
            endpoint="github",
            path=["GusFurtado", "dab_assets", "main", "data", "governadores.json"],
            verify=verificar_certificado,
        ).json
        data = data[self._UFS[self.uf]]

        # Criar atributos
        for key in data:
            setattr(self, key, data[key])
        self.mandato_inicio = datetime.strptime(self.mandato_inicio, "%Y-%m-%d").date()
        self.mandato_fim = datetime.strptime(self.mandato_fim, "%Y-%m-%d").date()

    def __str__(self) -> str:
        return self.nome

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.uf.Governador: {self.nome} ({self.uf})>"
