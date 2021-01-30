'''
Módulo para captura dos dados abertos da Câmara dos Deputados do Brasil.

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

Documentação da API original
----------------------------
https://dadosabertos.camara.leg.br/swagger/api.html
'''



import pandas as _pd

from . import API
from . import _utils



_api = API('camara')



def _df(
        dados: dict,
        index_col: str = None
    ) -> _pd.DataFrame:
    '''
    Converte dados brutos da API em um DataFrame.

    Parâmetros
    ----------
    dados: dict
        Dados brutos da API.
    index_col: str (default=None)
        Nome da coluna que será usada como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Dados convertidos em DataFrame.
    '''

    df = _pd.DataFrame(dados['dados'])
    if (index_col is not None) and (not df.empty):
        df.set_index(index_col, inplace=True)

    return df



class Bloco:
    '''
    Informações sobre um bloco partidário específico.

    Parâmetros
    ----------
    cod: int
        Código numérico do bloco partidário do qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico do bloco partidário.
    legislatura: str
        Legislatura do bloco partidário.
    nome: str
        Nome do bloco partidário.
    uri: str
        Endereço para coleta de dados direta pela API do bloco partidário.

    Exemplos
    --------
    Obter o nome do bloco #576.
    >>> bl = camara.Bloco(cod=576)
    >>> bl.nome
    ... 'PSL, PTB'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['blocos', str(cod)])['dados']
        self.legislatura = self.dados['idLegislatura']
        self.nome = self.dados['nome']
        self.uri = self.dados['uri']



class Deputado:
    '''
    Retorna os dados cadastrais de um parlamentar que, em algum momento
    da história e por qualquer período, entrou em exercício na Câmara.

    Parâmetros
    ----------
    cod: int
        Código do parlamentar.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código de identificação.
    condicao_eleitoral: str
        Condição eleitoral.
    cpf: str
        Número do CPF.
    descricao_status: str
        Descrição do último status.
    email: str
        E-mail.
    escolaridade: str
        Escolaridade.
    falecimento: str
        Data de falecimento no formato 'AAAA-MM-DD'.
        Retorna vazio caso o parlamentar não tenha falecido.
    foto: str
        URL da foto.
    gabinete: dict
        Informações de identificação e contato do gabinete.
    legislatura: int
        ID da legislatura mais recente.
    municipio_nascimento: str
        Município de nascimento.
    nascimento: str
        Data de nascimento no formato 'AAAA-MM-DD'.
    nome: str
        Nome mais comum.
    nome_completo: str
        Nome civil completo.
    nome_eleitoral: str
        Nome utilizado na campanha eleitoral.
    partido: str
        Último partido.
    rede_social: list
        Lista de nomes em redes sociais.
    sexo: str
        - 'M': Masculino;
        - 'F': Feminino.
    situacao: str
        Situação do último status.
    uf: str
        Sigla da Unidade Federativa pela qual foi eleito.
    uf_nascimento: str
        Unidade Federativa de nascimento.
    ultima_atualizacao: str
        Dia e horário da última atualização de status.
    uri: str
        Endereço para coleta de dados direta pela API.
    website: str
        Website.

    Exemplos
    --------
    Coletar partido mais recente do deputado Rodrigo Maia.
    >>> cod = 74693   # Código do deputado
    >>> dep = camara.Deputado(cod=cod)
    >>> dep.partido
    ... 'DEM'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['deputados', str(cod)])['dados']
        self.condicao_eleitoral = self.dados['ultimoStatus']['condicaoEleitoral']
        self.cpf = self.dados['cpf']
        self.descricao_status = self.dados['ultimoStatus']['descricaoStatus']
        self.email = self.dados['ultimoStatus']['email']
        self.escolaridade = self.dados['escolaridade']
        self.falecimento = self.dados['dataFalecimento']
        self.foto = self.dados['ultimoStatus']['urlFoto']
        self.gabinete = self.dados['ultimoStatus']['gabinete']
        self.legislatura = self.dados['ultimoStatus']['idLegislatura']
        self.municipio_nascimento = self.dados['municipioNascimento']
        self.nascimento = self.dados['dataNascimento']       
        self.nome = self.dados['ultimoStatus']
        self.nome_completo = self.dados['nomeCivil']
        self.nome_eleitoral = self.dados['ultimoStatus']['nomeEleitoral']
        self.partido = self.dados['ultimoStatus']['siglaPartido']
        self.rede_social = self.dados['redeSocial']
        self.sexo = self.dados['sexo']
        self.situacao = self.dados['ultimoStatus']['situacao']
        self.uf = self.dados['ultimoStatus']['siglaUf']
        self.uf_nascimento = self.dados['ufNascimento']
        self.ultima_atualizacao = self.dados['ultimoStatus']['data']
        self.uri = self.dados['uri']
        self.website = self.dados['urlWebsite']


    def despesas(
            self,
            legislatura: int = None,
            ano: int = None,
            mes: int = None,
            fornecedor: int = None,
            pagina: int = None,
            itens: int = None,
            asc: bool = True,
            ordenar_por: str = None
        ) -> _pd.DataFrame:
        '''
        As despesas com exercício parlamentar do deputado.

        Dá acesso aos registros de pagamentos e reembolsos feitos pela Câmara
        em prol do deputado, a título da Cota para Exercício da Atividade
        Parlamentar, a chamada "cota parlamentar".
        Se não forem passados os parâmetros de tempo, o serviço retorna os
        dados dos seis meses anteriores à requisição.

        Parâmetros
        ----------
        legislatura: int (default=None)
            ID da legislatura em que tenham ocorrido as despesas.
        ano: int (default=None)
            Ano de ocorrência das despesas.
        mes: int (default=None)
            Número do mês de ocorrência das despesas.
        fornecedor: int (default=None)
            CNPJ de uma pessoa jurídica, ou CPF de uma pessoa física,
            fornecedora do produto ou serviço (apenas números).
        pagina: int (default=None)
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido
            pelo parâmetro itens. Se omitido, assume o valor 1.
        itens: int (default=None)
            Número máximo de itens na página que se deseja obter com
            esta requisição.
        asc: bool (default=True)
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por: str (default=None)
            Nome do campo pelo qual a lista deverá ser ordenada:
            qualquer um dos campos do retorno, e também idLegislatura.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de despesas com exercício parlamentar do deputado.

        ----------------------------------------------------------------------
        '''

        params = {}
        if legislatura is not None:
            params['idLegislatura'] = legislatura
        if ano is not None:
            params['ano'] = ano
        if mes is not None:
            params['mes'] = mes
        if fornecedor is not None:
            params['cnpjCpfFornecedor'] = fornecedor
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        params['ordem'] = 'asc' if asc else 'desc'
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['deputados', str(self.cod), 'despesas']
        dados = _api.get(path=path, params=params)
        return _df(dados)


    def discursos(
            self,
            legislatura: int = None,
            inicio: str = None,
            fim: str = None,
            pagina: int = None,
            itens: int = None,
            asc: bool = True,
            ordenar_por: str = None
        ) -> _pd.DataFrame:
        '''
        Os discursos feitos por um deputado em eventos diversos.

        Retorna uma lista de informações sobre os pronunciamentos feitos
        pelo deputado que tenham sido registrados, em quaisquer eventos,
        nos sistemas da Câmara.
        Caso os parâmetros de tempo não sejam configurados na requisição,
        são buscados os discursos ocorridos nos sete dias anteriores ao
        da requisição.

        Parâmetros
        ----------
        legislatura: int (default=None)
            Número da legislatura a qual os dados buscados devem corresponder.
        inicio: str (default=None)
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        itens: int (default=None)
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        pagina: int (default=None)
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        asc: bool (default=True)
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por: str (default=None)
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de discursos feitos por um deputado em eventos diversos.

        ----------------------------------------------------------------------
        '''

        params = {}
        if legislatura is not None:
            params['idLegislatura'] = legislatura
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        params['ordem'] = 'asc' if asc else 'desc'
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['deputados', str(self.cod), 'discursos']
        dados = _api.get(path=path, params=params)
        return _df(dados)


    def eventos(
            self,
            legislatura: int = None,
            inicio: str = None,
            fim: str = None,
            pagina: int = None,
            itens: int = None,
            asc: bool = True,
            ordenar_por: str = None,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Uma lista de eventos com a participação do parlamentar.

        Retorna uma lista de objetos evento nos quais a participação do
        parlamentar era ou é prevista.
        Se não forem passados parâmetros de tempo, são retornados os eventos
        num período de cinco dias, sendo dois antes e dois depois do dia da
        requisição.

        Parâmetros
        ----------
        legislatura: int (default=None)
            Número da legislatura a qual os dados buscados devem corresponder.
        inicio: str (default=None)
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        pagina: int (default=None)
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        itens: int (default=None)
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        asc: bool (default=True)
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por: str (default=None)
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de discursos feitos por um deputado em eventos diversos.

        ----------------------------------------------------------------------
        '''

        params = {}
        if legislatura is not None:
            params['idLegislatura'] = legislatura
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        params['ordem'] = 'asc' if asc else 'desc'
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['deputados', str(self.cod), 'eventos']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def frentes(
            self,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        As frentes parlamentares das quais um deputado é integrante.

        Retorna uma lista de informações básicas sobre as frentes
        parlamentares das quais o parlamentar seja membro, ou, no caso de
        frentes existentes em legislaturas anteriores, tenha encerrado a
        legislatura como integrante.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de frentes parlamentares das quais um deputado é integrante.

        ----------------------------------------------------------------------
        '''

        path = ['deputados', str(self.cod), 'frentes']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def orgaos(
            self,
            legislatura: int = None,
            inicio: str = None,
            fim: str = None,
            pagina: int = None,
            itens: int = None,
            asc: bool = True,
            ordenar_por: str = None,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Os órgãos dos quais um deputado é integrante.

        Retorna uma lista de órgãos, como as comissões e procuradorias,
        dos quais o deputado participa ou participou durante um intervalo
        de tempo.
        Cada item identifica um órgão, o cargo ocupado pelo parlamentar neste
        órgão (como presidente, vice-presidente, titular ou suplente) e as
        datas de início e fim da ocupação deste cargo.
        Se não for passado algum parâmetro de tempo, são retornados os órgãos
        ocupados pelo parlamentar no momento da requisição. Neste caso a
        lista será vazia se o deputado não estiver em exercício.

        Parâmetros
        ----------
        inicio: str (default=None)
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        pagina: int (default=None)
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        itens: int (default=None)
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        asc: bool (default=True)
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por: str (default=None)
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        index: bool (default=False)
            Se True, define a coluna `idOrgao` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos órgãos dos quais um deputado é integrante.

        ----------------------------------------------------------------------
        '''

        params = {}
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        params['ordem'] = 'asc' if asc else 'desc'
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['deputados', str(self.cod), 'orgaos']
        dados = _api.get(path=path, params=params)
        index_col = 'idOrgao' if index else None
        return _df(dados, index_col)



class Evento:
    '''
    Retorna um conjunto detalhado de informações sobre o evento da Câmara.

    Parâmetros
    ----------
    cod: int
        Código numérico do evento do qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico do evento.
    andar: str
        Andar do prédio onde ocorreu o evento.
    descricao: str
        Descrição do evento.
    descricao_tipo: str
        Tipo do evento.
    fases: str
        Fases do evento.
    fim: str
        Data e horário que o evento foi finalizado no formato 'AAAA-MM-DD'.
    inicio: str
        Data e horário que o evento foi iniciado no formato 'AAAA-MM-DD'.
    local: str
        Local onde ocorreu o evento.
    local_externo: str
        Local externo do evento.
    lista_orgaos: list of dict
        Lista de orgãos e informações sobre os mesmos.
    predio: str
        Prédio que ocorreu o evento.
    requerimentos: list of dict
        Requerimentos do evento.
    sala: str
        Sala do prédio onde ocorreu o evento.
    situacao: str
        Situação do evento.
    uri: str
        Endereço para coleta de dados direta pela API do evento.
    uri_convidados: str
        Endereço para coleta de dados direta pela API dos convidados.
    uri_deputados: str
        Endereço para coleta de dados direta pela API dos deputados.
    url_documento_pauta: str
        Endereço URL para visualizar a pauta do evento.
    url_registro: str
        Endereço URL onde o evento foi registrado.

    Exemplos
    --------
    Obter a URL para assistir ao evento #59265.
    >>> ev = camara.Evento(cod=59265)
    >>> ev.url_registro
    ... 'https://www.youtube.com/watch?v=8D2gjMrTnMA'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['eventos', str(cod)])['dados']
        self.andar = self.dados['localCamra']['andar']
        self.descricao = self.dados['descricao']
        self.descricao_tipo = self.dados['descricaoTipo']
        self.fases = self.dados['fases']
        self.fim = self.dados['dataHoraFim']
        self.inicio = self.dados['dataHoraInicio']
        self.local = self.dados['localCamara']['nome']
        self.local_externo = self.dados['localExterno']
        self.lista_orgaos = self.dados['orgaos']
        self.predio = self.dados['localCamara']['predio']
        self.requerimentos = self.dados['requerimentos']
        self.sala = self.dados['localCamara']['sala']
        self.situacao = self.dados['situacao']
        self.uri = self.dados['uri']
        self.uri_convidados = self.dados['uriConvidados']
        self.uri_deputados = self.dados['uriDeputados']
        self.url_documento_pauta = self.dados['urlDocumentoPauta']
        self.url_registro = self.dados['urlRegistro']


    def deputados(
            self,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Os deputados participantes de um evento específico.

        Retorna uma lista de dados resumidos sobre deputados participantes do
        evento. Se o evento já ocorreu, a lista identifica os deputados que
        efetivamente registraram presença no evento. Se o evento ainda não
        ocorreu, a lista mostra os deputados que devem participar do evento,
        por serem convidados ou por serem membros do(s) órgão(s) responsável
        pelo evento.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos deputados participantes de um evento específico.

        ----------------------------------------------------------------------
        '''

        path = ['eventos', str(self.cod), 'deputados']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def orgaos(
            self,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Lista de órgãos organizadores do evento.

        Retorna uma lista em que cada item é um conjunto mínimo de dados sobre
        o(s) órgão(s) responsável(is) pelo evento.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de órgãos organizadores do evento.

        ----------------------------------------------------------------------
        '''

        path = ['eventos', str(self.cod), 'orgaos']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def pauta(
            self,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Lista de proposições que foram ou deverão ser avaliadas em um evento
        de caráter deliberativo.

        Se o evento for de caráter deliberativo (uma reunião ordinária,
        por exemplo) este serviço retorna a lista de proposições previstas
        para avaliação pelos parlamentares. Cada item identifica, se as
        informações estiverem disponíveis, a proposição avaliada, o regime
        de preferência para avaliação, o relator e seu parecer, o resultado
        da apreciação e a votação realizada.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `ordem` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de proposições do evento.

        ----------------------------------------------------------------------
        '''

        path = ['eventos', str(self.cod), 'pauta']
        dados = _api.get(path=path, params=None)
        index_col = 'ordem' if index else None
        return _df(dados, index_col)


    def votacoes(
            self,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Informações detalhadas de votações sobre o evento.

        Retorna uma lista de dados básicos sobre votações que tenham sido
        realizadas no evento. Votações só ocorrem em eventos de caráter
        deliberativo. Dados complementares sobre cada votação listada podem
        ser obtidos no recurso.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de de votações sobre o evento.

        ----------------------------------------------------------------------
        '''

        path = ['eventos', str(self.cod), 'votacoes']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Frente:
    '''
    Informações detalhadas sobre uma frente parlamentar.

    Parâmetros
    ----------
    cod: int
        Código numérico da frente parlamentar da qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico da frente parlamentar.
    coordenador: dict
        Informações do(a) coordenador(a) da frente parlamentar.
    documento: str
        URL do documento da frente parlamentar.
    email: str
        E-mail de contato.
    id_sitacao: int
        ID da situação da frente parlamentar.
    keywords: str
        Palavras-chaves da frente parlamentar.
    legislatura: int
        ID da legislatura da frente parlamentar.
    situacao: str
        Situação da frente parlamentar.
    telefone: str
        Telefone de contato.
    titulo: str
        Título da frente parlamentar.
    uri: str
        Endereço para coleta de dados direta pela API da frente parlamentar.
    website: str
        URL do website da frente parlamentar.

    Exemplos
    --------
    Obter título da frente parlamentar #54258.
    >>> fr = camara.Frente(cod=54258)
    >>> fr.url_registro
    ... 'Frente Parlamentar Mista da Telessaúde'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['frentes', str(cod)])['dados']
        self.coordenador = self.dados['coordenador']
        self.documento = self.dados['urlDocumento']
        self.email = self.dados['email']
        self.id_sitacao = self.dados['idSituacao']
        self.keywords = self.dados['keywords']
        self.legislatura = self.dados['idLegislatura']
        self.situacao = self.dados['situacao']
        self.telefone = self.dados['telefone']
        self.titulo = self.dados['titulo']
        self.uri = self.dados['uri']
        self.website = self.dados['urlWebsite']
        

    def membros(
            self,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Os deputados que participam da frente parlamentar.

        Uma lista dos deputados participantes da frente parlamentar e os
        papéis que exerceram nessa frente (signatário, coordenador ou
        presidente). Observe que, mesmo no caso de frentes parlamentares
        mistas (compostas por deputados e senadores), são retornados apenas
        dados sobre os deputados.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos deputados que participam da frente parlamentar.

        ----------------------------------------------------------------------
        '''

        path = ['frentes', str(self.cod), 'membros']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Legislatura:
    '''
    Informações extras sobre uma determinada legislatura da Câmara.

    Parâmetros
    ----------
    cod: int
        Código numérico da legislatura da qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico da legislatura.
    inicio: str
        Primeiro dia da legislatura.
    fim: str
        Último dia da legislatura.
    uri: str
        Endereço para coleta de dados direta pela API da legislatura.

    Exemplos
    --------
    Obter o primeiro e último dia da legislatura #56.
    >>> leg = camara.Legislatura(cod=54)
    >>> leg.inicio
    ... '2011-02-01'
    >>> leg.fim
    ... '2015-01-31'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['legislaturas', str(cod)])['dados']
        self.fim = self.dados['dataFim']
        self.inicio = self.dados['dataInicio']
        self.uri = self.dados['uri']


    def mesa(
            self,
            inicio: str = None,
            fim: str = None,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Quais deputados fizeram parte da Mesa Diretora em uma legislatura.

        Retorna uma lista com dados básicos sobre todos os deputados que
        ocuparam algum posto na Mesa Diretora da Câmara em algum período de
        tempo dentro da legislatura. Normalmente, cada legislatura tem duas
        Mesas Diretoras, com presidente, dois vice-presidentes, quatro
        secretários parlamentares e os suplentes dos secretários.

        Parâmetros
        ----------
        inicio: str (default=None)
            Dia de início do intervalo de tempo do qual se deseja saber a
            composição da Mesa, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término do intervalo de tempo do qual se deseja saber a
            composição da Mesa, no formato 'AAAA-MM-DD'.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos deputados que participam da frente parlamentar.

        ----------------------------------------------------------------------
        '''

        params = {}
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim

        path = ['legislaturas', str(self.cod), 'mesa']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Orgao:
    '''
    Informações detalhadas sobre um órgão da Câmara.

    Parâmetros
    ----------
    cod: int
        Código numérico do órgão do qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico do órgão.
    apelido: str
        Apelido do órgão.
    casa: str
        Casa do órgão.
    cod_tipo: int
        Código do tipo do órgão.
    fim: str
        Data final do órgão.
    inicio: str
        Data inicial do órgão.
    instalacao: str
        Data de instalação do órgão.
    nome: str
        Nome do órgão.
    nome_publicacao: str
        Nome de publicação.
    sala: str
        Sala do órgão.
    sigla: str
        Sigla do órgão.
    tipo: str
        Tipo do órgão.
    uri: str
        Endereço para coleta de dados direta pela API do órgão.
    urlWebsite: str
        URL para acessar o website do órgão.

    Exemplos
    --------
    Obter o apelido do órgão #4.
    >>> org = camara.Orgao(cod=4)
    >>> org.apelido
    ... 'Mesa Diretora'
    
    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['orgaos', str(cod)])['dados']
        self.apelido = self.dados['apelido']
        self.casa = self.dados['casa']
        self.cod_tipo = self.dados['codTipoOrgao']
        self.fim = self.dados['dataFim']
        self.inicio = self.dados['dataInicio']
        self.instalacao = self.dados['dataInstalacao']
        self.nome = self.dados['nome']
        self.nome_publicacao = self.dados['nomePublicacao']
        self.sala = self.dados['sala']
        self.sigla = self.dados['sigla']
        self.tipo = self.dados['tipoOrgao']
        self.uri = self.dados['uri']
        self.urlWebsite = self.dados['urlWebsite']



    def eventos(
            self,
            tipo_evento: str = None,
            inicio: str = None,
            fim: str = None,
            pagina: int = None,
            itens: int = None,
            asc: bool = True,
            ordenar_por: str = None,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Os eventos ocorridos ou previstos em um órgão legislativo.

        Retorna uma lista de informações resumidas dos eventos realizados
        (ou a realizar) pelo órgão legislativo. Por padrão, são retornados
        eventos em andamento ou previstos para o mesmo dia, dois dias antes
        e dois dias depois da requisição. Parâmetros podem ser passados para
        alterar esse período, bem como os tipos de eventos.

        Parâmetros
        ----------
        tipo_evento: str (default=None)
            Identificador numérico do tipo de evento que se deseja obter.
        inicio: str (default=None)
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        pagina: int (default=None)
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        itens: int (default=None)
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        asc: bool (default=True)
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por: str (default=None)
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de discursos feitos por um deputado em eventos diversos.

        ----------------------------------------------------------------------
        '''

        params = {}
        if tipo_evento is not None:
            params['idTipoEvento'] = tipo_evento
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        params['ordem'] = 'asc' if asc else 'desc'
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['orgaos', str(self.cod), 'eventos']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def membros(
            self,
            inicio: str = None,
            fim: str = None,
            pagina: int = None,
            itens: int = None,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Lista de cargos de um órgão e parlamentares que os ocupam.

        Retorna uma lista de dados resumidos que identificam cada parlamentar
        e o cargo ou posição que ocupa ou ocupou no órgão parlamentar durante
        um certo período de tempo. Se não forem passados parâmetros que
        delimitem esse período, o serviço retorna os membros do órgão no
        momento da requisição. Se o órgão não existir mais ou não estiver
        instalado, é retornada uma lista vazia.

        Parâmetros
        ----------
        inicio: str (default=None)
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        itens: int (default=None)
            Número máximo de itens na “página” que se deseja obter com esta
            requisição.
        pagina: int (default=None)
            Número da “página” de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de cargos de um órgão e parlamentares que os ocupam.

        ----------------------------------------------------------------------
        '''

        params = {}
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens

        path = ['orgaos', str(self.cod), 'membros']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def votacoes(
            self,
            proposicao: int = None,
            inicio: str = None,
            fim: str = None,
            pagina: int = None,
            itens: int = None,
            asc: bool = True,
            ordenar_por: str = None,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Uma lista de eventos com a participação do parlamentar.

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

        Parâmetros
        ----------
        proposicao: int (default=None)
            Código numérico da proposição, que podem ser obtidos por meio da
            função `camara.lista_proposicoes`. Se presente, listará as
            votações que tiveram a proposição como objeto de votação ou que
            afetaram as proposições listadas.
        inicio: str (default=None)
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        pagina: int (default=None)
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        itens: int (default=None)
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        asc: bool (default=True)
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por: str (default=None)
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de discursos feitos por um deputado em eventos diversos.

        ----------------------------------------------------------------------
        '''

        params = {}
        if proposicao is not None:
            params['idProposicao'] = proposicao
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        params['ordem'] = 'asc' if asc else 'desc'
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['orgaos', str(self.cod), 'votacoes']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Partido:
    '''
    Informações detalhadas sobre um partido.

    Parâmetros
    ----------
    cod: int
        Código numérico do partido do qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico do partido.
    facebook: str
        URL da página no Facebook do partido.
    legislatura: str
        Código numérico da última legislatura.
    lider: dict
        Informações sobre o líder do partido.
    logo: str
        URL da logo do partido.
    nome: str
        Nome completo do partido.
    numero: int
        Número eleitoral do partido.
    sigla: str
        Sigla do partido.
    situacao: str
        Situação do partido.
    total_membros: str
        Total de membros do partido.
    total_posse: str
        Total de posse do partido.
    ultima_atualizacao: str
        Última atualização das informações sobre o partido.
    uri: str
        Endereço para coleta de dados direta pela API do partido.
    uri_membros: str
        Endereço para coleta de dados direta pela API dos membros do partido.
    website: str
        URL do website do partido.


    Exemplos
    --------
    Obter o nome completo do partido #36899.
    >>> p = camara.Partido(cod=36899)
    >>> p.nome
    ... 'Movimento Democrático Brasileiro'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['partidos', str(cod)])['dados']
        self.facebook = self.dados['urlFacebook']
        self.legislatura = self.dados['status']['idLegislatura']
        self.lider = self.dados['status']['lider']
        self.logo = self.dados['urlLogo']
        self.nome = self.dados['nome']
        self.numero = self.dados['numeroEleitoral']
        self.sigla = self.dados['sigla']
        self.situacao = self.dados['status']['situacao']
        self.total_membros = self.dados['status']['totalMembros']
        self.total_posse = self.dados['status']['totalPosse']
        self.ultima_atualizacao = self.dados['status']['data']
        self.uri = self.dados['uri']
        self.uri_membros = self.dados['status']['uriMembros']
        self.website = self.dados['urlWebSite']


    def membros(
            self,
            inicio: str = None,
            fim: str = None,
            legislatura: int = None,
            pagina: int = None,
            itens: int = None,
            ordenar_por: str = None,
            asc: bool = True,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Uma lista dos parlamentares de um partido durante um período.

        Retorna uma lista de deputados que estão ou estiveram em exercício
        pelo partido. Opcionalmente, pode-se usar os parâmetros `inicio`,
        `fim` ou `legislatura` para se obter uma lista de deputados filiados
        ao partido num certo intervalo de tempo. Isso é equivalente à função
        `lista_deputados` com filtro por partido, mas é melhor para obter
        informações sobre membros de partidos já extintos.

        Parâmetros
        ----------
        inicio: str (default=None)
            Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
        legislatura: int (default=None)
            Número da legislatura, à qual os dados buscados devem corresponder.
        pagina: int (default=None)
            Número da página de resultados, a partir de 1, que se deseja
            obter com a requisição, contendo o número de itens definido pelo
            parâmetro itens. Se omitido, assume o valor 1.
        itens: int (default=None)
            Número máximo de itens na página que se deseja obter com esta
            requisição.
        asc: bool (default=True)
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por: str (default=None)
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista dos parlamentares de um partido durante um período.

        ----------------------------------------------------------------------
        '''

        params = {}
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim
        if legislatura is not None:
            params['idLegislatura'] = legislatura
        if pagina is not None:
            params['pagina'] = pagina
        if itens is not None:
            params['itens'] = itens
        params['ordem'] = 'asc' if asc else 'desc'
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['partidos', str(self.cod), 'membros']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Proposicao:
    '''
    Informações detalhadas sobre uma proposição específica.

    Parâmetros
    ----------
    cod: int
        Código numérico da proposição da qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: int
        Código numérico da proposição.
    uri: str
        Endereço para coleta de dados direta pela API da proposição.
    tipo_sigla: str
        Sigla do tipo de proposição.
    tipo_codigo: int
        Código numérico do tipo de proposição.
    numero: int
        Número da proposição.
    ano: int
        Ano da proposição.
    ementa: str
        Ementa da proposição.
    apresentacao: str
        Horário da apresentação da proposição no formato 'AAAA-MM-DD HH:MM'.
    uri_orgao_numerador: str
        Endereço para coleta de dados direta pela API do órgão numerador.
    ultima_atualizacao: str
        Data da última atualização do status da proposição.
    sequencia: int
        Sequência da proposição.
    sigla_orgao: str
        Sigla do órgão.
    uri_orgao: str
        Endereço para coleta de dados direta pela API do órgão.
    uri_ultimo_relator: str
        Endereço para coleta de dados direta pela API do último relaltor.
    regime: str
        Regime da proposição.
    descricao_tramitacao: str
        Descrição da tramitação.
    cod_tipo_tramitacao: str
        Código do tipo da tramitação.
    descricao_situacao: str
        Descrição da situação da proposição.
    cod_situacao: int
        Código númerico da situação da proposição.
    despacho: str
        Despacho.
    url: str
        URL da proposição.
    ambito: str
        Âmbito da proposição.
    uri_autores: str
        Endereço para coleta de dados direta pela API dos autores.
    descricao_tipo: str
        Descrição do tipo da proposição.
    ementa_detalhada: str
        Ementa detalhada da proposição.
    keywords: str
        Palavras-chaves da proposição.
    uri_proposicao_principal: str
        Endereço para coleta de dados direta pela API da proposição principal.
    uri_proposicao_anterior: str
        Endereço para coleta de dados direta pela API da proposição anterior.
    uri_proposicao_posterior: str
        Endereço para coleta de dados direta pela API da proposição posterior.
    url_inteiro_teor: str
        URL do inteiro teor.
    urn_final: str
        URN final.
    texto: str
        Texto da proposição.
    justificativa: str
        Justificativa da proposição.

    Exemplos
    --------
    Obter a ementa da proposição #15990.
    >>> prop = camara.Proposicao(cod=15990)
    >>> prop.ementa
    ... ''Cria salvaguardas para a tecnologia no campo nuclear...'

    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['proposicoes', str(cod)])['dados']
        self.uri = self.dados['uri']
        self.tipo_sigla = self.dados['siglaTipo']
        self.tipo_codigo = self.dados['codTipo']
        self.numero = self.dados['numero']
        self.ano = self.dados['ano']
        self.ementa = self.dados['ementa']
        self.apresentacao = self.dados['dataApresentacao']
        self.uri_orgao_numerador = self.dados['uriOrgaoNumerador']
        self.ultima_atualizacao = self.dados['statusProposicao']['dataHora']
        self.sequencia = self.dados['statusProposicao']['sequencia']
        self.sigla_orgao = self.dados['statusProposicao']['siglaOrgao']
        self.uri_orgao = self.dados['statusProposicao']['uriOrgao']
        self.uri_ultimo_relator = self.dados['statusProposicao']['uriUltimoRelator']
        self.regime = self.dados['statusProposicao']['regime']
        self.descricao_tramitacao = self.dados['statusProposicao']['descricaoTramitacao']
        self.cod_tipo_tramitacao = self.dados['statusProposicao']['codTipoTramitacao']
        self.descricao_situacao = self.dados['statusProposicao']['descricaoSituacao']
        self.cod_situacao = self.dados['statusProposicao']['codSituacao']
        self.despacho = self.dados['statusProposicao']['despacho']
        self.url = self.dados['statusProposicao']['url']
        self.ambito = self.dados['statusProposicao']['ambito']
        self.uri_autores = self.dados['uriAutores']
        self.descricao_tipo = self.dados['descricaoTipo']
        self.ementa_detalhada = self.dados['ementaDetalhada']
        self.keywords = self.dados['keywords']
        self.uri_proposicao_principal = self.dados['uriPropPrincipal']
        self.uri_proposicao_anterior = self.dados['uriPropAnterior']
        self.uri_proposicao_posterior = self.dados['uriPropPosterior']
        self.url_inteiro_teor = self.dados['urlInteiroTeor']
        self.urn_final = self.dados['urnFinal']
        self.texto = self.dados['texto']
        self.justificativa = self.dados['justificativa']


    def autores(self) -> _pd.DataFrame:
        '''
        Lista pessoas e/ou entidades autoras da proposição.

        Retorna uma lista em que cada item identifica uma pessoa ou entidade
        que é autora da proposição. Além de deputados, também podem ser
        autores de proposições os senadores, a sociedade civil, assembleias
        legislativas e os poderes Executivo e Judiciário.
        Pelo Regimento da Câmara, todos os que assinam uma proposição são
        considerados autores (art. 102), tanto os proponentes quanto os
        apoiadores.
        Para obter mais informações sobre cada autor, é recomendável acessar,
        se disponível, a URL que é valor do campo uri.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista pessoas e/ou entidades autoras da proposição.

        ----------------------------------------------------------------------
        '''

        path = ['proposicoes', str(self.cod), 'autores']
        dados = _api.get(path=path, params=None)
        return _df(dados, None)


    def relacionadas(
            self,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Uma lista de proposições relacionadas a uma em especial.

        Lista de informações básicas sobre proposições que de alguma forma se
        relacionam com a proposição, como pareceres, requerimentos,
        substitutivos, etc.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de proposições relacionadas a uma em especial.

        ----------------------------------------------------------------------
        '''

        path = ['proposicoes', str(self.cod), 'relacionadas']
        dados = _api.get(path=path, params=None)
        index_col = 'id' if index else None
        return _df(dados, index_col)


    def temas(
            self,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Lista de áreas temáticas de uma proposição.

        Lista em que cada item traz informações sobre uma área temática à qual
        a proposição se relaciona, segundo classificação oficial do Centro de
        Documentação e Informação da Câmara.

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `codTema` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de áreas temáticas de uma proposição.

        ----------------------------------------------------------------------
        '''

        path = ['proposicoes', str(self.cod), 'temas']
        dados = _api.get(path=path, params=None)
        index_col = 'codTema' if index else None
        return _df(dados, index_col)


    def tramitacoes(
            self,
            inicio: str = None,
            fim: str = None,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        O histórico de passos na tramitação de uma proposta.

        Lista que traz, como cada item, um “retrato” de informações que podem
        ser alteradas a cada etapa de tramitação na vida da proposição (como
        regime de tramitação e situação) e informações sobre o que causou esse
        novo estado. Esta representação das tramitações ainda é provisória.

        Parâmetros
        ----------
        inicio: str (default=None)
            Data de início da tramitação, no formato 'AAAA-MM-DD'.
        fim: str (default=None)
            Data de término da tramitação, no formato 'AAAA-MM-DD'.
        index: bool (default=False)
            Se True, define a coluna `sequencia` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de passos na tramitação de uma proposta.

        ----------------------------------------------------------------------
        '''

        params = {}
        if inicio is not None:
            params['dataInicio'] = inicio
        if fim is not None:
            params['dataFim'] = fim

        path = ['proposicoes', str(self.cod), 'tramitacoes']
        dados = _api.get(path=path, params=params)
        index_col = 'sequencia' if index else None
        return _df(dados, index_col)


    def votacoes(
            self,
            asc: bool = True,
            ordenar_por: str = None,
            index: bool = False
        ) -> _pd.DataFrame:
        '''
        Informações detalhadas de votações sobre a proposição.

        Retorna uma lista de identificadores básicos sobre as votações na
        Câmara que tiveram a proposição como objeto ou como afetada pelos seus
        resultados. Dados complementares sobre cada votação listada podem ser
        obtidos pelo objeto `camara.Votacao`.

        Parâmetros
        ----------
        asc: bool (default=True)
            Se os registros são ordenados no sentido ascendente:
            - True: De A a Z ou 0 a 9 (ascendente);
            - False: De Z a A ou 9 a 0 (descendente).
        ordenar_por: str (default=None)
            Qual dos elementos da representação deverá ser usado para aplicar
            ordenação à lista.
        index: bool (default=False)
            Se True, define a coluna `id` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de votações sobre a proposição.

        ----------------------------------------------------------------------
        '''

        params = {}
        params['ordem'] = 'asc' if asc else 'desc'
        if ordenar_por is not None:
            params['ordenarPor'] = ordenar_por

        path = ['proposicoes', str(self.cod), 'votacoes']
        dados = _api.get(path=path, params=params)
        index_col = 'id' if index else None
        return _df(dados, index_col)



class Votacao:
    '''
    Informações detalhadas sobre uma votação da Câmara.

    Retorna um conjunto detalhado de dados sobre a votação, tais como as
    proposições que podem ter sido o objeto da votação e os efeitos de
    tramitação de outras proposições que eventualmente tenham sido cadastrados
    em consequência desta votação.

    Parâmetros
    ----------
    cod: str
        Código alfa-numérico da votação da qual se deseja informações.

    Atributos
    ---------
    dados: dict
        Conjunto completo de dados.
    cod: str
        Código alfa-numérico da votação.
    aprovacao: int
        Aprovação da votação.
    data: str
        Data da votação.
    data_regitro: str
        Data e horário de registro da votação.
    data_ultima_abertura: str
        Data e horário da última abertura da votação.
    descricao: str
        Descrição da votação.
    efeitos_registrados: list
        Lista de efeitos registrados.
    evento: int
        Código numérico do evento da votação.
    orgao: int
        Código numérico do órgão da votação.
    objetos_possiveis: list of dict
        Lista de objetos possíveis.
    proposicoes_afetadas: str
        Proposições afetadas.
    sigla_orgao: str
        Sigla do órgão.
    ultima_apresentacao_proposicao: dict
        Última apresentação da proposição.
    uri: str
        Endereço para coleta de dados direta pela API da votação.
    uri_evento: str
        Endereço para coleta de dados direta pela API do evento.
    uri_orgao: str
        Endereço para coleta de dados direta pela API do órgão.

    Exemplos
    --------
    Obter a data da votação #2265603-43.
    >>> vot = camara.Votacao(cod='2265603-43')
    >>> vot.data
    ... '2020-12-22'
    
    --------------------------------------------------------------------------
    '''

    def __init__(self, cod:int):
        self.cod = cod
        self.dados = _api.get(['votacoes', str(cod)])['dados']
        self.aprovacao = self.dados['aprovacao']
        self.data = self.dados['data']
        self.data_regitro = self.dados['dataHoraRegistro']
        self.data_ultima_abertura = self.dados['dataHoraUltimaAberturaVotacao']
        self.descricao = self.dados['descricao']
        self.efeitos_registrados = self.dados['efeitosRegistrados']
        self.evento = self.dados['idEvento']
        self.orgao = self.dados['idOrgao']
        self.objetos_possiveis = self.dados['objetosPossiveis']
        self.proposicoes_afetadas = self.dados['proposicoesAfetadas']
        self.sigla_orgao = self.dados['siglaOrgao']
        self.ultima_apresentacao_proposicao = self.dados['ultimaApresentacaoProposicao']
        self.uri = self.dados['uri']
        self.uri_evento = self.dados['uriEvento']
        self.uri_orgao = self.dados['uriOrgao']


    def orientacoes(self, index=False) -> _pd.DataFrame:
        '''
        O voto recomendado pelas lideranças aos seus deputados na votação.

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

        Parâmetros
        ----------
        index: bool (default=False)
            Se True, define a coluna `codPartidoBloco` como index do DataFrame.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de recomendações pelas lideranças aos seus deputados.

        ----------------------------------------------------------------------
        '''

        path = ['votacoes', str(self.cod), 'orientacoes']
        dados = _api.get(path=path, params=None)
        index_col = 'codPartidoBloco' if index else None
        return _df(dados, index_col)


    def votos(self) -> _pd.DataFrame:
        '''
        Como cada parlamentar votou em uma votação nominal e aberta.

        Se a votação da Câmara é nominal e não foi secreta, retorna uma lista
        em que cada item contém os identificadores básicos de um deputado e o
        voto ou posicionamento que ele registrou.
        O resultado é uma lista vazia se a votação foi uma votação simbólica,
        em que os votos individuais não são contabilizados. Mas há algumas
        votações simbólicas que também têm registros de "votos": nesses casos,
        normalmente se trata de parlamentares que pediram expressamente que
        seus posicionamentos fossem registrados.
        Não são listados parlamentares ausentes à votação.

        Retorna
        -------
        pandas.core.frame.DataFrame
            Lista de parlamentares.

        ----------------------------------------------------------------------
        '''

        path = ['votacoes', str(self.cod), 'votos']
        dados = _api.get(path=path, params=None)
        return _df(dados, None)



def lista_blocos(
        legislatura: int = None,
        pagina: int = None,
        itens: int = None,
        asc: bool = True,
        ordenar_por: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Lista de dados sobre os blocos partidários.

    Nas atividades parlamentares, partidos podem se juntar em blocos
    partidários. Quando associados, os partidos passam a trabalhar como se
    fossem um "partidão", com um só líder e um mesmo conjunto de vice-líderes.
    Os blocos só podem existir até o fim da legislatura em que foram criados:
    na legislatura seguinte, os mesmos partidos, se associados, formam um novo
    bloco. Este recurso é uma lista dos blocos em atividade no momento da
    requisição. Se forem passados números de legislaturas com o parâmetro
    `legislatura`, são listados também os blocos formados e extintos nessas
    legislaturas.

    Parâmetros
    ----------
    legislatura: int (default=None)
        Número da legislatura a qual os dados buscados devem corresponder.
    pagina: int (default=None)
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido pelo
        parâmetro itens. Se omitido, assume o valor 1.
    itens: int (default=None)
        Número máximo de itens na página que se deseja obter com esta
        requisição.
    asc: bool (default=True)
        Se os registros são ordenados no sentido ascendente:
        - True: De A a Z ou 0 a 9 (ascendente);
        - False: De Z a A ou 9 a 0 (descendente).
    ordenar_por: str (default=None)
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.
    index: bool (default=False)
        Se True, define a coluna `id` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de dados sobre os blocos partidários.

    --------------------------------------------------------------------------
    '''

    params = {}
    if legislatura is not None:
        params['idLegislatura'] = legislatura
    if pagina is not None:
        params['pagina'] = pagina
    if itens is not None:
        params['itens'] = itens
    params['ordem'] = 'asc' if asc else 'desc'
    if ordenar_por is not None:
        params['ordenarPor'] = ordenar_por

    dados = _api.get(path='blocos', params=params)
    index_col = 'id' if index else None
    return _df(dados, index_col)



def lista_deputados(
        nome: str = None,
        legislatura: int = None,
        uf: str = None,
        partido: str = None,
        sexo: str = None,
        inicio: str = None,
        fim: str = None,
        pagina: int = None,
        itens: int = None,
        asc: bool = True,
        ordenar_por: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Listagem e busca de deputados, segundo critérios.

    Retorna uma lista de dados básicos sobre deputados que estiveram em
    exercício parlamentar em algum intervalo de tempo. Se não for passado um
    parâmetro de tempo, como `legislatura` ou `inicio`, a lista enumerará
    somente os deputados em exercício no momento da requisição.

    Parâmetros
    ----------
    nome: str (default=None)
        Parte do nome dos parlamentares.
    legislatura: int (default=None)
        Número da legislatura a qual os dados buscados devem corresponder.
    uf: str (default=None)
        Sigla da unidade federativa (estados e Distrito Federal).
        Se None, serão retornados deputados de todos os estados.
    partido: str (default=None)
        Sigla do partido ao qual sejam filiados os deputados.
        Para obter as siglas válidas, consulte a função `camara.lista_partidos`.
        Atenção: partidos diferentes podem usar a mesma sigla em diferentes
        legislaturas.
    sexo: str (default=None)
        Letra que designe o gênero dos parlamentares que se deseja buscar,
        - 'M': Masculino;
        - 'F': Feminino.
    inicio: str (default=None)
        Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
    fim: str (default=None)
        Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
    pagina: int (default=None)
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido pelo
        parâmetro itens. Se omitido, assume o valor 1.
    itens: int (default=None)
        Número máximo de itens na página que se deseja obter com esta
        requisição.
    asc: bool (default=True)
        Se os registros são ordenados no sentido ascendente:
        - True: De A a Z ou 0 a 9 (ascendente);
        - False: De Z a A ou 9 a 0 (descendente).
    ordenar_por: str (default=None)
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.
    index: bool (default=False)
        Se True, define a coluna `id` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de deputados.

    --------------------------------------------------------------------------
    '''

    params = {}
    if nome is not None:
        params['nome'] = nome
    if legislatura is not None:
        params['idLegislatura'] = legislatura
    if uf is not None:
        params['siglaUf'] = _utils.parse_uf(uf)
    if partido is not None:
        params['siglaPartido'] = partido
    if sexo is not None:
        params['siglaSexo'] = sexo
    if inicio is not None:
        params['dataInicio'] = inicio
    if fim is not None:
        params['dataFim'] = fim
    if pagina is not None:
        params['pagina'] = pagina
    if itens is not None:
        params['itens'] = itens
    params['ordem'] = 'asc' if asc else 'desc'
    if ordenar_por is not None:
        params['ordenarPor'] = ordenar_por

    dados = _api.get(path='deputados', params=params)
    index_col = 'id' if index else None
    return _df(dados, index_col)



def lista_eventos(
        tipo_evento: int = None,
        situacao: int = None,
        tipo_orgao: int = None,
        orgao: int = None,
        data_inicio: str = None,
        data_fim: str = None,
        hora_inicio: str = None,
        hora_fim: str = None,
        pagina: int = None,
        itens: int = None,
        asc: bool = True,
        ordenar_por: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Lista de eventos ocorridos ou previstos nos diversos órgãos da Câmara.

    Retorna uma lista cujos elementos trazem informações básicas sobre eventos
    dos órgãos legislativos da Câmara, previstos ou já ocorridos, em um certo
    intervalo de tempo. Esse intervalo pode ser configurado pelos parâmetros
    de data e hora listados abaixo. Se nenhum for passado, são listados
    eventos dos cinco dias anteriores, dos cinco dias seguintes e do próprio
    dia em que é feita a requisição.

    Parâmetros
    ----------
    tipo_evento: int (default=None)
        Identificador numérico do tipo de evento que se deseja obter.
        Os valores válidos podem ser obtidos pela função
        `camara.referencias('tiposEvento')`.
    situacao: int (default=None)
        Identificador numéricos do tipo de situação de evento.
        Valores válidos podem ser obtidos pela função
        `camara.referencias('situacoesEvento')`.
    tipo_orgao: int (default=None)
        Identificador numérico do tipo de órgão realizador dos eventos que se
        deseja obter. Os valores válidos podem ser obtidos pela função
        `camara.referencias('tiposOrgao').
    orgao: int (default=None)
        Identificador numérico do órgão. Os identificadores podem ser obtidos
        pela função `camara.lista_orgaos`.
    data_inicio: str (default=None)
        Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
    data_fim: str (default=None)
        Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
    hora_inicio: str (default=None)
        Hora inicial de um intervalo de tempo, no formato 'HH:MM', em horário
        de Brasília.
    hora_fim: str (default=None)
        Hora final de um intervalo de tempo, no formato 'HH:MM', em horário
        de Brasília.
    pagina: int (default=None)
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido pelo
        parâmetro itens. Se omitido, assume o valor 1.
    itens: int (default=None)
        Número máximo de itens na página que se deseja obter com esta
        requisição.
    asc: bool (default=True)
        Se os registros são ordenados no sentido ascendente:
        - True: De A a Z ou 0 a 9 (ascendente);
        - False: De Z a A ou 9 a 0 (descendente).
    ordenar_por: str (default=None)
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.
    index: bool (default=False)
        Se True, define a coluna `id` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de eventos ocorridos ou previstos nos diversos órgãos da
        Câmara.

    --------------------------------------------------------------------------
    '''

    params = {}

    if tipo_evento is not None:
        params['codTipoEvento'] = tipo_evento
    if situacao is not None:
        params['codSituacao'] = situacao
    if tipo_orgao is not None:
        params['codTipoOrgao'] = tipo_orgao
    if orgao is not None:
        params['idOrgao'] = orgao
    if data_inicio is not None:
        params['dataInicio'] = data_inicio
    if data_fim is not None:
        params['dataFim'] = data_fim
    if hora_inicio is not None:
        params['horaInicio'] = hora_inicio
    if hora_fim is not None:
        params['horaFim'] = hora_fim
    if pagina is not None:
        params['pagina'] = pagina
    if itens is not None:
        params['itens'] = itens
    params['ordem'] = 'asc' if asc else 'desc'
    if ordenar_por is not None:
        params['ordenarPor'] = ordenar_por

    dados = _api.get(path='eventos', params=params)
    index_col = 'id' if index else None
    return _df(dados, index_col)



def lista_frentes(
        legislatura: int = None,
        pagina: int = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Lista de frentes parlamentares de uma ou mais legislaturas.

    Retorna uma lista de informações sobre uma frente parlamentar - um
    agrupamento oficial de parlamentares em torno de um determinado tema ou
    proposta. As frentes existem até o fim da legislatura em que foram
    criadas, e podem ser recriadas a cada legislatura. Algumas delas são
    compostas por deputados e senadores.
    Um número de legislatura pode ser passado como parâmetro, mas se for
    omitido são retornadas todas as frentes parlamentares criadas desde 2003.

    Parâmetros
    ----------
    legislatura: int (default=None)
        Número da legislatura a qual os dados buscados devem corresponder.
    pagina: int (default=None)
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido pelo
        parâmetro itens. Se omitido, assume o valor 1.
    index: bool (default=False)
        Se True, define a coluna `id` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de frentes parlamentares de uma ou mais legislaturas.

    --------------------------------------------------------------------------
    '''

    params = {}

    if legislatura is not None:
        params['idLegislatura'] = legislatura
    if pagina is not None:
        params['pagina'] = pagina

    dados = _api.get(path='frentes', params=params)
    index_col = 'id' if index else None
    return _df(dados, index_col)



def lista_legislaturas(
        data: str = None,
        pagina: int = None,
        itens: int = None,
        asc: bool = True,
        ordenar_por: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Os períodos de mandatos e atividades parlamentares da Câmara.

    Legislatura é o nome dado ao período de trabalhos parlamentares entre uma
    eleição e outra. Esta função retorna uma lista em que cada item contém as
    informações básicas sobre um desses períodos. Os números que identificam
    as legislaturas são sequenciais, desde a primeira que ocorreu.

    Parâmetros
    ----------
    data: str (default=None)
        Data no formato 'AAAA-MM-DD'. Se este parâmetro estiver presente, a
        função retornará as informações básicas sobre a legislatura que estava
        em curso na data informada.
    pagina: int (default=None)
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido pelo
        parâmetro itens. Se omitido, assume o valor 1.
    itens: int (default=None)
        Número máximo de itens na página que se deseja obter com esta
        requisição.
    asc: bool (default=True)
        Se os registros são ordenados no sentido ascendente:
        - True: De A a Z ou 0 a 9 (ascendente);
        - False: De Z a A ou 9 a 0 (descendente).
    ordenar_por: str (default=None)
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.
    index: bool (default=False)
        Se True, define a coluna `id` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de legislaturas da Câmara.

    --------------------------------------------------------------------------
    '''

    params = {}

    if data is not None:
        params['data'] = data
    if pagina is not None:
        params['pagina'] = pagina
    if itens is not None:
        params['itens'] = itens
    params['ordem'] = 'asc' if asc else 'desc'
    if ordenar_por is not None:
        params['ordenarPor'] = ordenar_por

    dados = _api.get(path='legislaturas', params=params)
    index_col = 'id' if index else None
    return _df(dados, index_col)



def lista_orgaos(
        sigla: str = None,
        tipo: int = None,
        inicio: str = None,
        fim: str = None,
        pagina: int = None,
        itens: int = None,
        asc: bool = True,
        ordenar_por: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Lista das comissões e outros órgãos legislativos da Câmara.

    Retorna uma lista de informações básicas sobre os órgãos legislativos e
    seus identificadores, tipos e descrições. É possível filtrar a lista por
    identificadores, tipos de órgãos, sigla, situação do órgão ou período de
    tempo em que os órgãos estiveram ativos, se aplicável.
    
    Parâmetros
    ----------
    sigla: str (default=None)
        Sigla oficialmente usadas para designar o órgão da câmara.
    tipo: int (default=None)
        Código numérico do tipo de órgãos que se deseja buscar dados. Pode ser
        obtido pela função `camara.referencias`.
    inicio: str (default=None)
        Data de início, no formato 'AAAA-MM-DD', de um intervalo de tempo no
        qual os órgãos buscados devem ter estado em atividade.
    fim: str (default=None)
        Data de término, no formato 'AAAA-MM-DD', de um intervalo de tempo no
        qual os órgãos buscados devem ter estado em atividade.
    pagina: int (default=None)
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido pelo
        parâmetro itens. Se omitido, assume o valor 1.
    itens: int (default=None)
        Número máximo de itens na página que se deseja obter com esta
        requisição.
    asc: bool (default=True)
        Se os registros são ordenados no sentido ascendente:
        - True: De A a Z ou 0 a 9 (ascendente);
        - False: De Z a A ou 9 a 0 (descendente).
    ordenar_por: str (default=None)
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.
    index: bool (default=False)
        Se True, define a coluna `id` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista das comissões e outros órgãos legislativos da Câmara.

    --------------------------------------------------------------------------
    '''

    params = {}

    if sigla is not None:
        params['sigla'] = sigla
    if tipo is not None:
        params['codTipoOrgao'] = tipo
    if inicio is not None:
        params['dataInicio'] = inicio
    if fim is not None:
        params['dataFim'] = fim
    if pagina is not None:
        params['pagina'] = pagina
    if itens is not None:
        params['itens'] = itens
    params['ordem'] = 'asc' if asc else 'desc'
    if ordenar_por is not None:
        params['ordenarPor'] = ordenar_por

    dados = _api.get(path='orgaos', params=params)
    index_col = 'id' if index else None
    return _df(dados, index_col)



def lista_partidos(
        legislatura: int = None,
        inicio: str = None,
        fim: str = None,
        pagina: int = None,
        itens: int = None,
        asc: bool = True,
        ordenar_por: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Os partidos políticos que têm ou já tiveram parlamentares em exercício na
    Câmara.

    Retorna uma lista de dados básicos sobre os partidos políticos que têm ou
    já tiveram deputados na Câmara. Se não forem passados parâmetros, a função
    retorna os partidos que têm deputados em exercício no momento da
    requisição. É possível obter uma lista de partidos representados na Câmara
    em um certo intervalo de datas ou de legislaturas.
    
    Parâmetros
    ----------
    legislatura: int (default=None)
        Número da legislatura a qual os dados buscados devem corresponder.
    inicio: str (default=None)
        Data de início de um intervalo de tempo, no formato 'AAAA-MM-DD'.
    fim: str (default=None)
        Data de término de um intervalo de tempo, no formato 'AAAA-MM-DD'.
    pagina: int (default=None)
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido pelo
        parâmetro itens. Se omitido, assume o valor 1.
    itens: int (default=None)
        Número máximo de itens na página que se deseja obter com esta
        requisição.
    asc: bool (default=True)
        Se os registros são ordenados no sentido ascendente:
        - True: De A a Z ou 0 a 9 (ascendente);
        - False: De Z a A ou 9 a 0 (descendente).
    ordenar_por: str (default=None)
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.
    index: bool (default=False)
        Se True, define a coluna `id` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de partidos políticos que têm ou já tiveram parlamentares em
        exercício na Câmara.

    --------------------------------------------------------------------------
    '''

    params = {}

    if legislatura is not None:
        params['idLegislatura'] = legislatura
    if inicio is not None:
        params['dataInicio'] = inicio
    if fim is not None:
        params['dataFim'] = fim
    if pagina is not None:
        params['pagina'] = pagina
    if itens is not None:
        params['itens'] = itens
    params['ordem'] = 'asc' if asc else 'desc'
    if ordenar_por is not None:
        params['ordenarPor'] = ordenar_por

    dados = _api.get(path='partidos', params=params)
    index_col = 'id' if index else None
    return _df(dados, index_col)



def lista_proposicoes(
        tipo: str = None,
        numero: int = None,
        ano: int = None,
        autor_cod: int = None,
        autor_nome: str = None,
        partido_sigla: str = None,
        partido_cod: int = None,
        autor_uf: str = None,
        keyword: str = None,
        tramitacao_senado = None,
        apresentacao_inicio: str = None,
        apresentacao_fim: str = None,
        situacao: int = None,
        tema: int = None,
        inicio: str = None,
        fim: str = None,
        pagina: int = None,
        itens: int = None,
        asc: bool = True,
        ordenar_por: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Lista de proposições na Câmara.

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
    
    Parâmetros
    ----------
    tipo: str (default=None)
        Sigla do tipo das proposições que se deseja obter. A lista de tipos e
        siglas existentes pode ser obtida pela função `camara.referencias`.
    numero: int (default=None)
        Número oficialmente atribuídos às proposições segundo o art. 137 do
        Regimento Interno, como “PL 1234/2016”
    ano: int (default=None)
        Ano de apresentação das proposições que serão listadas no formato
        'AAAA'.
    autor_cod: int (default=None)
        Código numérico identificador do deputado autor das proposições que
        serão listadas.
    autor_nome: str (default=None)
        Nome ou parte do nome do(s) autor(es) das proposições que se deseja
        obter. Deve estar entre aspas.
    partido_sigla: str (default=None)
        Sigla do partido a que pertençam os autores das proposições a serem
        listadas.
    partido_cod: int (default=None)
        Identificador numérico do partido a que pertençam os autores das
        proposições que serão listadas. Esses identificadores podem ser
        obtidos pela função `camara.lista_partidos` e são mais precisos do
        que as siglas, que podem ser usadas por partidos diferentes em épocas
        diferentes.
    autor_uf: str (default=None)
        Sigla da unidade da federação (estados e Distrito Federal) pela qual
        o(s) autor(es) das proposições selecionadas tenha(m) sido eleito(s).
    keyword: str (default=None)
        Palavra-chave sobre o tema a que a proposição se relaciona.
    tramitacao_senado
        Indicador booleano, com valor TRUE ou FALSE para trazer apenas
        proposições que já tenha tramitado no Senado.
    inicio: str (default=None)
        Data do início do intervalo de tempo em que tenha havido tramitação
        das proposições a serem listadas, no formato 'AAAA-MM-DD'. Se omitido,
        é assumido como a data de 30 dias anteriores à proposição.
    fim: str (default=None)
        Data do fim do intervalo de tempo em que tenha havido tramitação das
        proposições a serem listadas. Se omitido, é considerado ser o dia em
        que é feita a requisição.
    apresentacao_inicio: str (default=None)
        Data do início do intervalo de tempo em que tenham sido apresentadas
        as proposições a serem listadas, no formato 'AAAA-MM-DD'.
    apresentacao_fim: str (default=None)
        Data do fim do intervalo de tempo em que tenham sido apresentadas as
        proposições a serem listadas.
    situacao: int (default=None)
        Código numérico do tipo de situação em que se encontram as proposições
        que serão listadas. As situações possíveis podem ser obtidas pela
        função `camara.referencias`. Atenção: este parâmetro pode apresentar
        resultados inesperados, por problemas com o registro dos dados.
    tema: int (default=None)
        Código numérico das áreas temáticas das proposições que serão
        listadas. Os temas possíveis podem ser obtidos pela função
        `camara.referencias`.
    pagina: int (default=None)
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido pelo
        parâmetro itens. Se omitido, assume o valor 1.
    itens: int (default=None)
        Número máximo de itens na página que se deseja obter com esta
        requisição.
    asc: bool (default=True)
        Se os registros são ordenados no sentido ascendente:
        - True: De A a Z ou 0 a 9 (ascendente);
        - False: De Z a A ou 9 a 0 (descendente).
    ordenar_por: str (default=None)
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.
    index: bool (default=False)
        Se True, define a coluna `id` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de proposições na Câmara.

    --------------------------------------------------------------------------
    '''

    params = {}

    if tipo is not None:
        params['siglaTipo'] = tipo
    if numero is not None:
        params['numero'] = numero
    if ano is not None:
        params['ano'] = ano
    if autor_cod is not None:
        params['idDeputadoAutor'] = autor_cod
    if autor_nome is not None:
        params['autor'] = autor_nome
    if partido_sigla is not None:
        params['siglaPartidoAutor'] = partido_sigla
    if partido_cod is not None:
        params['idPartidoAutor'] = partido_cod
    if autor_uf is not None:
        params['siglaUfAutor'] = _utils.parse_uf(autor_uf)
    if keyword is not None:
        params['keywords'] = keyword
    if tramitacao_senado is not None:
        params['tramitacaoSenado'] = tramitacao_senado
    if apresentacao_inicio is not None:
        params['dataApresentacaoInicio'] = apresentacao_inicio
    if apresentacao_fim is not None:
        params['dataApresentacaoFim'] = apresentacao_fim
    if situacao is not None:
        params['codSituacao'] = situacao
    if tema is not None:
        params['codTema'] = tema
    if inicio is not None:
        params['dataInicio'] = inicio
    if fim is not None:
        params['dataFim'] = fim
    if pagina is not None:
        params['pagina'] = pagina
    if itens is not None:
        params['itens'] = itens
    params['ordem'] = 'asc' if asc else 'desc'
    if ordenar_por is not None:
        params['ordenarPor'] = ordenar_por

    dados = _api.get(path='proposicoes', params=params)
    index_col = 'id' if index else None
    return _df(dados, index_col)



def lista_votacoes(
        proposicao: int = None,
        evento: int = None,
        orgao: int = None,
        inicio: str = None,
        fim: str = None,
        pagina: int = None,
        itens: int = None,
        asc: bool = True,
        ordenar_por: str = None,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Lista de votações na Câmara.

    Retorna uma lista de informações básicas sobre as votações ocorridas em
    eventos dos diversos órgãos da Câmara. Se não forem passados parâmetros
    que delimitem o intervalo de tempo da pesquisa, são retornados dados sobre
    todas as votações ocorridas nos últimos 30 dias, em eventos de todos os
    órgãos.

    Os parâmetros de data permitem estender o período, mas por enquanto é
    necessário que as duas datas sejam de um mesmo ano. Quando apenas uma
    delas está presente, são retornadas somente as votações ocorridas no mesmo
    ano, antes de `fim` ou após `inicio`.
    
    Parâmetros
    ----------
    proposicao: int (default=None)
        Código numérico da proposição, que podem ser obtidos pela função
        `camara.lista_proposições`. Se presente, listará as votações que
        tiveram a proposição como objeto de votação ou que afetaram as
        proposições listadas.
    evento: int (default=None)
        Código numérico do evento realizado na Câmara, no qual tenham sido
        realizadas as votações a serem listadas. Os códigos podem ser obtidos
        pela função `camara.lista_eventos`. Somente os eventos deliberativos
        podem ter votações. Os eventos podem ter ocorrido fora do intervalo de
        tempo padrão ou definido por `inicio` e/ou `fim`.
    orgao: int (default=None)
        Código numérico do órgão da Câmara. Se presente, serão retornadas
        somente votações do órgão enumerado. Os códigos existentes podem ser
        obtidos pela função `camara.lista_orgaos`.
    inicio: str (default=None)
        Data em formato 'AAAA-MM-DD' para início do intervalo de tempo no qual
        tenham sido realizadas as votações a serem listadas. Se usado sozinho,
        esse parâmetro faz com que sejam retornadas votações ocorridas dessa
        data até o fim do mesmo ano. Se usado com `fim`, as duas datas devem
        ser de um mesmo ano.
    fim: str (default=None)
        Data em formato 'AAAA-MM-DD' que define o fim do intervalo de tempo no
        qual tenham sido realizadas as votações a serem listadas. Se usado
        sozinho, esse parâmetro faz com que sejam retornadas todas as votações
        ocorridas desde 1º de janeiro do mesmo ano até esta data. Se usado com
        `inicio`, é preciso que as duas datas sejam de um mesmo ano.
    pagina: int (default=None)
        Número da página de resultados, a partir de 1, que se deseja
        obter com a requisição, contendo o número de itens definido pelo
        parâmetro itens. Se omitido, assume o valor 1.
    itens: int (default=None)
        Número máximo de itens na página que se deseja obter com esta
        requisição.
    asc: bool (default=True)
        Se os registros são ordenados no sentido ascendente:
        - True: De A a Z ou 0 a 9 (ascendente);
        - False: De Z a A ou 9 a 0 (descendente).
    ordenar_por: str (default=None)
        Qual dos elementos da representação deverá ser usado para aplicar
        ordenação à lista.
    index: bool (default=False)
        Se True, define a coluna `id` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista de votações na Câmara.

    --------------------------------------------------------------------------
    '''

    params = {}

    if proposicao is not None:
        params['idProposicao'] = proposicao
    if evento is not None:
        params['idEvento'] = evento
    if orgao is not None:
        params['idOrgao'] = orgao
    if inicio is not None:
        params['dataInicio'] = inicio
    if fim is not None:
        params['dataFim'] = fim
    if pagina is not None:
        params['pagina'] = pagina
    if itens is not None:
        params['itens'] = itens
    params['ordem'] = 'asc' if asc else 'desc'
    if ordenar_por is not None:
        params['ordenarPor'] = ordenar_por

    dados = _api.get(path='votacoes', params=params)
    index_col = 'id' if index else None
    return _df(dados, index_col)



def referencias(
        lista: str,
        index: bool = False
    ) -> _pd.DataFrame:
    '''
    Listas de valores válidos para as funções deste módulo.

    Parâmetros
    ----------
    lista: str
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
    index: bool (default=False)
        Se True, define a coluna `cod` como index do DataFrame.

    Retorna
    -------
    pandas.core.frame.DataFrame
        Lista das referências válidas.
    '''
    
    referencia = {
        'autores': 'proposicoes/codTipoAutor',
        'temas': 'proposicoes/codTema',
        'eventos': 'tiposEvento',
        'orgaos': 'tiposOrgao',
        'proposicoes': 'tiposProposicao',
        'tramitacoes': 'tiposTramitacao',
        'ufs': 'uf',
        'situacoes_deputados': 'situacoesDeputado',
        'situacoes_eventos': 'situacoesEvento',
        'situacoes_orgaos': 'situacoesOrgao',
        'situacoes_proposicoes': 'situacoesProposicao'
    }
    
    if lista in referencia.keys():
        data = _api.get(f'referencias/{referencia[lista]}')
    else:
        raise TypeError('Referência inválida. Insira um dos seguintes valores para `lista`: ' \
            + ', '.join(list(referencia.keys())))
    
    df = _pd.DataFrame(data['dados'])
    if index:
        df.set_index('cod', inplace=True)
    
    return df