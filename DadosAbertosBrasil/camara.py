"""Módulo para captura dos dados abertos da Câmara dos Deputados do Brasil.

Mini-Tutorial
-------------
1. Importe o módulo `camara`.
>>> from DadosAbertosBrasil import camara

2. Busque o código do objeto de estudo utilizando as funções `lista`.
>>> camara.lista_deputados( ... )

3. Instancie o objeto de estudo utilizando o código encontrado.
>>> dep = camara.Deputado(cod)

4. Utilize os atributos da classe para obter informações básicas do objeto.
>>> dep.dados

5. Utilize os métodos da classe para obter informações detalhadas do objeto.
>>> dep.despesas( ... )

References
----------
.. [1] https://dadosabertos.camara.leg.br/swagger/api.html

"""

from datetime import datetime
from typing import Optional, Union

import pandas as pd

from ._utils import parse
from ._utils.get_data import DAB_Base, get_and_format


class Bloco(DAB_Base):
    """Informações sobre um bloco partidário específico.

    Parameters
    ----------
    cod: int
        Código numérico do bloco partidário do qual se deseja informações.

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

    def __init__(self, cod: int):

        self.cod = cod
        atributos = {"legislatura": ["idLegislatura"], "nome": ["nome"], "uri": ["uri"]}

        super().__init__(
            api="camara",
            path=["blocos", str(cod)],
            unpack_keys=["dados"],
            error_key="nome",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.camara: Bloco {self.nome}>"

    def __str__(self) -> str:
        return f"Bloco {self.nome}"


class Deputado(DAB_Base):
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

    def __init__(self, cod: int):

        self.cod = cod
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
            api="camara",
            path=["deputados", str(cod)],
            unpack_keys=["dados"],
            error_key="ultimoStatus",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.camara: Deputad{'a' if self.sexo == 'F' else 'o'} {self.nome_eleitoral}>"

    def __str__(self) -> str:
        return self.nome

    def despesas(
        self,
        legislatura: Optional[int] = None,
        ano: Optional[int] = None,
        mes: Optional[int] = None,
        fornecedor: Optional[int] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        asc: bool = True,
        ordenar_por: str = "ano",
        url: bool = True,
        index: bool = False,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
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

        return get_and_format(
            api="camara",
            path=["deputados", self.cod, "despesas"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data"],
            url_cols=["url"],
            url=url,
            index=index,
            formato=formato,
        )

    def discursos(
        self,
        legislatura: Optional[int] = None,
        inicio: Union[datetime, str, None] = None,
        fim: Union[datetime, str, None] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
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

        return get_and_format(
            api="camara",
            path=["deputados", self.cod, "discursos"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["evento_uri", "texto_uri", "audio_url", "video_url"],
            url=url,
            formato=formato,
        )

    def eventos(
        self,
        legislatura: Optional[int] = None,
        inicio: Union[datetime, str, None] = None,
        fim: Union[datetime, str, None] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
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

        df = get_and_format(
            api="camara",
            path=["deputados", self.cod, "eventos"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "url"],
            url=url,
            index=index,
            formato=formato,
        )

        if formato == "dataframe":

            def get_orgaos(orgaos):
                cod = [orgao["id"] for orgao in orgaos]
                if len(cod) < 2:
                    return cod[0]
                return cod

            df.orgaos = df.orgaos.apply(get_orgaos)

        return df

    def frentes(
        self, url: bool = True, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
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

        return get_and_format(
            api="camara",
            path=["deputados", self.cod, "frentes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri"],
            url=url,
            index=index,
            formato=formato,
        )

    def ocupacoes(self, formato: str = "dataframe") -> Union[dict, pd.DataFrame]:
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

        return get_and_format(
            api="camara",
            path=["deputados", self.cod, "ocupacoes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            formato=formato,
        )

    def orgaos(
        self,
        inicio: Union[datetime, str, None] = None,
        fim: Union[datetime, str, None] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        asc: bool = True,
        ordenar_por: str = "dataInicio",
        url: bool = True,
        index: bool = False,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
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

        return get_and_format(
            api="camara",
            path=["deputados", self.cod, "orgaos"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["titulo_codigo"],
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri"],
            url=url,
            index=index,
            formato=formato,
        )

    def profissoes(
        self, url: bool = True, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
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

        return get_and_format(
            api="camara",
            path=["deputados", self.cod, "profissoes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data"],
            url_cols=["uri"],
            url=url,
            index=index,
            formato=formato,
        )


class Evento(DAB_Base):
    """Retorna um conjunto detalhado de informações sobre o evento da Câmara.

    Parameters
    ----------
    cod : int
        Código numérico do evento do qual se deseja informações.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.
    cod : int
        Código numérico do evento.
    andar : str
        Andar do prédio onde ocorreu o evento.
    descricao : str
        Descrição do evento.
    descricao_tipo : str
        Tipo do evento.
    fases : str
        Fases do evento.
    fim : str
        Data e horário que o evento foi finalizado no formato 'AAAA-MM-DD'.
    inicio : str
        Data e horário que o evento foi iniciado no formato 'AAAA-MM-DD'.
    local : str
        Local onde ocorreu o evento.
    local_externo : str
        Local externo do evento.
    lista_orgaos : list of dict
        Lista de orgãos e informações sobre os mesmos.
    predio : str
        Prédio que ocorreu o evento.
    requerimentos : list of dict
        Requerimentos do evento.
    sala : str
        Sala do prédio onde ocorreu o evento.
    situacao : str
        Situação do evento.
    uri : str
        Endereço para coleta de dados direta pela API do evento.
    uri_convidados : str
        Endereço para coleta de dados direta pela API dos convidados.
    uri_deputados : str
        Endereço para coleta de dados direta pela API dos deputados.
    url_documento_pauta : str
        Endereço URL para visualizar a pauta do evento.
    url_registro : str
        Endereço URL onde o evento foi registrado.

    Methods
    -------
    deputados()
        Os deputados participantes do evento.
    orgaos()
        Lista de órgãos organizadores do evento.
    pauta()
        Lista de proposições que foram ou deverão ser avaliadas.
    votacoes()
        Informações detalhadas de votações sobre o evento.

    Examples
    --------
    Obter a URL para assistir ao evento #59265.
    >>> ev = camara.Evento(cod=59265)
    >>> ev.url_registro
    ... 'https://www.youtube.com/watch?v=8D2gjMrTnMA'

    """

    def __init__(self, cod: int):

        self.cod = cod
        atributos = {
            "andar": ["localCamara", "andar"],
            "descricao": ["descricao"],
            "descricao_tipo": ["descricaoTipo"],
            "fases": ["fases"],
            "fim": ["dataHoraFim"],
            "inicio": ["dataHoraInicio"],
            "local": ["localCamara", "nome"],
            "local_externo": ["localExterno"],
            "lista_orgaos": ["orgaos"],
            "predio": ["localCamara", "predio"],
            "requerimentos": ["requerimentos"],
            "sala": ["localCamara", "sala"],
            "situacao": ["situacao"],
            "uri": ["uri"],
            "uri_convidados": ["uriConvidados"],
            "uri_deputados": ["uriDeputados"],
            "url_documento_pauta": ["urlDocumentoPauta"],
            "url_registro": ["urlRegistro"],
        }

        super().__init__(
            api="camara",
            path=["eventos", str(cod)],
            unpack_keys=["dados"],
            error_key="localCamara",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Evento {self.descricao}"

    def __str__(self) -> str:
        return self.descricao

    def deputados(
        self, url: bool = True, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
        """Os deputados participantes do evento.

        Retorna uma lista de dados resumidos sobre deputados participantes do
        evento. Se o evento já ocorreu, a lista identifica os deputados que
        efetivamente registraram presença no evento. Se o evento ainda não
        ocorreu, a lista mostra os deputados que devem participar do evento,
        por serem convidados ou por serem membros do(s) órgão(s) responsável
        pelo evento.

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
            "nome": "nome",
            "siglaPartido": "partido",
            "uriPartido": "partido_uri",
            "siglaUf": "uf",
            "idLegislatura": "legislatura",
            "urlFoto": "foto",
            "email": "email",
        }

        return get_and_format(
            api="camara",
            path=["eventos", self.cod, "deputados"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri", "partido_uri", "foto", "email"],
            url=url,
            index=index,
            formato=formato,
        )

    def orgaos(
        self, url: bool = True, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
        """Lista de órgãos organizadores do evento.

        Retorna uma lista em que cada item é um conjunto mínimo de dados sobre
        o(s) órgão(s) responsável(is) pelo evento.

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
            "nome": "nome",
            "siglaPartido": "partido",
            "uriPartido": "partido_uri",
            "siglaUf": "uf",
            "idLegislatura": "legislatura",
            "urlFoto": "foto",
            "email": "email",
        }

        return get_and_format(
            api="camara",
            path=["eventos", self.cod, "orgaos"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri", "partido_uri", "foto", "email"],
            url=url,
            index=index,
            formato=formato,
        )

    def pauta(
        self, url: bool = True, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
        """Lista de proposições que foram ou deverão ser avaliadas em um evento
        de caráter deliberativo.

        Se o evento for de caráter deliberativo (uma reunião ordinária,
        por exemplo) este serviço retorna a lista de proposições previstas
        para avaliação pelos parlamentares. Cada item identifica, se as
        informações estiverem disponíveis, a proposição avaliada, o regime
        de preferência para avaliação, o relator e seu parecer, o resultado
        da apreciação e a votação realizada.

        Parameters
        ----------
        url : bool, default=False
            Se False, remove as colunas contendo URI, URL e e-mails.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        index : bool, default=False
            Se True, define a coluna `ordem` como index do DataFrame.
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
            "ordem": "ordem",
            "topico": "topico",
            "regime": "regime",
            "codRegime": "regime_codigo",
            "titulo": "titulo",
            "proposicao_": "proposicao",
            "relator": "relator",
            "textoParecer": "parecer",
            "proposicaoRelacionada_": "proposicao_relacionada",
            "uriVotacao": "uri",
            "situacaoItem": "situacao",
        }

        return get_and_format(
            api="camara",
            path=["eventos", self.cod, "pauta"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri"],
            url=url,
            index_col="ordem",
            index=index,
            formato=formato,
        )

    def votacoes(
        self, url: bool = True, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
        """Informações detalhadas de votações sobre o evento.

        Retorna uma lista de dados básicos sobre votações que tenham sido
        realizadas no evento. Votações só ocorrem em eventos de caráter
        deliberativo. Dados complementares sobre cada votação listada podem
        ser obtidos no recurso.

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
            "data": "data",
            "dataHoraRegistro": "data_registro",
            "siglaOrgao": "orgao_sigla",
            "uriOrgao": "orgao_uri",
            "uriEvento": "evento_uri",
            "proposicaoObjeto": "proposicao",
            "uriProposicaoObjeto": "proposicao_uri",
            "descricao": "descricao",
            "aprovacao": "aprovacao",
        }

        return get_and_format(
            api="camara",
            path=["eventos", self.cod, "votacoes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data", "data_registro"],
            url_cols=["uri", "orgao_uri", "evento_uri", "proposicao_uri"],
            url=url,
            index=index,
            formato=formato,
        )


class Frente(DAB_Base):
    """Informações detalhadas sobre uma frente parlamentar.

    Parameters
    ----------
    cod : int
        Código numérico da frente parlamentar da qual se deseja informações.

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

    def __init__(self, cod: int):

        self.cod = cod
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
            api="camara",
            path=["frentes", str(cod)],
            unpack_keys=["dados"],
            error_key="titulo",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: {self.titulo}"

    def __str__(self) -> str:
        return self.titulo

    def membros(
        self, url: bool = True, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
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

        return get_and_format(
            api="camara",
            path=["frentes", self.cod, "membros"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "partido_uri", "foto", "email"],
            url=url,
            index=index,
            formato=formato,
        )


class Legislatura(DAB_Base):
    """Informações extras sobre uma determinada legislatura da Câmara.

    Parameters
    ----------
    cod : int
        Código numérico da legislatura da qual se deseja informações.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.
    cod : int
        Código numérico da legislatura.
    inicio : str
        Primeiro dia da legislatura.
    fim : str
        Último dia da legislatura.
    uri : str
        Endereço para coleta de dados direta pela API da legislatura.

    Examples
    --------
    Obter o primeiro e último dia da legislatura #56.
    >>> leg = camara.Legislatura(cod=54)
    >>> leg.inicio
    ... '2011-02-01'
    >>> leg.fim
    ... '2015-01-31'

    """

    def __init__(self, cod: int):

        self.cod = cod
        atributos = {"fim": ["dataFim"], "inicio": ["dataInicio"], "uri": ["uri"]}

        super().__init__(
            api="camara",
            path=["legislaturas", str(cod)],
            unpack_keys=["dados"],
            error_key="dataInicio",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Legislatura {self.cod}"

    def __str__(self) -> str:
        return f"Legislatura {self.cod}"

    def mesa(
        self,
        inicio: Union[datetime, str, None] = None,
        fim: Union[datetime, str, None] = None,
        url: bool = True,
        index: bool = False,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
        """Quais deputados fizeram parte da Mesa Diretora em uma legislatura.

        Retorna uma lista com dados básicos sobre todos os deputados que
        ocuparam algum posto na Mesa Diretora da Câmara em algum período de
        tempo dentro da legislatura. Normalmente, cada legislatura tem duas
        Mesas Diretoras, com presidente, dois vice-presidentes, quatro
        secretários parlamentares e os suplentes dos secretários.

        Parameters
        ----------
        inicio : str, optional
            Dia de início do intervalo de tempo do qual se deseja saber a
            composição da Mesa, no formato 'AAAA-MM-DD'.
        fim : str, optional
            Data de término do intervalo de tempo do qual se deseja saber a
            composição da Mesa, no formato 'AAAA-MM-DD'.
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

        params = {}
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")

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
            "dataInicio": "data_inicio",
            "dataFim": "data_fim",
            "titulo": "titulo",
            "codTitulo": "titulo_codigo",
        }

        return get_and_format(
            api="camara",
            path=["legislaturas", self.cod, "mesa"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["titulo_codigo"],
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "partido_uri", "foto", "email"],
            url=url,
            index=index,
            formato=formato,
        )


class Orgao(DAB_Base):
    """Informações detalhadas sobre um órgão da Câmara.

    Parameters
    ----------
    cod : int
        Código numérico do órgão do qual se deseja informações.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.
    cod : int
        Código numérico do órgão.
    apelido : str
        Apelido do órgão.
    casa : str
        Casa do órgão.
    cod_tipo : int
        Código do tipo do órgão.
    fim : str
        Data final do órgão.
    inicio : str
        Data inicial do órgão.
    instalacao : str
        Data de instalação do órgão.
    nome : str
        Nome do órgão.
    nome_publicacao : str
        Nome de publicação.
    sala : str
        Sala do órgão.
    sigla : str
        Sigla do órgão.
    tipo : str
        Tipo do órgão.
    uri : str
        Endereço para coleta de dados direta pela API do órgão.
    urlWebsite : str
        URL para acessar o website do órgão.

    Examples
    --------
    Obter o apelido do órgão #4.
    >>> org = camara.Orgao(cod=4)
    >>> org.apelido
    ... 'Mesa Diretora'

    """

    def __init__(self, cod: int):

        self.cod = cod
        atributos = {
            "apelido": ["apelido"],
            "casa": ["casa"],
            "cod_tipo": ["codTipoOrgao"],
            "fim": ["dataFim"],
            "inicio": ["dataInicio"],
            "instalacao": ["dataInstalacao"],
            "nome": ["nome"],
            "nome_publicacao": ["nomePublicacao"],
            "sala": ["sala"],
            "sigla": ["sigla"],
            "tipo": ["tipoOrgao"],
            "uri": ["uri"],
            "urlWebsite": ["urlWebsite"],
        }

        super().__init__(
            api="camara",
            path=["orgaos", str(cod)],
            unpack_keys=["dados"],
            error_key="nome",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Órgão {self.nome}"

    def __str__(self) -> str:
        return f"Órgão {self.nome}"

    def eventos(
        self,
        tipo_evento: Optional[str] = None,
        inicio: Union[datetime, str, None] = None,
        fim: Union[datetime, str, None] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        asc: bool = True,
        ordenar_por: str = "dataHoraInicio",
        url: bool = True,
        index: bool = False,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
        """Os eventos ocorridos ou previstos em um órgão legislativo.

        Retorna uma lista de informações resumidas dos eventos realizados
        (ou a realizar) pelo órgão legislativo. Por padrão, são retornados
        eventos em andamento ou previstos para o mesmo dia, dois dias antes
        e dois dias depois da requisição. Parâmetros podem ser passados para
        alterar esse período, bem como os tipos de eventos.

        Parameters
        ----------
        tipo_evento : str, optional
            Identificador numérico do tipo de evento que se deseja obter.
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
            Se True, define a coluna `id` como index do DataFrame.
        formato : {'dataframe', 'json'}, default='dataframe'
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.


        Returns
        -------
        pandas.core.frame.DataFrame
            Lista de discursos feitos por um deputado em eventos diversos.

        """

        params = {
            "pagina": pagina,
            "ordem": "asc" if asc else "desc",
            "ordenarPor": ordenar_por,
        }
        if tipo_evento is not None:
            params["idTipoEvento"] = tipo_evento
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
            "localCamara": "local_camara",
            "urlRegistro": "url",
        }

        return get_and_format(
            api="camara",
            path=["orgaos", self.cod, "eventos"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "url"],
            url=url,
            index=index,
            formato=formato,
        )

    def membros(
        self,
        inicio: Union[datetime, str, None] = None,
        fim: Union[datetime, str, None] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        url: bool = True,
        index: bool = False,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
        """Lista de cargos de um órgão e parlamentares que os ocupam.

        Retorna uma lista de dados resumidos que identificam cada parlamentar
        e o cargo ou posição que ocupa ou ocupou no órgão parlamentar durante
        um certo período de tempo. Se não forem passados parâmetros que
        delimitem esse período, o serviço retorna os membros do órgão no
        momento da requisição. Se o órgão não existir mais ou não estiver
        instalado, é retornada uma lista vazia.

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
            Número máximo de itens na “página” que se deseja obter com esta
            requisição.
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

        params = {"pagina": pagina}
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
            "dataInicio": "data_inicio",
            "dataFim": "data_fim",
            "titulo": "titulo",
            "codTitulo": "titulo_codigo",
        }

        return get_and_format(
            api="camara",
            path=["orgaos", self.cod, "membros"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["titulo_codigo"],
            cols_to_date=["data_inicio", "data_fim"],
            url_cols=["uri", "partido_uri", "foto", "email"],
            url=url,
            index=index,
            formato=formato,
        )

    def votacoes(
        self,
        proposicao: Optional[int] = None,
        inicio: Union[datetime, str, None] = None,
        fim: Union[datetime, str, None] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        asc: bool = False,
        ordenar_por: str = "dataHoraRegistro",
        url: bool = True,
        index: bool = False,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
        """Uma lista de eventos com a participação do parlamentar.

        Retorna uma lista de dados básicos de votações que tenham sido
        realizadas em eventos realizados no órgão. Se este for um órgão
        permanente da Câmara, são retornados, por padrão, dados sobre as
        votações realizadas pelo órgão nos últimos 30 dias. Esse período pode
        ser alterado com o uso dos parâmetros `inicio` e/ou `fim`, que por
        enquanto são limitados a selecionar somente votações ocorridas em um
        mesmo ano.
        Caso este seja um órgão temporário, como uma comissão especial, são
        listadas por padrão todas as votações ocorridas no órgão, em qualquer
        período de tempo.
        Dados complementares sobre cada votação listada podem ser obtidos com
        o objeto `camara.Votacao`.

        Parameters
        ----------
        proposicao : int, optional
            Código numérico da proposição, que podem ser obtidos por meio da
            função `camara.lista_proposicoes`. Se presente, listará as
            votações que tiveram a proposição como objeto de votação ou que
            afetaram as proposições listadas.
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

        params = {
            "pagina": pagina,
            "ordem": "asc" if asc else "desc",
            "ordenarPor": ordenar_por,
        }
        if proposicao is not None:
            params["idProposicao"] = proposicao
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")
        if itens is not None:
            params["itens"] = itens

        cols_to_rename = {
            "aprovacao": "aprovacao",
            "data": "data",
            "dataHoraRegistro": "data_registro",
            "descricao": "descricao",
            "id": "codigo",
            "proposicaoObjeto": "proposicao",
            "siglaOrgao": "orgao",
            "uri": "uri",
            "uriEvento": "evento_uri",
            "uriOrgao": "orgao_uri",
            "uriProposicaoObjeto": "proposicao_uri",
        }

        return get_and_format(
            api="camara",
            path=["orgaos", self.cod, "votacoes"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data", "data_registro"],
            url_cols=["uri", "evento_uri", "orgao_uri", "proposicao_uri"],
            url=url,
            index=index,
            formato=formato,
        )


class Partido(DAB_Base):
    """Informações detalhadas sobre um partido.

    Parameters
    ----------
    cod : int
        Código numérico do partido do qual se deseja informações.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.
    cod : int
        Código numérico do partido.
    facebook : str
        URL da página no Facebook do partido.
    legislatura : str
        Código numérico da última legislatura.
    lider : dict
        Informações sobre o líder do partido.
    logo : str
        URL da logo do partido.
    nome : str
        Nome completo do partido.
    numero : int
        Número eleitoral do partido.
    sigla : str
        Sigla do partido.
    situacao : str
        Situação do partido.
    total_membros : str
        Total de membros do partido.
    total_posse : str
        Total de posse do partido.
    ultima_atualizacao : str
        Última atualização das informações sobre o partido.
    uri : str
        Endereço para coleta de dados direta pela API do partido.
    uri_membros : str
        Endereço para coleta de dados direta pela API dos membros do partido.
    website : str
        URL do website do partido.


    Examples
    --------
    Obter o nome completo do partido #36899.
    >>> p = camara.Partido(cod=36899)
    >>> p.nome
    ... 'Movimento Democrático Brasileiro'

    """

    def __init__(self, cod: int):

        self.cod = cod
        atributos = {
            "facebook": ["urlFacebook"],
            "legislatura": ["status", "idLegislatura"],
            "lider": ["status", "lider"],
            "logo": ["urlLogo"],
            "nome": ["nome"],
            "numero": ["numeroEleitoral"],
            "sigla": ["sigla"],
            "situacao": ["status", "situacao"],
            "total_membros": ["status", "totalMembros"],
            "total_posse": ["status", "totalPosse"],
            "ultima_atualizacao": ["status", "data"],
            "uri": ["uri"],
            "uri_membros": ["status", "uriMembros"],
            "website": ["urlWebSite"],
        }

        super().__init__(
            api="camara",
            path=["partidos", str(cod)],
            unpack_keys=["dados"],
            error_key="status",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: {self.nome}"

    def __str__(self) -> str:
        return self.nome

    def membros(
        self,
        inicio: Union[datetime, str, None] = None,
        fim: Union[datetime, str, None] = None,
        legislatura: Optional[int] = None,
        pagina: int = 1,
        itens: Optional[int] = None,
        ordenar_por: Optional[str] = None,
        asc: bool = True,
        url: bool = True,
        index: bool = False,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
        """Uma lista dos parlamentares de um partido durante um período.

        Retorna uma lista de deputados que estão ou estiveram em exercício
        pelo partido. Opcionalmente, pode-se usar os parâmetros `inicio`,
        `fim` ou `legislatura` para se obter uma lista de deputados filiados
        ao partido num certo intervalo de tempo. Isso é equivalente à função
        `lista_deputados` com filtro por partido, mas é melhor para obter
        informações sobre membros de partidos já extintos.

        Parameters
        ----------
        inicio : str, optional
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim : str, optional
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        legislatura : int, optional
            Número da legislatura, à qual os dados buscados devem corresponder.
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
        ordenar_por : str, optional
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

        params = {"pagina": pagina, "ordem": "asc" if asc else "desc"}
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "camara")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "camara")
        if legislatura is not None:
            params["idLegislatura"] = legislatura
        if itens is not None:
            params["itens"] = itens
        if ordenar_por is not None:
            params["ordenarPor"] = ordenar_por

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

        return get_and_format(
            api="camara",
            path=["partidos", self.cod, "membros"],
            params=params,
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["uri", "partido_uri", "foto", "email"],
            url=url,
            index=index,
            formato=formato,
        )


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
        self, url: bool = True, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
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
        self, url: bool = True, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
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
        self, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
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
        inicio: Union[datetime, str, None] = None,
        fim: Union[datetime, str, None] = None,
        url: bool = True,
        index: bool = False,
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
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
        formato: str = "dataframe",
    ) -> Union[dict, pd.DataFrame]:
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


class Votacao(DAB_Base):
    """Informações detalhadas sobre uma votação da Câmara.

    Retorna um conjunto detalhado de dados sobre a votação, tais como as
    proposições que podem ter sido o objeto da votação e os efeitos de
    tramitação de outras proposições que eventualmente tenham sido cadastrados
    em consequência desta votação.

    Parameters
    ----------
    cod : str
        Código alfa-numérico da votação da qual se deseja informações.

    Attributes
    ----------
    dados : dict
        Conjunto completo de dados.
    cod : str
        Código alfa-numérico da votação.
    aprovacao : int
        Aprovação da votação.
    data : str
        Data da votação.
    data_regitro : str
        Data e horário de registro da votação.
    data_ultima_abertura : str
        Data e horário da última abertura da votação.
    descricao : str
        Descrição da votação.
    efeitos_registrados : list
        Lista de efeitos registrados.
    evento : int
        Código numérico do evento da votação.
    orgao : int
        Código numérico do órgão da votação.
    objetos_possiveis : list of dict
        Lista de objetos possíveis.
    proposicoes_afetadas : str
        Proposições afetadas.
    sigla_orgao : str
        Sigla do órgão.
    ultima_apresentacao_proposicao : dict
        Última apresentação da proposição.
    uri : str
        Endereço para coleta de dados direta pela API da votação.
    uri_evento : str
        Endereço para coleta de dados direta pela API do evento.
    uri_orgao : str
        Endereço para coleta de dados direta pela API do órgão.

    Examples
    --------
    Obter a data da votação #2265603-43.
    >>> vot = camara.Votacao(cod='2265603-43')
    >>> vot.data
    ... '2020-12-22'

    """

    def __init__(self, cod: int):

        self.cod = cod
        atributos = {
            "aprovacao": ["aprovacao"],
            "data": ["data"],
            "data_regitro": ["dataHoraRegistro"],
            "data_ultima_abertura": ["dataHoraUltimaAberturaVotacao"],
            "descricao": ["descricao"],
            "efeitos_registrados": ["efeitosRegistrados"],
            "evento": ["idEvento"],
            "orgao": ["idOrgao"],
            "objetos_possiveis": ["objetosPossiveis"],
            "proposicoes_afetadas": ["proposicoesAfetadas"],
            "sigla_orgao": ["siglaOrgao"],
            "ultima_apresentacao_proposicao": ["ultimaApresentacaoProposicao"],
            "uri": ["uri"],
            "uri_evento": ["uriEvento"],
            "uri_orgao": ["uriOrgao"],
        }

        super().__init__(
            api="camara",
            path=["votacoes", str(cod)],
            unpack_keys=["dados"],
            error_key="descricao",
            atributos=atributos,
        )

    def __repr__(self) -> str:
        return f"DadosAbertosBrasil.camara: Votação {self.cod}"

    def __str__(self) -> str:
        return f"Votação {self.cod}"

    def orientacoes(
        self, url: bool = True, index: bool = False, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
        """O voto recomendado pelas lideranças aos seus deputados na votação.

        Em muitas votações, os líderes de partidos e blocos – as bancadas –
        fazem recomendações de voto para seus parlamentares. Essas orientações
        de uma votação também são feitas pelas lideranças de Governo, Minoria
        e as mais recentes Maioria e Oposição. Uma liderança também pode
        liberar a bancada para que cada deputado vote como quiser, ou entrar
        em obstrução, para que seus parlamentares não sejam contados para o
        quórum da votação.
        Se a votação teve orientações, este recurso retorna uma lista em que
        cada item contém os identificadores de um partido, bloco ou liderança,
        e o posicionamento ou voto que foi recomendado aos seus parlamentares.
        Até o momento, só estão disponíveis dados sobre orientações dadas em
        votações no Plenário.

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
            "orientacaoVoto": "orientacao",
            "codTipoLideranca": "lideranca",
            "siglaPartidoBloco": "bloco",
            "codPartidoBloco": "bloco_codigo",
            "uriPartidoBloco": "bloco_uri",
        }

        return get_and_format(
            api="camara",
            path=["votacoes", self.cod, "orientacoes"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            url_cols=["bloco_uri"],
            url=url,
            index_col="bloco_codigo",
            index=index,
            formato=formato,
        )

    def votos(
        self, url: bool = True, formato: str = "dataframe"
    ) -> Union[dict, pd.DataFrame]:
        """Como cada parlamentar votou em uma votação nominal e aberta.

        Se a votação da Câmara é nominal e não foi secreta, retorna uma lista
        em que cada item contém os identificadores básicos de um deputado e o
        voto ou posicionamento que ele registrou.
        O resultado é uma lista vazia se a votação foi uma votação simbólica,
        em que os votos individuais não são contabilizados. Mas há algumas
        votações simbólicas que também têm registros de "votos": nesses casos,
        normalmente se trata de parlamentares que pediram expressamente que
        seus posicionamentos fossem registrados.
        Não são listados parlamentares ausentes à votação.

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
            "tipoVoto": "voto",
            "dataRegistroVoto": "data",
            "deputado_.id": "deputado_codigo",
            "deputado_.uri": "deputado_uri",
            "deputado_.nome": "deputado_nome",
            "deputado_.siglaPartido": "deputado_partido",
            "deputado_.uriPartido": "deputado_partido_uri",
            "deputado_.siglaUf": "deputado_uf",
            "deputado_.idLegislatura": "deputado_legislatura",
            "deputado_.urlFoto": "deputado_foto",
            "deputado_.email": "deputado_email",
        }

        return get_and_format(
            api="camara",
            path=["votacoes", self.cod, "votos"],
            unpack_keys=["dados"],
            cols_to_rename=cols_to_rename,
            cols_to_date=["data"],
            url_cols=[
                "deputado_uri",
                "deputado_partido_uri",
                "deputado_foto",
                "deputado_email",
            ],
            url=url,
            formato=formato,
        )


def lista_blocos(
    legislatura: Optional[int] = None,
    pagina: int = 1,
    itens: Optional[int] = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    formato: str = "dataframe",
) -> Union[dict, pd.DataFrame]:
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

    return get_and_format(
        api="camara",
        path="blocos",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo", "legislatura"],
        url_cols=["uri"],
        url=url,
        index=index,
        formato=formato,
    )


def lista_deputados(
    nome: Optional[str] = None,
    legislatura: Optional[int] = None,
    uf: Optional[str] = None,
    partido: Optional[str] = None,
    sexo: Optional[str] = None,
    inicio: Union[datetime, str, None] = None,
    fim: Union[datetime, str, None] = None,
    pagina: int = 1,
    itens: Optional[int] = None,
    asc: bool = True,
    ordenar_por: str = "nome",
    url: bool = True,
    index: bool = False,
    formato: str = "dataframe",
) -> Union[dict, pd.DataFrame]:
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
    sexo : {'M', 'F'}, optional
        Letra que designe o gênero dos parlamentares que se deseja buscar,
        - 'M': Masculino;
        - 'F': Feminino.
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
        params["siglaSexo"] = sexo
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

    return get_and_format(
        api="camara",
        path="deputados",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo", "legislatura"],
        url_cols=["uri", "partido_uri", "foto", "email"],
        url=url,
        index=index,
        formato=formato,
    )


def lista_eventos(
    tipo_evento: Optional[int] = None,
    situacao: Optional[int] = None,
    tipo_orgao: Optional[int] = None,
    orgao: Optional[int] = None,
    inicio: Union[datetime, str, None] = None,
    fim: Union[datetime, str, None] = None,
    hora_inicio: Optional[str] = None,
    hora_fim: Optional[str] = None,
    pagina: int = 1,
    itens: Optional[int] = None,
    asc: bool = True,
    ordenar_por: str = "dataHoraInicio",
    url: bool = True,
    index: bool = False,
    formato: str = "dataframe",
) -> Union[dict, pd.DataFrame]:
    """Lista de eventos ocorridos ou previstos nos diversos órgãos da Câmara.

    Retorna uma lista cujos elementos trazem informações básicas sobre eventos
    dos órgãos legislativos da Câmara, previstos ou já ocorridos, em um certo
    intervalo de tempo. Esse intervalo pode ser configurado pelos parâmetros
    de data e hora listados abaixo. Se nenhum for passado, são listados
    eventos dos cinco dias anteriores, dos cinco dias seguintes e do próprio
    dia em que é feita a requisição.

    Parameters
    ----------
    tipo_evento : int, optional
        Identificador numérico do tipo de evento que se deseja obter.
        Os valores válidos podem ser obtidos pela função
        `camara.referencias('tiposEvento')`.
    situacao : int, optional
        Identificador numéricos do tipo de situação de evento.
        Valores válidos podem ser obtidos pela função
        `camara.referencias('situacoesEvento')`.
    tipo_orgao : int, optional
        Identificador numérico do tipo de órgão realizador dos eventos que se
        deseja obter. Os valores válidos podem ser obtidos pela função
        `camara.referencias('tiposOrgao').
    orgao : int, optional
        Identificador numérico do órgão. Os identificadores podem ser obtidos
        pela função `camara.lista_orgaos`.
    inicio : str, optional
        Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
    fim : str, optional
        Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
    hora_inicio : str, optional
        Hora inicial de um intervalo de tempo, no formato 'HH:MM', em horário
        de Brasília.
    hora_fim : str, optional
        Hora final de um intervalo de tempo, no formato 'HH:MM', em horário
        de Brasília.
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

    if tipo_evento is not None:
        params["codTipoEvento"] = tipo_evento
    if situacao is not None:
        params["codSituacao"] = situacao
    if tipo_orgao is not None:
        params["codTipoOrgao"] = tipo_orgao
    if orgao is not None:
        params["idOrgao"] = orgao
    if inicio is not None:
        params["dataInicio"] = parse.data(inicio, "camara")
    if fim is not None:
        params["dataFim"] = parse.data(fim, "camara")
    if hora_inicio is not None:
        params["horaInicio"] = hora_inicio
    if hora_fim is not None:
        params["horaFim"] = hora_fim
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
        "orgaos": "orgaos",
        "urlRegistro": "registro",
        "localExterno": "local_externo",
        "localCamara.nome": "local_nome",
        "localCamara.predio": "local_predio",
        "localCamara.sala": "local_sala",
        "localCamara.andar": "local_andar",
    }

    df = get_and_format(
        api="camara",
        path="eventos",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_date=["data_inicio", "data_fim"],
        url_cols=["uri"],
        url=url,
        index=index,
        formato=formato,
    )

    if formato == "dataframe":

        def get_orgaos(orgaos):
            cod = [orgao["id"] for orgao in orgaos]
            if len(cod) < 2:
                return cod[0]
            return cod

        df.orgaos = df.orgaos.apply(get_orgaos)

    return df


def lista_frentes(
    legislatura: Optional[int] = None,
    pagina: int = 1,
    url: bool = True,
    index: bool = False,
    formato: str = "dataframe",
) -> Union[dict, pd.DataFrame]:
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

    params = {"pagina": pagina}
    if legislatura is not None:
        params["idLegislatura"] = legislatura

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "titulo": "titulo",
        "idLegislatura": "legislatura",
    }

    return get_and_format(
        api="camara",
        path="frentes",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_date=["data_inicio", "date_fim"],
        url_cols=["uri"],
        url=url,
        index=index,
        formato=formato,
    )


def lista_legislaturas(
    data: Optional[str] = None,
    pagina: int = 1,
    itens: Optional[int] = None,
    asc: bool = False,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    formato: str = "dataframe",
) -> Union[dict, pd.DataFrame]:
    """Os períodos de mandatos e atividades parlamentares da Câmara.

    Legislatura é o nome dado ao período de trabalhos parlamentares entre uma
    eleição e outra. Esta função retorna uma lista em que cada item contém as
    informações básicas sobre um desses períodos. Os números que identificam
    as legislaturas são sequenciais, desde a primeira que ocorreu.

    Parameters
    ----------
    data : str, optional
        Data no formato 'AAAA-MM-DD'. Se este parâmetro estiver presente, a
        função retornará as informações básicas sobre a legislatura que estava
        em curso na data informada.
    pagina : int, default=1
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido
        pelo parâmetro `itens`. Se omitido, assume o valor 1.
    itens : int, optional
        Número máximo de itens na página que se deseja obter com esta
        requisição.
    asc : bool, default=False
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
    if data is not None:
        params["data"] = data
    if itens is not None:
        params["itens"] = itens

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "dataInicio": "data_inicio",
        "dataFim": "data_fim",
    }

    return get_and_format(
        api="camara",
        path="legislaturas",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_date=["data_inicio", "data_fim"],
        url_cols=["uri"],
        url=url,
        index=index,
        formato=formato,
    )


def lista_orgaos(
    sigla: Optional[str] = None,
    tipo: Optional[int] = None,
    inicio: Union[datetime, str, None] = None,
    fim: Union[datetime, str, None] = None,
    pagina: int = 1,
    itens: Optional[int] = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    formato: str = "dataframe",
) -> Union[dict, pd.DataFrame]:
    """Lista das comissões e outros órgãos legislativos da Câmara.

    Retorna uma lista de informações básicas sobre os órgãos legislativos e
    seus identificadores, tipos e descrições. É possível filtrar a lista por
    identificadores, tipos de órgãos, sigla, situação do órgão ou período de
    tempo em que os órgãos estiveram ativos, se aplicável.

    Parameters
    ----------
    sigla : str, optional
        Sigla oficialmente usadas para designar o órgão da câmara.
    tipo : int, optional
        Código numérico do tipo de órgãos que se deseja buscar dados. Pode ser
        obtido pela função `camara.referencias`.
    inicio : str, optional
        Data de início, no formato 'AAAA-MM-DD', de um intervalo de tempo no
        qual os órgãos buscados devem ter estado em atividade.
    fim : str, optional
        Data de término, no formato 'AAAA-MM-DD', de um intervalo de tempo no
        qual os órgãos buscados devem ter estado em atividade.
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
    if sigla is not None:
        params["sigla"] = sigla
    if tipo is not None:
        params["codTipoOrgao"] = tipo
    if inicio is not None:
        params["dataInicio"] = parse.data(inicio, "camara")
    if fim is not None:
        params["dataFim"] = parse.data(fim, "camara")
    if itens is not None:
        params["itens"] = itens

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "sigla": "sigla",
        "nome": "nome",
        "apelido": "apelido",
        "codTipoOrgao": "orgao_tipo_codigo",
        "tipoOrgao": "orgao_tipo",
        "nomePublicacao": "nome_publicacao",
    }

    return get_and_format(
        api="camara",
        path="orgaos",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        url_cols=["uri"],
        url=url,
        index=index,
        formato=formato,
    )


def lista_partidos(
    legislatura: Optional[int] = None,
    inicio: Union[datetime, str, None] = None,
    fim: Union[datetime, str, None] = None,
    pagina: int = 1,
    itens: Optional[int] = None,
    asc: bool = True,
    ordenar_por: str = "sigla",
    url: bool = True,
    index: bool = False,
    formato: str = "dataframe",
) -> Union[dict, pd.DataFrame]:
    """Os partidos políticos que têm ou já tiveram parlamentares em exercício
    na Câmara.

    Retorna uma lista de dados básicos sobre os partidos políticos que têm ou
    já tiveram deputados na Câmara. Se não forem passados parâmetros, a função
    retorna os partidos que têm deputados em exercício no momento da
    requisição. É possível obter uma lista de partidos representados na Câmara
    em um certo intervalo de datas ou de legislaturas.

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
    ordenar_por : str, default='sigla'
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

    cols_to_rename = {"id": "codigo", "sigla": "sigla", "nome": "nome", "uri": "uri"}

    return get_and_format(
        api="camara",
        path="partidos",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        url_cols=["uri"],
        url=url,
        index=index,
        formato=formato,
    )


def lista_proposicoes(
    tipo: Optional[str] = None,
    numero: Optional[int] = None,
    ano: Optional[int] = None,
    autor_cod: Optional[int] = None,
    autor_nome: Optional[str] = None,
    partido_sigla: Optional[str] = None,
    partido_cod: Optional[int] = None,
    autor_uf: Optional[str] = None,
    keyword: Optional[str] = None,
    tramitacao_senado: bool = None,
    apresentacao_inicio: Union[datetime, str, None] = None,
    apresentacao_fim: Optional[str] = None,
    situacao: Optional[int] = None,
    tema: Optional[int] = None,
    inicio: Union[datetime, str, None] = None,
    fim: Union[datetime, str, None] = None,
    pagina: int = 1,
    itens: Optional[int] = None,
    asc: bool = True,
    ordenar_por: str = "id",
    url: bool = True,
    index: bool = False,
    formato: str = "dataframe",
) -> Union[dict, pd.DataFrame]:
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
        params["dataApresentacaoInicio"] = apresentacao_inicio
    if apresentacao_fim is not None:
        params["dataApresentacaoFim"] = apresentacao_fim
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


def lista_votacoes(
    proposicao: Optional[int] = None,
    evento: Optional[int] = None,
    orgao: Optional[int] = None,
    inicio: Union[datetime, str, None] = None,
    fim: Union[datetime, str, None] = None,
    pagina: int = 1,
    itens: Optional[int] = None,
    asc: bool = False,
    ordenar_por: str = "dataHoraRegistro",
    url: bool = True,
    index: bool = False,
    formato: str = "dataframe",
) -> Union[dict, pd.DataFrame]:
    """Lista de votações na Câmara.

    Retorna uma lista de informações básicas sobre as votações ocorridas em
    eventos dos diversos órgãos da Câmara. Se não forem passados parâmetros
    que delimitem o intervalo de tempo da pesquisa, são retornados dados sobre
    todas as votações ocorridas nos últimos 30 dias, em eventos de todos os
    órgãos.

    Os parâmetros de data permitem estender o período, mas por enquanto é
    necessário que as duas datas sejam de um mesmo ano. Quando apenas uma
    delas está presente, são retornadas somente as votações ocorridas no mesmo
    ano, antes de `fim` ou após `inicio`.

    Parameters
    ----------
    proposicao : int, optional
        Código numérico da proposição, que podem ser obtidos pela função
        `camara.lista_proposições`. Se presente, listará as votações que
        tiveram a proposição como objeto de votação ou que afetaram as
        proposições listadas.
    evento : int, optional
        Código numérico do evento realizado na Câmara, no qual tenham sido
        realizadas as votações a serem listadas. Os códigos podem ser obtidos
        pela função `camara.lista_eventos`. Somente os eventos deliberativos
        podem ter votações. Os eventos podem ter ocorrido fora do intervalo de
        tempo padrão ou definido por `inicio` e/ou `fim`.
    orgao : int, optional
        Código numérico do órgão da Câmara. Se presente, serão retornadas
        somente votações do órgão enumerado. Os códigos existentes podem ser
        obtidos pela função `camara.lista_orgaos`.
    inicio : str, optional
        Data em formato 'AAAA-MM-DD' para início do intervalo de tempo no qual
        tenham sido realizadas as votações a serem listadas. Se usado sozinho,
        esse parâmetro faz com que sejam retornadas votações ocorridas dessa
        data até o fim do mesmo ano. Se usado com `fim`, as duas datas devem
        ser de um mesmo ano.
    fim : str, optional
        Data em formato 'AAAA-MM-DD' que define o fim do intervalo de tempo no
        qual tenham sido realizadas as votações a serem listadas. Se usado
        sozinho, esse parâmetro faz com que sejam retornadas todas as votações
        ocorridas desde 1º de janeiro do mesmo ano até esta data. Se usado com
        `inicio`, é preciso que as duas datas sejam de um mesmo ano.
    pagina : int, default=1
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido
        pelo parâmetro `itens`. Se omitido, assume o valor 1.
    itens : int, optional
        Número máximo de itens na página que se deseja obter com esta
        requisição.
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

    params = {
        "pagina": pagina,
        "ordem": "asc" if asc else "desc",
        "ordenarPor": ordenar_por,
    }
    if proposicao is not None:
        params["idProposicao"] = proposicao
    if evento is not None:
        params["idEvento"] = evento
    if orgao is not None:
        params["idOrgao"] = orgao
    if inicio is not None:
        params["dataInicio"] = parse.data(inicio, "camara")
    if fim is not None:
        params["dataFim"] = parse.data(fim, "camara")
    if itens is not None:
        params["itens"] = itens

    cols_to_rename = {
        "id": "codigo",
        "uri": "uri",
        "data": "data",
        "dataHoraRegistro": "data_registro",
        "siglaOrgao": "orgao",
        "uriOrgao": "orgao_uri",
        "uriEvento": "evento_uri",
        "proposicaoObjeto": "proposicao",
        "uriProposicaoObjeto": "proposicao_uri",
        "descricao": "descricao",
        "aprovacao": "aprovacao",
    }

    return get_and_format(
        api="camara",
        path="votacoes",
        params=params,
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        cols_to_date=["data", "data_registro"],
        url_cols=["uri", "orgao_uri", "evento_uri", "proposicao_uri"],
        url=url,
        index=index,
        formato=formato,
    )


def referencias(
    lista: str, index: bool = False, formato: str = "dataframe"
) -> Union[dict, pd.DataFrame]:
    """Listas de valores válidos para as funções deste módulo.

    Parameters
    ----------
    lista : str
        Referências que serão listadas. Deve ser uma destas opções:
            - 'autores'
            - 'temas'
            - 'eventos'
            - 'orgaos'
            - 'proposicoes'
            - 'tramitacoes'
            - 'ufs'
            - 'situacoes_deputados'
            - 'situacoes_eventos'
            - 'situacoes_orgaos'
            - 'situacoes_proposicoes'
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

    referencia = {
        "autores": "proposicoes/codTipoAutor",
        "temas": "proposicoes/codTema",
        "eventos": "tiposEvento",
        "orgaos": "tiposOrgao",
        "proposicoes": "tiposProposicao",
        "tramitacoes": "tiposTramitacao",
        "ufs": "uf",
        "situacoes_deputados": "situacoesDeputado",
        "situacoes_eventos": "situacoesEvento",
        "situacoes_orgaos": "situacoesOrgao",
        "situacoes_proposicoes": "situacoesProposicao",
    }

    if lista not in referencia.keys():
        raise TypeError(
            "Referência inválida. Insira um dos seguintes valores para `lista`: "
            + ", ".join(list(referencia.keys()))
        )

    cols_to_rename = {
        "cod": "codigo",
        "sigla": "sigla",
        "nome": "nome",
        "descricao": "descricao",
    }

    return get_and_format(
        api="camara",
        path=["referencias", referencia[lista]],
        unpack_keys=["dados"],
        cols_to_rename=cols_to_rename,
        index=index,
        formato=formato,
    )
