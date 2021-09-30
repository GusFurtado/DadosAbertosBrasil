'''Módulo para captura dos dados abertos da Senado Brasileiro.

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

Documentação da API original
----------------------------
http://legis.senado.gov.br/dadosabertos/docs/

'''
from typing import List, Union

import pandas as _pd

from ._utils import parse
from ._utils.get_data import get_data



def _format_df(
        data: dict,
        mapping: dict,
        cols_to_int: List[str] = None,
        cols_to_date: List[str] = None,
        cols_to_bool: List[str] = None
    ) -> _pd.DataFrame:
    '''Função auxiliar para converter `json` em `dataframe`.

    Parâmetros
    ----------
    data : list[dict]
        Dados obtidos pela função auxiliar `_get_request`.
    mapping : dict
        Dicionário para selecionar e corrigir nomes das colunas do DataFrame.
    cols_to_int : list[str]
        Colunas cujo `dtype` deve ser `int`.
    cols_to_date : list[str]
        Colunas cujo `dtype` deve ser `datetime.date`.
    cols_to_bool : list[str]
        Colunas cujo `dtype` deve ser `bool`.

    Retorna
    -------
    pandas.core.frame.DataFrame
        DataFrame formatado.
    
    '''

    _normalize = _pd.io.json.json_normalize \
        if _pd.__version__[0] == '0' else _pd.json_normalize

    df = _normalize(data)
    df = df[[col for col in mapping.keys() if col in df.columns]]
    df.columns = df.columns.map(mapping)

    if isinstance(cols_to_int, list):
        for col in cols_to_int:
            if col in df.columns:
                df[col] = _pd.to_numeric(
                    df[col],
                    errors = 'coerce',
                    downcast = 'integer'
                )

    if isinstance(cols_to_date, list):
        for col in cols_to_date:
            if col in df.columns:
                df[col] = _pd.to_datetime(df[col])

    if isinstance(cols_to_date, list):
        for col in cols_to_bool:
            if col in df.columns:
                df[col] = df[col].map({'Sim': True, 'Não': False})

    return df



def _get_request(
        path: str,
        params: dict = None,
        keys: list = None
    ) -> dict:

    data = get_data(
        endpoint = 'http://legis.senado.gov.br/dadosabertos/',
        path = path,
        params = params
    )

    if keys is not None:
        for key in keys:
            if data is not None:
                if key in data:
                    data = data[key]

    if data is None:
        raise ValueError('Nenhum dado encontrado. Verifique os parâmetros da consulta.')
    else:
        return data



def lista_senadores(
        tipo: str = 'atual',
        uf: str = None,
        sexo: str = None,
        partido: str = None,
        contendo: str = None,
        excluindo: str = None,
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[_pd.DataFrame, List[dict]]:
    '''Lista de senadores da república.

    Parâmetros
    ----------
    tipo : str {'atual', 'titulares', 'suplentes', 'afastados'}
        - 'atual' (default): Todos os senadores em exercício;
        - 'titulares': Apenas senadores que iniciaram o mandato como titulares;
        - 'suplentes': Apenas senadores que iniciaram o mandato como suplentes;
        - 'afastados': Todos os senadores afastados.
    uf : str (default=None)
        Filtro de Unidade Federativa dos senadores.
    sexo : str (default=None)
        Filtro de sexo dos senadores.
    partido : str (default=None)
        Filtro de partido dos senadores.
    contendo : str (default=None)
        Captura apenas senadores contendo esse texto no nome.
    excluindo : str (default=None)
        Exclui da consulta senadores contendo esse texto no nome.
    index : bool (default=False)
        Se True, define a coluna `codigo` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'.
    formato : str {'dataframe', 'json'} (default='dataframe')
        Formato do dado que será retornado.
        Os dados no formato 'json' são mais completos, porém alguns filtros
        podem não ser aplicados.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Se formato = 'dataframe', retorna os dados formatados em uma tabela.
    list[dict]
        Se formato = 'json', retorna os dados brutos no formato json.

    Erros
    -----
    DAB_UFError
        Caso seja inserida uma UF inválida no argumento `uf`.

    Ver também
    ----------
    DadosAbertosBrasil.senado.Senador
        Use o `codigo` para obter um detalhamento do senador.
    DadosAbertosBrasil.senado.lista_legislatura
        Pesquisa por senadores de outras legislaturas, além da atual.
    DadosAbertosBrasil.camara.lista_deputados
        Função similar para o módulo `camara`.
    
    Exemplos
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
    
    '''

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

    lista = _get_request(
        path = ['senador', 'lista', TIPOS[tipo]['path']],
        keys = [TIPOS[tipo]['key'], 'Parlamentares', 'Parlamentar'],
        params = params
    )

    if formato == 'json':
        return lista

    col_mapping = {
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
    df = _format_df(
        data = lista,
        mapping = col_mapping,
        cols_to_int = ['codigo'],
        cols_to_date= ['data_inicio', 'data_fim']
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

    if index:
        df.set_index('codigo', inplace=True)
    else:
        df.reset_index(drop=True, inplace=True)

    return df



def lista_legislatura(
        inicio: int,
        fim: int = None,
        exercicio: str = None,
        participacao: str = None,
        uf: str = None,
        sexo: str = None,
        partido: str = None,
        contendo: str = None,
        excluindo: str = None,
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[_pd.DataFrame, List[dict]]:
    '''Lista senadores de uma legislatura ou de um intervalo de legislaturas.

    Parâmetros
    ----------
    inicio : int
        Código da primeira legislatura da consulta.
    fim : int (default=None)
        Código da última legislatura da consulta.
        Se fim=None, pesquisa apenas pela legislatura do campo `inicio`.
        Caso contrário, pesquisa todas os valores de todas as legislaturas
        entre `inicio` e `fim`. 
    exercicio : str (default=None)
        - True: Consulta apenas os senadores que entraram em exercício.
        - False: Consulta apenas os senadores que não entratam em exercício.
    participacao : str {None, 'titulares', 'suplentes'} (default=None)
        - None: Busca qualquer tipo de participação.
        - 'titulares': Busca apenas titulares.
        - 'suplentes': Busca apenas suplentes.
    uf : str (default=None)
        Filtra uma unidade federativa.
        Se uf=None, lista senadores de todas as UFs.
    sexo : str (default=None)
        Filtro de sexo dos senadores.
    partido : str (default=None)
        Filtro de partido dos senadores.
    contendo : str (default=None)
        Captura apenas senadores contendo esse texto no nome.
    excluindo : str (default=None)
        Exclui da consulta senadores contendo esse texto no nome.
    index : bool (default=False)
        Se True, define a coluna `codigo` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'.
    formato : str {'dataframe', 'json'} (default='dataframe')
        Formato do dado que será retornado.
        Os dados no formato 'json' são mais completos, porém alguns filtros
        podem não ser aplicados.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Se formato = 'dataframe', retorna os dados formatados em uma tabela.
    list[dict]
        Se formato = 'json', retorna os dados brutos no formato json.

    Erros
    -----
    DAB_UFError
        Caso seja inserida uma UF inválida no argumento `uf`.

    Ver também
    ----------
    DadosAbertosBrasil.senado.Senador
        Use o `codigo` para obter um detalhamento do senador.
    DadosAbertosBrasil.senado.lista_senadores
        Função de busca de senadores específica para a legislação atual.

    Exemplos
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

    '''

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
    lista = _get_request(path=path, params=params, keys=keys)

    if formato == 'json':
        return lista

    col_mapping = {
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
    df = _format_df(
        data = lista,
        mapping = col_mapping,
        cols_to_int = ['codigo'],
        cols_to_date= ['data_inicio', 'data_fim']
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

    if index:
        df.set_index('codigo', inplace=True)
    else:
        df.reset_index(drop=True, inplace=True)

    return df



def orcamento(
        autor: str = None,
        tipo: str = None,
        ano_execucao: int = None,
        ano_materia: int = None,
        formato: str = 'dataframe'
    ) -> Union[_pd.DataFrame, List[dict]]:
    '''Obtém a lista dos lotes de emendas orçamentárias.

    Parâmetros
    ----------
    autor : str (default=None)
        Texto contendo nome do autor.
    tipo : str (default=None)
        Tipo de orçamento.
    ano_execucao : int (default=None)
        Ano que o orçamento foi executado.
    ano_materia : int (default)
        Ano da matéria.
    formato : str {'dataframe', 'json'} (default='dataframe')
        Formato do dado que será retornado.
        Os dados no formato 'json' são mais completos, porém alguns filtros
        podem não ser aplicados.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Se formato = 'dataframe', retorna os dados formatados em uma tabela.
    list[dict]
        Se formato = 'json', retorna os dados brutos no formato json.

    Exemplos
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

    '''

    data = _get_request(
        path = ['orcamento', 'lista'],
        keys = ['ListaLoteEmendas', 'LotesEmendasOrcamento', 'LoteEmendasOrcamento']
    )

    if formato == 'lista':
        return data

    col_mapping = {
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
    df = _format_df(
        data = data,
        mapping = col_mapping,
        cols_to_int = ['autor_codigo', 'quantidade_emendas', 'ano_execucao', 'materia_ano'],
        cols_to_date = ['data_operacao']
    )
    df.ativo = df.ativo == 'Sim'

    if autor is not None:
        df = df[df.autor_nome.str.contains(autor)]
    if tipo is not None:
        df = df[df.tipo_sigla == tipo]
    if ano_execucao is not None:
        df = df[df.ano_execucao == ano_execucao]
    if ano_materia is not None:
        df = df[df.ano_materia == ano_materia]

    return df.reset_index(drop=True)



def lista_partidos(
        inativos: bool = False,
        index: bool = False,
        formato: str = 'dataframe'
    ) -> Union[_pd.DataFrame, List[dict]]:
    '''Lista os partidos políticos.

    Parâmetros
    ----------
    inativos : bool (default=False)
        - True para incluir partidos inativos na lista.
        - False para listar apenas os partidos ativos.
    index : bool (default=False)
        Se True, define a coluna `codigo` como index do DataFrame.
        Esse argumento é ignorado se `formato` for igual a 'json'.
    formato : str {'dataframe', 'json'} (default='dataframe')
        Formato do dado que será retornado.
        Os dados no formato 'json' são mais completos, porém alguns filtros
        podem não ser aplicados.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Se formato = 'dataframe', retorna os dados formatados em uma tabela.
    list[dict]
        Se formato = 'json', retorna os dados brutos no formato json.

    Ver também
    ----------
    DadosAbertosBrasil.camara.lista_partidos
        Função semelhante do módulo `camara`.

    Exemplos
    --------
    Capturar todos os partidos, incluindo inativos.
    
    >>> senado.lista_partido(inativos=True)
       codigo          sigla                          nome data_criacao \
    0     525            ANL  Aliança Nacional Libertadora   1935-01-01   
    1     238          ARENA   Aliança Renovadora Nacional   1965-11-24   
    2     578         AVANTE                        AVANTE   2017-09-12

    '''

    path = ['senador', 'partidos']
    params = {'indAtivos': 'N'} if inativos else {}
    
    keys = ['ListaPartidos', 'Partidos', 'Partido']
    lista = _get_request(path, params, keys)

    if formato == 'json':
        return lista

    col_mapping = {
        'Codigo': 'codigo',
        'Sigla': 'sigla',
        'Nome': 'nome',
        'DataCriacao': 'data_criacao',
        'DataExtincao': 'data_extincao'
    }
    df = _format_df(
        data = lista,
        mapping = col_mapping,
        cols_to_int = ['codigo'],
        cols_to_date = ['data_criacao', 'data_extincao']
    )
    if index:
        df.set_index('codigo', inplace=True)

    return df



class Senador:
    '''Coleta os dados dos senadores.

    Parâmetros
    ----------
    cod : int
        Código de senador que se dejesa consulta.
        O código pode ser encontrado pela função `lista_senadores`.

    Atributos
    ---------
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

    '''

    def __init__(self, cod:int):
        self.cod = cod
        keys = ['DetalheParlamentar', 'Parlamentar']
        self.dados = _get_request(
            path = ['senador', cod],
            keys = keys
        )

        _ATTR = {
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
        for attr in _ATTR:
            self._set_attribute(attr, _ATTR)

        if 'Telefones' in self.dados:
            self.telefones = [fone['NumeroTelefone'] \
                for fone in self.dados['Telefones']['Telefone']]


    def __repr__(self):
        return f"<DadosAbertosBrasil.senado: Senador{'a' if self.sexo == 'Feminino' else ''} {self.nome}>"


    def _set_attribute(self, attr:str, attr_dict:dict):
        x = self.dados
        try:
            for key in attr_dict[attr]:
                x = x[key]
            setattr(self, attr, x)
        except (KeyError, TypeError):
            return


    def apartes(
            self,
            casa: str = None,
            inicio: int = None,
            fim: int = None,
            numero_sessao: int = None,
            tipo_pronunciamento: str = None,
            tipo_sessao: str = None,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém a relação de apartes do senador.

        Parâmetros
        ----------
        casa : str (default=None)
            Sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        inicio : datetime.date ou str (default=None)
            Data inicial do período da pesquisa no formato 'AAAA-MM-DD'
        fim : datetime.date ou str (default=None)
            Data final do período da pesquisa no formato 'AAAA-MM-DD'
        numero_sessao : int (default=None)
            Número da sessão plenária.
        tipo_pronunciamento : str (default=None)
            Sigla do tipo de pronunciamento.
        tipo_sessao : str (default=None)
            Tipo da sessão plenária.
        index : bool (default=False)
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = f'senador/{self.cod}/apartes'
        keys = ['ApartesParlamentar', 'Parlamentar', 'Apartes', 'Aparte']
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
        lista = _get_request(path=path, params=params, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
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

        df = _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_date = ['data', 'publicacao_data'],
            cols_to_bool = ['republicacao'],
            cols_to_int = [
                'codigo',
                'uso_palavra',
                'sessao',
                'orador',
                'publicacao_primeira_pagina',
                'publicacao_ultima_pagina'
            ]
        )
        if index:
            df.set_index('codigo', inplace=True)

        return df

        
    def autorias(
            self,
            ano: int = None,
            numero: int = None,
            primeiro_autor: bool = None,
            sigla: str = None,
            tramitando: bool = None,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém as matérias de autoria de um senador.

        Parâmetros
        ----------
        ano : int (default=None)
            Retorna apenas as matérias do ano informado.
        numero : int (default=None)
            Retorna apenas as matérias do número informado.
        primeiro_autor : bool (default=None)
            - True: Retorna apenas as matérias cujo senador é o primeiro autor;
            - False: Retorna apenas as que o senador é coautor;
            - None: Retorna ambas.
        sigla : str (default=None)
            Retorna apenas as matérias da sigla informada.
        tramitando : bool (default=None)
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.
        index : bool (default=False)
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'autorias']
        keys = ['MateriasAutoriaParlamentar', 'Parlamentar', 'Autorias', 'Autoria']
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
        lista = _get_request(path=path, params=params, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
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

        df = _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_date = ['data'],
            cols_to_int = ['codigo', 'processo', 'ano'],
            cols_to_bool = ['autor_principal', 'outros_autores']
        )
        if index:
            df.set_index('codigo', inplace=True)

        return df

    
    def cargos(
            self,
            comissao: bool = None,
            ativos: bool = None,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém a relação de cargos que o senador ja ocupou.

        Parâmetros
        ----------
        comissao : str (default=None)
            Retorna apenas os cargos da sigla de comissão informada.
        ativos : bool (default=None)
            - True: Retorna apenas os cargos atuais;
            - False: Retorna apenas os cargos já finalizadas;
            - None: Retorna ambos.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'cargos']
        keys = ['CargoParlamentar', 'Parlamentar', 'Cargos', 'Cargo']
        params = {}
        if comissao is not None:
            params['comissao'] = comissao
        if ativos is not None:
            params['indAtivos'] = 'S' if ativos else 'N'
        lista = _get_request(path=path, params=params, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
            'CodigoCargo': 'cargo_codigo',
            'DescricaoCargo': 'cargo_descricao',
            'DataInicio': 'data_inicio',
            'DataFim': 'data_fim',
            'IdentificacaoComissao.CodigoComissao': 'comissao_codigo',
            'IdentificacaoComissao.SiglaComissao': 'comissao_sigla',
            'IdentificacaoComissao.NomeComissao': 'comissao_nome',
            'IdentificacaoComissao.SiglaCasaComissao': 'casa'
        }

        return _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_date = ['data_inicio', 'data_fim'],
            cols_to_int = ['cargo_codigo', 'comisao_codigo']
        )


    def comissoes(
            self,
            comissao: str = None,
            ativos: bool = None,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém as comissões de que um senador é membro.

        Parâmetros
        ----------
        comissao : str (default=None)
            Retorna apenas as comissões com a sigla informada.
        ativos : bool (default=None)
            - True: Retorna apenas as comissões atuais;
            - False: Retorna apenas as comissões já finalizadas;
            - None: Retorna ambas.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'comissoes']
        keys = ['MembroComissaoParlamentar', 'Parlamentar', 'MembroComissoes', 'Comissao']
        params = {}
        if comissao is not None:
            params['comissao'] = comissao
        if ativos is not None:
            params['indAtivos'] = 'S' if ativos else 'N'
        lista = _get_request(path=path, params=params, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
            'DescricaoParticipacao': 'participacao',
            'DataInicio': 'data_inicio',
            'DataFim': 'data_fim',
            'IdentificacaoComissao.CodigoComissao': 'comissao_codigo',
            'IdentificacaoComissao.SiglaComissao': 'comissao_sigla',
            'IdentificacaoComissao.NomeComissao': 'comissao_nome',
            'IdentificacaoComissao.SiglaCasaComissao': 'casa'
        }

        return _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_date = ['data_inicio', 'data_fim'],
            cols_to_int = ['comissao_codigo']
        )


    def discursos(
            self,
            casa: str = None,
            inicio: int = None,
            fim: int = None,
            numero_sessao: int = None,
            tipo_pronunciamento: str = None,
            tipo_sessao: str = None,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém a relação de discursos do senador.

        Se os argumentos `inicio` e `fim` não forem informados, retorna os
        pronunciamentos dos últimos 30 dias.

        Parâmetros
        ----------
        casa : str (default=None)
            Sigla da casa aonde ocorre o pronunciamento:
            - 'SF' para Senado;
            - 'CD' para Câmara;
            - 'CN' para Congresso;
            - 'PR' para Presidência;
            - 'CR' para Comissão Representativa do Congresso;
            - 'AC' para Assembléia Constituinte.
        inicio : datetime.date ou str (default=None)
            Data inicial do período da pesquisa no formato 'AAAA-MM-DD'
        fim : datetime.date ou str (default=None)
            Data final do período da pesquisa no formato 'AAAA-MM-DD'
        numero_sessao : int (default=None)
            Número da sessão plenária.
        tipo_pronunciamento : str (default=None)
            Sigla do tipo de pronunciamento.
        tipo_sessao : str (default=None)
            Tipo da sessão plenária.
        index : bool (default=False)
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'discursos']
        keys = ['DiscursosParlamentar', 'Parlamentar', 'Pronunciamentos', 'Pronunciamento']
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
        lista = _get_request(path=path, params=params, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
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

        df = _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_date = ['data', 'publicacao_data'],
            cols_to_bool = ['republicacao'],
            cols_to_int = [
                'codigo',
                'uso_palavra',
                'sessao',
                'publicacao_primeira_pagina',
                'publicacao_ultima_pagina'
            ]
        )
        if index:
            df.set_index('codigo', inplace=True)

        return df


    def filiacoes(
            self,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém as filiações partidárias que o senador já teve.

        Parâmetros
        ----------
        index : bool (default=False)
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'filiacoes']
        keys = ['FiliacaoParlamentar', 'Parlamentar', 'Filiacoes', 'Filiacao']
        lista = _get_request(path=path, params=None, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
            'Partido.CodigoPartido': 'codigo',
            'Partido.SiglaPartido': 'sigla',
            'Partido.NomePartido': 'nome',
            'DataFiliacao': 'data_filiacao',
            'DataDesfiliacao': 'data_desfiliacao'
        }

        df = _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_int = ['codigo'],
            cols_to_date = ['data_filiacao', 'data_desfiliacao']
        )
        if index:
            df.set_index('codigo', inplace=True)

        return df


    def historico(self) -> dict:
        '''Obtém todos os detalhes de um parlamentar no(s) mandato(s) como
        senador (mandato atual e anteriores, se houver).

        Retorna
        -------
        dict
            Dados históricos do(a) parlamentar.

        '''

        path = ['senador', self.cod, 'historico']
        keys = ['DetalheParlamentar', 'Parlamentar']
        return _get_request(path=path, params=None, keys=keys)
        

    def mandatos(
            self,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém os mandatos que o senador já teve.

        Parâmetros
        ----------
        index : bool (default=False)
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'mandatos']
        keys = ['MandatoParlamentar', 'Parlamentar', 'Mandatos', 'Mandato']
        lista = _get_request(path=path, params=None, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
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
        df = _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_int = ['codigo'],
            cols_to_date = [
                'primeira_legislatura_inicio',
                'primeira_legislatura_fim',
                'segunda_legislatura_inicio',
                'segunda_legislatura_fim'
            ]
        )
        if index:
            df.set_index('codigo', inplace=True)

        return df


    def liderancas(
            self,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém os cargos de liderança de um senador.

        Parâmetros
        ----------
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'liderancas']
        keys = ['LiderancaParlamentar', 'Parlamentar', 'Liderancas', 'Lideranca']
        lista = _get_request(path=path, params=None, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
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
        return _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_int = ['partido_codigo', 'bloco_codigo'],
            cols_to_date = ['data_designacao', 'data_fim']
        )


    def licencas(
            self,
            inicio: str = None,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém as licenças de um senador.

        Parâmetros
        ----------
        inicio : datetime.date | str (default=None)
            Retorna as licenças a partir da data especificada.
        index : bool (default=False)
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'licencas']
        keys = ['LicencaParlamentar', 'Parlamentar', 'Licencas', 'Licenca']
        params = {}
        if inicio is not None:
            params['dataInicio'] = parse.data(inicio, 'senado')
        lista = _get_request(path=path, params=params, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
            'Codigo': 'codigo',
            'DataInicio': 'inicio',
            'DataInicioPrevista': 'inicio_previsto',
            'DataFim': 'fim',
            'DataFimPrevista': 'fim_previsto',
            'SiglaTipoAfastamento': 'afastamento_sigla',
            'DescricaoTipoAfastamento': 'afastamento_descricao',
        }
        df = _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_int = ['codigo'],
            cols_to_date = ['inicio', 'inicio_previsto', 'fim', 'fim_previsto']
        )
        if index:
            df.set_index('codigo', inplace=True)

        return df


    def relatorias(
            self,
            ano: int = None,
            comissao: str = None,
            numero: int = None,
            sigla: str = None,
            tramitando: bool = None,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém as matérias de relatoria de um senador.

        Parâmetros
        ----------
        ano : int (default=None)
            Retorna apenas as matérias do ano informado.
        comissao : str (default=None)
            Retorna apenas as relatorias da comissão informada.
        numero : int (default=None)
            Retorna apenas as matérias do número informado. 
        sigla : str (default=None)
            Retorna apenas as matérias da sigla informada.	 
        tramitando : bool (default=None)
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'relatorias']
        keys = ['MateriasRelatoriaParlamentar', 'Parlamentar', 'Relatorias', 'Relatoria']
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
        lista = _get_request(path=path, params=params, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
            'Materia.Codigo': 'materia',
            'Comissao.Codigo': 'comissao',
            'CodigoTipoRelator': 'codigo',
            'DescricaoTipoRelator': 'descricao',
            'DataDesignacao': 'data_designacao',
            'DataDestituicao': 'data_destituicao',
            'DescricaoMotivoDestituicao': 'motivo_destituicao'
        }
        return _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_int = ['codigo', 'materia', 'comissao'],
            cols_to_date = ['data_designacao', 'data_destituicao']    
        )


    def votacoes(
            self,
            ano: int = None,
            numero: int = None,
            sigla: str = None,
            tramitando: bool = None,
            index: bool = False,
            formato: str = 'dataframe'
        ) -> Union[_pd.DataFrame, List[dict]]:
        '''Obtém as votações de um senador.

        Parâmetros
        ----------
        ano : int (default=None)
            Retorna apenas as matérias do ano informado.
        numero : int (default=None)
            Retorna apenas as matérias do número informado. 	 
        sigla : str (default=None)
            Retorna apenas as matérias da sigla informada. 	 
        tramitando : bool (default=None)
            - True: Retorna apenas as matérias que estão tramitando;
            - False: Retorna apenas as que não estão tramitando;
            - None: Retorna ambas.
        index : bool (default=False)
            Se True, define a coluna `codigo` como index do DataFrame.
            Esse argumento é ignorado se `formato` for igual a 'json'.
        formato : str {'dataframe', 'json'} (default='dataframe')
            Formato do dado que será retornado.
            Os dados no formato 'json' são mais completos, porém alguns filtros
            podem não ser aplicados.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Se formato = 'dataframe', retorna os dados formatados em uma tabela.
        list[dict]
            Se formato = 'json', retorna os dados brutos no formato json.

        '''

        path = ['senador', self.cod, 'votacoes']
        keys = ['VotacaoParlamentar', 'Parlamentar', 'Votacoes', 'Votacao']
        params = {}
        if ano is not None:
            params['ano'] = ano
        if numero is not None:
            params['numero'] = numero
        if sigla is not None:
            params['sigla'] = sigla
        if tramitando is not None:
            params['tramitando'] = 'S' if tramitando else 'N'
        lista = _get_request(path=path, params=params, keys=keys)

        if formato == 'json':
            return lista

        col_mapping = {
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
        df = _format_df(
            data = lista,
            mapping = col_mapping,
            cols_to_int = ['sequencial', 'votacao', 'sessao', 'materia', 'tramitacao'],
            cols_to_bool = ['votacao_secreta']
        )
        if index:
            df.set_index('codigo', inplace=True)

        return df
