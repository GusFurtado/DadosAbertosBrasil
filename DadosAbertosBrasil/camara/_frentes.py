from typing import Optional

from pydantic import validate_call, PositiveInt

from ..utils import Base, Get, Formato, Output


class Frente(Base):
    """Informações detalhadas sobre uma frente parlamentar.

    Parameters
    ----------
    cod : int
        Código numérico da frente parlamentar da qual se deseja informações.

    verificar_certificado : bool, default=True
        Defina esse argumento como `False` em caso de falha na verificação do
        certificado SSL.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.

    cod : int
        Código numérico da frente parlamentar.

    coordenador : dict
        Informações do(a) coordenador(a) da frente parlamentar.

    documento : str
        URL do documento da frente parlamentar.

    email : str
        E-mail de contato.

    id_sitacao : int
        ID da situação da frente parlamentar.

    keywords : str
        Palavras-chaves da frente parlamentar.

    legislatura : int
        ID da legislatura da frente parlamentar.

    situacao : str
        Situação da frente parlamentar.

    telefone : str
        Telefone de contato.

    titulo : str
        Título da frente parlamentar.

    uri : str
        Endereço para coleta de dados direta pela API da frente parlamentar.

    website : str
        URL do website da frente parlamentar.

    Methods
    -------
    membros()
        Os deputados que participam da frente parlamentar.

    Examples
    --------
    Obter título da frente parlamentar #54258.
    >>> fr = camara.Frente(cod=54258)
    >>> fr.url_registro
    ... 'Frente Parlamentar Mista da Telessaúde'

    """

    def __init__(self, cod: int, verificar_certificado: bool = True):
        self.cod = cod
        self.verify = verificar_certificado
        atributos = {
            "coordenador": ["coordenador"],
            "documento": ["urlDocumento"],
            "email": ["email"],
            "id_sitacao": ["idSituacao"],
            "keywords": ["keywords"],
            "legislatura": ["idLegislatura"],
            "situacao": ["situacao"],
            "telefone": ["telefone"],
            "titulo": ["titulo"],
            "uri": ["uri"],
            "website": ["urlWebsite"],
        }

        super().__init__(
            endpoint="camara",
            path=["frentes", str(cod)],
            unpack_keys=["dados"],
            error_key="titulo",
            atributos=atributos,
            verify=self.verify,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: {self.titulo}"

    def __str__(self) -> str:
        return self.titulo

    def membros(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Os deputados que participam da frente parlamentar.

        Uma lista dos deputados participantes da frente parlamentar e os
        papéis que exerceram nessa frente (signatário, coordenador ou
        presidente). Observe que, mesmo no caso de frentes parlamentares
        mistas (compostas por deputados e senadores), são retornados apenas
        dados sobre os deputados.

        Parameters
        ----------
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

        Returns
        -------
        pandas.core.frame.DataFrame | str | dict | list[dict]
            Os deputados que participam da frente parlamentar.

        """

        cols_to_rename = {
            "id": "codigo",
            "uri": "uri",
            "nome": "nome",
            "siglaPartido": "partido",
            "uriPartido": "partido_uri",
            "siglaUf": "uf",
            "idLegislatura": "legislatura",
            "urlFoto": "foto",
            "email": "email",
            "titulo": "titulo",
            "codTitulo": "titulo_codigo",
            "dataInicio": "data_inicio",
            "dataFim": "data_fim",
        }

        return Get(
            endpoint="camara",
            path=["frentes", str(self.cod), "membros"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "partido_uri", "foto", "email"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)


@validate_call
def lista_frentes(
    legislatura: Optional[PositiveInt] = None,
    pagina: PositiveInt = 1,
    url: bool = True,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Lista de frentes parlamentares de uma ou mais legislaturas.

    Retorna uma lista de informações sobre uma frente parlamentar - um
    agrupamento oficial de parlamentares em torno de um determinado tema ou
    proposta. As frentes existem até o fim da legislatura em que foram
    criadas, e podem ser recriadas a cada legislatura. Algumas delas são
    compostas por deputados e senadores.
    Um número de legislatura pode ser passado como parâmetro, mas se for
    omitido são retornadas todas as frentes parlamentares criadas desde 2003.

    Parameters
    ----------
    legislatura : int, optional
        Número da legislatura a qual os dados buscados devem corresponder.

    pagina : int, default=1
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido
        pelo parâmetro `itens`. Se omitido, assume o valor 1.

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
        Lista de frentes parlamentares de uma ou mais legislaturas.

    """

    params = {"pagina": pagina}
    if legislatura is not None:
        params["idLegislatura"] = legislatura

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "titulo": "titulo",
        "idLegislatura": "legislatura",
    }

    return Get(
        endpoint="camara",
        path=["frentes"],
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_date=["data_inicio", "date_fim"],
        url_cols=["uri"],
        remover_url=not url,
        index=index,
        verify=verificar_certificado,
    ).get(formato)
