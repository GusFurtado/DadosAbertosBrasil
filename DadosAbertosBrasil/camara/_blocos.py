
from pydantic import Field, PositiveInt, validate_call

from ..utils.modelos import com_params
from ..utils.objeto import Objeto
from ..utils.typing import Formato, Saida
from . import modelos as m
from ._comum import Ordenacao, consultar_camara, requisicao


class Bloco(Objeto):
    """Informações sobre um bloco partidário específico.

    Parameters
    ----------
    cod: int
        Código numérico do bloco partidário do qual se deseja informações.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.

    cod : int
        Código numérico do bloco partidário.

    legislatura : str
        Legislatura do bloco partidário.

    nome : str
        Nome do bloco partidário.

    uri : str
        Endereço para coleta de dados direta pela API do bloco partidário.

    Examples
    --------
    Obter o nome do bloco #576.
    >>> bl = camara.Bloco(cod=576)
    >>> bl.nome
    ... 'PSL, PTB'

    """

    modelo = m.BlocoDetalhes
    chave_obrigatoria = "nome"

    def __init__(self, cod: int, verificar_certificado: bool | None = None):
        self.cod = cod
        self.verify = verificar_certificado
        self._carregar(requisicao(["blocos", cod], verificar_certificado=verificar_certificado))

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.camara: Bloco {self.nome}>"

    def __str__(self) -> str:
        return f"Bloco {self.nome}"


class _ParamsBlocos(Ordenacao):
    legislatura: PositiveInt | None = Field(None, serialization_alias="idLegislatura")


@validate_call
@com_params(_ParamsBlocos)
def lista_blocos(
    legislatura: PositiveInt | None = None,
    pagina: PositiveInt = 1,
    itens: PositiveInt | None = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Lista de dados sobre os blocos partidários.

    Nas atividades parlamentares, partidos podem se juntar em blocos
    partidários. Quando associados, os partidos passam a trabalhar como se
    fossem um "partidão", com um só líder e um mesmo conjunto de vice-líderes.
    Os blocos só podem existir até o fim da legislatura em que foram criados:
    na legislatura seguinte, os mesmos partidos, se associados, formam um novo
    bloco. Este recurso é uma lista dos blocos em atividade no momento da
    requisição. Se forem passados números de legislaturas com o parâmetro
    `legislatura`, são listados também os blocos formados e extintos nessas
    legislaturas.

    Parameters
    ----------
    legislatura : int, optional
        Número da legislatura a qual os dados buscados devem corresponder.
        Se omitido, busca os dados da legislatura atual.

    pagina : int, default=1
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido
        pelo parâmetro `itens`. Se omitido, assume o valor 1.

    itens : int, optional
        Número máximo de itens na página que se deseja obter com esta
        requisição.

    asc : bool, default=True
        Se os registros são ordenados no sentido ascendente:
        - True: De A a Z ou 0 a 9 (ascendente);
        - False: De Z a A ou 9 a 0 (descendente).

    ordenar_por : str, default='nome'
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.

    url : bool, default=True
        Se False, remove as colunas contendo URI, URL e e-mails.
        Vale para os formatos 'json', 'pandas' e 'polars'.

    index : bool, default=False
        Se True, define a coluna `codigo` como index do DataFrame.
        Só se aplica ao formato 'pandas'; com 'polars', é ignorado com aviso.

    formato : {"json", "bruto", "pydantic", "pandas", "polars", "url"}, optional
        Formato do dado que será retornado:
        - "json": lista de registros (`list[dict]`), com os mesmos campos e
          tipos das colunas do DataFrame;
        - "bruto": JSON original da API, como veio;
        - "pydantic": lista de modelos Pydantic, um por registro;
        - "pandas": DataFrame pandas;
        - "polars": DataFrame polars;
        - "url": endereço da consulta.
        Se omitido, usa `DadosAbertosBrasil.config.formato`.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Returns
    -------
    list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
        Lista de blocos partidários.

    """

    return consultar_camara(
        ["blocos"],
        _ParamsBlocos.de_locais(locals()),
        m.Bloco,
        formato,
        url=url,
        index=index,
        verificar_certificado=verificar_certificado,
    )
