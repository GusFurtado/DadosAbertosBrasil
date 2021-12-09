"""Módulo para captura dos dados abertos da Senado Brasileiro.

Mini-Tutorial
-------------
1. Importe o módulo `senado`
>>> from DadosAbertosBrasil import senado

2. Utilize as funções `lista` para identificar o código do Senado desejado.
>>> senado.lista_senadores( ... )
>>> senado.lista_legislatura( ... )

3. Utilize a class `Senador` para obter as informações do(a) parlamentar.
>>> sen = senado.Senador(cod)

4. Após a class `Senador` ser instanciada, utilize seus métodos para buscas
outros tipos de informação sobre ele(a).
>>> sen.cargos( ... )
>>> sen.votacoes( ... )
>>> ... 

References
----------
.. [1] http://legis.senado.gov.br/dadosabertos/docs/

"""

from datetime import datetime
from typing import List, Optional, Union

import pandas as pd

from ._utils import parse
from ._utils.get_data import DAB_Base, get_and_format



def lista_blocos(
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[pd.DataFrame, List[dict]]:
    """Obtém a lista e a composição dos Blocos Parlamentares no
    Congresso Nacional.
    
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
        'CodigoBloco': 'codigo',
        'NomeBloco': 'nome',
        'NomeApelido': 'apelido',
        'SiglaBloco': 'sigla',
        'DataCriacao': 'data_criacao'
    }  

    return get_and_format(
        api = 'senado',
        path = ['blocoParlamentar', 'lista'],
        unpack_keys = ['ListaBlocoParlamentar', 'Blocos', 'Bloco'],
        cols_to_rename = cols_to_rename,
        cols_to_int = ['codigo'],
        cols_to_date = ['data_criacao'],
        index = index,
        formato = formato
    )



def lista_legislatura(
        inicio: int,
        fim: int = None,
        exercicio: Optional[str] = None,
        participacao: Optional[str] = None,
        uf: Optional[str] = None,
        sexo: Optional[str] = None,
        partido: Optional[str] = None,
        contendo: Optional[str] = None,
        excluindo: Optional[str] = None,
        url: bool = True,
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[pd.DataFrame, List[dict]]:
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
    participacao : {'titulares', 'suplentes'}, optional
        - None: Busca qualquer tipo de participação.
        - 'titulares': Busca apenas titulares.
        - 'suplentes': Busca apenas suplentes.
    uf : str, optional
        Filtra uma unidade federativa.
        Se uf=None, lista senadores de todas as UFs.
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

    path = ['senador', 'lista', 'legislatura', inicio]
    if fim is not None:
        path.append(fim)

    params = {}
    if exercicio is not None:
        params['exercicio'] = 'S' if exercicio else 'N'
    if participacao is not None:
        params['participacao'] = participacao[0].upper()
    if uf is not None:
        params['uf'] = parse.uf(uf)

    keys = ['ListaParlamentarLegislatura', 'Parlamentares', 'Parlamentar']

    cols_to_rename = {
        'IdentificacaoParlamentar.CodigoParlamentar': 'codigo',
        'IdentificacaoParlamentar.NomeParlamentar': 'nome_parlamentar',
        'IdentificacaoParlamentar.NomeCompletoParlamentar': 'nome_completo',
        'IdentificacaoParlamentar.SexoParlamentar': 'sexo',
        'IdentificacaoParlamentar.FormaTratamento': 'forma_tratamento',
        'IdentificacaoParlamentar.UrlFotoParlamentar': 'foto',
        'IdentificacaoParlamentar.UrlPaginaParlamentar': 'pagina_parlamentar',
        'IdentificacaoParlamentar.UrlPaginaParticular': 'pagina_particular',
        'IdentificacaoParlamentar.EmailParlamentar': 'email',
        'IdentificacaoParlamentar.SiglaPartidoParlamentar': 'partido',
        'Mandato.UfParlamentar': 'uf',
        'Mandato.Exercicios.Exercicio.DataInicio': 'data_inicio',
        'Mandato.Exercicios.Exercicio.DataFim': 'data_fim',
        'Mandato.Exercicios.Exercicio.DescricaoCausaAfastamento': 'causa_afastamento'
    }

    df = get_and_format(
        api = 'senado',
        path = path,
        params = params,
        unpack_keys = keys,
        cols_to_rename = cols_to_rename,
        cols_to_int = ['codigo'],
        cols_to_date= ['data_inicio', 'data_fim'],
        url_cols = ['foto', 'pagina_parlamentar', 'pagina_particular', 'email'],
        url = url,
        index = index,
        formato = formato
    )

    if sexo is not None:
        sexo = sexo.title()
        SEXOS = {
            'Masculino': 'Masculino',
            'Feminino': 'Feminino',
            'M': 'Masculino',
            'F': 'Feminino'
        }
        df = df[df.sexo == SEXOS[sexo]]

    if partido is not None:
        df = df[df.partido == partido.upper()]

    if contendo is not None:
        nome_parlamentar = df.nome_parlamentar.str.contains(contendo)
        nome_completo = df.nome_completo.str.contains(contendo)
        df = df[nome_parlamentar | nome_completo]

    if excluindo is not None:
        nome_parlamentar = ~df.nome_parlamentar.str.contains(excluindo)
        nome_completo = ~df.nome_completo.str.contains(excluindo)
        df = df[nome_parlamentar | nome_completo]

    return df



def lista_partidos(
        inativos: bool = False,
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[pd.DataFrame, List[dict]]:
    """Lista os partidos políticos.

    Parameters
    ----------
    inativos : bool, default=False
        - True para incluir partidos inativos na lista.
        - False para listar apenas os partidos ativos.
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

    See Also
    --------
    DadosAbertosBrasil.camara.lista_partidos
        Função semelhante do módulo `camara`.

    Examples
    --------
    Capturar todos os partidos, incluindo inativos.
    
    >>> senado.lista_partido(inativos=True)
       codigo          sigla                          nome data_criacao \
    0     525            ANL  Aliança Nacional Libertadora   1935-01-01   
    1     238          ARENA   Aliança Renovadora Nacional   1965-11-24   
    2     578         AVANTE                        AVANTE   2017-09-12

    """

    cols_to_rename = {
        'Codigo': 'codigo',
        'Sigla': 'sigla',
        'Nome': 'nome',
        'DataCriacao': 'data_criacao',
        'DataExtincao': 'data_extincao'
    }

    return get_and_format(
        api = 'senado',
        path = ['senador', 'partidos'],
        params = {'indAtivos': 'N'} if inativos else {},
        unpack_keys = ['ListaPartidos', 'Partidos', 'Partido'],
        cols_to_rename = cols_to_rename,
        cols_to_int = ['codigo'],
        cols_to_date = ['data_criacao', 'data_extincao'],
        index = index,
        formato = formato
    )



def lista_senadores(
        tipo: str = 'atual',
        uf: Optional[str] = None,
        sexo: Optional[str] = None,
        partido: Optional[str] = None,
        contendo: Optional[str] = None,
        excluindo: Optional[str] = None,
        url: bool = True,
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[pd.DataFrame, List[dict]]:
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
        'titulares': {
            'path': 'atual',
            'key': 'ListaParlamentarEmExercicio',
            'params': {'participacao': 'T'}
        },
        'suplentes': {
            'path': 'atual',
            'key': 'ListaParlamentarEmExercicio',
            'params': {'participacao': 'S'}
        },
        'atual': {
            'path': 'atual',
            'key': 'ListaParlamentarEmExercicio',
            'params': {}
        },
        'afastados': {
            'path': 'afastados',
            'key': 'AfastamentoAtual',
            'params': {}
        }
    }

    params = TIPOS[tipo]['params']
    if uf is not None:
        params['uf'] = parse.uf(uf=uf)

    cols_to_rename = {
        'IdentificacaoParlamentar.CodigoParlamentar': 'codigo',
        'IdentificacaoParlamentar.NomeParlamentar': 'nome_parlamentar',
        'IdentificacaoParlamentar.NomeCompletoParlamentar': 'nome_completo',
        'IdentificacaoParlamentar.SexoParlamentar': 'sexo',
        'IdentificacaoParlamentar.FormaTratamento': 'forma_tratamento',
        'IdentificacaoParlamentar.UrlFotoParlamentar': 'foto',
        'IdentificacaoParlamentar.UrlPaginaParlamentar': 'pagina_parlamentar',
        'IdentificacaoParlamentar.UrlPaginaParticular': 'pagina_particular',
        'IdentificacaoParlamentar.EmailParlamentar': 'email',
        'IdentificacaoParlamentar.SiglaPartidoParlamentar': 'partido',
        'Mandato.UfParlamentar': 'uf',
        'Mandato.Exercicios.Exercicio.DataInicio': 'data_inicio',
        'Mandato.Exercicios.Exercicio.DataFim': 'data_fim',
        'Mandato.Exercicios.Exercicio.DescricaoCausaAfastamento': 'causa_afastamento'
    }

    df = get_and_format(
        api = 'senado',
        path = ['senador', 'lista', TIPOS[tipo]['path']],
        params = params,
        unpack_keys = [TIPOS[tipo]['key'], 'Parlamentares', 'Parlamentar'],
        cols_to_rename = cols_to_rename,
        cols_to_int = ['codigo'],
        cols_to_date = ['data_inicio', 'data_fim'],
        url_cols = ['foto', 'pagina_parlamentar', 'pagina_particular', 'email'],
        url = url,
        index = index,
        formato = formato
    )

    if sexo is not None:
        sexo = sexo.title()
        SEXOS = {
            'Masculino': 'Masculino',
            'Feminino': 'Feminino',
            'M': 'Masculino',
            'F': 'Feminino'
        }
        df = df[df.sexo == SEXOS[sexo]]

    if (uf is not None) and (tipo == 'afastados'):
        df = df[df.uf == parse.uf(uf=uf)]

    if partido is not None:
        df = df[df.partido == partido.upper()]

    if contendo is not None:
        nome_parlamentar = df.nome_parlamentar.str.contains(contendo)
        nome_completo = df.nome_completo.str.contains(contendo)
        df = df[nome_parlamentar | nome_completo]

    if excluindo is not None:
        nome_parlamentar = ~df.nome_parlamentar.str.contains(excluindo)
        nome_completo = ~df.nome_completo.str.contains(excluindo)
        df = df[nome_parlamentar | nome_completo]

    return df



def lista_uso_palavra(
        ativos: bool = False,
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[pd.DataFrame, List[dict]]:
    """Lista os tipos de uso da palavra.
    
    Parameters
    ----------
    ativos : bool, default=False
        Se True, retorna apenas os tipos de uso de palavra atualmente ativos.
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
        'Codigo': 'codigo',
        'Sigla': 'sigla',
        'Descricao': 'descricao',
        'IndicadorAtivo': 'ativo'
    }

    return get_and_format(
        api = 'senado',
        path = ['senador', 'lista', 'tiposUsoPalavra'],
        params = {'indAtivos': 'S' if ativos else 'N'},
        unpack_keys = ['ListaTiposUsoPalavra', 'TiposUsoPalavra', 'TipoUsoPalavra'],
        cols_to_rename = cols_to_rename,
        cols_to_int = ['codigo'],
        cols_to_bool = ['ativo'],
        true_value = 'S',
        false_value = 'N',
        index = index,
        formato = formato
    )



def orcamento(
        autor: Optional[str] = None,
        tipo: Optional[str] = None,
        ano_execucao: Optional[int] = None,
        ano_materia: Optional[int] = None,
        url: bool = True,
        formato: str = 'dataframe'
    ) -> Union[pd.DataFrame, List[dict]]:
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
        'NomeAutorOrcamento': 'autor_nome',
        'IndicadorAtivo': 'ativo',
        'EmailAutorOrcamento': 'autor_email',
        'CodigoAutorOrcamento': 'autor_codigo',
        'DataOperacao': 'data_operacao',
        'QuantidadeEmendas': 'quantidade_emendas',
        'AnoExecucao': 'ano_execucao',
        'NumeroMateria': 'materia_numero',
        'AnoMateria': 'materia_ano',
        'SiglaTipoPlOrcamento': 'tipo_sigla',
        'DescricaoTipoPlOrcamento': 'tipo_descricao'
    }

    df = get_and_format(
        api = 'senado',
        path = ['orcamento', 'lista'],
        unpack_keys = ['ListaLoteEmendas', 'LotesEmendasOrcamento', 'LoteEmendasOrcamento'],
        cols_to_rename = cols_to_rename,
        cols_to_int = ['autor_codigo', 'quantidade_emendas', 'ano_execucao', 'materia_ano'],
        cols_to_date = ['data_operacao'],
        cols_to_bool = ['ativo'],
        true_value = 'Sim',
        false_value = 'Não',
        url_cols = ['autor_email'],
        url = url,
        formato = formato
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



class Senador(DAB_Base):
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

    def __init__(self, cod:int):
        
        self.cod = cod
        atributos = {
            'email': ['IdentificacaoParlamentar', 'EmailParlamentar'],
            'endereco': ['DadosBasicosParlamentar', 'EnderecoParlamentar'],
            'foto': ['IdentificacaoParlamentar', 'UrlFotoParlamentar'],
            'nascimento': ['DadosBasicosParlamentar', 'DataNascimento'],
            'naturalidade': ['DadosBasicosParlamentar', 'Naturalidade'],
            'nome': ['IdentificacaoParlamentar', 'NomeParlamentar'],
            'nome_completo': ['IdentificacaoParlamentar', 'NomeCompletoParlamentar'],
            'pagina': ['IdentificacaoParlamentar', 'UrlPaginaParlamentar'],
            'partido': ['IdentificacaoParlamentar', 'SiglaPartidoParlamentar'],
            'sexo': ['IdentificacaoParlamentar', 'SexoParlamentar'],
            'tratamento': ['IdentificacaoParlamentar', 'FormaTratamento'],
            'uf': ['IdentificacaoParlamentar', 'UfParlamentar'],
            'uf_naturalidade': ['DadosBasicosParlamentar', 'UfNaturalidade'],
        }

        super().__init__(
            api = 'senado',
            path = ['senador', cod],
            unpack_keys = ['DetalheParlamentar', 'Parlamentar'],
            error_key = 'IdentificacaoParlamentar',
            atributos = atributos
        )

        if 'Telefones' in self.dados:
            lista_telefones = self.dados['Telefones']['Telefone']
            if isinstance(lista_telefones, list):
                self.telefones = [fone['NumeroTelefone'] \
                    for fone in lista_telefones]
            elif isinstance(lista_telefones, dict):
                self.telefones = [lista_telefones['NumeroTelefone']]


    def __repr__(self) -> str:
        return f"<DadosAbertosBrasil.senado: Senador{'a' if self.sexo == 'Feminino' else ''} {self.nome}>"


    def __str__(self) -> str:
        return self.nome_completo


    def apartes(
            self,
            casa: Optional[str] = None,
            inicio: Union[datetime, str] = None,
            fim: Union[datetime, str] = None,
            numero_sessao: Optional[int] = None,
            tipo_pronunciamento: Optional[str] = None,
            tipo_sessao: Optional[str] = None,
            url: bool = True,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            params['casa'] = casa
        if inicio is not None:
            params['dataInicio'] = parse.data(inicio, 'senado')
        if fim is not None:
            params['dataFim'] = parse.data(fim, 'senado')
        if numero_sessao is not None:
            params['numeroSessao'] = numero_sessao
        if tipo_pronunciamento is not None:
            params['tipoPronunciamento'] = tipo_pronunciamento
        if tipo_sessao is not None:
            params['tipoSessao'] = tipo_sessao

        cols_to_rename = {
            'CodigoPronunciamento': 'codigo',
            'DataPronunciamento': 'data',
            'SiglaCasaPronunciamento': 'casa_sigla',
            'NomeCasaPronunciamento': 'casa_nome',
            'TextoResumo': 'resumo',
            'Indexacao': 'indexacao',
            'UrlTexto': 'url',
            'TipoUsoPalavra.Codigo': 'uso_palavra',
            'SessaoPlenaria.CodigoSessao': 'sessao',
            'Orador.CodigoParlamentar': 'orador',
            'Publicacoes.Publicacao.DescricaoVeiculoPublicacao': 'publicacao_veiculo',
            'Publicacoes.Publicacao.DataPublicacao': 'publicacao_data',
            'Publicacoes.Publicacao.NumeroPagInicioPublicacao': 'publicacao_primeira_pagina',
            'Publicacoes.Publicacao.NumeroPagFimPublicacao': 'publicacao_ultima_pagina',
            'Publicacoes.Publicacao.IndicadorRepublicacao': 'republicacao',
            'Publicacoes.Publicacao.UrlDiario': 'publicacao_url'
        }

        return get_and_format(
            api = 'senado',
            path = f'senador/{self.cod}/apartes',
            params = params,
            unpack_keys = ['ApartesParlamentar', 'Parlamentar', 'Apartes', 'Aparte'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['codigo', 'uso_palavra', 'sessao', 'orador',
                'publicacao_primeira_pagina', 'publicacao_ultima_pagina'],
            cols_to_date = ['data', 'publicacao_data'],
            cols_to_bool = ['republicacao'],
            true_value = 'Sim',
            false_value = 'Não',
            url_cols = ['url', 'publicacao_url'],
            url = url,
            index = index,
            formato = formato
        )

        
    def autorias(
            self,
            ano: Optional[int] = None,
            numero: Optional[int] = None,
            primeiro_autor: Optional[bool] = None,
            sigla: Optional[str] = None,
            tramitando: Optional[bool] = None,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            params['ano'] = ano
        if numero is not None:
            params['numero'] = numero
        if primeiro_autor is not None:
            params['primeiro'] = 'S' if primeiro_autor else 'N'
        else:
            params['primeiro'] = 'T'
        if sigla is not None:
            params['sigla'] = sigla
        if tramitando is not None:
            params['tramitando'] = 'S' if tramitando else 'N'

        cols_to_rename = {
            'IndicadorAutorPrincipal': 'autor_principal',
            'Materia.Codigo': 'codigo',
            'Materia.IdentificacaoProcesso': 'processo',
            'Materia.DescricaoIdentificacao': 'descricao',
            'Materia.Sigla': 'sigla',
            'Materia.Numero': 'numero',
            'Materia.Ano': 'ano',
            'Materia.Ementa': 'ementa',
            'Materia.Data': 'data',
            'IndicadorOutrosAutores': 'outros_autores'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'autorias'],
            params = params,
            unpack_keys = ['MateriasAutoriaParlamentar', 'Parlamentar', 'Autorias', 'Autoria'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['codigo', 'processo', 'ano'],
            cols_to_date = ['data'],
            cols_to_bool = ['autor_principal', 'outros_autores'],
            true_value = 'Sim',
            false_value = 'Não',
            index = index,
            formato = formato
        )

    
    def cargos(
            self,
            comissao: Optional[str] = None,
            ativos: Optional[bool] = None,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            params['comissao'] = comissao
        if ativos is not None:
            params['indAtivos'] = 'S' if ativos else 'N'

        cols_to_rename = {
            'CodigoCargo': 'cargo_codigo',
            'DescricaoCargo': 'cargo_descricao',
            'DataInicio': 'data_inicio',
            'DataFim': 'data_fim',
            'IdentificacaoComissao.CodigoComissao': 'comissao_codigo',
            'IdentificacaoComissao.SiglaComissao': 'comissao_sigla',
            'IdentificacaoComissao.NomeComissao': 'comissao_nome',
            'IdentificacaoComissao.SiglaCasaComissao': 'casa'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'cargos'],
            params = params,
            unpack_keys = ['CargoParlamentar', 'Parlamentar', 'Cargos', 'Cargo'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['cargo_codigo', 'comisao_codigo'],
            cols_to_date = ['data_inicio', 'data_fim'],
            formato = formato
        )


    def comissoes(
            self,
            comissao: Optional[str] = None,
            ativos: Optional[bool] = None,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            params['comissao'] = comissao
        if ativos is not None:
            params['indAtivos'] = 'S' if ativos else 'N'

        cols_to_rename = {
            'DescricaoParticipacao': 'participacao',
            'DataInicio': 'data_inicio',
            'DataFim': 'data_fim',
            'IdentificacaoComissao.CodigoComissao': 'comissao_codigo',
            'IdentificacaoComissao.SiglaComissao': 'comissao_sigla',
            'IdentificacaoComissao.NomeComissao': 'comissao_nome',
            'IdentificacaoComissao.SiglaCasaComissao': 'casa'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'comissoes'],
            params = params,
            unpack_keys = ['MembroComissaoParlamentar', 'Parlamentar', 'MembroComissoes', 'Comissao'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['comissao_codigo'],
            cols_to_date = ['data_inicio', 'data_fim'],
            formato = formato
        )


    def cursos(
            self,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            'NomeCurso': 'nome',
            'GrauInstrucao': 'grau_instrucao',
            'Estabelecimento': 'estabelecimento',
            'Local': 'local'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'historicoAcademico'],
            unpack_keys = ['HistoricoAcademicoParlamentar', 'Parlamentar', 'HistoricoAcademico', 'Curso'],
            cols_to_rename = cols_to_rename,
            cols_to_bool = ['atividade_principal'],
            true_value = 'Sim',
            false_value = 'Não',
            formato = formato
        )


    def discursos(
            self,
            casa: Optional[str] = None,
            inicio: Union[datetime, str] = None,
            fim: Union[datetime, str] = None,
            numero_sessao: Optional[int] = None,
            tipo_pronunciamento: Optional[str] = None,
            tipo_sessao: Optional[str] = None,
            url: bool = True,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            params['casa'] = casa
        if inicio is not None:
            params['dataInicio'] = parse.data(inicio, 'senado')
        if fim is not None:
            params['dataFim'] = parse.data(fim, 'senado')
        if numero_sessao is not None:
            params['numeroSessao'] = numero_sessao
        if tipo_pronunciamento is not None:
            params['tipoPronunciamento'] = tipo_pronunciamento
        if tipo_sessao is not None:
            params['tipoSessao'] = tipo_sessao

        cols_to_rename = {
            'CodigoPronunciamento': 'codigo',
            'DataPronunciamento': 'data',
            'SiglaCasaPronunciamento': 'casa_sigla',
            'NomeCasaPronunciamento': 'casa_nome',
            'TextoResumo': 'resumo',
            'Indexacao': 'indexacao',
            'UrlTexto': 'url',
            'TipoUsoPalavra.Codigo': 'uso_palavra',
            'SessaoPlenaria.CodigoSessao': 'sessao',
            'Publicacoes.Publicacao.DescricaoVeiculoPublicacao': 'publicacao_veiculo',
            'Publicacoes.Publicacao.DataPublicacao': 'publicacao_data',
            'Publicacoes.Publicacao.NumeroPagInicioPublicacao': 'publicacao_primeira_pagina',
            'Publicacoes.Publicacao.NumeroPagFimPublicacao': 'publicacao_ultima_pagina',
            'Publicacoes.Publicacao.IndicadorRepublicacao': 'republicacao',
            'Publicacoes.Publicacao.UrlDiario': 'publicacao_url'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'discursos'],
            params = params,
            unpack_keys = ['DiscursosParlamentar', 'Parlamentar', 'Pronunciamentos', 'Pronunciamento'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['codigo', 'uso_palavra', 'sessao',
                'publicacao_primeira_pagina', 'publicacao_ultima_pagina'],
            cols_to_date = ['data', 'publicacao_data'],
            cols_to_bool = ['republicacao'],
            true_value = 'Sim',
            false_value = 'Não',
            url_cols = ['url', 'publicacao_url'],
            url = url,
            index = index,
            formato = formato
        )


    def filiacoes(
            self,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            'Partido.CodigoPartido': 'codigo',
            'Partido.SiglaPartido': 'sigla',
            'Partido.NomePartido': 'nome',
            'DataFiliacao': 'data_filiacao',
            'DataDesfiliacao': 'data_desfiliacao'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'filiacoes'],
            unpack_keys = ['FiliacaoParlamentar', 'Parlamentar', 'Filiacoes', 'Filiacao'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['codigo'],
            cols_to_date = ['data_filiacao', 'data_desfiliacao'],
            index = index,
            formato = formato
        )


    def historico(self) -> dict:
        """Obtém todos os detalhes de um parlamentar no(s) mandato(s) como
        senador (mandato atual e anteriores, se houver).

        Returns
        -------
        dict
            Dados históricos do(a) parlamentar.

        """

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'historico'],
            unpack_keys = ['DetalheParlamentar', 'Parlamentar'],
            formato = 'json'
        )


    def mandatos(
            self,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            'CodigoMandato': 'codigo',
            'UfParlamentar': 'uf',
            'DescricaoParticipacao': 'participacao',
            'PrimeiraLegislaturaDoMandato.NumeroLegislatura': 'primeira_legislatura',
            'PrimeiraLegislaturaDoMandato.DataInicio': 'primeira_legislatura_inicio',
            'PrimeiraLegislaturaDoMandato.DataFim': 'primeira_legislatura_fim',
            'SegundaLegislaturaDoMandato.NumeroLegislatura': 'segunda_legislatura',
            'SegundaLegislaturaDoMandato.DataInicio': 'segunda_legislatura_inicio',
            'SegundaLegislaturaDoMandato.DataFim': 'segunda_legislatura_fim'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'mandatos'],
            unpack_keys = ['MandatoParlamentar', 'Parlamentar', 'Mandatos', 'Mandato'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['codigo'],
            cols_to_date = ['primeira_legislatura_inicio', 'primeira_legislatura_fim',
                'segunda_legislatura_inicio', 'segunda_legislatura_fim'],
            index = index,
            formato = formato
        )


    def liderancas(
            self,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            'UnidadeLideranca': 'lideranca',
            'DescricaoTipoLideranca': 'tipo',
            'SiglaCasaLideranca': 'casa_sigla',
            'NomeCasaLideranca': 'casa_nome',
            'DataDesignacao': 'data_designacao',
            'DataFim': 'data_fim',
            'Partido.CodigoPartido': 'partido_codigo',
            'Partido.SiglaPartido': 'partido_sigla',
            'Partido.NomePartido': 'partido_nome',
            'Bloco.CodigoBloco': 'bloco_codigo',
            'Bloco.SiglaBloco': 'bloco_sigla',
            'Bloco.NomeBloco': 'bloco_nome',
            'Bloco.ApelidoBloco': 'bloco_apelido'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'liderancas'],
            unpack_keys = ['LiderancaParlamentar', 'Parlamentar', 'Liderancas', 'Lideranca'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['partido_codigo', 'bloco_codigo'],
            cols_to_date = ['data_designacao', 'data_fim'],
            formato = formato
        )


    def licencas(
            self,
            inicio: Union[datetime, str] = None,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            'Codigo': 'codigo',
            'DataInicio': 'inicio',
            'DataInicioPrevista': 'inicio_previsto',
            'DataFim': 'fim',
            'DataFimPrevista': 'fim_previsto',
            'SiglaTipoAfastamento': 'afastamento_sigla',
            'DescricaoTipoAfastamento': 'afastamento_descricao',
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'licencas'],
            params = {'dataInicio': parse.data(inicio, 'senado')} if inicio is not None else {},
            unpack_keys = ['LicencaParlamentar', 'Parlamentar', 'Licencas', 'Licenca'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['codigo'],
            cols_to_date = ['inicio', 'inicio_previsto', 'fim', 'fim_previsto'],
            index = index,
            formato = formato
        )


    def profissoes(
            self,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            'NomeProfissao': 'nome',
            'IndicadorAtividadePrincipal': 'atividade_principal'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'profissao'],
            unpack_keys = ['ProfissaoParlamentar', 'Parlamentar', 'Profissoes', 'Profissao'],
            cols_to_rename = cols_to_rename,
            cols_to_bool = ['atividade_principal'],
            true_value = 'Sim',
            false_value = 'Não',
            formato = formato
        )


    def relatorias(
            self,
            ano: Optional[int] = None,
            comissao: Optional[str] = None,
            numero: Optional[int] = None,
            sigla: Optional[str] = None,
            tramitando: Optional[bool] = None,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            params['ano'] = ano
        if comissao is not None:
            params['comissao'] = comissao
        if numero is not None:
            params['numero'] = numero
        if sigla is not None:
            params['sigla'] = sigla
        if tramitando is not None:
            params['tramitando'] = 'S' if tramitando else 'N'

        cols_to_rename = {
            'Materia.Codigo': 'materia',
            'Comissao.Codigo': 'comissao',
            'CodigoTipoRelator': 'codigo',
            'DescricaoTipoRelator': 'descricao',
            'DataDesignacao': 'data_designacao',
            'DataDestituicao': 'data_destituicao',
            'DescricaoMotivoDestituicao': 'motivo_destituicao'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'relatorias'],
            params = params,
            unpack_keys = ['MateriasRelatoriaParlamentar', 'Parlamentar', 'Relatorias', 'Relatoria'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['codigo', 'materia', 'comissao'],
            cols_to_date = ['data_designacao', 'data_destituicao'],
            formato = formato
        )


    def votacoes(
            self,
            ano: Optional[int] = None,
            numero: Optional[int] = None,
            sigla: Optional[str] = None,
            tramitando: Optional[bool] = None,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[pd.DataFrame, List[dict]]:
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
            params['ano'] = ano
        if numero is not None:
            params['numero'] = numero
        if sigla is not None:
            params['sigla'] = sigla
        if tramitando is not None:
            params['tramitando'] = 'S' if tramitando else 'N'

        cols_to_rename = {
            'CodigoSessaoVotacao': 'codigo',
            'SessaoPlenaria.CodigoSessao': 'sessao',
            'Materia.Codigo': 'materia',
            'Tramitacao.IdentificacaoTramitacao.CodigoTramitacao': 'tramitacao',
            'Sequencial': 'sequencial',
            'DescricaoVotacao': 'descricao',
            'IndicadorVotacaoSecreta': 'votacao_secreta',
            'SiglaDescricaoVoto': 'voto',
            'DescricaoResultado': 'resultado'
        }

        return get_and_format(
            api = 'senado',
            path = ['senador', self.cod, 'votacoes'],
            params = params,
            unpack_keys = ['VotacaoParlamentar', 'Parlamentar', 'Votacoes', 'Votacao'],
            cols_to_rename = cols_to_rename,
            cols_to_int = ['sequencial', 'votacao', 'sessao', 'materia', 'tramitacao'],
            cols_to_bool = ['votacao_secreta'],
            true_value = 'Sim',
            false_value = 'Não',
            index = index,
            formato = formato
        )
