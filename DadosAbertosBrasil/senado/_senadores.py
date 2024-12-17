from datetime import date
from typing import Literal, Optional

from pydantic import validate_call

from ..utils import Base, Get, parse, Formato, Output


class Senador(Base):
    """Coleta os dados dos senadores.

    Parameters
    ----------
    cod : int
        Código de senador que se dejesa consulta.
        O código pode ser encontrado pela função `lista_senadores`.

    Attributes
    ----------
    dados : dict
        Dicionário completo de dados do(a) parlamentar.
    email : str
        E-mail do parlamentar.
    endereco : str
        Endereço da sala do parlamentar no Senado Federal.
    foto : str
        URL para a foto do parlamentar.
    nascimento : str
        Data de nascimento do parlamentar no formato 'AAAA-MM-DD'.
    naturalidade : str
        Município de nascimento do parlamentar.
    nome : str
        Nome do parlamentar.
    nome_completo : str
        Nome completo do parlamentar.
    pagina : str
        Website do parlamentar.
    partido : str
        Atual partido político do parlamentar.
    sexo : str
        Sexo ('Masculino' ou 'Feminino') do parlamentar.
    telefones : list of str
        Lista de telefones oficiais do parlamentar.
    tratamento : str
        Pronome de tratamento usado para o parlamentar.
    uf : str
        Unidade Federativa pela qual o parlamentar foi eleito.
    uf_naturalidade : str
        Unidade Federativa de nascimento do parlamentar.

    Methods
    -------
    apartes()
        Obtém a relação de apartes do senador.
    autorias()
        Obtém as matérias de autoria de um senador.
    cargos()
        Obtém a relação de cargos que o senador ja ocupou.
    comissoes()
        Obtém as comissões de que um senador é membro.
    discursos()
        Obtém a relação de discursos do senador.
    filiacoes()
        Obtém as filiações partidárias que o senador já teve.
    historico()
        Obtém todos os detalhes de um parlamentar no(s) mandato(s) como
        senador (mandato atual e anteriores, se houver).
    mandatos()
        Obtém os mandatos que o senador já teve.
    liderancas()
        Obtém os cargos de liderança de um senador.
    licencas()
        Obtém os cargos de liderança de um senador.
    profissoes()
        Obtém a(s) profissão(ões) de um senador.
    relatorias()
        Obtém as matérias de relatoria de um senador.
    votacoes()
        Obtém as votações de um senador.

    Raises
    ------
    DadosAbertosBrasil._utils.errors.DAB_InputError
        Quando os dados do Senador não forem encontrado, por qualquer que seja
        o motivo.

    References
    ----------
    .. [1] http://legis.senado.gov.br/dadosabertos/docs/

    Examples
    --------
    Utilize as funções `lista` para identificar o código do Senado desejado.

    >>> senado.lista_senadores( ... )
    >>> senado.lista_legislatura( ... )

    Instancie a classe `Senador` para obter as informações do(a) parlamentar.

    >>> sen = senado.Senador(cod)

    Após a class `Senador` ser instanciada, utilize seus métodos e atributos
    para buscar outros tipos de informação sobre ele(a).

    >>> sen.telefones
    >>> sen.partido
    >>> sen.cargos( ... )
    >>> sen.votacoes( ... )
    >>> ...

    """

    def __init__(self, cod: int, verificar_certificado: bool = True):
        self.cod = cod
        self.verify = verificar_certificado
        atributos = {
            "email": ["IdentificacaoParlamentar", "EmailParlamentar"],
            "endereco": ["DadosBasicosParlamentar", "EnderecoParlamentar"],
            "foto": ["IdentificacaoParlamentar", "UrlFotoParlamentar"],
            "nascimento": ["DadosBasicosParlamentar", "DataNascimento"],
            "naturalidade": ["DadosBasicosParlamentar", "Naturalidade"],
            "nome": ["IdentificacaoParlamentar", "NomeParlamentar"],
            "nome_completo": ["IdentificacaoParlamentar", "NomeCompletoParlamentar"],
            "pagina": ["IdentificacaoParlamentar", "UrlPaginaParlamentar"],
            "partido": ["IdentificacaoParlamentar", "SiglaPartidoParlamentar"],
            "sexo": ["IdentificacaoParlamentar", "SexoParlamentar"],
            "tratamento": ["IdentificacaoParlamentar", "FormaTratamento"],
            "uf": ["IdentificacaoParlamentar", "UfParlamentar"],
            "uf_naturalidade": ["DadosBasicosParlamentar", "UfNaturalidade"],
        }

        super().__init__(
            endpoint="senado",
            path=["senador", cod],
            unpack_keys=["DetalheParlamentar", "Parlamentar"],
            error_key="IdentificacaoParlamentar",
            atributos=atributos,
            verify=self.verify,
        )

        if "Telefones" in self.dados:
            lista_telefones = self.dados["Telefones"]["Telefone"]
            if isinstance(lista_telefones, list):
                self.telefones = [fone["NumeroTelefone"] for fone in lista_telefones]
            elif isinstance(lista_telefones, dict):
                self.telefones = [lista_telefones["NumeroTelefone"]]

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.senado: Senador{'a' if self.sexo == 'Feminino' else ''} {self.nome}>"

    def __str__(self) -> str:
        return self.nome_completo

    def apartes(
        self,
        casa: Optional[str] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        numero_sessao: Optional[int] = None,
        tipo_pronunciamento: Optional[str] = None,
        tipo_sessao: Optional[str] = None,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém a relação de apartes do senador.

        Parameters
        ----------
        casa : {'SF', 'CD', 'CN', 'PR', 'CR', 'AC'}, optional
            Sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        inicio :  datetime or str, default=None
            Data inicial do período da pesquisa.
        fim :  datetime or str, default=None
            Data final do período da pesquisa.
        numero_sessao : int, optional
            Número da sessão plenária.
        tipo_pronunciamento : str, optional
            Sigla do tipo de pronunciamento.
        tipo_sessao : str, optional
            Tipo da sessão plenária.
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
        if casa is not None:
            params["casa"] = casa
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "senado")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "senado")
        if numero_sessao is not None:
            params["numeroSessao"] = numero_sessao
        if tipo_pronunciamento is not None:
            params["tipoPronunciamento"] = tipo_pronunciamento
        if tipo_sessao is not None:
            params["tipoSessao"] = tipo_sessao

        cols_to_rename = {
            "CodigoPronunciamento": "codigo",
            "DataPronunciamento": "data",
            "SiglaCasaPronunciamento": "casa_sigla",
            "NomeCasaPronunciamento": "casa_nome",
            "TextoResumo": "resumo",
            "Indexacao": "indexacao",
            "UrlTexto": "url",
            "TipoUsoPalavra.Codigo": "uso_palavra",
            "SessaoPlenaria.CodigoSessao": "sessao",
            "Orador.CodigoParlamentar": "orador",
            "Publicacoes.Publicacao.DescricaoVeiculoPublicacao": "publicacao_veiculo",
            "Publicacoes.Publicacao.DataPublicacao": "publicacao_data",
            "Publicacoes.Publicacao.NumeroPagInicioPublicacao": "publicacao_primeira_pagina",
            "Publicacoes.Publicacao.NumeroPagFimPublicacao": "publicacao_ultima_pagina",
            "Publicacoes.Publicacao.IndicadorRepublicacao": "republicacao",
            "Publicacoes.Publicacao.UrlDiario": "publicacao_url",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "apartes"],
            params=params,
            unpack_keys=["ApartesParlamentar", "Parlamentar", "Apartes", "Aparte"],
            cols_to_rename=cols_to_rename,
            cols_to_int=[
                "codigo",
                "uso_palavra",
                "sessao",
                "orador",
                "publicacao_primeira_pagina",
                "publicacao_ultima_pagina",
            ],
            cols_to_date=["data", "publicacao_data"],
            cols_to_bool=["republicacao"],
            true_value="Sim",
            false_value="Não",
            url_cols=["url", "publicacao_url"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

    def autorias(
        self,
        ano: Optional[int] = None,
        numero: Optional[int] = None,
        primeiro_autor: Optional[bool] = None,
        sigla: Optional[str] = None,
        tramitando: Optional[bool] = None,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém as matérias de autoria de um senador.

        Parameters
        ----------
        ano : int, optional
            Retorna apenas as matérias do ano informado.
        numero : int, optional
            Retorna apenas as matérias do número informado.
        primeiro_autor : bool, optional
            - True: Retorna apenas as matérias cujo senador é o primeiro autor;
            - False: Retorna apenas as que o senador é coautor;
            - None: Retorna ambas.
        sigla : str, optional
            Retorna apenas as matérias da sigla informada.
        tramitando : bool, optional
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.
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
        if ano is not None:
            params["ano"] = ano
        if numero is not None:
            params["numero"] = numero
        if primeiro_autor is not None:
            params["primeiro"] = "S" if primeiro_autor else "N"
        else:
            params["primeiro"] = "T"
        if sigla is not None:
            params["sigla"] = sigla
        if tramitando is not None:
            params["tramitando"] = "S" if tramitando else "N"

        cols_to_rename = {
            "IndicadorAutorPrincipal": "autor_principal",
            "Materia.Codigo": "codigo",
            "Materia.IdentificacaoProcesso": "processo",
            "Materia.DescricaoIdentificacao": "descricao",
            "Materia.Sigla": "sigla",
            "Materia.Numero": "numero",
            "Materia.Ano": "ano",
            "Materia.Ementa": "ementa",
            "Materia.Data": "data",
            "IndicadorOutrosAutores": "outros_autores",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "autorias"],
            params=params,
            unpack_keys=[
                "MateriasAutoriaParlamentar",
                "Parlamentar",
                "Autorias",
                "Autoria",
            ],
            cols_to_rename=cols_to_rename,
            cols_to_int=["codigo", "processo", "ano"],
            cols_to_date=["data"],
            cols_to_bool=["autor_principal", "outros_autores"],
            true_value="Sim",
            false_value="Não",
            index=index,
            verify=self.verify,
        ).get(formato)

    def cargos(
        self,
        comissao: Optional[str] = None,
        ativos: Optional[bool] = None,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém a relação de cargos que o senador ja ocupou.

        Parameters
        ----------
        comissao : str, optional
            Retorna apenas os cargos da sigla de comissão informada.
        ativos : bool, optional
            - True: Retorna apenas os cargos atuais;
            - False: Retorna apenas os cargos já finalizadas;
            - None: Retorna ambos.
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
        if comissao is not None:
            params["comissao"] = comissao
        if ativos is not None:
            params["indAtivos"] = "S" if ativos else "N"

        cols_to_rename = {
            "CodigoCargo": "cargo_codigo",
            "DescricaoCargo": "cargo_descricao",
            "DataInicio": "data_inicio",
            "DataFim": "data_fim",
            "IdentificacaoComissao.CodigoComissao": "comissao_codigo",
            "IdentificacaoComissao.SiglaComissao": "comissao_sigla",
            "IdentificacaoComissao.NomeComissao": "comissao_nome",
            "IdentificacaoComissao.SiglaCasaComissao": "casa",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "cargos"],
            params=params,
            unpack_keys=["CargoParlamentar", "Parlamentar", "Cargos", "Cargo"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["cargo_codigo", "comisao_codigo"],
            cols_to_date=["data_inicio", "data_fim"],
            verify=self.verify,
        ).get(formato)

    def comissoes(
        self,
        comissao: Optional[str] = None,
        ativos: Optional[bool] = None,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém as comissões de que um senador é membro.

        Parameters
        ----------
        comissao : str, optional
            Retorna apenas as comissões com a sigla informada.
        ativos : bool, optional
            - True: Retorna apenas as comissões atuais;
            - False: Retorna apenas as comissões já finalizadas;
            - None: Retorna ambas.
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
        if comissao is not None:
            params["comissao"] = comissao
        if ativos is not None:
            params["indAtivos"] = "S" if ativos else "N"

        cols_to_rename = {
            "DescricaoParticipacao": "participacao",
            "DataInicio": "data_inicio",
            "DataFim": "data_fim",
            "IdentificacaoComissao.CodigoComissao": "comissao_codigo",
            "IdentificacaoComissao.SiglaComissao": "comissao_sigla",
            "IdentificacaoComissao.NomeComissao": "comissao_nome",
            "IdentificacaoComissao.SiglaCasaComissao": "casa",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "comissoes"],
            params=params,
            unpack_keys=[
                "MembroComissaoParlamentar",
                "Parlamentar",
                "MembroComissoes",
                "Comissao",
            ],
            cols_to_rename=cols_to_rename,
            cols_to_int=["comissao_codigo"],
            cols_to_date=["data_inicio", "data_fim"],
            verify=self.verify,
        ).get(formato)

    def cursos(self, formato: Literal["dataframe", "json"] = "dataframe") -> Output:
        """Obtém o histórico acadêmico de um senador.

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
            "NomeCurso": "nome",
            "GrauInstrucao": "grau_instrucao",
            "Estabelecimento": "estabelecimento",
            "Local": "local",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "historicoAcademico"],
            unpack_keys=[
                "HistoricoAcademicoParlamentar",
                "Parlamentar",
                "HistoricoAcademico",
                "Curso",
            ],
            cols_to_rename=cols_to_rename,
            cols_to_bool=["atividade_principal"],
            true_value="Sim",
            false_value="Não",
            verify=self.verify,
        ).get(formato)

    def discursos(
        self,
        casa: Optional[str] = None,
        inicio: Optional[date] = None,
        fim: Optional[date] = None,
        numero_sessao: Optional[int] = None,
        tipo_pronunciamento: Optional[str] = None,
        tipo_sessao: Optional[str] = None,
        url: bool = True,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém a relação de discursos do senador.

        Se os argumentos `inicio` e `fim` não forem informados, retorna os
        pronunciamentos dos últimos 30 dias.

        Parameters
        ----------
        casa : {'SF', 'CD', 'CN', 'PR', 'CR', AC'}, optional
            Sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        inicio : datetime or str, default=None
            Data inicial do período da pesquisa no formato 'AAAA-MM-DD'
        fim : datetime or str, default=None
            Data final do período da pesquisa no formato 'AAAA-MM-DD'
        numero_sessao : int, optional
            Número da sessão plenária.
        tipo_pronunciamento : str, optional
            Sigla do tipo de pronunciamento.
        tipo_sessao : str, optional
            Tipo da sessão plenária.
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
        if casa is not None:
            params["casa"] = casa
        if inicio is not None:
            params["dataInicio"] = parse.data(inicio, "senado")
        if fim is not None:
            params["dataFim"] = parse.data(fim, "senado")
        if numero_sessao is not None:
            params["numeroSessao"] = numero_sessao
        if tipo_pronunciamento is not None:
            params["tipoPronunciamento"] = tipo_pronunciamento
        if tipo_sessao is not None:
            params["tipoSessao"] = tipo_sessao

        cols_to_rename = {
            "CodigoPronunciamento": "codigo",
            "DataPronunciamento": "data",
            "SiglaCasaPronunciamento": "casa_sigla",
            "NomeCasaPronunciamento": "casa_nome",
            "TextoResumo": "resumo",
            "Indexacao": "indexacao",
            "UrlTexto": "url",
            "TipoUsoPalavra.Codigo": "uso_palavra",
            "SessaoPlenaria.CodigoSessao": "sessao",
            "Publicacoes.Publicacao.DescricaoVeiculoPublicacao": "publicacao_veiculo",
            "Publicacoes.Publicacao.DataPublicacao": "publicacao_data",
            "Publicacoes.Publicacao.NumeroPagInicioPublicacao": "publicacao_primeira_pagina",
            "Publicacoes.Publicacao.NumeroPagFimPublicacao": "publicacao_ultima_pagina",
            "Publicacoes.Publicacao.IndicadorRepublicacao": "republicacao",
            "Publicacoes.Publicacao.UrlDiario": "publicacao_url",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "discursos"],
            params=params,
            unpack_keys=[
                "DiscursosParlamentar",
                "Parlamentar",
                "Pronunciamentos",
                "Pronunciamento",
            ],
            cols_to_rename=cols_to_rename,
            cols_to_int=[
                "codigo",
                "uso_palavra",
                "sessao",
                "publicacao_primeira_pagina",
                "publicacao_ultima_pagina",
            ],
            cols_to_date=["data", "publicacao_data"],
            cols_to_bool=["republicacao"],
            true_value="Sim",
            false_value="Não",
            url_cols=["url", "publicacao_url"],
            remover_url=not url,
            index=index,
            verify=self.verify,
        ).get(formato)

    def filiacoes(
        self,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém as filiações partidárias que o senador já teve.

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
            "Partido.CodigoPartido": "codigo",
            "Partido.SiglaPartido": "sigla",
            "Partido.NomePartido": "nome",
            "DataFiliacao": "data_filiacao",
            "DataDesfiliacao": "data_desfiliacao",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "filiacoes"],
            unpack_keys=["FiliacaoParlamentar", "Parlamentar", "Filiacoes", "Filiacao"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["codigo"],
            cols_to_date=["data_filiacao", "data_desfiliacao"],
            index=index,
            verify=self.verify,
        ).get(formato)

    def historico(self) -> dict:
        """Obtém todos os detalhes de um parlamentar no(s) mandato(s) como
        senador (mandato atual e anteriores, se houver).

        Returns
        -------
        dict
            Dados históricos do(a) parlamentar.

        """

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "historico"],
            unpack_keys=["DetalheParlamentar", "Parlamentar"],
            formato="json",
        )

    def mandatos(
        self,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém os mandatos que o senador já teve.

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
            "CodigoMandato": "codigo",
            "UfParlamentar": "uf",
            "DescricaoParticipacao": "participacao",
            "PrimeiraLegislaturaDoMandato.NumeroLegislatura": "primeira_legislatura",
            "PrimeiraLegislaturaDoMandato.DataInicio": "primeira_legislatura_inicio",
            "PrimeiraLegislaturaDoMandato.DataFim": "primeira_legislatura_fim",
            "SegundaLegislaturaDoMandato.NumeroLegislatura": "segunda_legislatura",
            "SegundaLegislaturaDoMandato.DataInicio": "segunda_legislatura_inicio",
            "SegundaLegislaturaDoMandato.DataFim": "segunda_legislatura_fim",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "mandatos"],
            unpack_keys=["MandatoParlamentar", "Parlamentar", "Mandatos", "Mandato"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["codigo"],
            cols_to_date=[
                "primeira_legislatura_inicio",
                "primeira_legislatura_fim",
                "segunda_legislatura_inicio",
                "segunda_legislatura_fim",
            ],
            index=index,
            verify=self.verify,
        ).get(formato)

    def liderancas(self, formato: Literal["dataframe", "json"] = "dataframe") -> Output:
        """Obtém os cargos de liderança de um senador.

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
            "UnidadeLideranca": "lideranca",
            "DescricaoTipoLideranca": "tipo",
            "SiglaCasaLideranca": "casa_sigla",
            "NomeCasaLideranca": "casa_nome",
            "DataDesignacao": "data_designacao",
            "DataFim": "data_fim",
            "Partido.CodigoPartido": "partido_codigo",
            "Partido.SiglaPartido": "partido_sigla",
            "Partido.NomePartido": "partido_nome",
            "Bloco.CodigoBloco": "bloco_codigo",
            "Bloco.SiglaBloco": "bloco_sigla",
            "Bloco.NomeBloco": "bloco_nome",
            "Bloco.ApelidoBloco": "bloco_apelido",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "liderancas"],
            unpack_keys=[
                "LiderancaParlamentar",
                "Parlamentar",
                "Liderancas",
                "Lideranca",
            ],
            cols_to_rename=cols_to_rename,
            cols_to_int=["partido_codigo", "bloco_codigo"],
            cols_to_date=["data_designacao", "data_fim"],
            verify=self.verify,
        ).get(formato)

    def licencas(
        self,
        inicio: Optional[date] = None,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém as licenças de um senador.

        Parameters
        ----------
        inicio : datetime or str, default=None
            Retorna as licenças a partir da data especificada.
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
            "Codigo": "codigo",
            "DataInicio": "inicio",
            "DataInicioPrevista": "inicio_previsto",
            "DataFim": "fim",
            "DataFimPrevista": "fim_previsto",
            "SiglaTipoAfastamento": "afastamento_sigla",
            "DescricaoTipoAfastamento": "afastamento_descricao",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "licencas"],
            params=(
                {"dataInicio": parse.data(inicio, "senado")}
                if inicio is not None
                else {}
            ),
            unpack_keys=["LicencaParlamentar", "Parlamentar", "Licencas", "Licenca"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["codigo"],
            cols_to_date=["inicio", "inicio_previsto", "fim", "fim_previsto"],
            index=index,
            verify=self.verify,
        ).get(formato)

    def profissoes(self, formato: Literal["dataframe", "json"] = "dataframe") -> Output:
        """Obtém a(s) profissão(ões) de um senador.

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
            "NomeProfissao": "nome",
            "IndicadorAtividadePrincipal": "atividade_principal",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "profissao"],
            unpack_keys=[
                "ProfissaoParlamentar",
                "Parlamentar",
                "Profissoes",
                "Profissao",
            ],
            cols_to_rename=cols_to_rename,
            cols_to_bool=["atividade_principal"],
            true_value="Sim",
            false_value="Não",
            verify=self.verify,
        ).get(formato)

    def relatorias(
        self,
        ano: Optional[int] = None,
        comissao: Optional[str] = None,
        numero: Optional[int] = None,
        sigla: Optional[str] = None,
        tramitando: Optional[bool] = None,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém as matérias de relatoria de um senador.

        Parameters
        ----------
        ano : int, optional
            Retorna apenas as matérias do ano informado.
        comissao : str, optional
            Retorna apenas as relatorias da comissão informada.
        numero : int, optional
            Retorna apenas as matérias do número informado.
        sigla : str, optional
            Retorna apenas as matérias da sigla informada.
        tramitando : bool, optional
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.
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
        if ano is not None:
            params["ano"] = ano
        if comissao is not None:
            params["comissao"] = comissao
        if numero is not None:
            params["numero"] = numero
        if sigla is not None:
            params["sigla"] = sigla
        if tramitando is not None:
            params["tramitando"] = "S" if tramitando else "N"

        cols_to_rename = {
            "Materia.Codigo": "materia",
            "Comissao.Codigo": "comissao",
            "CodigoTipoRelator": "codigo",
            "DescricaoTipoRelator": "descricao",
            "DataDesignacao": "data_designacao",
            "DataDestituicao": "data_destituicao",
            "DescricaoMotivoDestituicao": "motivo_destituicao",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "relatorias"],
            params=params,
            unpack_keys=[
                "MateriasRelatoriaParlamentar",
                "Parlamentar",
                "Relatorias",
                "Relatoria",
            ],
            cols_to_rename=cols_to_rename,
            cols_to_int=["codigo", "materia", "comissao"],
            cols_to_date=["data_designacao", "data_destituicao"],
            verify=self.verify,
        ).get(formato)

    def votacoes(
        self,
        ano: Optional[int] = None,
        numero: Optional[int] = None,
        sigla: Optional[str] = None,
        tramitando: Optional[bool] = None,
        index: bool = False,
        formato: Formato = "pandas",
    ) -> Output:
        """Obtém as votações de um senador.

        Parameters
        ----------
        ano : int, optional
            Retorna apenas as matérias do ano informado.
        numero : int, optional
            Retorna apenas as matérias do número informado.
        sigla : str, optional
            Retorna apenas as matérias da sigla informada.
        tramitando : bool, optional
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.
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
        if ano is not None:
            params["ano"] = ano
        if numero is not None:
            params["numero"] = numero
        if sigla is not None:
            params["sigla"] = sigla
        if tramitando is not None:
            params["tramitando"] = "S" if tramitando else "N"

        cols_to_rename = {
            "CodigoSessaoVotacao": "codigo",
            "SessaoPlenaria.CodigoSessao": "sessao",
            "Materia.Codigo": "materia",
            "Tramitacao.IdentificacaoTramitacao.CodigoTramitacao": "tramitacao",
            "Sequencial": "sequencial",
            "DescricaoVotacao": "descricao",
            "IndicadorVotacaoSecreta": "votacao_secreta",
            "SiglaDescricaoVoto": "voto",
            "DescricaoResultado": "resultado",
        }

        return Get(
            endpoint="senado",
            path=["senador", str(self.cod), "votacoes"],
            params=params,
            unpack_keys=["VotacaoParlamentar", "Parlamentar", "Votacoes", "Votacao"],
            cols_to_rename=cols_to_rename,
            cols_to_int=["sequencial", "votacao", "sessao", "materia", "tramitacao"],
            cols_to_bool=["votacao_secreta"],
            true_value="Sim",
            false_value="Não",
            index=index,
            verify=self.verify,
        ).get(formato)


@validate_call
def lista_senadores(
    tipo: str = "atual",
    uf: Optional[str] = None,
    sexo: Optional[Literal["f", "m"]] = None,
    partido: Optional[str] = None,
    contendo: Optional[str] = None,
    excluindo: Optional[str] = None,
    url: bool = True,
    index: bool = False,
    formato: Formato = "pandas",
    verificar_certificado: bool = True,
) -> Output:
    """Lista de senadores da república.

    Parameters
    ----------
    tipo : {'atual', 'titulares', 'suplentes', 'afastados'}
        - 'atual': Todos os senadores em exercício;
        - 'titulares': Apenas senadores que iniciaram o mandato como titulares;
        - 'suplentes': Apenas senadores que iniciaram o mandato como suplentes;
        - 'afastados': Todos os senadores afastados.
    uf : str, optional
        Filtro de Unidade Federativa dos senadores.
    sexo : {'F', 'M'}, optional
        Filtro de sexo dos senadores.
    partido : str, optional
        Filtro de partido dos senadores.
    contendo : str, optional
        Captura apenas senadores contendo esse texto no nome.
    excluindo : str, optional
        Exclui da consulta senadores contendo esse texto no nome.
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

    Raises
    ------
    DAB_UFError
        Caso seja inserida uma UF inválida no argumento `uf`.

    See Also
    --------
    DadosAbertosBrasil.senado.Senador
        Use o `codigo` para obter um detalhamento do senador.
    DadosAbertosBrasil.senado.lista_legislatura
        Pesquisa por senadores de outras legislaturas, além da atual.
    DadosAbertosBrasil.camara.lista_deputados
        Função similar para o módulo `camara`.
    
    Examples
    --------
    Lista todos os senadores ativos, colocando o código como index da tabela.

    >>> senado.lista_senadores(index=True)
                   nome_parlamentar                nome_completo \
    codigo                                                         
    4981               Acir Gurgacz          Acir Marcos Gurgacz
    5982          Alessandro Vieira            Alessandro Vieira
    945                 Alvaro Dias        Alvaro Fernandes Dias
    ...                         ...                          ...

    Lista senadores do partido PL do Rio de Janeiro.

    >>> senado.lista_senadores(partido='PL', uf='RJ')
      codigo nome_parlamentar              nome_completo       sexo \
    0   5936  Carlos Portinho  Carlos Francisco Portinho  Masculino
    1   5322          Romário     Romario de Souza Faria  Masculino

    Lista senadores contendo 'Gomes' no nome, exceto os que contém 'Cid'.

    >>> senado.lista_senadores(contendo='Gomes', excluindo='Cid')
      codigo nome_parlamentar                nome_completo       sexo \
    0   3777    Eduardo Gomes  Carlos Eduardo Torres Gomes  Masculino
    1   5979     Leila Barros   Leila Gomes de Barros Rêgo   Feminino
    2   5557     Mailza Gomes        Mailza Assis da Silva   Feminino

    Lista senadoras afastadas do sexo feminino.

    >>> senado.lista_senadores(tipo='afastados', sexo='F')
      codigo nome_parlamentar                    nome_completo      sexo \
    0   3713   Fátima Bezerra          Maria de Fátima Bezerra  Feminino
    1   5929      Juíza Selma       Selma Rosane Santos Arruda  Feminino
    2   5997     Nailde Panta  Nailde Fernandes Panta da Silva  Feminino
    ..   ...              ...                              ...       ...
    
    """

    tipo = tipo.lower()
    TIPOS = {
        "titulares": {
            "path": "atual",
            "key": "ListaParlamentarEmExercicio",
            "params": {"participacao": "T"},
        },
        "suplentes": {
            "path": "atual",
            "key": "ListaParlamentarEmExercicio",
            "params": {"participacao": "S"},
        },
        "atual": {"path": "atual", "key": "ListaParlamentarEmExercicio", "params": {}},
        "afastados": {"path": "afastados", "key": "AfastamentoAtual", "params": {}},
    }

    params = TIPOS[tipo]["params"]
    if uf is not None:
        params["uf"] = parse.uf(uf=uf)

    cols_to_rename = {
        "IdentificacaoParlamentar.CodigoParlamentar": "codigo",
        "IdentificacaoParlamentar.NomeParlamentar": "nome_parlamentar",
        "IdentificacaoParlamentar.NomeCompletoParlamentar": "nome_completo",
        "IdentificacaoParlamentar.SexoParlamentar": "sexo",
        "IdentificacaoParlamentar.FormaTratamento": "forma_tratamento",
        "IdentificacaoParlamentar.UrlFotoParlamentar": "foto",
        "IdentificacaoParlamentar.UrlPaginaParlamentar": "pagina_parlamentar",
        "IdentificacaoParlamentar.UrlPaginaParticular": "pagina_particular",
        "IdentificacaoParlamentar.EmailParlamentar": "email",
        "IdentificacaoParlamentar.SiglaPartidoParlamentar": "partido",
        "Mandato.UfParlamentar": "uf",
        "Mandato.Exercicios.Exercicio.DataInicio": "data_inicio",
        "Mandato.Exercicios.Exercicio.DataFim": "data_fim",
        "Mandato.Exercicios.Exercicio.DescricaoCausaAfastamento": "causa_afastamento",
    }

    data = Get(
        endpoint="senado",
        path=["senador", "lista", TIPOS[tipo]["path"]],
        params=params,
        unpack_keys=[TIPOS[tipo]["key"], "Parlamentares", "Parlamentar"],
        cols_to_rename=cols_to_rename,
        cols_to_int=["codigo"],
        cols_to_date=["data_inicio", "data_fim"],
        url_cols=["foto", "pagina_parlamentar", "pagina_particular", "email"],
        remover_url=not url,
        index=index,
        verify=verificar_certificado,
    ).get(formato)

    if formato == "pandas":
        if sexo is not None:
            SEXOS = {"m": "Masculino", "f": "Feminino"}
            data = data[data["sexo"] == SEXOS[sexo]]

        if (uf is not None) and (tipo == "afastados"):
            data = data[data["uf"] == parse.uf(uf=uf)]

        if partido is not None:
            data = data[data["partido"] == partido.upper()]

        if contendo is not None:
            nome_parlamentar = data["nome_parlamentar"].str.contains(contendo)
            nome_completo = data["nome_completo"].str.contains(contendo)
            data = data[nome_parlamentar | nome_completo]

        if excluindo is not None:
            nome_parlamentar = ~data["nome_parlamentar"].str.contains(excluindo)
            nome_completo = ~data["nome_completo"].str.contains(excluindo)
            data = data[nome_parlamentar | nome_completo]

    return data
