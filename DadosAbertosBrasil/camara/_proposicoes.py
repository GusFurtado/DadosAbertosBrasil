from datetime import date
from typing import Literal, Optional

import pandas as pd
from pydantic import validate_call, PositiveInt

from .._utils import parse
from .._utils.get_data import DAB_Base, get_and_format


class Proposicao(DAB_Base):
    """Informações detalhadas sobre uma proposição específica.

    Parameters
    ----------
    cod : int
        Código numérico da proposição da qual se deseja informações.

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

    def __init__(self, cod: int):
        self.cod = cod
        atributos = {
            "uri": ["uri"],
            "tipo_sigla": ["siglaTipo"],
            "tipo_codigo": ["codTipo"],
            "numero": ["numero"],
            "ano": ["ano"],
            "ementa": ["ementa"],
            "apresentacao": ["dataApresentacao"],
            "uri_orgao_numerador": ["uriOrgaoNumerador"],
            "ultima_atualizacao": ["statusProposicao", "dataHora"],
            "sequencia": ["statusProposicao", "sequencia"],
            "sigla_orgao": ["statusProposicao", "siglaOrgao"],
            "uri_orgao": ["statusProposicao", "uriOrgao"],
            "uri_ultimo_relator": ["statusProposicao", "uriUltimoRelator"],
            "regime": ["statusProposicao", "regime"],
            "descricao_tramitacao": ["statusProposicao", "descricaoTramitacao"],
            "cod_tipo_tramitacao": ["statusProposicao", "codTipoTramitacao"],
            "descricao_situacao": ["statusProposicao", "descricaoSituacao"],
            "cod_situacao": ["statusProposicao", "codSituacao"],
            "despacho": ["statusProposicao", "despacho"],
            "url": ["statusProposicao", "url"],
            "ambito": ["statusProposicao", "ambito"],
            "uri_autores": ["uriAutores"],
            "descricao_tipo": ["descricaoTipo"],
            "ementa_detalhada": ["ementaDetalhada"],
            "keywords": ["keywords"],
            "uri_proposicao_principal": ["uriPropPrincipal"],
            "uri_proposicao_anterior": ["uriPropAnterior"],
            "uri_proposicao_posterior": ["uriPropPosterior"],
            "url_inteiro_teor": ["urlInteiroTeor"],
            "urn_final": ["urnFinal"],
            "texto": ["texto"],
            "justificativa": ["justificativa"],
        }

        super().__init__(
            api="camara",
            path=["proposicoes", str(cod)],
            unpack_keys=["dados"],
            error_key="statusProposicao",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Proposição {self.cod}"

    def __str__(self) -> str:
        return f"Proposição {self.cod}"

    def autores(
        self,
        url: bool = True,
        formato: Literal["dataframe", "json"] = "dataframe",
    ) -> dict | pd.DataFrame:
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
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Returns
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list of dict
            Se formato = 'json', retorna os dados brutos no formato json.

        """

        cols_to_rename = {
            "nome": "nome",
            "uri": "uri",
            "codTipo": "tipo_codigo",
            "tipo": "tipo",
            "ordemAssinatura": "ordem_assinatura",
            "proponente": "proponente",
        }

        return get_and_format(
            api="camara",
            path=["proposicoes", self.cod, "autores"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri"],
            url=url,
            formato=formato,
        )

    def relacionadas(
        self,
        url: bool = True,
        index: bool = False,
        formato: Literal["dataframe", "json"] = "dataframe",
    ) -> dict | pd.DataFrame:
        """Uma lista de proposições relacionadas a uma em especial.

        Lista de informações básicas sobre proposições que de alguma forma se
        relacionam com a proposição, como pareceres, requerimentos,
        substitutivos, etc.

        Parameters
        ----------
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        index : bool, default=False
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Returns
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list of dict
            Se formato = 'json', retorna os dados brutos no formato json.

        """

        cols_to_rename = {
            "id": "codigo",
            "uri": "uri",
            "siglaTipo": "tipo_sigla",
            "codTipo": "tipo_codigo",
            "numero": "numero",
            "ano": "ano",
            "ementa": "ementa",
        }

        return get_and_format(
            api="camara",
            path=["proposicoes", self.cod, "relacionadas"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["tipo_codigo", "numero", "ano"],
            url_cols=["uri"],
            url=url,
            index=index,
            formato=formato,
        )

    def temas(
        self, index: bool = False, formato: Literal["dataframe", "json"] = "dataframe"
    ) -> dict | pd.DataFrame:
        """Lista de áreas temáticas de uma proposição.

        Lista em que cada item traz informações sobre uma área temática à qual
        a proposição se relaciona, segundo classificação oficial do Centro de
        Documentação e Informação da Câmara.

        Parameters
        ----------
        index : bool, default=False
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Returns
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list of dict
            Se formato = 'json', retorna os dados brutos no formato json.

        """

        cols_to_rename = {
            "codTema": "codigo",
            "tema": "tema",
            "relevancia": "relevancia",
        }

        return get_and_format(
            api="camara",
            path=["proposicoes", self.cod, "temas"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            index=index,
            formato=formato,
        )

    def tramitacoes(
        self,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        url: bool = True,
        index: bool = False,
        formato: Literal["dataframe", "json"] = "dataframe",
    ) -> dict | pd.DataFrame:
        """O histórico de passos na tramitação de uma proposta.

        Lista que traz, como cada item, um “retrato” de informações que podem
        ser alteradas a cada etapa de tramitação na vida da proposição (como
        regime de tramitação e situação) e informações sobre o que causou esse
        novo estado. Esta representação das tramitações ainda é provisória.

        Parameters
        ----------
        inicio : datetime.datetime or str, optional
            Data de início da tramitação, no formato 'AAAA-MM-DD'.
        fim : datetime.datetime or str, optional
            Data de término da tramitação, no formato 'AAAA-MM-DD'.
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        index : bool, default=False
            Se True, define a coluna `sequencia` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Returns
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list of dict
            Se formato = 'json', retorna os dados brutos no formato json.

        """

        params = {}
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")

        cols_to_rename = {
            "dataHora": "data",
            "sequencia": "sequencia",
            "siglaOrgao": "orgao",
            "uriOrgao": "orgao_uri",
            "uriUltimoRelator": "ultimo_relator_uri",
            "regime": "regime",
            "descricaoTramitacao": "tramitacao",
            "codTipoTramitacao": "tramitacao_codigo",
            "descricaoSituacao": "situacao",
            "codSituacao": "situacao_codigo",
            "despacho": "despacho",
            "url": "url",
            "ambito": "ambito",
        }

        return get_and_format(
            api="camara",
            path=["proposicoes", self.cod, "tramitacoes"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data"],
            cols_to_int=["tramitacao_codigo", "situacao_codigo"],
            url_cols=["orgao_uri", "ultimo_relator_uri", "url"],
            url=url,
            index_col="sequencia",
            index=index,
            formato=formato,
        )

    def votacoes(
        self,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        formato: Literal["dataframe", "json"] = "dataframe",
    ) -> dict | pd.DataFrame:
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
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        index : bool, default=False
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Returns
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list of dict
            Se formato = 'json', retorna os dados brutos no formato json.

        """

        params = {"ordem": "asc" if asc else "desc", "ordenarPor": ordenar_por}

        cols_to_rename = {
            "id": "codigo",
            "aprovacao": "aprovacao",
            "data": "data",
            "dataHoraRegistro": "data_registro",
            "descricao": "descricao",
            "proposicaoObjeto": "proposicao",
            "siglaOrgao": "orgao",
            "uri": "uri",
            "uriEvento": "evento_uri",
            "uriOrgao": "orgao_uri",
            "uriProposicaoObjeto": "proposicao_uri",
        }

        return get_and_format(
            api="camara",
            path=["proposicoes", self.cod, "votacoes"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data"],
            cols_to_int=["tramitacao_codigo", "situacao_codigo"],
            url_cols=["uri", "evento_uri", "orgao_uri", "proposicao_uri"],
            url=url,
            index=index,
            formato=formato,
        )


@validate_call
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
    formato: Literal["dataframe", "json"] = "dataframe",
) -> dict | pd.DataFrame:
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
        Regimento Interno, como “PL 1234/2016”
    ano : int, optional
        Ano de apresentação das proposições que serão listadas no formato
        'AAAA'.
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
        das proposições a serem listadas, no formato 'AAAA-MM-DD'. Se omitido,
        é assumido como a data de 30 dias anteriores à proposição.
    fim : str, optional
        Data do fim do intervalo de tempo em que tenha havido tramitação das
        proposições a serem listadas. Se omitido, é considerado ser o dia em
        que é feita a requisição.
    apresentacao_inicio : str, optional
        Data do início do intervalo de tempo em que tenham sido apresentadas
        as proposições a serem listadas, no formato 'AAAA-MM-DD'.
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
    url : bool, default=False
        Se False, remove as colunas contendo URI, URL e e-mails.
        Esse argumento é ignorado se `formato` for igual a 'json'.
    index : bool, default=False
        Se True, define a coluna `codigo` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'.
    formato : {'dataframe', 'json'}, default='dataframe'
        Formato do dado que será retornado.
        Os dados no formato 'json' são mais completos, porém alguns filtros
        podem não ser aplicados.

    Returns
    -------
    pandas.core.frame.DataFrame
        Se formato = 'dataframe', retorna os dados formatados em uma tabela.
    list of dict
        Se formato = 'json', retorna os dados brutos no formato json.

    """

    params = {
        "pagina": pagina,
        "ordem": "asc" if asc else "desc",
        "ordenarPor": ordenar_por,
    }
    if tipo is not None:
        params["siglaTipo"] = tipo
    if numero is not None:
        params["numero"] = numero
    if ano is not None:
        params["ano"] = ano
    if autor_cod is not None:
        params["idDeputadoAutor"] = autor_cod
    if autor_nome is not None:
        params["autor"] = autor_nome
    if partido_sigla is not None:
        params["siglaPartidoAutor"] = partido_sigla
    if partido_cod is not None:
        params["idPartidoAutor"] = partido_cod
    if autor_uf is not None:
        params["siglaUfAutor"] = parse.uf(autor_uf)
    if keyword is not None:
        params["keywords"] = keyword
    if tramitacao_senado is not None:
        params["tramitacaoSenado"] = "true" if tramitacao_senado else "false"
    if apresentacao_inicio is not None:
        params["dataApresentacaoInicio"] = str(apresentacao_inicio)
    if apresentacao_fim is not None:
        params["dataApresentacaoFim"] = str(apresentacao_fim)
    if situacao is not None:
        params["codSituacao"] = situacao
    if tema is not None:
        params["codTema"] = tema
    if inicio is not None:
        params["dataInicio"] = parse.data(inicio, "camara")
    if fim is not None:
        params["dataFim"] = parse.data(fim, "camara")
    if itens is not None:
        params["itens"] = itens

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "siglaTipo": "tipo",
        "codTipo": "tipo_codigo",
        "numero": "numero",
        "ano": "ano",
        "ementa": "ementa",
    }

    return get_and_format(
        api="camara",
        path="proposicoes",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        url_cols=["uri"],
        url=url,
        index=index,
        formato=formato,
    )
