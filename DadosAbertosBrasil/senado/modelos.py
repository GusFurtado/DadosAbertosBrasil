"""Modelos de saída do módulo `senado`.

Cada classe descreve um registro de uma função do módulo. Os nomes dos campos
são os das colunas dos DataFrames; os aliases apontam para os nomes da API.

A API do Senado devolve um objeto quando há um item e uma lista quando há
vários (`Exercicio`, `Publicacao`, `Mandato`...). Os aliases aceitam as duas
formas: com lista, vale o último item (o mais recente).

"""

from pydantic import AliasChoices, AliasPath, Field

from ..utils.modelos import Bool, Data, Inteiro, Registro, Texto, Url


def _caminho(*partes: str | int) -> AliasChoices:
    """Aceita `a.b.c` com qualquer nível do meio sendo objeto ou lista."""
    opcoes = [list(partes)]
    for i in range(1, len(partes) - 1):
        novas = []
        for opcao in opcoes:
            j = opcao.index(partes[i]) + 1
            novas.append(opcao[:j] + [-1] + opcao[j:])
        opcoes += novas
    return AliasChoices(*(AliasPath(*o) for o in opcoes))


class Bloco(Registro):
    """Bloco parlamentar (`lista_blocos`)."""

    codigo: Inteiro = Field(None, validation_alias="CodigoBloco")
    nome: Texto = Field(None, validation_alias="NomeBloco")
    apelido: Texto = Field(None, validation_alias="NomeApelido")
    sigla: Texto = Field(None, validation_alias="SiglaBloco")
    data_criacao: Data = Field(None, validation_alias="DataCriacao")


class Senador(Registro):
    """Senador (`lista_senadores`, `lista_legislaturas`)."""

    codigo: Inteiro = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "CodigoParlamentar"))
    nome_parlamentar: Texto = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "NomeParlamentar"))
    nome_completo: Texto = Field(
        None, validation_alias=AliasPath("IdentificacaoParlamentar", "NomeCompletoParlamentar")
    )
    sexo: Texto = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "SexoParlamentar"))
    forma_tratamento: Texto = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "FormaTratamento"))
    foto: Url = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "UrlFotoParlamentar"))
    pagina_parlamentar: Url = Field(
        None, validation_alias=AliasPath("IdentificacaoParlamentar", "UrlPaginaParlamentar")
    )
    pagina_particular: Url = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "UrlPaginaParticular"))
    email: Url = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "EmailParlamentar"))
    partido: Texto = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "SiglaPartidoParlamentar"))
    uf: Texto = Field(
        None,
        validation_alias=AliasChoices(
            AliasPath("Mandato", "UfParlamentar"), *_caminho("Mandatos", "Mandato", "UfParlamentar").choices
        ),
    )
    data_inicio: Data = Field(
        None,
        validation_alias=AliasChoices(
            *_caminho("Mandato", "Exercicios", "Exercicio", "DataInicio").choices,
            *_caminho("Mandatos", "Mandato", "Exercicios", "Exercicio", "DataInicio").choices,
        ),
    )
    data_fim: Data = Field(
        None,
        validation_alias=AliasChoices(
            *_caminho("Mandato", "Exercicios", "Exercicio", "DataFim").choices,
            *_caminho("Mandatos", "Mandato", "Exercicios", "Exercicio", "DataFim").choices,
        ),
    )
    causa_afastamento: Texto = Field(
        None,
        validation_alias=AliasChoices(
            *_caminho("Mandato", "Exercicios", "Exercicio", "DescricaoCausaAfastamento").choices,
            *_caminho("Mandatos", "Mandato", "Exercicios", "Exercicio", "DescricaoCausaAfastamento").choices,
        ),
    )


class LoteEmendas(Registro):
    """Lote de emendas orçamentárias (`lista_orcamentos`)."""

    autor_nome: Texto = Field(None, validation_alias="NomeAutorOrcamento")
    ativo: Bool = Field(None, validation_alias="IndicadorAtivo")
    autor_email: Url = Field(None, validation_alias="EmailAutorOrcamento")
    autor_codigo: Inteiro = Field(None, validation_alias="CodigoAutorOrcamento")
    data_operacao: Data = Field(None, validation_alias="DataOperacao")
    quantidade_emendas: Inteiro = Field(None, validation_alias="QuantidadeEmendas")
    ano_execucao: Inteiro = Field(None, validation_alias="AnoExecucao")
    materia_numero: Texto = Field(None, validation_alias="NumeroMateria")
    materia_ano: Inteiro = Field(None, validation_alias="AnoMateria")
    tipo_sigla: Texto = Field(None, validation_alias="SiglaTipoPlOrcamento")
    tipo_descricao: Texto = Field(None, validation_alias="DescricaoTipoPlOrcamento")


class Partido(Registro):
    """Partido político (`lista_partidos`)."""

    codigo: Inteiro = Field(None, validation_alias="Codigo")
    sigla: Texto = Field(None, validation_alias="Sigla")
    nome: Texto = Field(None, validation_alias="Nome")
    data_criacao: Data = Field(None, validation_alias="DataCriacao")
    data_extincao: Data = Field(None, validation_alias="DataExtincao")


class SenadorDetalhes(Registro):
    """Atributos de `senado.Senador`."""

    email: Url = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "EmailParlamentar"))
    endereco: Texto = Field(None, validation_alias=AliasPath("DadosBasicosParlamentar", "EnderecoParlamentar"))
    foto: Url = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "UrlFotoParlamentar"))
    nascimento: Data = Field(None, validation_alias=AliasPath("DadosBasicosParlamentar", "DataNascimento"))
    naturalidade: Texto = Field(None, validation_alias=AliasPath("DadosBasicosParlamentar", "Naturalidade"))
    nome: Texto = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "NomeParlamentar"))
    nome_completo: Texto = Field(
        None, validation_alias=AliasPath("IdentificacaoParlamentar", "NomeCompletoParlamentar")
    )
    pagina: Url = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "UrlPaginaParlamentar"))
    partido: Texto = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "SiglaPartidoParlamentar"))
    sexo: Texto = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "SexoParlamentar"))
    tratamento: Texto = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "FormaTratamento"))
    uf: Texto = Field(None, validation_alias=AliasPath("IdentificacaoParlamentar", "UfParlamentar"))
    uf_naturalidade: Texto = Field(None, validation_alias=AliasPath("DadosBasicosParlamentar", "UfNaturalidade"))


class Aparte(Registro):
    """Aparte de um senador (`Senador.apartes`)."""

    codigo: Inteiro = Field(None, validation_alias="CodigoPronunciamento")
    data: Data = Field(None, validation_alias="DataPronunciamento")
    casa_sigla: Texto = Field(None, validation_alias="SiglaCasaPronunciamento")
    casa_nome: Texto = Field(None, validation_alias="NomeCasaPronunciamento")
    resumo: Texto = Field(None, validation_alias="TextoResumo")
    indexacao: Texto = Field(None, validation_alias="Indexacao")
    url: Url = Field(None, validation_alias="UrlTexto")
    uso_palavra: Inteiro = Field(None, validation_alias=AliasPath("TipoUsoPalavra", "Codigo"))
    sessao: Inteiro = Field(None, validation_alias=AliasPath("SessaoPlenaria", "CodigoSessao"))
    orador: Inteiro = Field(None, validation_alias=AliasPath("Orador", "CodigoParlamentar"))
    publicacao_veiculo: Texto = Field(
        None, validation_alias=_caminho("Publicacoes", "Publicacao", "DescricaoVeiculoPublicacao")
    )
    publicacao_data: Data = Field(None, validation_alias=_caminho("Publicacoes", "Publicacao", "DataPublicacao"))
    publicacao_primeira_pagina: Inteiro = Field(
        None, validation_alias=_caminho("Publicacoes", "Publicacao", "NumeroPagInicioPublicacao")
    )
    publicacao_ultima_pagina: Inteiro = Field(
        None, validation_alias=_caminho("Publicacoes", "Publicacao", "NumeroPagFimPublicacao")
    )
    republicacao: Bool = Field(None, validation_alias=_caminho("Publicacoes", "Publicacao", "IndicadorRepublicacao"))
    publicacao_url: Url = Field(None, validation_alias=_caminho("Publicacoes", "Publicacao", "UrlDiario"))


class Autoria(Registro):
    """Matéria de autoria de um senador (`Senador.autorias`)."""

    autor_principal: Bool = Field(None, validation_alias="IndicadorAutorPrincipal")
    codigo: Inteiro = Field(None, validation_alias=AliasPath("Materia", "Codigo"))
    processo: Inteiro = Field(None, validation_alias=AliasPath("Materia", "IdentificacaoProcesso"))
    descricao: Texto = Field(None, validation_alias=AliasPath("Materia", "DescricaoIdentificacao"))
    sigla: Texto = Field(None, validation_alias=AliasPath("Materia", "Sigla"))
    numero: Texto = Field(None, validation_alias=AliasPath("Materia", "Numero"))
    ano: Inteiro = Field(None, validation_alias=AliasPath("Materia", "Ano"))
    ementa: Texto = Field(None, validation_alias=AliasPath("Materia", "Ementa"))
    data: Data = Field(None, validation_alias=AliasPath("Materia", "Data"))
    outros_autores: Bool = Field(None, validation_alias="IndicadorOutrosAutores")


class Cargo(Registro):
    """Cargo ocupado por um senador (`Senador.cargos`)."""

    cargo_codigo: Inteiro = Field(None, validation_alias="CodigoCargo")
    cargo_descricao: Texto = Field(None, validation_alias="DescricaoCargo")
    data_inicio: Data = Field(None, validation_alias="DataInicio")
    data_fim: Data = Field(None, validation_alias="DataFim")
    comissao_codigo: Inteiro = Field(None, validation_alias=AliasPath("IdentificacaoComissao", "CodigoComissao"))
    comissao_sigla: Texto = Field(None, validation_alias=AliasPath("IdentificacaoComissao", "SiglaComissao"))
    comissao_nome: Texto = Field(None, validation_alias=AliasPath("IdentificacaoComissao", "NomeComissao"))
    casa: Texto = Field(None, validation_alias=AliasPath("IdentificacaoComissao", "SiglaCasaComissao"))


class MembroComissao(Registro):
    """Participação em comissão (`Senador.comissoes`)."""

    participacao: Texto = Field(None, validation_alias="DescricaoParticipacao")
    data_inicio: Data = Field(None, validation_alias="DataInicio")
    data_fim: Data = Field(None, validation_alias="DataFim")
    comissao_codigo: Inteiro = Field(None, validation_alias=AliasPath("IdentificacaoComissao", "CodigoComissao"))
    comissao_sigla: Texto = Field(None, validation_alias=AliasPath("IdentificacaoComissao", "SiglaComissao"))
    comissao_nome: Texto = Field(None, validation_alias=AliasPath("IdentificacaoComissao", "NomeComissao"))
    casa: Texto = Field(None, validation_alias=AliasPath("IdentificacaoComissao", "SiglaCasaComissao"))


class Curso(Registro):
    """Curso do histórico acadêmico (`Senador.cursos`)."""

    nome: Texto = Field(None, validation_alias="NomeCurso")
    grau_instrucao: Texto = Field(None, validation_alias="GrauInstrucao")
    estabelecimento: Texto = Field(None, validation_alias="Estabelecimento")
    local: Texto = Field(None, validation_alias="Local")


class Discurso(Registro):
    """Discurso de um senador (`Senador.discursos`)."""

    codigo: Inteiro = Field(None, validation_alias="CodigoPronunciamento")
    data: Data = Field(None, validation_alias="DataPronunciamento")
    casa_sigla: Texto = Field(None, validation_alias="SiglaCasaPronunciamento")
    casa_nome: Texto = Field(None, validation_alias="NomeCasaPronunciamento")
    resumo: Texto = Field(None, validation_alias="TextoResumo")
    indexacao: Texto = Field(None, validation_alias="Indexacao")
    url: Url = Field(None, validation_alias="UrlTexto")
    uso_palavra: Inteiro = Field(None, validation_alias=AliasPath("TipoUsoPalavra", "Codigo"))
    sessao: Inteiro = Field(None, validation_alias=AliasPath("SessaoPlenaria", "CodigoSessao"))
    publicacao_veiculo: Texto = Field(
        None, validation_alias=_caminho("Publicacoes", "Publicacao", "DescricaoVeiculoPublicacao")
    )
    publicacao_data: Data = Field(None, validation_alias=_caminho("Publicacoes", "Publicacao", "DataPublicacao"))
    publicacao_primeira_pagina: Inteiro = Field(
        None, validation_alias=_caminho("Publicacoes", "Publicacao", "NumeroPagInicioPublicacao")
    )
    publicacao_ultima_pagina: Inteiro = Field(
        None, validation_alias=_caminho("Publicacoes", "Publicacao", "NumeroPagFimPublicacao")
    )
    republicacao: Bool = Field(None, validation_alias=_caminho("Publicacoes", "Publicacao", "IndicadorRepublicacao"))
    publicacao_url: Url = Field(None, validation_alias=_caminho("Publicacoes", "Publicacao", "UrlDiario"))


class Filiacao(Registro):
    """Filiação partidária (`Senador.filiacoes`)."""

    codigo: Inteiro = Field(None, validation_alias=AliasPath("Partido", "CodigoPartido"))
    sigla: Texto = Field(None, validation_alias=AliasPath("Partido", "SiglaPartido"))
    nome: Texto = Field(None, validation_alias=AliasPath("Partido", "NomePartido"))
    data_filiacao: Data = Field(None, validation_alias="DataFiliacao")
    data_desfiliacao: Data = Field(None, validation_alias="DataDesfiliacao")


class Mandato(Registro):
    """Mandato de um senador (`Senador.mandatos`)."""

    codigo: Inteiro = Field(None, validation_alias="CodigoMandato")
    uf: Texto = Field(None, validation_alias="UfParlamentar")
    participacao: Texto = Field(None, validation_alias="DescricaoParticipacao")
    primeira_legislatura: Inteiro = Field(
        None, validation_alias=AliasPath("PrimeiraLegislaturaDoMandato", "NumeroLegislatura")
    )
    primeira_legislatura_inicio: Data = Field(
        None, validation_alias=AliasPath("PrimeiraLegislaturaDoMandato", "DataInicio")
    )
    primeira_legislatura_fim: Data = Field(None, validation_alias=AliasPath("PrimeiraLegislaturaDoMandato", "DataFim"))
    segunda_legislatura: Inteiro = Field(
        None, validation_alias=AliasPath("SegundaLegislaturaDoMandato", "NumeroLegislatura")
    )
    segunda_legislatura_inicio: Data = Field(
        None, validation_alias=AliasPath("SegundaLegislaturaDoMandato", "DataInicio")
    )
    segunda_legislatura_fim: Data = Field(None, validation_alias=AliasPath("SegundaLegislaturaDoMandato", "DataFim"))


class Lideranca(Registro):
    """Cargo de liderança (`Senador.liderancas`)."""

    lideranca: Texto = Field(None, validation_alias="UnidadeLideranca")
    tipo: Texto = Field(None, validation_alias="DescricaoTipoLideranca")
    casa_sigla: Texto = Field(None, validation_alias="SiglaCasaLideranca")
    casa_nome: Texto = Field(None, validation_alias="NomeCasaLideranca")
    data_designacao: Data = Field(None, validation_alias="DataDesignacao")
    data_fim: Data = Field(None, validation_alias="DataFim")
    partido_codigo: Inteiro = Field(None, validation_alias=AliasPath("Partido", "CodigoPartido"))
    partido_sigla: Texto = Field(None, validation_alias=AliasPath("Partido", "SiglaPartido"))
    partido_nome: Texto = Field(None, validation_alias=AliasPath("Partido", "NomePartido"))
    bloco_codigo: Inteiro = Field(None, validation_alias=AliasPath("Bloco", "CodigoBloco"))
    bloco_sigla: Texto = Field(None, validation_alias=AliasPath("Bloco", "SiglaBloco"))
    bloco_nome: Texto = Field(None, validation_alias=AliasPath("Bloco", "NomeBloco"))
    bloco_apelido: Texto = Field(None, validation_alias=AliasPath("Bloco", "ApelidoBloco"))


class Licenca(Registro):
    """Licença de um senador (`Senador.licencas`)."""

    codigo: Inteiro = Field(None, validation_alias="Codigo")
    inicio: Data = Field(None, validation_alias="DataInicio")
    inicio_previsto: Data = Field(None, validation_alias="DataInicioPrevista")
    fim: Data = Field(None, validation_alias="DataFim")
    fim_previsto: Data = Field(None, validation_alias="DataFimPrevista")
    afastamento_sigla: Texto = Field(None, validation_alias="SiglaTipoAfastamento")
    afastamento_descricao: Texto = Field(None, validation_alias="DescricaoTipoAfastamento")


class Profissao(Registro):
    """Profissão de um senador (`Senador.profissoes`)."""

    nome: Texto = Field(None, validation_alias="NomeProfissao")
    atividade_principal: Bool = Field(None, validation_alias="IndicadorAtividadePrincipal")


class Relatoria(Registro):
    """Matéria relatada por um senador (`Senador.relatorias`)."""

    materia: Inteiro = Field(None, validation_alias=AliasPath("Materia", "Codigo"))
    comissao: Inteiro = Field(None, validation_alias=AliasPath("Comissao", "Codigo"))
    codigo: Inteiro = Field(None, validation_alias="CodigoTipoRelator")
    descricao: Texto = Field(None, validation_alias="DescricaoTipoRelator")
    data_designacao: Data = Field(None, validation_alias="DataDesignacao")
    data_destituicao: Data = Field(None, validation_alias="DataDestituicao")
    motivo_destituicao: Texto = Field(None, validation_alias="DescricaoMotivoDestituicao")


class Voto(Registro):
    """Voto de um senador (`Senador.votacoes`)."""

    codigo: Inteiro = Field(None, validation_alias="CodigoSessaoVotacao")
    sessao: Inteiro = Field(None, validation_alias=AliasPath("SessaoPlenaria", "CodigoSessao"))
    materia: Inteiro = Field(None, validation_alias=AliasPath("Materia", "Codigo"))
    tramitacao: Inteiro = Field(
        None, validation_alias=AliasPath("Tramitacao", "IdentificacaoTramitacao", "CodigoTramitacao")
    )
    sequencial: Inteiro = Field(None, validation_alias="Sequencial")
    descricao: Texto = Field(None, validation_alias="DescricaoVotacao")
    votacao_secreta: Bool = Field(None, validation_alias="IndicadorVotacaoSecreta")
    voto: Texto = Field(None, validation_alias="SiglaDescricaoVoto")
    resultado: Texto = Field(None, validation_alias="DescricaoResultado")


class TipoUsoPalavra(Registro):
    """Tipo de uso da palavra (`lista_tipos_uso_palavra`)."""

    codigo: Inteiro = Field(None, validation_alias="Codigo")
    sigla: Texto = Field(None, validation_alias="Sigla")
    descricao: Texto = Field(None, validation_alias="Descricao")
    ativo: Bool = Field(None, validation_alias="IndicadorAtivo")
