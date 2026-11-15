from typing import Optional

from pydantic import Field, PositiveInt, validate_call

from ..utils.modelos import com_params
from ..utils.objeto import Objeto
from ..utils.typing import Formato, Saida
from . import modelos as m
from ._comum import ParamsCamara, consultar_camara, requisicao


class _ParamsFrentes(ParamsCamara):
    legislatura: PositiveInt | None = Field(None, serialization_alias="idLegislatura")
    pagina: PositiveInt = 1


class Frente(Objeto):
    """Informações detalhadas sobre uma frente parlamentar.

    Parameters
    ----------
    cod : int
        Código numérico da frente parlamentar da qual se deseja informações.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

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

    modelo = m.FrenteDetalhes
    chave_obrigatoria = "titulo"

    def __init__(self, cod: int, verificar_certificado: bool | None = None):
        self.cod = cod
        self.verify = verificar_certificado
        self._carregar(requisicao(["frentes", cod], verificar_certificado=verificar_certificado))

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: {self.titulo}"

    def __str__(self) -> str:
        return self.titulo

    def membros(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Os deputados que participam da frente parlamentar.

        Uma lista dos deputados participantes da frente parlamentar e os
        papéis que exerceram nessa frente (signatário, coordenador ou
        presidente). Observe que, mesmo no caso de frentes parlamentares
        mistas (compostas por deputados e senadores), são retornados apenas
        dados sobre os deputados.

        Parameters
        ----------
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

        Returns
        -------
        list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
            Os deputados que participam da frente parlamentar.

        """

        return consultar_camara(
            ["frentes", self.cod, "membros"],
            None,
            m.MembroFrente,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )


@validate_call
@com_params(_ParamsFrentes)
def lista_frentes(
    legislatura: Optional[PositiveInt] = None,
    pagina: PositiveInt = 1,
    url: bool = True,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
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
        Lista de frentes parlamentares de uma ou mais legislaturas.

    """

    return consultar_camara(
        ["frentes"],
        _ParamsFrentes.de_locais(locals()),
        m.Frente,
        formato,
        url=url,
        index=index,
        verificar_certificado=verificar_certificado,
    )
