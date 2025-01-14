from typing import Optional

from pydantic import validate_call, PositiveInt

from ..utils import Base, Get, Formato, Output


class Bloco(Base):
    """Informações sobre um bloco partidário específico.

    Parameters
    ----------
    cod: int
        Código numérico do bloco partidário do qual se deseja informações.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

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

    def __init__(self, cod: int, verificar_certificado: bool = True):
        self.cod = cod
        self.verify = verificar_certificado
        atributos = {"legislatura": ["idLegislatura"], "nome": ["nome"], "uri": ["uri"]}

        super().__init__(
            endpoint="camara",
            path=["blocos", str(cod)],
            unpack_keys=["dados"],
            error_key="nome",
            atributos=atributos,
            verify=self.verify,
        )

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.camara: Bloco {self.nome}>"

    def __str__(self) -> str:
        return f"Bloco {self.nome}"


@validate_call
def lista_blocos(
    legislatura: Optional[PositiveInt] = None,
    pagina: PositiveInt = 1,
    itens: Optional[PositiveInt] = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
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

    url : bool, default=False
        Se False, remove as colunas contendo URI, URL e e-mails.
        Esse argumento é ignorado se `formato` for igual a 'json'.

    index : bool, default=False
        Se True, define a coluna `codigo` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'.

    formato : {"json", "pandas", "url"}, default="pandas"
        Formato do dado que será retornado:
        - "json": Dicionário com as chaves e valores originais da API;
        - "pandas": DataFrame formatado;
        - "url": Endereço da API que retorna o arquivo JSON.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Returns
    -------
    pandas.core.frame.DataFrame | str | dict | list[dict]
        Lista de blocos partidários.

    """

    params = {
        "pagina": pagina,
        "ordem": "asc" if asc else "desc",
        "ordenarPor": ordenar_por,
    }
    if legislatura is not None:
        params["idLegislatura"] = legislatura
    if itens is not None:
        params["itens"] = itens

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "nome": "nome",
        "idLegislatura": "legislatura",
    }

    return Get(
        endpoint="camara",
        path=["blocos"],
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo", "legislatura"],
        url_cols=["uri"],
        remover_url=not url,
        index=index,
        verify=verificar_certificado,
    ).get(formato)
