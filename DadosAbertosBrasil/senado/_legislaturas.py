from typing import Literal, Optional

from pydantic import validate_call

from ..utils import Get, parse, Formato, Output


@validate_call
def lista_legislatura(
    inicio: int,
    fim: int = None,
    exercicio: Optional[str] = None,
    participacao: Optional[Literal["titulares", "suplentes"]] = None,
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
    """Lista senadores de uma legislatura ou de um intervalo de legislaturas.

    Parameters
    ----------
    inicio : int
        Código da primeira legislatura da consulta.

    fim : int, optional
        Código da última legislatura da consulta.
        Se fim=None, pesquisa apenas pela legislatura do campo `inicio`.
        Caso contrário, pesquisa todas os valores de todas as legislaturas
        entre `inicio` e `fim`.

    exercicio : str, optional
        - True: Consulta apenas os senadores que entraram em exercício.
        - False: Consulta apenas os senadores que não entratam em exercício.

    participacao : {"titulares", "suplentes"}, optional
        - None: Busca qualquer tipo de participação.
        - "titulares": Busca apenas titulares.
        - "suplentes": Busca apenas suplentes.

    uf : str, optional
        Filtra uma unidade federativa.
        Se uf=None, lista senadores de todas as UFs.

    sexo : {"f", "m"}, optional
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
        Lista senadores de uma legislatura ou de um intervalo de legislaturas.

    Raises
    ------
    DAB_UFError
        Caso seja inserida uma UF inválida no argumento `uf`.

    See Also
    --------
    DadosAbertosBrasil.senado.Senador
        Use o `codigo` para obter um detalhamento do senador.
        
    DadosAbertosBrasil.senado.lista_senadores
        Função de busca de senadores específica para a legislação atual.

    Examples
    --------
    Lista senadores titulares em exercício na legislatura 56.

    >>> senado.lista_legislatura(
    ...     inicio = 56,
    ...     participacao = 'titulares',
    ...     exercicio = True
    ... )
       codigo         nome_parlamentar               nome_completo \
    0    4981             Acir Gurgacz         Acir Marcos Gurgacz   
    1    5982        Alessandro Vieira           Alessandro Vieira   
    2     945              Alvaro Dias       Alvaro Fernandes Dias 
    ..    ...                      ...                         ...

    Lista mulheres senadoras do PT na legislatura 55.

    >>> senado.lista_legislatura(inicio=55, partido='PT', sexo='F')
      codigo nome_parlamentar                      nome_completo      sexo \
    0   3713   Fátima Bezerra            Maria de Fátima Bezerra  Feminino   
    1   5006  Gleisi Hoffmann             Gleisi Helena Hoffmann  Feminino   
    2   5575         Marizete  Marizete Lisboa Fernandes Pereira  Feminino   
    3   5182     Regina Sousa                 Maria Regina Sousa  Feminino 

    """

    path = ["senador", "lista", "legislatura", str(inicio)]
    if fim is not None:
        path.append(fim)

    params = {}
    if exercicio is not None:
        params["exercicio"] = "S" if exercicio else "N"
    if participacao is not None:
        params["participacao"] = participacao[0].upper()
    if uf is not None:
        params["uf"] = parse.uf(uf)

    keys = ["ListaParlamentarLegislatura", "Parlamentares", "Parlamentar"]

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
        path=path,
        params=params,
        unpack_keys=keys,
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
            SEXOS = {"f": "Feminino", "m": "Masculino"}
            data = data[data["sexo"] == SEXOS[sexo]]

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
