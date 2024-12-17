"""Funções para padronização de parâmetros entre os módulos.

Padroniza argumentos de data, UF, localidades e moeda, gerando `Exceptions`
especiais do módulo `_utils.errors`.

"""

from datetime import datetime, date
from unicodedata import normalize

from . import errors


def data(data: datetime | date | str, modulo: str) -> str:
    """Padroniza o input de datas entre módulos.

    Parameters
    ----------
    data: datetime.datetime or datetime.date or str
        Input a ser padronizado.
        Pode ser uma objeto date, datetime ou uma string no formato ISO-8601.
    modulo: {'camara', 'senado', 'bacen'}
        Módulo que o parser seja aplicado para selecionar a formatação
        adequada:
            - 'camara': API da Câmara dos Deputados;
            - 'senado': API do Senado Federal;
            - 'bacen': Consultas do Banco Central do Brasil.

    Returns
    -------
    str
        Data no formato adequado para o módulo escolhido.

    """

    if isinstance(data, str):
        try:
            data = datetime.strptime(data, "%Y-%m-%d")
        except ValueError:
            raise errors.DAB_DataError(
                "Formato de data inválido.\n"
                "Se você está tentando inserir um string com padrão de data, "
                "utilize o formato ISO-8601: 'AAAA-MM-DD'."
            )

    try:
        if modulo == "camara":
            return data.strftime("%Y-%m-%d")
        elif modulo == "senado":
            return data.strftime("%Y%m%d")
        elif modulo == "bacen":
            return data.strftime("%m-%d-%Y")
        elif modulo == "sgs":
            return data.strftime("%d/%m/%Y")

    except AttributeError:
        raise errors.DAB_DataError(
            "Formato de data inválido.\n"
            "Insira uma data no formato datetime.datetime, datetime.date ou str."
        )


def uf(uf: str | int, extintos: bool = False) -> str:
    """Converte os nomes dos estados em siglas padrões.
    Suporta abreviaturas, acentuação e case sensibility.

    Parametros
    ----------
    uf: str | int
        Nome, sigla ou código IBGE da UF.
    extintos: bool, default=False
        Verificar também as UFs extintas:
            - 20: Fernando de Noronha / FN
            - 34: Guanabara / GB

    Returns
    -------
    str
        String de dois caracteres maiúsculos que representam a sigla da
        Unidade Federativa desejada.

    """

    UFS = {
        "1": "BR",
        "11": "RO",
        "12": "AC",
        "13": "AM",
        "14": "RR",
        "15": "PA",
        "16": "AP",
        "17": "TO",
        "21": "MA",
        "22": "PI",
        "23": "CE",
        "24": "RN",
        "25": "PB",
        "26": "PE",
        "27": "AL",
        "28": "SE",
        "29": "BA",
        "31": "MG",
        "32": "ES",
        "33": "RJ",
        "35": "SP",
        "41": "PR",
        "42": "SC",
        "43": "RS",
        "50": "MS",
        "51": "MT",
        "52": "GO",
        "53": "DF",
        "BRASIL": "BR",
        "ACRE": "AC",
        "ALAGOAS": "AL",
        "AMAZONAS": "AM",
        "AMAPA": "AP",
        "BAHIA": "BA",
        "CEARA": "CE",
        "DISTRITOFEDERAL": "DF",
        "ESPIRITOSANTO": "ES",
        "GOIAS": "GO",
        "MARANHAO": "MA",
        "MATOGROSSO": "MT",
        "MATOGROSSODOSUL": "MS",
        "MINASGERAIS": "MG",
        "MINAS": "MG",
        "PARA": "PA",
        "PARAIBA": "PB",
        "PARANA": "PR",
        "PERNAMBUCO": "PE",
        "PIAUI": "PI",
        "RIODEJANEIRO": "RJ",
        "RIO": "RJ",
        "RIOGRANDEDONORTE": "RN",
        "RIOGRANDEDOSUL": "RS",
        "RONDONIA": "RO",
        "RORAIMA": "RR",
        "SAOPAULO": "SP",
        "SANTACATARINA": "SC",
        "SERGIPE": "SE",
        "TOCANTINS": "TO",
    }

    _uf = str(uf).upper().replace(" ", "")
    _uf = normalize("NFKD", _uf).encode("ASCII", "ignore").decode("ASCII")

    if extintos:
        UFS.update(
            {
                "20": "FN",
                "34": "GB",
                "FERNANDODENORONHA": "FN",
                "GUANABARA": "GB",
            }
        )

    if _uf in UFS.values():
        return _uf
    else:
        try:
            return UFS[_uf]
        except KeyError:
            raise errors.DAB_UFError(
                f"UF {uf} não identificada.\n" "Insira uma UF válida."
            )


def localidade(localidade: str, brasil=1, on_error="raise") -> str:
    """Verifica se o código da localidade é válido.

    Parametros
    ----------
    localidade: str ou int
        Código da localidade que se deseja verificar.
        Caso localidade == None, retorna o valor padrão do Brasil.
    brasil: default = 1
        Valor padrão para o Brasil.
    on_error: {'raise', 'brasil'}, default='raise'
        - 'raise': Gera um erro quando o valor não for válido;
        - 'brasil': Retorna o valor Brasil quando o valor não for válido.

    Returns
    -------
    str ou int
        Valor da localidade validado.

    """

    if localidade is None:
        return brasil

    elif isinstance(localidade, int):
        return localidade

    elif isinstance(localidade, str):
        if localidade.isnumeric():
            return localidade

    if on_error == "raise":
        raise errors.DAB_LocalidadeError(
            "O código da localidade não está em um formato numérico."
        )
    elif on_error == "brasil":
        return brasil
    else:
        raise errors.DAB_LocalidadeError(
            "Valor incorreto para o argumento `on_error`:\n"
            "  - 'raise': Gera um erro quando o valor não for válido;\n"
            "  - 'brasil': Retorna o valor Brasil quando o valor não for válido."
        )


def moeda(moedas: str | list[str]) -> list[str]:
    """Verifica se o(s) código(s) da(s) moeda(s) inserida(s) está(ão) em um
    formato válido.

    Parameters
    ----------
    moedas : str or list of str
        Símbolo da moeda ou lista de símbolos de moedas que se deseja validar.

    Returns
    -------
    list of str
        Lista de símbolos de moedas formatados.

    """

    if isinstance(moedas, str):
        moedas = [moedas]

    parsed = []
    for moeda in moedas:
        if not isinstance(moeda, str):
            raise errors.DAB_MoedaError(
                "Tipo inválido.\n" "Insira apenas valores do tipo string para moedas."
            )
        elif len(moeda) != 3:
            raise errors.DAB_MoedaError(
                "Código inválido.\n" "O código das moedas possuem três caracteres."
            )

        parsed.append(moeda.upper())

    return parsed
