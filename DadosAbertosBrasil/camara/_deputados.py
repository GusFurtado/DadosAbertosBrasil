from datetime import date
from typing import Literal, Optional

from pydantic import Field, PositiveInt, validate_call

from ..utils.modelos import Maiusculo, SiglaUF, com_params
from ..utils.objeto import Objeto
from ..utils.typing import Formato, Saida
from . import modelos as m
from ._comum import Ordenacao, Periodo, consultar_camara, requisicao


class _ParamsDespesas(Ordenacao):
    legislatura: PositiveInt | None = Field(None, serialization_alias="idLegislatura")
    ano: PositiveInt | None = None
    mes: PositiveInt | None = None
    fornecedor: int | None = Field(None, serialization_alias="cnpjCpfFornecedor")


class _ParamsDiscursos(Ordenacao, Periodo):
    legislatura: PositiveInt | None = Field(None, serialization_alias="idLegislatura")


class _ParamsEventosDeputado(Ordenacao, Periodo):
    legislatura: PositiveInt | None = Field(None, serialization_alias="idLegislatura")


class _ParamsOrgaosDeputado(Ordenacao, Periodo):
    pass


class _ParamsDeputados(Ordenacao, Periodo):
    nome: str | None = None
    legislatura: PositiveInt | None = Field(None, serialization_alias="idLegislatura")
    uf: SiglaUF = Field(None, serialization_alias="siglaUf")
    partido: str | None = Field(None, serialization_alias="siglaPartido")
    sexo: Maiusculo = Field(None, serialization_alias="siglaSexo")


class Deputado(Objeto):
    """Retorna os dados cadastrais de um parlamentar que, em algum momento
    da história e por qualquer período, entrou em exercício na Câmara.

    Parameters
    ----------
    cod : int
        Código do parlamentar.

    verificar_certificado : bool, optional
        Defina como `False` em caso de falha na verificação do certificado
        SSL. Se omitido, usa `DadosAbertosBrasil.config.verificar_certificado`.

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
        Data de falecimento no formato `'AAAA-MM-DD'`.
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
        Data de nascimento no formato `'AAAA-MM-DD'`.

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

    modelo = m.DeputadoDetalhes
    chave_obrigatoria = "ultimoStatus"

    def __init__(self, cod: int, verificar_certificado: bool | None = None):
        self.cod = cod
        self.verify = verificar_certificado
        self._carregar(requisicao(["deputados", cod], verificar_certificado=verificar_certificado))

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.camara: Deputad{'a' if self.sexo == 'F' else 'o'} {self.nome_eleitoral}>"

    def __str__(self) -> str:
        return self.nome

    @com_params(_ParamsDespesas)
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
        formato: Formato | None = None,
    ) -> Saida:
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
            As despesas com exercício parlamentar do deputado.

        """

        return consultar_camara(
            ["deputados", self.cod, "despesas"],
            _ParamsDespesas.de_locais(locals()),
            m.Despesa,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    @com_params(_ParamsDiscursos)
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
        formato: Formato | None = None,
    ) -> Saida:
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
            Data de início de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

        fim : str, optional
            Data de término de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

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
            Os discursos feitos por um deputado em eventos diversos.

        """

        return consultar_camara(
            ["deputados", self.cod, "discursos"],
            _ParamsDiscursos.de_locais(locals()),
            m.Discurso,
            formato,
            url=url,
            verificar_certificado=self.verify,
        )

    @com_params(_ParamsEventosDeputado)
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
        formato: Formato | None = None,
    ) -> Saida:
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
            Data de início de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

        fim : str, optional
            Data de término de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

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
            Uma lista de eventos com a participação do parlamentar.

        """

        return consultar_camara(
            ["deputados", self.cod, "eventos"],
            _ParamsEventosDeputado.de_locais(locals()),
            m.EventoDeputado,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    def frentes(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """As frentes parlamentares das quais um deputado é integrante.

        Retorna uma lista de informações básicas sobre as frentes
        parlamentares das quais o parlamentar seja membro, ou, no caso de
        frentes existentes em legislaturas anteriores, tenha encerrado a
        legislatura como integrante.

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
            As frentes parlamentares das quais um deputado é integrante.

        """

        return consultar_camara(
            ["deputados", self.cod, "frentes"],
            None,
            m.Frente,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    def ocupacoes(
        self,
        formato: Formato | None = None,
    ) -> Saida:
        """Os empregos e atividades que o(a) deputado(a) já teve.

        Enumera as atividades profissionais ou ocupacionais que o deputado
        já teve em sua carreira e declarou à Câmara dos Deputados.

        Parameters
        ----------
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
            Os empregos e atividades que o(a) deputado(a) já teve.

        """

        return consultar_camara(
            ["deputados", self.cod, "ocupacoes"],
            None,
            m.Ocupacao,
            formato,
            verificar_certificado=self.verify,
        )

    @com_params(_ParamsOrgaosDeputado)
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
        formato: Formato | None = None,
    ) -> Saida:
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
            Data de início de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

        fim : str, optional
            Data de término de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

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
            Os órgãos dos quais um deputado é integrante.

        """

        return consultar_camara(
            ["deputados", self.cod, "orgaos"],
            _ParamsOrgaosDeputado.de_locais(locals()),
            m.OrgaoDeputado,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    def profissoes(
        self,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """As frentes parlamentares das quais um deputado é integrante.

        Retorna uma lista de dados sobre profissões que o parlamentar declarou
        à Câmara que já exerceu ou que pode exercer pela sua formação e/ou
        experiência.

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
            As frentes parlamentares das quais um deputado é integrante.

        """

        return consultar_camara(
            ["deputados", self.cod, "profissoes"],
            None,
            m.Profissao,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )


@validate_call
@com_params(_ParamsDeputados)
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
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
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
        Data de início de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

    fim : str, optional
        Data de término de um intervalo de tempo, no formato `'AAAA-MM-DD'`.

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
        Lista de deputados.

    """

    return consultar_camara(
        ["deputados"],
        _ParamsDeputados.de_locais(locals()),
        m.Deputado,
        formato,
        url=url,
        index=index,
        verificar_certificado=verificar_certificado,
    )
