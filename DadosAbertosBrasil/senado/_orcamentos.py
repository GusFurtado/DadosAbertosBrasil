from typing import Literal, Optional

import pandas as pd
from pydantic import validate_call, PositiveInt

from .._utils.get_data import get_and_format


@validate_call
def lista_orcamentos(
    autor: Optional[str] = None,
    tipo: Optional[str] = None,
    ano_execucao: Optional[PositiveInt] = None,
    ano_materia: Optional[PositiveInt] = None,
    url: bool = True,
    formato: Literal["dataframe", "json"] = "dataframe",
) -> pd.DataFrame | list[dict]:
    """Obtém a lista dos lotes de emendas orçamentárias.

    Parameters
    ----------
    autor : str, optional
        Texto contendo nome do autor.
    tipo : str, optional
        Tipo de orçamento.
    ano_execucao : int, optional
        Ano que o orçamento foi executado.
    ano_materia : int, optional
        Ano da matéria.
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

    Examples
    --------
    Buscar o orçamento da Lei de Diretrizes Orçamentárias de 2020.

    >>> senado.orcamento(tipo='LDO', ano_execucao=2020)
              autor_nome  ativo                       autor_email  autor_codigo \
    0          Abou Anni   True        dep.abouanni@camara.leg.br          3896
    1       Acir Gurgacz   True               acir@senador.leg.br          2633
    2    Adriana Ventura   True  dep.adrianaventura@camara.leg.br          3899
    ..               ...    ...                               ...           ...

    Pesquisar por emendas da deputada Adriana Ventura

    >>> senado.orcamento(autor='Adriana')
            autor_nome  ativo                       autor_email  autor_codigo \
    0  Adriana Ventura   True  dep.adrianaventura@camara.leg.br          3899

    """

    cols_to_rename = {
        "NomeAutorOrcamento": "autor_nome",
        "IndicadorAtivo": "ativo",
        "EmailAutorOrcamento": "autor_email",
        "CodigoAutorOrcamento": "autor_codigo",
        "DataOperacao": "data_operacao",
        "QuantidadeEmendas": "quantidade_emendas",
        "AnoExecucao": "ano_execucao",
        "NumeroMateria": "materia_numero",
        "AnoMateria": "materia_ano",
        "SiglaTipoPlOrcamento": "tipo_sigla",
        "DescricaoTipoPlOrcamento": "tipo_descricao",
    }

    df = get_and_format(
        api="senado",
        path=["orcamento", "lista"],
        unpack_keys=[
            "ListaLoteEmendas",
            "LotesEmendasOrcamento",
            "LoteEmendasOrcamento",
        ],
        cols_to_rename=cols_to_rename,
        cols_to_int=[
            "autor_codigo",
            "quantidade_emendas",
            "ano_execucao",
            "materia_ano",
        ],
        cols_to_date=["data_operacao"],
        cols_to_bool=["ativo"],
        true_value="Sim",
        false_value="Não",
        url_cols=["autor_email"],
        url=url,
        formato=formato,
    )

    if autor is not None:
        df = df[df.autor_nome.str.contains(autor)]
    if tipo is not None:
        df = df[df.tipo_sigla == tipo]
    if ano_execucao is not None:
        df = df[df.ano_execucao == ano_execucao]
    if ano_materia is not None:
        df = df[df.ano_materia == ano_materia]

    return df
