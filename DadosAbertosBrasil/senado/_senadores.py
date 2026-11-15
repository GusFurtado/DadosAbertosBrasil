from datetime import date
from typing import Any, Literal, overload

from pydantic import Field, PositiveInt, computed_field, validate_call

from ..utils.modelos import Maiusculo, SiglaUF, com_params
from ..utils.objeto import Objeto
from ..utils.typing import DataFramePandas, DataFramePolars, Formato, Saida
from . import modelos as m
from ._comum import ParamsSenado, consultar_senado, filtro_parlamentares, requisicao


class _ParamsPronunciamentos(ParamsSenado):
    casa: Maiusculo = None
    inicio: date | None = Field(None, serialization_alias="dataInicio")
    fim: date | None = Field(None, serialization_alias="dataFim")
    numero_sessao: int | None = Field(None, serialization_alias="numeroSessao")
    tipo_pronunciamento: str | None = Field(None, serialization_alias="tipoPronunciamento")
    tipo_sessao: str | None = Field(None, serialization_alias="tipoSessao")


class _ParamsMaterias(ParamsSenado):
    ano: PositiveInt | None = None
    numero: int | None = None
    sigla: str | None = None
    tramitando: bool | None = None


class _ParamsAutorias(_ParamsMaterias):
    primeiro_autor: bool | None = Field(None, exclude=True)

    @computed_field
    @property
    def primeiro(self) -> str:
        if self.primeiro_autor is None:
            return "T"
        return "S" if self.primeiro_autor else "N"


class _ParamsRelatorias(_ParamsMaterias):
    comissao: str | None = None


class _ParamsComissoes(ParamsSenado):
    comissao: str | None = None
    ativos: bool | None = Field(None, serialization_alias="indAtivos")


class _ParamsLicencas(ParamsSenado):
    inicio: date | None = Field(None, serialization_alias="dataInicio")


class _ParamsSenadores(ParamsSenado):
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = Field("atual", exclude=True)
    uf: SiglaUF = None
    sexo: Literal["f", "m"] | None = Field(None, exclude=True)
    partido: str | None = Field(None, exclude=True)
    contendo: str | None = Field(None, exclude=True)
    excluindo: str | None = Field(None, exclude=True)

    @computed_field
    @property
    def participacao(self) -> str | None:
        return {"titulares": "T", "suplentes": "S"}.get(self.tipo)

    def para_api(self) -> dict:
        params = super().para_api()
        # A lista de afastados não aceita `uf`: o filtro é feito pelo pacote.
        if self.tipo == "afastados":
            params.pop("uf", None)
        return params


_TIPOS_SENADORES = {
    "titulares": ("atual", "ListaParlamentarEmExercicio"),
    "suplentes": ("atual", "ListaParlamentarEmExercicio"),
    "atual": ("atual", "ListaParlamentarEmExercicio"),
    "afastados": ("afastados", "AfastamentoAtual"),
}


class Senador(Objeto):
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
        Data de nascimento do parlamentar no formato `"AAAA-MM-DD"`.

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
    DadosAbertosBrasil._utils.errors.DABInputError
        Quando os dados do Senador não forem encontrado, por qualquer que seja
        o motivo.

    Notes
    -----
    https://legis.senado.gov.br/dadosabertos/docs/

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

    modelo = m.SenadorDetalhes
    chave_obrigatoria = "IdentificacaoParlamentar"

    def __init__(self, cod: int, verificar_certificado: bool | None = None):
        self.cod = cod
        self.verify = verificar_certificado
        self._carregar(
            requisicao(["senador", cod], ["DetalheParlamentar", "Parlamentar"], verificar_certificado=verificar_certificado)
        )
        telefones = (self.dados.get("Telefones") or {}).get("Telefone")
        if isinstance(telefones, dict):
            telefones = [telefones]
        if telefones:
            self.telefones = [fone["NumeroTelefone"] for fone in telefones]

    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.senado: Senador{'a' if self.sexo == 'Feminino' else ''} {self.nome}>"

    def __str__(self) -> str:
        return self.nome_completo

    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        formato: Literal["bruto"] | None = ...,
    ) -> Any: ...

    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...

    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Aparte]: ...

    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...

    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...

    @overload
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["url"],
    ) -> str: ...

    @com_params(_ParamsPronunciamentos)
    def apartes(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Obtém a relação de apartes do senador.

        Parameters
        ----------
        casa : {"sf", "cd", "cn", "pr", "cr", "ac"}, optional
            Sigla da casa aonde ocorre o pronunciamento:
            - "sf": Senado;
            - "cd": Câmara;
            - "cn": Congresso;
            - "pr": Presidência;
            - "cr": Comissão Representativa do Congresso;
            - "ac": Assembléia Constituinte.

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
            Apartes do senador.

        """

        return consultar_senado(
            ["senador", self.cod, "apartes"],
            ["ApartesParlamentar", "Parlamentar", "Apartes", "Aparte"],
            _ParamsPronunciamentos.de_locais(locals()),
            m.Aparte,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    @overload
    def autorias(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        primeiro_autor: bool | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        formato: Literal["bruto"] | None = ...,
    ) -> Any: ...

    @overload
    def autorias(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        primeiro_autor: bool | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...

    @overload
    def autorias(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        primeiro_autor: bool | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Autoria]: ...

    @overload
    def autorias(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        primeiro_autor: bool | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...

    @overload
    def autorias(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        primeiro_autor: bool | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...

    @overload
    def autorias(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        primeiro_autor: bool | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["url"],
    ) -> str: ...

    @com_params(_ParamsAutorias)
    def autorias(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        primeiro_autor: bool | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
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
            Matérias de autoria do senador.

        """

        return consultar_senado(
            ["senador", self.cod, "autorias"],
            ["MateriasAutoriaParlamentar", "Parlamentar", "Autorias", "Autoria"],
            _ParamsAutorias.de_locais(locals()),
            m.Autoria,
            formato,
            index=index,
            verificar_certificado=self.verify,
        )

    @overload
    def cargos(
        self, comissao: str | None = ..., ativos: bool | None = ..., formato: Literal["bruto"] | None = ...
    ) -> Any: ...

    @overload
    def cargos(
        self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["json"]
    ) -> list[dict[str, Any]]: ...

    @overload
    def cargos(
        self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["pydantic"]
    ) -> list[m.Cargo]: ...

    @overload
    def cargos(
        self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["pandas"]
    ) -> DataFramePandas: ...

    @overload
    def cargos(
        self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["polars"]
    ) -> DataFramePolars: ...

    @overload
    def cargos(self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["url"]) -> str: ...

    @com_params(_ParamsComissoes)
    def cargos(
        self,
        comissao: str | None = None,
        ativos: bool | None = None,
        formato: Formato | None = None,
    ) -> Saida:
        """Obtém a relação de cargos que o senador ja ocupou.

        Parameters
        ----------
        comissao : str, optional
            Retorna apenas os cargos da sigla de comissão informada.

        ativos : bool, optional
            - True: Retorna apenas os cargos atuais;
            - False: Retorna apenas os cargos já finalizadas;
            - None: Retorna ambos.

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
            Relação de cargos que o senador já ocupou.

        """

        return consultar_senado(
            ["senador", self.cod, "cargos"],
            ["CargoParlamentar", "Parlamentar", "Cargos", "Cargo"],
            _ParamsComissoes.de_locais(locals()),
            m.Cargo,
            formato,
            verificar_certificado=self.verify,
        )

    @overload
    def comissoes(
        self, comissao: str | None = ..., ativos: bool | None = ..., formato: Literal["bruto"] | None = ...
    ) -> Any: ...

    @overload
    def comissoes(
        self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["json"]
    ) -> list[dict[str, Any]]: ...

    @overload
    def comissoes(
        self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["pydantic"]
    ) -> list[m.MembroComissao]: ...

    @overload
    def comissoes(
        self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["pandas"]
    ) -> DataFramePandas: ...

    @overload
    def comissoes(
        self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["polars"]
    ) -> DataFramePolars: ...

    @overload
    def comissoes(self, comissao: str | None = ..., ativos: bool | None = ..., *, formato: Literal["url"]) -> str: ...

    @com_params(_ParamsComissoes)
    def comissoes(
        self,
        comissao: str | None = None,
        ativos: bool | None = None,
        formato: Formato | None = None,
    ) -> Saida:
        """Obtém as comissões de que um senador é membro.

        Parameters
        ----------
        comissao : str, optional
            Retorna apenas as comissões com a sigla informada.

        ativos : bool, optional
            - True: Retorna apenas as comissões atuais;
            - False: Retorna apenas as comissões já finalizadas;
            - None: Retorna ambas.

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
            Comissões que o senador é membro.

        """

        return consultar_senado(
            ["senador", self.cod, "comissoes"],
            ["MembroComissaoParlamentar", "Parlamentar", "MembroComissoes", "Comissao"],
            _ParamsComissoes.de_locais(locals()),
            m.MembroComissao,
            formato,
            verificar_certificado=self.verify,
        )

    @overload
    def cursos(self, formato: Literal["bruto"] | None = ...) -> Any: ...

    @overload
    def cursos(self, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...

    @overload
    def cursos(self, *, formato: Literal["pydantic"]) -> list[m.Curso]: ...

    @overload
    def cursos(self, *, formato: Literal["pandas"]) -> DataFramePandas: ...

    @overload
    def cursos(self, *, formato: Literal["polars"]) -> DataFramePolars: ...

    @overload
    def cursos(self, *, formato: Literal["url"]) -> str: ...

    def cursos(self, formato: Formato | None = None) -> Saida:
        """Obtém o histórico acadêmico de um senador.

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
            Histórico acadêmico do senador.

        """

        return consultar_senado(
            ["senador", self.cod, "historicoAcademico"],
            ["HistoricoAcademicoParlamentar", "Parlamentar", "HistoricoAcademico", "Curso"],
            None,
            m.Curso,
            formato,
            verificar_certificado=self.verify,
        )

    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        formato: Literal["bruto"] | None = ...,
    ) -> Any: ...

    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...

    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Discurso]: ...

    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...

    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...

    @overload
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = ...,
        inicio: date | None = ...,
        fim: date | None = ...,
        numero_sessao: int | None = ...,
        tipo_pronunciamento: str | None = ...,
        tipo_sessao: str | None = ...,
        url: bool = ...,
        index: bool = ...,
        *,
        formato: Literal["url"],
    ) -> str: ...

    @com_params(_ParamsPronunciamentos)
    def discursos(
        self,
        casa: Literal["sf", "cd", "cn", "pr", "cr", "ac"] | None = None,
        inicio: date | None = None,
        fim: date | None = None,
        numero_sessao: int | None = None,
        tipo_pronunciamento: str | None = None,
        tipo_sessao: str | None = None,
        url: bool = True,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Obtém a relação de discursos do senador.

        Se os argumentos `inicio` e `fim` não forem informados, retorna os
        pronunciamentos dos últimos 30 dias.

        Parameters
        ----------
        casa : {"sf", "cd", "cn", "pr", "cr", "ac"}, optional
            Sigla da casa aonde ocorre o pronunciamento:
            - "sf": Senado;
            - "cd": Câmara;
            - "cn": Congresso;
            - "pr": Presidência;
            - "cr": Comissão Representativa do Congresso;
            - "ac": Assembléia Constituinte.

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
            Relação de discursos do senador.

        """

        return consultar_senado(
            ["senador", self.cod, "discursos"],
            ["DiscursosParlamentar", "Parlamentar", "Pronunciamentos", "Pronunciamento"],
            _ParamsPronunciamentos.de_locais(locals()),
            m.Discurso,
            formato,
            url=url,
            index=index,
            verificar_certificado=self.verify,
        )

    @overload
    def filiacoes(self, index: bool = ..., formato: Literal["bruto"] | None = ...) -> Any: ...

    @overload
    def filiacoes(self, index: bool = ..., *, formato: Literal["json"]) -> list[dict[str, Any]]: ...

    @overload
    def filiacoes(self, index: bool = ..., *, formato: Literal["pydantic"]) -> list[m.Filiacao]: ...

    @overload
    def filiacoes(self, index: bool = ..., *, formato: Literal["pandas"]) -> DataFramePandas: ...

    @overload
    def filiacoes(self, index: bool = ..., *, formato: Literal["polars"]) -> DataFramePolars: ...

    @overload
    def filiacoes(self, index: bool = ..., *, formato: Literal["url"]) -> str: ...

    def filiacoes(
        self,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Obtém as filiações partidárias que o senador já teve.

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
            Filiações partidárias que o senador já teve.

        """

        return consultar_senado(
            ["senador", self.cod, "filiacoes"],
            ["FiliacaoParlamentar", "Parlamentar", "Filiacoes", "Filiacao"],
            None,
            m.Filiacao,
            formato,
            index=index,
            verificar_certificado=self.verify,
        )

    def historico(self) -> dict:
        """Obtém todos os detalhes de um parlamentar no(s) mandato(s) como
        senador (mandato atual e anteriores, se houver).

        Returns
        -------
        dict
            Dados históricos do(a) parlamentar.

        """

        return requisicao(
            ["senador", self.cod, "historico"], ["DetalheParlamentar", "Parlamentar"], verificar_certificado=self.verify
        ).json()

    @overload
    def mandatos(self, index: bool = ..., formato: Literal["bruto"] | None = ...) -> Any: ...

    @overload
    def mandatos(self, index: bool = ..., *, formato: Literal["json"]) -> list[dict[str, Any]]: ...

    @overload
    def mandatos(self, index: bool = ..., *, formato: Literal["pydantic"]) -> list[m.Mandato]: ...

    @overload
    def mandatos(self, index: bool = ..., *, formato: Literal["pandas"]) -> DataFramePandas: ...

    @overload
    def mandatos(self, index: bool = ..., *, formato: Literal["polars"]) -> DataFramePolars: ...

    @overload
    def mandatos(self, index: bool = ..., *, formato: Literal["url"]) -> str: ...

    def mandatos(
        self,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Obtém os mandatos que o senador já teve.

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
            Mandatos que o senador já teve.

        """

        return consultar_senado(
            ["senador", self.cod, "mandatos"],
            ["MandatoParlamentar", "Parlamentar", "Mandatos", "Mandato"],
            None,
            m.Mandato,
            formato,
            index=index,
            verificar_certificado=self.verify,
        )

    @overload
    def liderancas(self, formato: Literal["bruto"] | None = ...) -> Any: ...

    @overload
    def liderancas(self, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...

    @overload
    def liderancas(self, *, formato: Literal["pydantic"]) -> list[m.Lideranca]: ...

    @overload
    def liderancas(self, *, formato: Literal["pandas"]) -> DataFramePandas: ...

    @overload
    def liderancas(self, *, formato: Literal["polars"]) -> DataFramePolars: ...

    @overload
    def liderancas(self, *, formato: Literal["url"]) -> str: ...

    def liderancas(self, formato: Formato | None = None) -> Saida:
        """Obtém os cargos de liderança de um senador.

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
            Cargos de liderança do senador.

        """

        return consultar_senado(
            ["senador", self.cod, "liderancas"],
            ["LiderancaParlamentar", "Parlamentar", "Liderancas", "Lideranca"],
            None,
            m.Lideranca,
            formato,
            verificar_certificado=self.verify,
        )

    @overload
    def licencas(self, inicio: date | None = ..., index: bool = ..., formato: Literal["bruto"] | None = ...) -> Any: ...

    @overload
    def licencas(
        self, inicio: date | None = ..., index: bool = ..., *, formato: Literal["json"]
    ) -> list[dict[str, Any]]: ...

    @overload
    def licencas(
        self, inicio: date | None = ..., index: bool = ..., *, formato: Literal["pydantic"]
    ) -> list[m.Licenca]: ...

    @overload
    def licencas(
        self, inicio: date | None = ..., index: bool = ..., *, formato: Literal["pandas"]
    ) -> DataFramePandas: ...

    @overload
    def licencas(
        self, inicio: date | None = ..., index: bool = ..., *, formato: Literal["polars"]
    ) -> DataFramePolars: ...

    @overload
    def licencas(self, inicio: date | None = ..., index: bool = ..., *, formato: Literal["url"]) -> str: ...

    @com_params(_ParamsLicencas)
    def licencas(
        self,
        inicio: date | None = None,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
        """Obtém as licenças de um senador.

        Parameters
        ----------
        inicio : datetime or str, default=None
            Retorna as licenças a partir da data especificada.

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
            Licenças do senador.

        """

        return consultar_senado(
            ["senador", self.cod, "licencas"],
            ["LicencaParlamentar", "Parlamentar", "Licencas", "Licenca"],
            _ParamsLicencas.de_locais(locals()),
            m.Licenca,
            formato,
            index=index,
            verificar_certificado=self.verify,
        )

    @overload
    def profissoes(self, formato: Literal["bruto"] | None = ...) -> Any: ...

    @overload
    def profissoes(self, *, formato: Literal["json"]) -> list[dict[str, Any]]: ...

    @overload
    def profissoes(self, *, formato: Literal["pydantic"]) -> list[m.Profissao]: ...

    @overload
    def profissoes(self, *, formato: Literal["pandas"]) -> DataFramePandas: ...

    @overload
    def profissoes(self, *, formato: Literal["polars"]) -> DataFramePolars: ...

    @overload
    def profissoes(self, *, formato: Literal["url"]) -> str: ...

    def profissoes(self, formato: Formato | None = None) -> Saida:
        """Obtém a(s) profissão(ões) de um senador.

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
            Profissões do senador.

        """

        return consultar_senado(
            ["senador", self.cod, "profissao"],
            ["HistoricoAcademicoParlamentar", "Parlamentar", "Profissoes", "Profissao"],
            None,
            m.Profissao,
            formato,
            verificar_certificado=self.verify,
        )

    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = ...,
        comissao: str | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        formato: Literal["bruto"] | None = ...,
    ) -> Any: ...

    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = ...,
        comissao: str | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...

    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = ...,
        comissao: str | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Relatoria]: ...

    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = ...,
        comissao: str | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...

    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = ...,
        comissao: str | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...

    @overload
    def relatorias(
        self,
        ano: PositiveInt | None = ...,
        comissao: str | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        *,
        formato: Literal["url"],
    ) -> str: ...

    @com_params(_ParamsRelatorias)
    def relatorias(
        self,
        ano: PositiveInt | None = None,
        comissao: str | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        formato: Formato | None = None,
    ) -> Saida:
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
            Matérias de relatoria do senador.

        """

        return consultar_senado(
            ["senador", self.cod, "relatorias"],
            ["MateriasRelatoriaParlamentar", "Parlamentar", "Relatorias", "Relatoria"],
            _ParamsRelatorias.de_locais(locals()),
            m.Relatoria,
            formato,
            verificar_certificado=self.verify,
        )

    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        formato: Literal["bruto"] | None = ...,
    ) -> Any: ...

    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["json"],
    ) -> list[dict[str, Any]]: ...

    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["pydantic"],
    ) -> list[m.Voto]: ...

    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["pandas"],
    ) -> DataFramePandas: ...

    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["polars"],
    ) -> DataFramePolars: ...

    @overload
    def votacoes(
        self,
        ano: PositiveInt | None = ...,
        numero: int | None = ...,
        sigla: str | None = ...,
        tramitando: bool | None = ...,
        index: bool = ...,
        *,
        formato: Literal["url"],
    ) -> str: ...

    @com_params(_ParamsMaterias)
    def votacoes(
        self,
        ano: PositiveInt | None = None,
        numero: int | None = None,
        sigla: str | None = None,
        tramitando: bool | None = None,
        index: bool = False,
        formato: Formato | None = None,
    ) -> Saida:
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
            Votações do senador.

        """

        return consultar_senado(
            ["senador", self.cod, "votacoes"],
            ["VotacaoParlamentar", "Parlamentar", "Votacoes", "Votacao"],
            _ParamsMaterias.de_locais(locals()),
            m.Voto,
            formato,
            index=index,
            verificar_certificado=self.verify,
        )


@overload
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = ...,
    uf: str | None = ...,
    sexo: Literal["f", "m"] | None = ...,
    partido: str | None = ...,
    contendo: str | None = ...,
    excluindo: str | None = ...,
    url: bool = ...,
    index: bool = ...,
    formato: Literal["bruto"] | None = ...,
    verificar_certificado: bool | None = ...,
) -> Any: ...


@overload
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = ...,
    uf: str | None = ...,
    sexo: Literal["f", "m"] | None = ...,
    partido: str | None = ...,
    contendo: str | None = ...,
    excluindo: str | None = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["json"],
    verificar_certificado: bool | None = ...,
) -> list[dict[str, Any]]: ...


@overload
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = ...,
    uf: str | None = ...,
    sexo: Literal["f", "m"] | None = ...,
    partido: str | None = ...,
    contendo: str | None = ...,
    excluindo: str | None = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["pydantic"],
    verificar_certificado: bool | None = ...,
) -> list[m.Senador]: ...


@overload
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = ...,
    uf: str | None = ...,
    sexo: Literal["f", "m"] | None = ...,
    partido: str | None = ...,
    contendo: str | None = ...,
    excluindo: str | None = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["pandas"],
    verificar_certificado: bool | None = ...,
) -> DataFramePandas: ...


@overload
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = ...,
    uf: str | None = ...,
    sexo: Literal["f", "m"] | None = ...,
    partido: str | None = ...,
    contendo: str | None = ...,
    excluindo: str | None = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["polars"],
    verificar_certificado: bool | None = ...,
) -> DataFramePolars: ...


@overload
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = ...,
    uf: str | None = ...,
    sexo: Literal["f", "m"] | None = ...,
    partido: str | None = ...,
    contendo: str | None = ...,
    excluindo: str | None = ...,
    url: bool = ...,
    index: bool = ...,
    *,
    formato: Literal["url"],
    verificar_certificado: bool | None = ...,
) -> str: ...


@validate_call
@com_params(_ParamsSenadores)
def lista_senadores(
    tipo: Literal["atual", "titulares", "suplentes", "afastados"] = "atual",
    uf: str | None = None,
    sexo: Literal["f", "m"] | None = None,
    partido: str | None = None,
    contendo: str | None = None,
    excluindo: str | None = None,
    url: bool = True,
    index: bool = False,
    formato: Formato | None = None,
    verificar_certificado: bool | None = None,
) -> Saida:
    """Lista de senadores da república.

    Parameters
    ----------
    tipo : {"atual", "titulares", "suplentes", "afastados"}, default="atual"
        - "atual": Todos os senadores em exercício;
        - "titulares": Apenas senadores que iniciaram o mandato como titulares;
        - "suplentes": Apenas senadores que iniciaram o mandato como suplentes;
        - "afastados": Todos os senadores afastados.

    uf : str, optional
        Filtro de Unidade Federativa dos senadores.

    sexo : {"f", "m"}, optional
        Filtro de sexo dos senadores.

    partido : str, optional
        Filtro de partido dos senadores.

    contendo : str, optional
        Captura apenas senadores contendo esse texto no nome.

    excluindo : str, optional
        Exclui da consulta senadores contendo esse texto no nome.

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
        Lista de senadores da república.

    Raises
    ------
    DABUFError
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

    params = _ParamsSenadores.de_locais(locals())
    caminho, chave = _TIPOS_SENADORES[tipo]
    return consultar_senado(
        ["senador", "lista", caminho],
        [chave, "Parlamentares", "Parlamentar"],
        params,
        m.Senador,
        formato,
        url=url,
        index=index,
        filtro=filtro_parlamentares(
            sexo=sexo,
            partido=partido,
            uf=params.uf if tipo == "afastados" else None,
            contendo=contendo,
            excluindo=excluindo,
        ),
        verificar_certificado=verificar_certificado,
    )
