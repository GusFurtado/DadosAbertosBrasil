from datetime import date
from typing import Literal, Optional

from pydantic import validate_call, PositiveInt

from ..utils import Base, Get, parse, Formato, Output


class Deputado(Base):
    """Retorna os dados cadastrais de um parlamentar que, em algum momento
    da história e por qualquer período, entrou em exercício na Câmara.

    Parameters
    ----------
    cod : int
        Código do parlamentar.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.
    cod : int
        Código de identificação.
    condicao_eleitoral : str
        Condição eleitoral.
    cpf : str
        Número do CPF.
    descricao_status : str
        Descrição do último status.
    email : str
        E-mail.
    escolaridade : str
        Escolaridade.
    falecimento : str
        Data de falecimento no formato 'AAAA-MM-DD'.
        Retorna vazio caso o parlamentar não tenha falecido.
    foto : str
        URL da foto.
    gabinete : dict
        Informações de identificação e contato do gabinete.
    legislatura : int
        ID da legislatura mais recente.
    municipio_nascimento : str
        Município de nascimento.
    nascimento : str
        Data de nascimento no formato 'AAAA-MM-DD'.
    nome : str
        Nome mais comum.
    nome_completo : str
        Nome civil completo.
    nome_eleitoral : str
        Nome utilizado na campanha eleitoral.
    partido : str
        Último partido.
    rede_social : list
        Lista de nomes em redes sociais.
    sexo : str
        - 'M': Masculino;
        - 'F': Feminino.
    situacao : str
        Situação do último status.
    uf : str
        Sigla da Unidade Federativa pela qual foi eleito.
    uf_nascimento : str
        Unidade Federativa de nascimento.
    ultima_atualizacao : str
        Dia e horário da última atualização de status.
    uri : str
        Endereço para coleta de dados direta pela API.
    website : str
        Website.

    Methods
    -------
    despesas()
        As despesas com exercício parlamentar do deputado.
    discursos()
        Os discursos feitos por um deputado em eventos diversos.
    eventos()
        Uma lista de eventos com a participação do parlamentar.
    frentes()
        As frentes parlamentares das quais um deputado é integrante.
    ocupacoes()
        Os empregos e atividades que o(a) deputado(a) já teve.
    orgaos()
        Os órgãos dos quais um deputado é integrante.
    profissoes()
        As frentes parlamentares das quais um deputado é integrante.

    Examples
    --------
    Coletar partido mais recente do deputado Rodrigo Maia.
    >>> cod = 74693   # Código do deputado
    >>> dep = camara.Deputado(cod=cod)
    >>> dep.partido
    ... 'DEM'

    """

    def __init__(self, cod: int, verificar_certificado: bool = True):
        self.cod = cod
        self.verify = verificar_certificado
        atributos = {
            "condicao_eleitoral": ["ultimoStatus", "condicaoEleitoral"],
            "cpf": ["cpf"],
            "descricao_status": ["ultimoStatus", "descricaoStatus"],
            "email": ["ultimoStatus", "email"],
            "escolaridade": ["escolaridade"],
            "falecimento": ["dataFalecimento"],
            "foto": ["ultimoStatus", "urlFoto"],
            "gabinete": ["ultimoStatus", "gabinete"],
            "legislatura": ["ultimoStatus", "idLegislatura"],
            "municipio_nascimento": ["municipioNascimento"],
            "nascimento": ["dataNascimento"],
            "nome": ["ultimoStatus", "nome"],
            "nome_completo": ["nomeCivil"],
            "nome_eleitoral": ["ultimoStatus", "nomeEleitoral"],
            "partido": ["ultimoStatus", "siglaPartido"],
            "rede_social": ["redeSocial"],
            "sexo": ["sexo"],
            "situacao": ["ultimoStatus", "situacao"],
            "uf": ["ultimoStatus", "siglaUf"],
            "uf_nascimento": ["ufNascimento"],
            "ultima_atualizacao": ["ultimoStatus", "data"],
            "uri": ["uri"],
            "website": ["urlWebsite"],
        }

        super().__init__(
            endpoint="camara",
            path=["deputados", str(cod)],
            unpack_keys=["dados"],
            error_key="ultimoStatus",
            atributos=atributos,
            verify=self.verify,
        )

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.camara: Deputad{'a' if self.sexo == 'F' else 'o'} {self.nome_eleitoral}>"

    def __str__(self) -> str:
        return self.nome

    def despesas(
        self,
        legislatura: Optional[PositiveInt] = None,
        ano: Optional[PositiveInt] = None,
        mes: Optional[PositiveInt] = None,
        fornecedor: Optional[int] = None,
        pagina: PositiveInt = 1,
        itens: Optional[PositiveInt] = None,
        asc: bool = True,
        ordenar_por: str = "ano",
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """As despesas com exercício parlamentar do deputado.

        Dá acesso aos registros de pagamentos e reembolsos feitos pela Câmara
        em prol do deputado, a título da Cota para Exercício da Atividade
        Parlamentar, a chamada "cota parlamentar".
        Se não forem passados os parâmetros de tempo, o serviço retorna os
        dados dos seis meses anteriores à requisição.

        Parameters
        ----------
        legislatura : int, optional
            ID da legislatura em que tenham ocorrido as despesas.
        ano : int, optional
            Ano de ocorrência das despesas.
        mes : int, optional
            Número do mês de ocorrência das despesas.
        fornecedor : int, optional
            CNPJ de uma pessoa jurídica, ou CPF de uma pessoa física,
            fornecedora do produto ou serviço (apenas números).
        pagina : int, default=1
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido
            pelo parâmetro `itens`. Se omitido, assume o valor 1.
        itens : int, optional
            Número máximo de itens na página que se deseja obter com
            esta requisição.
        asc : bool, default=True
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por : str, default='ano'
            Nome do campo pelo qual a lista deverá ser ordenada:
            qualquer um dos campos do retorno, e também idLegislatura.
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
        if legislatura is not None:
            params["idLegislatura"] = legislatura
        if ano is not None:
            params["ano"] = ano
        if mes is not None:
            params["mes"] = mes
        if fornecedor is not None:
            params["cnpjCpfFornecedor"] = fornecedor
        if itens is not None:
            params["itens"] = itens

        cols_to_rename = {
            "codDocumento": "codigo",
            "ano": "ano",
            "mes": "mes",
            "tipoDespesa": "despesa",
            "tipoDocumento": "tipo",
            "codTipoDocumento": "tipo_codigo",
            "dataDocumento": "data",
            "numDocumento": "numero",
            "valorDocumento": "valor",
            "urlDocumento": "url",
            "nomeFornecedor": "fornecedor_nome",
            "cnpjCpfFornecedor": "fornecedor_cnpj",
            "valorLiquido": "valor_liquido",
            "valorGlosa": "valor_glosa",
            "numRessarcimento": "ressarcimento",
            "codLote": "lote",
            "parcela": "parcela",
        }

        return Get(
            endpoint="camara",
            path=["deputados", str(self.cod), "despesas"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data"],
            url_cols=["url"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

    def discursos(
        self,
        legislatura: Optional[PositiveInt] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        pagina: PositiveInt = 1,
        itens: Optional[PositiveInt] = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        formato: Formato = "pandas",
    ) -> Output:
        """Os discursos feitos por um deputado em eventos diversos.

        Retorna uma lista de informações sobre os pronunciamentos feitos
        pelo deputado que tenham sido registrados, em quaisquer eventos,
        nos sistemas da Câmara.
        Caso os parâmetros de tempo não sejam configurados na requisição,
        são buscados os discursos ocorridos nos sete dias anteriores ao
        da requisição.

        Parameters
        ----------
        legislatura : int, optional
            Número da legislatura a qual os dados buscados devem corresponder.
        inicio : str, optional
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim : str, optional
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        itens : int, optional
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        pagina : int, default=1
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido
            pelo parâmetro `itens`. Se omitido, assume o valor 1.
        asc : bool, default=True
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por : str, default='dataHoraInicio'
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
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

        params = {
            "pagina": pagina,
            "ordem": "asc" if asc else "desc",
            "ordenarPor": ordenar_por,
        }
        if legislatura is not None:
            params["idLegislatura"] = legislatura
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")
        if itens is not None:
            params["itens"] = itens

        cols_to_rename = {
            "dataHoraInicio": "data_inicio",
            "dataHoraFim": "data_fim",
            "uriEvento": "evento_uri",
            "faseEvento": "evento_fase",
            "tipoDiscurso": "tipo",
            "urlTexto": "texto_uri",
            "urlAudio": "audio_url",
            "urlVideo": "video_url",
            "keywords": "keywords",
            "sumario": "sumario",
            "transcricao": "transcricao",
        }

        return Get(
            endpoint="camara",
            path=["deputados", str(self.cod), "discursos"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["evento_uri", "texto_uri", "audio_url", "video_url"],
            remover_url=not url,
            verify=self.verify,
        ).get(formato)

    def eventos(
        self,
        legislatura: Optional[PositiveInt] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        pagina: PositiveInt = 1,
        itens: Optional[PositiveInt] = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Uma lista de eventos com a participação do parlamentar.

        Retorna uma lista de objetos evento nos quais a participação do
        parlamentar era ou é prevista.
        Se não forem passados parâmetros de tempo, são retornados os eventos
        num período de cinco dias, sendo dois antes e dois depois do dia da
        requisição.

        Parameters
        ----------
        legislatura : int, optional
            Número da legislatura a qual os dados buscados devem corresponder.
        inicio : str, optional
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim : str, optional
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
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
        ordenar_por : str, default='dataHoraInicio'
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
        if legislatura is not None:
            params["idLegislatura"] = legislatura
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")
        if itens is not None:
            params["itens"] = itens

        cols_to_rename = {
            "id": "codigo",
            "uri": "uri",
            "dataHoraInicio": "data_inicio",
            "dataHoraFim": "data_fim",
            "situacao": "situacao",
            "descricaoTipo": "descricao_tipo",
            "descricao": "descricao",
            "localExterno": "local_externo",
            "orgaos": "orgaos",
            "localCamara.nome": "local",
            "localCamara.predio": "local_predio",
            "localCamara.sala": "local_sala",
            "localCamara.andar": "local_andar",
            "urlRegistro": "url",
        }

        data = Get(
            endpoint="camara",
            path=["deputados", str(self.cod), "eventos"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "url"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

        if formato == "pandas":

            def get_orgaos(orgaos):
                cod = [orgao["id"] for orgao in orgaos]
                if len(cod) < 2:
                    return cod[0]
                return cod

            data["orgaos"] = data["orgaos"].apply(get_orgaos)

        return data

    def frentes(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """As frentes parlamentares das quais um deputado é integrante.

        Retorna uma lista de informações básicas sobre as frentes
        parlamentares das quais o parlamentar seja membro, ou, no caso de
        frentes existentes em legislaturas anteriores, tenha encerrado a
        legislatura como integrante.

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
            "titulo": "titulo",
            "idLegislatura": "legislatura",
        }

        return Get(
            endpoint="camara",
            path=["deputados", str(self.cod), "frentes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

    def ocupacoes(
        self,
        formato: Formato = "pandas",
    ) -> Output:
        """Os empregos e atividades que o(a) deputado(a) já teve.

        Enumera as atividades profissionais ou ocupacionais que o deputado
        já teve em sua carreira e declarou à Câmara dos Deputados.

        Parameters
        ----------
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
            "anoInicio": "ano_inicio",
            "anoFim": "ano_fim",
            "entidade": "entidade",
            "entidadePais": "pais",
            "entidadeUF": "uf",
            "titulo": "titulo",
        }

        return Get(
            endpoint="camara",
            path=["deputados", str(self.cod), "ocupacoes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            verify=self.verify,
        ).get(formato)

    def orgaos(
        self,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        pagina: PositiveInt = 1,
        itens: Optional[PositiveInt] = None,
        asc: bool = True,
        ordenar_por: str = "dataInicio",
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Os órgãos dos quais um deputado é integrante.

        Retorna uma lista de órgãos, como as comissões e procuradorias,
        dos quais o deputado participa ou participou durante um intervalo
        de tempo.
        Cada item identifica um órgão, o cargo ocupado pelo parlamentar neste
        órgão (como presidente, vice-presidente, titular ou suplente) e as
        datas de início e fim da ocupação deste cargo.
        Se não for passado algum parâmetro de tempo, são retornados os órgãos
        ocupados pelo parlamentar no momento da requisição. Neste caso a
        lista será vazia se o deputado não estiver em exercício.

        Parameters
        ----------
        inicio : str, optional
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim : str, optional
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
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
        ordenar_por : str, default='dataInicio'
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
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")
        if itens is not None:
            params["itens"] = itens

        cols_to_rename = {
            "idOrgao": "codigo",
            "uriOrgao": "uri",
            "siglaOrgao": "sigla",
            "nomeOrgao": "nome",
            "nomePublicacao": "publicacao",
            "titulo": "titulo",
            "codTitulo": "titulo_codigo",
            "dataInicio": "data_inicio",
            "dataFim": "data_fim",
        }

        return Get(
            endpoint="camara",
            path=["deputados", str(self.cod), "orgaos"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["titulo_codigo"],
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

    def profissoes(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """As frentes parlamentares das quais um deputado é integrante.

        Retorna uma lista de dados sobre profissões que o parlamentar declarou
        à Câmara que já exerceu ou que pode exercer pela sua formação e/ou
        experiência.

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
            "idLegislatura": "legislatura",
            "titulo": "titulo",
            "uri": "uri",
            "dataHora": "data",
            "codTipoProfissao": "tipo",
        }

        return Get(
            endpoint="camara",
            path=["deputados", str(self.cod), "profissoes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data"],
            url_cols=["uri"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)


@validate_call
def lista_deputados(
    nome: Optional[str] = None,
    legislatura: Optional[PositiveInt] = None,
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    sexo: Optional[Literal["f", "m"]] = None,
    inicio: Optional[date] = None,
    fim: Optional[date] = None,
    pagina: PositiveInt = 1,
    itens: Optional[PositiveInt] = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Listagem e busca de deputados, segundo critérios.

    Retorna uma lista de dados básicos sobre deputados que estiveram em
    exercício parlamentar em algum intervalo de tempo. Se não for passado um
    parâmetro de tempo, como `legislatura` ou `inicio`, a lista enumerará
    somente os deputados em exercício no momento da requisição.

    Parameters
    ----------
    nome : str, optional
        Parte do nome dos parlamentares.
    legislatura : int, optional
        Número da legislatura a qual os dados buscados devem corresponder.
    uf : str, optional
        Sigla da unidade federativa (estados e Distrito Federal).
        Se None, serão retornados deputados de todos os estados.
    partido : str, optional
        Sigla do partido ao qual sejam filiados os deputados.
        Para obter as siglas válidas, consulte a função `camara.lista_partidos`.
        Atenção: partidos diferentes podem usar a mesma sigla em diferentes
        legislaturas.
    sexo : {'f', 'm'}, optional
        Letra que designe o gênero dos parlamentares que se deseja buscar,
        - 'f': Feminino;
        - 'm': Masculino.
    inicio : str, optional
        Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
    fim : str, optional
        Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
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
    if nome is not None:
        params["nome"] = nome
    if legislatura is not None:
        params["idLegislatura"] = legislatura
    if uf is not None:
        params["siglaUf"] = parse.uf(uf)
    if partido is not None:
        params["siglaPartido"] = partido
    if sexo is not None:
        params["siglaSexo"] = sexo.upper()
    if inicio is not None:
        params["dataInicio"] = parse.data(inicio, "camara")
    if fim is not None:
        params["dataFim"] = parse.data(fim, "camara")
    if itens is not None:
        params["itens"] = itens

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
    }

    return Get(
        endpoint="camara",
        path=["deputados"],
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo", "legislatura"],
        url_cols=["uri", "partido_uri", "foto", "email"],
        remover_url=not url,
        index=index,
        verify=verificar_certificado,
    ).get(formato)
