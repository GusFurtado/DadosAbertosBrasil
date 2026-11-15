import functools
from typing import Literal

from pydantic import Field, validate_call

from ..utils.errors import descontinuado
from ..utils.modelos import SiglaUF, com_params
from ..utils.typing import Formato, Saida
from . import modelos as m
from ._comum import ParamsSenado, consultar_senado, filtro_parlamentares


class _ParamsLegislaturas(ParamsSenado):
    inicio: int = Field(exclude=True)
    fim: int | None = Field(None, exclude=True)
    exercicio: bool | None = None
    participacao: Literal["titulares", "suplentes"] | None = None
    uf: SiglaUF = None
    sexo: Literal["f", "m"] | None = Field(None, exclude=True)
    partido: str | None = Field(None, exclude=True)
    contendo: str | None = Field(None, exclude=True)
    excluindo: str | None = Field(None, exclude=True)

    def para_api(self) -> dict:
        params = super().para_api()
        if self.participacao is not None:
            params["participacao"] = self.participacao[0].upper()
        return params


@validate_call
@com_params(_ParamsLegislaturas)
def lista_legislaturas(
    inicio: int,
    fim: int | None = None,
    exercicio: bool | None = None,
    participacao: Literal["titulares", "suplentes"] | None = None,
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
        Lista senadores de uma legislatura ou de um intervalo de legislaturas.

    Raises
    ------
    DABUFError
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

    path = ["senador", "lista", "legislatura", inicio]
    if fim is not None:
        path.append(fim)
    return consultar_senado(
        path,
        ["ListaParlamentarLegislatura", "Parlamentares", "Parlamentar"],
        _ParamsLegislaturas.de_locais(locals()),
        m.Senador,
        formato,
        url=url,
        index=index,
        filtro=filtro_parlamentares(sexo=sexo, partido=partido, contendo=contendo, excluindo=excluindo),
        verificar_certificado=verificar_certificado,
    )


@functools.wraps(lista_legislaturas)
def lista_legislatura(*args, **kwargs):
    """Nome antigo de `lista_legislaturas`.

    Descontinuado: use `senado.lista_legislaturas`.
    """
    descontinuado(
        "`senado.lista_legislatura` foi renomeada para `senado.lista_legislaturas` e o nome "
        "antigo deixa de existir em uma versão futura do 3.x."
    )
    return lista_legislaturas(*args, **kwargs)
