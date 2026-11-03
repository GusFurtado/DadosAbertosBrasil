from datetime import date
from typing import Optional

from pydantic import Field, PositiveInt, computed_field, validate_call

from ..utils.modelos import SiglaUF, com_params
from ..utils.objeto import Objeto
from ..utils.typing import Formato, Saida
from . import modelos as m
from ._comum import Ordenacao, ParamsCamara, Periodo, consultar_camara, requisicao


class _ParamsTramitacoes(Periodo):
    pass


class _ParamsVotacoesProposicao(ParamsCamara):
    asc: bool = Field(True, exclude=True)
    ordenar_por: str | None = Field(None, serialization_alias="ordenarPor")

    @computed_field
    @property
    def ordem(self) -> str:
        return "asc" if self.asc else "desc"


class _ParamsProposicoes(Ordenacao, Periodo):
    tipo: str | None = Field(None, serialization_alias="siglaTipo")
    numero: int | None = None
    ano: PositiveInt | None = None
    autor_cod: int | None = Field(None, serialization_alias="idDeputadoAutor")
    autor_nome: str | None = Field(None, serialization_alias="autor")
    partido_sigla: str | None = Field(None, serialization_alias="siglaPartidoAutor")
    partido_cod: PositiveInt | None = Field(None, serialization_alias="idPartidoAutor")
    autor_uf: SiglaUF = Field(None, serialization_alias="siglaUfAutor")
    keyword: str | None = Field(None, serialization_alias="keywords")
    tramitacao_senado: bool | None = Field(None, serialization_alias="tramitacaoSenado")
    apresentacao_inicio: date | None = Field(None, serialization_alias="dataApresentacaoInicio")
    apresentacao_fim: date | None = Field(None, serialization_alias="dataApresentacaoFim")
    situacao: int | None = Field(None, serialization_alias="codSituacao")
    tema: int | None = Field(None, serialization_alias="codTema")


class Proposicao(Objeto):
    """Informações detalhadas sobre uma proposição específica.

    Parameters
    ----------
    cod : int
        Código numérico da proposição da qual se deseja informações.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.

    cod : int
        Código numérico da proposição.

    uri : str
        Endereço para coleta de dados direta pela API da proposição.

    tipo_sigla : str
        Sigla do tipo de proposição.

    tipo_codigo : int
        Código numérico do tipo de proposição.

    numero : int
        Número da proposição.

    ano : int
        Ano da proposição.

    ementa : str
        Ementa da proposição.

    apresentacao : str
        Horário da apresentação da proposição no formato 'AAAA-MM-DD HH:MM'.

    uri_orgao_numerador : str
        Endereço para coleta de dados direta pela API do órgão numerador.

    ultima_atualizacao : str
        Data da última atualização do status da proposição.

    sequencia : int
        Sequência da proposição.

    sigla_orgao : str
        Sigla do órgão.

    uri_orgao : str
        Endereço para coleta de dados direta pela API do órgão.

    uri_ultimo_relator : str
        Endereço para coleta de dados direta pela API do último relaltor.

    regime : str
        Regime da proposição.

    descricao_tramitacao : str
        Descrição da tramitação.

    cod_tipo_tramitacao : str
        Código do tipo da tramitação.

    descricao_situacao : str
        Descrição da situação da proposição.

    cod_situacao : int
        Código númerico da situação da proposição.

    despacho : str
        Despacho.

    url : str
        URL da proposição.

    ambito : str
        Âmbito da proposição.

    uri_autores : str
        Endereço para coleta de dados direta pela API dos autores.

    descricao_tipo : str
        Descrição do tipo da proposição.

    ementa_detalhada : str
        Ementa detalhada da proposição.

    keywords : str
        Palavras-chaves da proposição.

    uri_proposicao_principal : str
        Endereço para coleta de dados direta pela API da proposição principal.

    uri_proposicao_anterior : str
        Endereço para coleta de dados direta pela API da proposição anterior.

    uri_proposicao_posterior : str
        Endereço para coleta de dados direta pela API da proposição posterior.

    url_inteiro_teor : str
        URL do inteiro teor.

    urn_final : str
        URN final.

    texto : str
        Texto da proposição.

    justificativa : str
        Justificativa da proposição.

    Examples
    --------
    Obter a ementa da proposição #15990.
    >>> prop = camara.Proposicao(cod=15990)
    >>> prop.ementa
    ... ''Cria salvaguardas para a tecnologia no campo nuclear...'

    """

    modelo = m.ProposicaoDetalhes
    chave_obrigatoria = "statusProposicao"

    def __init__(self, cod: int, verificar_certificado: bool | None = None):
        self.cod = cod
        self.verify = verificar_certificado
        self._carregar(requisicao(["proposicoes", cod], verificar_certificado=verificar_certificado))

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Proposição {self.cod}"

    def __str__(self) -> str:
        return f"Proposição {self.cod}"

    def autores(
        self,
        url: bool = True,
        formato: Formato | None = None,
    ) -> Saida:
        """Lista pessoas e/ou entidades autoras da proposição.

        Retorna uma lista em que cada item identifica uma pessoa ou entidade
        que é autora da proposição. Além de deputados, também podem ser
        autores de proposições os senadores, a sociedade civil, assembleias
        legislativas e os poderes Executivo e Judiciário.

        Pelo Regimento da Câmara, todos os que assinam uma proposição são
        considerados autores (art. 102), tanto os proponentes quanto os
        apoiadores.

        Para obter mais informações sobre cada autor, é recomendável acessar,
        se disponível, a URL que é valor do campo uri.

        Parameters
        ----------
        url : bool, default=True
            Se False, remove as colunas contendo URI, URL e e-mails.
            Vale para os formatos 'json', 'pandas' e 'polars'.

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
            Lista pessoas e/ou entidades autoras da proposição.

        """

        return consultar_camara(
            ["proposicoes", self.cod, "autores"],
            None,
            m.Autor,
            formato,
            url=url,
            verificar_certificado=self.verify,
        )

    def relacionadas(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Uma lista de proposições relacionadas a uma em especial.

        Lista de informações básicas sobre proposições que de alguma forma se
        relacionam com a proposição, como pareceres, requerimentos,
        substitutivos, etc.

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
            Uma lista de proposições relacionadas a uma em especial.

        """

        return consultar_camara(
            ["proposicoes", self.cod, "relacionadas"],
            None,
            m.ProposicaoRelacionada,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    def temas(
        self, index: bool = False, formato: Formato | None = None
    ) -> Saida:
        """Lista de áreas temáticas de uma proposição.

        Lista em que cada item traz informações sobre uma área temática à qual
        a proposição se relaciona, segundo classificação oficial do Centro de
        Documentação e Informação da Câmara.

        Parameters
        ----------
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
            Lista de áreas temáticas de uma proposição.

        """

        return consultar_camara(
            ["proposicoes", self.cod, "temas"],
            None,
            m.Tema,
            formato,
            index=index,
            verificar_certificado=self.verify,
        )

    @com_params(_ParamsTramitacoes)
    def tramitacoes(
        self,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """O histórico de passos na tramitação de uma proposta.

        Lista que traz, como cada item, um “retrato” de informações que podem
        ser alteradas a cada etapa de tramitação na vida da proposição (como
        regime de tramitação e situação) e informações sobre o que causou esse
        novo estado. Esta representação das tramitações ainda é provisória.

        Parameters
        ----------
        inicio : datetime.datetime or str, optional
            Data de início da tramitação, no formato `'AAAA-MM-DD'`.

        fim : datetime.datetime or str, optional
            Data de término da tramitação, no formato `'AAAA-MM-DD'`.

        url : bool, default=True
            Se False, remove as colunas contendo URI, URL e e-mails.
            Vale para os formatos 'json', 'pandas' e 'polars'.

        index : bool, default=False
            Se True, define a coluna `sequencia` como index do DataFrame.
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
            O histórico de passos na tramitação de uma proposta.

        """

        return consultar_camara(
            ["proposicoes", self.cod, "tramitacoes"],
            _ParamsTramitacoes.de_locais(locals()),
            m.Tramitacao,
            formato,
            url=url,
            index=index,
            index_col="sequencia",
            verificar_certificado=self.verify,
        )

    @com_params(_ParamsVotacoesProposicao)
    def votacoes(
        self,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Informações detalhadas de votações sobre a proposição.

        Retorna uma lista de identificadores básicos sobre as votações na
        Câmara que tiveram a proposição como objeto ou como afetada pelos seus
        resultados. Dados complementares sobre cada votação listada podem ser
        obtidos pelo objeto `camara.Votacao`.

        Parameters
        ----------
        asc : bool, default=False
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).

        ordenar_por : str, default='dataHoraRegistro'
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

        Returns
        -------
        list[dict] | list[Registro] | pandas.DataFrame | polars.DataFrame | str | dict
            Informações detalhadas de votações sobre a proposição.

        """

        return consultar_camara(
            ["proposicoes", self.cod, "votacoes"],
            _ParamsVotacoesProposicao.de_locais(locals()),
            m.Votacao,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )


@validate_call
@com_params(_ParamsProposicoes)
def lista_proposicoes(
    tipo: Optional[str] = None,
    numero: Optional[int] = None,
    ano: Optional[PositiveInt] = None,
    autor_cod: Optional[int] = None,
    autor_nome: Optional[str] = None,
    partido_sigla: Optional[str] = None,
    partido_cod: Optional[PositiveInt] = None,
    autor_uf: Optional[str] = None,
    keyword: Optional[str] = None,
    tramitacao_senado: bool = None,
    apresentacao_inicio: Optional[date] = None,
    apresentacao_fim: Optional[date] = None,
    situacao: Optional[int] = None,
    tema: Optional[int] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    pagina: PositiveInt = 1,
    itens: Optional[int] = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Lista de proposições na Câmara.

    Lista de informações básicas sobre projetos de lei, resoluções, medidas
    provisórias, emendas, pareceres e todos os outros tipos de proposições na
    Câmara. Por padrão, são retornadas todas as proposições que foram
    apresentadas ou tiveram alguma mudança de situação nos últimos 30 dias.
    Esse intervalo de tramitação pode ser configurado pelos parâmetros
    `inicio` e `fim`.

    Se for(em) passado(s) um ou mais dos parâmetros `id`, `ano`,
    `apresentacao_inicio`, `apresentacao_fim`, `autor_cod`, `autor_nome`,
    o intervalo de tramitação só será levado em consideração se os parâmetros
    `inico` e/ou `fim` estiverem explicitamente configurados. Se não
    estiverem, poderão ser listadas proposições que não tiveram tramitação
    recente (e a resposta pode demorar bastante).

    Parameters
    ----------
    tipo : str, optional
        Sigla do tipo das proposições que se deseja obter. A lista de tipos e
        siglas existentes pode ser obtida pela função `camara.referencias`.

    numero : int, optional
        Número oficialmente atribuídos às proposições segundo o art. 137 do
        Regimento Interno, como “PL 1234/2016”.

    ano : int, optional
        Ano de apresentação das proposições que serão listadas no formato
        `'AAAA'`.

    autor_cod : int, optional
        Código numérico identificador do deputado autor das proposições que
        serão listadas.

    autor_nome : str, optional
        Nome ou parte do nome do(s) autor(es) das proposições que se deseja
        obter. Deve estar entre aspas.

    partido_sigla : str, optional
        Sigla do partido a que pertençam os autores das proposições a serem
        listadas.

    partido_cod : int, optional
        Identificador numérico do partido a que pertençam os autores das
        proposições que serão listadas. Esses identificadores podem ser
        obtidos pela função `camara.lista_partidos` e são mais precisos do
        que as siglas, que podem ser usadas por partidos diferentes em épocas
        diferentes.

    autor_uf : str, optional
        Sigla da unidade da federação (estados e Distrito Federal) pela qual
        o(s) autor(es) das proposições selecionadas tenha(m) sido eleito(s).

    keyword : str, optional
        Palavra-chave sobre o tema a que a proposição se relaciona.

    tramitacao_senado : bool, optional
        Buscar proposições que já tenha tramitado no Senado.

    inicio : str, optional
        Data do início do intervalo de tempo em que tenha havido tramitação
        das proposições a serem listadas, no formato `'AAAA-MM-DD'`. Se omitido,
        é assumido como a data de 30 dias anteriores à proposição.

    fim : str, optional
        Data do fim do intervalo de tempo em que tenha havido tramitação das
        proposições a serem listadas. Se omitido, é considerado ser o dia em
        que é feita a requisição.

    apresentacao_inicio : str, optional
        Data do início do intervalo de tempo em que tenham sido apresentadas
        as proposições a serem listadas, no formato `'AAAA-MM-DD'`.

    apresentacao_fim : str, optional
        Data do fim do intervalo de tempo em que tenham sido apresentadas as
        proposições a serem listadas.

    situacao : int, optional
        Código numérico do tipo de situação em que se encontram as proposições
        que serão listadas. As situações possíveis podem ser obtidas pela
        função `camara.referencias`. Atenção: este parâmetro pode apresentar
        resultados inesperados, por problemas com o registro dos dados.

    tema : int, optional
        Código numérico das áreas temáticas das proposições que serão
        listadas. Os temas possíveis podem ser obtidos pela função
        `camara.referencias`.

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

    ordenar_por : str, default='id'
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
        Lista de proposições na Câmara.

    """

    return consultar_camara(
        ["proposicoes"],
        _ParamsProposicoes.de_locais(locals()),
        m.Proposicao,
        formato,
        url=url,
        index=index,
        verificar_certificado=verificar_certificado,
    )
