"""Modelos de saída do módulo `camara`.

Cada classe descreve um registro de uma função do módulo. Os nomes dos campos
são os das colunas dos DataFrames; os aliases apontam para os nomes da API.

"""

from typing import Annotated

from pydantic import AliasPath, BeforeValidator, Field

from ..utils.modelos import Bool, Data, DataHora, Inteiro, Real, Registro, Texto, Url  # noqa: F401


def _codigos(orgaos):
    if isinstance(orgaos, list):
        return [o.get("id") if isinstance(o, dict) else o for o in orgaos]
    return orgaos


CodigosOrgaos = Annotated[list[int] | None, BeforeValidator(_codigos)]
"""Lista de órgãos da API reduzida aos códigos."""


class Bloco(Registro):
    """Bloco partidário (`lista_blocos`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    nome: Texto = None
    legislatura: Inteiro = Field(None, validation_alias="idLegislatura")


class BlocoDetalhes(Registro):
    """Atributos de `camara.Bloco`."""

    legislatura: Inteiro = Field(None, validation_alias="idLegislatura")
    nome: Texto = None
    uri: Url = None


class Deputado(Registro):
    """Deputado (`lista_deputados`, `Evento.deputados`, `Partido.membros`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    nome: Texto = None
    partido: Texto = Field(None, validation_alias="siglaPartido")
    partido_uri: Url = Field(None, validation_alias="uriPartido")
    uf: Texto = Field(None, validation_alias="siglaUf")
    legislatura: Inteiro = Field(None, validation_alias="idLegislatura")
    foto: Url = Field(None, validation_alias="urlFoto")
    email: Url = None


class DeputadoDetalhes(Registro):
    """Atributos de `camara.Deputado`."""

    condicao_eleitoral: Texto = Field(None, validation_alias=AliasPath("ultimoStatus", "condicaoEleitoral"))
    cpf: Texto = None
    descricao_status: Texto = Field(None, validation_alias=AliasPath("ultimoStatus", "descricaoStatus"))
    email: Url = Field(None, validation_alias=AliasPath("ultimoStatus", "email"))
    escolaridade: Texto = None
    falecimento: Texto = Field(None, validation_alias="dataFalecimento")
    foto: Url = Field(None, validation_alias=AliasPath("ultimoStatus", "urlFoto"))
    gabinete: dict | None = Field(None, validation_alias=AliasPath("ultimoStatus", "gabinete"))
    legislatura: Inteiro = Field(None, validation_alias=AliasPath("ultimoStatus", "idLegislatura"))
    municipio_nascimento: Texto = Field(None, validation_alias="municipioNascimento")
    nascimento: Data = Field(None, validation_alias="dataNascimento")
    nome: Texto = Field(None, validation_alias=AliasPath("ultimoStatus", "nome"))
    nome_completo: Texto = Field(None, validation_alias="nomeCivil")
    nome_eleitoral: Texto = Field(None, validation_alias=AliasPath("ultimoStatus", "nomeEleitoral"))
    partido: Texto = Field(None, validation_alias=AliasPath("ultimoStatus", "siglaPartido"))
    rede_social: list | None = Field(None, validation_alias="redeSocial")
    sexo: Texto = None
    situacao: Texto = Field(None, validation_alias=AliasPath("ultimoStatus", "situacao"))
    uf: Texto = Field(None, validation_alias=AliasPath("ultimoStatus", "siglaUf"))
    uf_nascimento: Texto = Field(None, validation_alias="ufNascimento")
    ultima_atualizacao: Data = Field(None, validation_alias=AliasPath("ultimoStatus", "data"))
    uri: Url = None
    website: Url = Field(None, validation_alias="urlWebsite")


class Despesa(Registro):
    """Despesa de um deputado (`Deputado.despesas`)."""

    codigo: Inteiro = Field(None, validation_alias="codDocumento")
    ano: Inteiro = None
    mes: Inteiro = None
    despesa: Texto = Field(None, validation_alias="tipoDespesa")
    tipo: Texto = Field(None, validation_alias="tipoDocumento")
    tipo_codigo: Inteiro = Field(None, validation_alias="codTipoDocumento")
    data: Data = Field(None, validation_alias="dataDocumento")
    numero: Texto = Field(None, validation_alias="numDocumento")
    valor: Real = Field(None, validation_alias="valorDocumento")
    url: Url = Field(None, validation_alias="urlDocumento")
    fornecedor_nome: Texto = Field(None, validation_alias="nomeFornecedor")
    fornecedor_cnpj: Texto = Field(None, validation_alias="cnpjCpfFornecedor")
    valor_liquido: Real = Field(None, validation_alias="valorLiquido")
    valor_glosa: Real = Field(None, validation_alias="valorGlosa")
    ressarcimento: Texto = Field(None, validation_alias="numRessarcimento")
    lote: Inteiro = Field(None, validation_alias="codLote")
    parcela: Inteiro = None


class Discurso(Registro):
    """Discurso de um deputado (`Deputado.discursos`)."""

    data_inicio: DataHora = Field(None, validation_alias="dataHoraInicio")
    data_fim: DataHora = Field(None, validation_alias="dataHoraFim")
    evento_uri: Url = Field(None, validation_alias="uriEvento")
    evento_fase: dict | None = Field(None, validation_alias="faseEvento")
    tipo: Texto = Field(None, validation_alias="tipoDiscurso")
    texto_uri: Url = Field(None, validation_alias="urlTexto")
    audio_url: Url = Field(None, validation_alias="urlAudio")
    video_url: Url = Field(None, validation_alias="urlVideo")
    keywords: Texto = None
    sumario: Texto = None
    transcricao: Texto = None


class EventoDeputado(Registro):
    """Evento com participação de um deputado (`Deputado.eventos`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    data_inicio: DataHora = Field(None, validation_alias="dataHoraInicio")
    data_fim: DataHora = Field(None, validation_alias="dataHoraFim")
    situacao: Texto = None
    descricao_tipo: Texto = Field(None, validation_alias="descricaoTipo")
    descricao: Texto = None
    local_externo: Texto = Field(None, validation_alias="localExterno")
    orgaos: CodigosOrgaos = None
    local: Texto = Field(None, validation_alias=AliasPath("localCamara", "nome"))
    local_predio: Texto = Field(None, validation_alias=AliasPath("localCamara", "predio"))
    local_sala: Texto = Field(None, validation_alias=AliasPath("localCamara", "sala"))
    local_andar: Texto = Field(None, validation_alias=AliasPath("localCamara", "andar"))
    url: Url = Field(None, validation_alias="urlRegistro")


class Frente(Registro):
    """Frente parlamentar (`lista_frentes`, `Deputado.frentes`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    titulo: Texto = None
    legislatura: Inteiro = Field(None, validation_alias="idLegislatura")


class Ocupacao(Registro):
    """Emprego ou atividade de um deputado (`Deputado.ocupacoes`)."""

    ano_inicio: Inteiro = Field(None, validation_alias="anoInicio")
    ano_fim: Inteiro = Field(None, validation_alias="anoFim")
    entidade: Texto = None
    pais: Texto = Field(None, validation_alias="entidadePais")
    uf: Texto = Field(None, validation_alias="entidadeUF")
    titulo: Texto = None


class OrgaoDeputado(Registro):
    """Órgão de que um deputado participa (`Deputado.orgaos`)."""

    codigo: Inteiro = Field(None, validation_alias="idOrgao")
    uri: Url = Field(None, validation_alias="uriOrgao")
    sigla: Texto = Field(None, validation_alias="siglaOrgao")
    nome: Texto = Field(None, validation_alias="nomeOrgao")
    publicacao: Texto = Field(None, validation_alias="nomePublicacao")
    titulo: Texto = None
    titulo_codigo: Inteiro = Field(None, validation_alias="codTitulo")
    data_inicio: DataHora = Field(None, validation_alias="dataInicio")
    data_fim: DataHora = Field(None, validation_alias="dataFim")


class Profissao(Registro):
    """Profissão de um deputado (`Deputado.profissoes`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    legislatura: Inteiro = Field(None, validation_alias="idLegislatura")
    titulo: Texto = None
    uri: Url = None
    data: DataHora = Field(None, validation_alias="dataHora")
    tipo: Inteiro = Field(None, validation_alias="codTipoProfissao")


class Evento(Registro):
    """Evento da Câmara (`lista_eventos`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    data_inicio: DataHora = Field(None, validation_alias="dataHoraInicio")
    data_fim: DataHora = Field(None, validation_alias="dataHoraFim")
    situacao: Texto = None
    descricao_tipo: Texto = Field(None, validation_alias="descricaoTipo")
    descricao: Texto = None
    orgaos: CodigosOrgaos = None
    registro: Texto = Field(None, validation_alias="urlRegistro")
    local_externo: Texto = Field(None, validation_alias="localExterno")
    local_nome: Texto = Field(None, validation_alias=AliasPath("localCamara", "nome"))
    local_predio: Texto = Field(None, validation_alias=AliasPath("localCamara", "predio"))
    local_sala: Texto = Field(None, validation_alias=AliasPath("localCamara", "sala"))
    local_andar: Texto = Field(None, validation_alias=AliasPath("localCamara", "andar"))


class EventoDetalhes(Registro):
    """Atributos de `camara.Evento`."""

    andar: Texto = Field(None, validation_alias=AliasPath("localCamara", "andar"))
    descricao: Texto = None
    descricao_tipo: Texto = Field(None, validation_alias="descricaoTipo")
    fases: list | None = None
    fim: DataHora = Field(None, validation_alias="dataHoraFim")
    inicio: DataHora = Field(None, validation_alias="dataHoraInicio")
    local: Texto = Field(None, validation_alias=AliasPath("localCamara", "nome"))
    local_externo: Texto = Field(None, validation_alias="localExterno")
    lista_orgaos: list | None = Field(None, validation_alias="orgaos")
    predio: Texto = Field(None, validation_alias=AliasPath("localCamara", "predio"))
    requerimentos: list | None = None
    sala: Texto = Field(None, validation_alias=AliasPath("localCamara", "sala"))
    situacao: Texto = None
    uri: Url = None
    uri_convidados: Url = Field(None, validation_alias="uriConvidados")
    uri_deputados: Url = Field(None, validation_alias="uriDeputados")
    url_documento_pauta: Url = Field(None, validation_alias="urlDocumentoPauta")
    url_registro: Url = Field(None, validation_alias="urlRegistro")


class ItemPauta(Registro):
    """Item da pauta de um evento (`Evento.pauta`)."""

    ordem: Inteiro = None
    topico: Texto = None
    regime: Texto = None
    regime_codigo: Inteiro = Field(None, validation_alias="codRegime")
    titulo: Texto = None
    proposicao: dict | None = Field(None, validation_alias="proposicao_")
    relator: dict | None = None
    parecer: Texto = Field(None, validation_alias="textoParecer")
    proposicao_relacionada: dict | None = Field(None, validation_alias="proposicaoRelacionada_")
    uri: Url = Field(None, validation_alias="uriVotacao")
    situacao: Texto = Field(None, validation_alias="situacaoItem")


class VotacaoEvento(Registro):
    """Votação de um evento (`Evento.votacoes`)."""

    codigo: Texto = Field(None, validation_alias="id")
    uri: Url = None
    data: Data = None
    data_registro: DataHora = Field(None, validation_alias="dataHoraRegistro")
    orgao_sigla: Texto = Field(None, validation_alias="siglaOrgao")
    orgao_uri: Url = Field(None, validation_alias="uriOrgao")
    evento_uri: Url = Field(None, validation_alias="uriEvento")
    proposicao: Texto = Field(None, validation_alias="proposicaoObjeto")
    proposicao_uri: Url = Field(None, validation_alias="uriProposicaoObjeto")
    descricao: Texto = None
    aprovacao: Inteiro = None


class FrenteDetalhes(Registro):
    """Atributos de `camara.Frente`."""

    coordenador: dict | None = None
    documento: Url = Field(None, validation_alias="urlDocumento")
    email: Url = None
    id_situacao: Inteiro = Field(None, validation_alias="idSituacao")
    keywords: Texto = None
    legislatura: Inteiro = Field(None, validation_alias="idLegislatura")
    situacao: Texto = None
    telefone: Texto = None
    titulo: Texto = None
    uri: Url = None
    website: Url = Field(None, validation_alias="urlWebsite")


class MembroFrente(Registro):
    """Membro de uma frente parlamentar (`Frente.membros`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    nome: Texto = None
    partido: Texto = Field(None, validation_alias="siglaPartido")
    partido_uri: Url = Field(None, validation_alias="uriPartido")
    uf: Texto = Field(None, validation_alias="siglaUf")
    legislatura: Inteiro = Field(None, validation_alias="idLegislatura")
    foto: Url = Field(None, validation_alias="urlFoto")
    email: Url = None
    titulo: Texto = None
    titulo_codigo: Inteiro = Field(None, validation_alias="codTitulo")
    data_inicio: Data = Field(None, validation_alias="dataInicio")
    data_fim: Data = Field(None, validation_alias="dataFim")


class Legislatura(Registro):
    """Legislatura (`lista_legislaturas`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    data_inicio: Data = Field(None, validation_alias="dataInicio")
    data_fim: Data = Field(None, validation_alias="dataFim")


class LegislaturaDetalhes(Registro):
    """Atributos de `camara.Legislatura`."""

    fim: Data = Field(None, validation_alias="dataFim")
    inicio: Data = Field(None, validation_alias="dataInicio")
    uri: Url = None


class Membro(Registro):
    """Cargo e ocupante (`Legislatura.mesa`, `Orgao.membros`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    nome: Texto = None
    partido: Texto = Field(None, validation_alias="siglaPartido")
    partido_uri: Url = Field(None, validation_alias="uriPartido")
    uf: Texto = Field(None, validation_alias="siglaUf")
    legislatura: Inteiro = Field(None, validation_alias="idLegislatura")
    foto: Url = Field(None, validation_alias="urlFoto")
    email: Url = None
    data_inicio: Data = Field(None, validation_alias="dataInicio")
    data_fim: Data = Field(None, validation_alias="dataFim")
    titulo: Texto = None
    titulo_codigo: Inteiro = Field(None, validation_alias="codTitulo")


class Orgao(Registro):
    """Órgão da Câmara (`lista_orgaos`, `Evento.orgaos`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    sigla: Texto = None
    nome: Texto = None
    apelido: Texto = None
    orgao_tipo_codigo: Inteiro = Field(None, validation_alias="codTipoOrgao")
    orgao_tipo: Texto = Field(None, validation_alias="tipoOrgao")
    nome_publicacao: Texto = Field(None, validation_alias="nomePublicacao")


class OrgaoDetalhes(Registro):
    """Atributos de `camara.Orgao`."""

    apelido: Texto = None
    casa: Texto = None
    cod_tipo: Inteiro = Field(None, validation_alias="codTipoOrgao")
    fim: DataHora = Field(None, validation_alias="dataFim")
    inicio: DataHora = Field(None, validation_alias="dataInicio")
    instalacao: DataHora = Field(None, validation_alias="dataInstalacao")
    nome: Texto = None
    nome_publicacao: Texto = Field(None, validation_alias="nomePublicacao")
    sala: Texto = None
    sigla: Texto = None
    tipo: Texto = Field(None, validation_alias="tipoOrgao")
    uri: Url = None
    website: Url = Field(None, validation_alias="urlWebsite")


class EventoOrgao(Registro):
    """Evento de um órgão (`Orgao.eventos`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    data_inicio: DataHora = Field(None, validation_alias="dataHoraInicio")
    data_fim: DataHora = Field(None, validation_alias="dataHoraFim")
    situacao: Texto = None
    descricao_tipo: Texto = Field(None, validation_alias="descricaoTipo")
    descricao: Texto = None
    local_externo: Texto = Field(None, validation_alias="localExterno")
    orgaos: CodigosOrgaos = None
    local_camara: dict | None = Field(None, validation_alias="localCamara")
    url: Url = Field(None, validation_alias="urlRegistro")


class Partido(Registro):
    """Partido (`lista_partidos`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    sigla: Texto = None
    nome: Texto = None
    uri: Url = None


class PartidoDetalhes(Registro):
    """Atributos de `camara.Partido`."""

    facebook: Url = Field(None, validation_alias="urlFacebook")
    legislatura: Inteiro = Field(None, validation_alias=AliasPath("status", "idLegislatura"))
    lider: dict | None = Field(None, validation_alias=AliasPath("status", "lider"))
    logo: Url = Field(None, validation_alias="urlLogo")
    nome: Texto = None
    numero: Inteiro = Field(None, validation_alias="numeroEleitoral")
    sigla: Texto = None
    situacao: Texto = Field(None, validation_alias=AliasPath("status", "situacao"))
    total_membros: Inteiro = Field(None, validation_alias=AliasPath("status", "totalMembros"))
    total_posse: Inteiro = Field(None, validation_alias=AliasPath("status", "totalPosse"))
    ultima_atualizacao: DataHora = Field(None, validation_alias=AliasPath("status", "data"))
    uri: Url = None
    uri_membros: Url = Field(None, validation_alias=AliasPath("status", "uriMembros"))
    website: Url = Field(None, validation_alias="urlWebSite")


class Proposicao(Registro):
    """Proposição (`lista_proposicoes`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    tipo: Texto = Field(None, validation_alias="siglaTipo")
    tipo_codigo: Inteiro = Field(None, validation_alias="codTipo")
    numero: Inteiro = None
    ano: Inteiro = None
    ementa: Texto = None


class ProposicaoDetalhes(Registro):
    """Atributos de `camara.Proposicao`."""

    uri: Url = None
    tipo_sigla: Texto = Field(None, validation_alias="siglaTipo")
    tipo_codigo: Inteiro = Field(None, validation_alias="codTipo")
    numero: Inteiro = None
    ano: Inteiro = None
    ementa: Texto = None
    apresentacao: DataHora = Field(None, validation_alias="dataApresentacao")
    uri_orgao_numerador: Url = Field(None, validation_alias="uriOrgaoNumerador")
    ultima_atualizacao: DataHora = Field(None, validation_alias=AliasPath("statusProposicao", "dataHora"))
    sequencia: Inteiro = Field(None, validation_alias=AliasPath("statusProposicao", "sequencia"))
    sigla_orgao: Texto = Field(None, validation_alias=AliasPath("statusProposicao", "siglaOrgao"))
    uri_orgao: Url = Field(None, validation_alias=AliasPath("statusProposicao", "uriOrgao"))
    uri_ultimo_relator: Url = Field(None, validation_alias=AliasPath("statusProposicao", "uriUltimoRelator"))
    regime: Texto = Field(None, validation_alias=AliasPath("statusProposicao", "regime"))
    descricao_tramitacao: Texto = Field(None, validation_alias=AliasPath("statusProposicao", "descricaoTramitacao"))
    cod_tipo_tramitacao: Inteiro = Field(None, validation_alias=AliasPath("statusProposicao", "codTipoTramitacao"))
    descricao_situacao: Texto = Field(None, validation_alias=AliasPath("statusProposicao", "descricaoSituacao"))
    cod_situacao: Inteiro = Field(None, validation_alias=AliasPath("statusProposicao", "codSituacao"))
    despacho: Texto = Field(None, validation_alias=AliasPath("statusProposicao", "despacho"))
    url: Url = Field(None, validation_alias=AliasPath("statusProposicao", "url"))
    ambito: Texto = Field(None, validation_alias=AliasPath("statusProposicao", "ambito"))
    uri_autores: Url = Field(None, validation_alias="uriAutores")
    descricao_tipo: Texto = Field(None, validation_alias="descricaoTipo")
    ementa_detalhada: Texto = Field(None, validation_alias="ementaDetalhada")
    keywords: Texto = None
    uri_proposicao_principal: Url = Field(None, validation_alias="uriPropPrincipal")
    uri_proposicao_anterior: Url = Field(None, validation_alias="uriPropAnterior")
    uri_proposicao_posterior: Url = Field(None, validation_alias="uriPropPosterior")
    url_inteiro_teor: Url = Field(None, validation_alias="urlInteiroTeor")
    urn_final: Texto = Field(None, validation_alias="urnFinal")
    texto: Texto = None
    justificativa: Texto = None


class Autor(Registro):
    """Autor de uma proposição (`Proposicao.autores`)."""

    nome: Texto = None
    uri: Url = None
    tipo_codigo: Inteiro = Field(None, validation_alias="codTipo")
    tipo: Texto = None
    ordem_assinatura: Inteiro = Field(None, validation_alias="ordemAssinatura")
    proponente: Inteiro = None


class ProposicaoRelacionada(Registro):
    """Proposição relacionada (`Proposicao.relacionadas`)."""

    codigo: Inteiro = Field(None, validation_alias="id")
    uri: Url = None
    tipo_sigla: Texto = Field(None, validation_alias="siglaTipo")
    tipo_codigo: Inteiro = Field(None, validation_alias="codTipo")
    numero: Inteiro = None
    ano: Inteiro = None
    ementa: Texto = None


class Tema(Registro):
    """Área temática (`Proposicao.temas`)."""

    codigo: Inteiro = Field(None, validation_alias="codTema")
    tema: Texto = None
    relevancia: Inteiro = None


class Tramitacao(Registro):
    """Passo da tramitação (`Proposicao.tramitacoes`)."""

    data: DataHora = Field(None, validation_alias="dataHora")
    sequencia: Inteiro = None
    orgao: Texto = Field(None, validation_alias="siglaOrgao")
    orgao_uri: Url = Field(None, validation_alias="uriOrgao")
    ultimo_relator_uri: Url = Field(None, validation_alias="uriUltimoRelator")
    regime: Texto = None
    tramitacao: Texto = Field(None, validation_alias="descricaoTramitacao")
    tramitacao_codigo: Inteiro = Field(None, validation_alias="codTipoTramitacao")
    situacao: Texto = Field(None, validation_alias="descricaoSituacao")
    situacao_codigo: Inteiro = Field(None, validation_alias="codSituacao")
    despacho: Texto = None
    url: Url = None
    ambito: Texto = None


class Referencia(Registro):
    """Valor de referência (`referencias`)."""

    codigo: Texto = Field(None, validation_alias="cod")
    sigla: Texto = None
    nome: Texto = None
    descricao: Texto = None


class Votacao(Registro):
    """Votação (`lista_votacoes`, `Orgao.votacoes`, `Proposicao.votacoes`)."""

    codigo: Texto = Field(None, validation_alias="id")
    uri: Url = None
    data: Data = None
    data_registro: DataHora = Field(None, validation_alias="dataHoraRegistro")
    orgao: Texto = Field(None, validation_alias="siglaOrgao")
    orgao_uri: Url = Field(None, validation_alias="uriOrgao")
    evento_uri: Url = Field(None, validation_alias="uriEvento")
    proposicao: Texto = Field(None, validation_alias="proposicaoObjeto")
    proposicao_uri: Url = Field(None, validation_alias="uriProposicaoObjeto")
    descricao: Texto = None
    aprovacao: Inteiro = None


class VotacaoDetalhes(Registro):
    """Atributos de `camara.Votacao`."""

    aprovacao: Inteiro = None
    data: Data = None
    data_registro: DataHora = Field(None, validation_alias="dataHoraRegistro")
    data_ultima_abertura: DataHora = Field(None, validation_alias="dataHoraUltimaAberturaVotacao")
    descricao: Texto = None
    efeitos_registrados: list | None = Field(None, validation_alias="efeitosRegistrados")
    evento: Inteiro = Field(None, validation_alias="idEvento")
    orgao: Inteiro = Field(None, validation_alias="idOrgao")
    objetos_possiveis: list | None = Field(None, validation_alias="objetosPossiveis")
    proposicoes_afetadas: list | None = Field(None, validation_alias="proposicoesAfetadas")
    sigla_orgao: Texto = Field(None, validation_alias="siglaOrgao")
    ultima_apresentacao_proposicao: dict | None = Field(None, validation_alias="ultimaApresentacaoProposicao")
    uri: Url = None
    uri_evento: Url = Field(None, validation_alias="uriEvento")
    uri_orgao: Url = Field(None, validation_alias="uriOrgao")


class Orientacao(Registro):
    """Orientação de bancada (`Votacao.orientacoes`)."""

    orientacao: Texto = Field(None, validation_alias="orientacaoVoto")
    lideranca: Texto = Field(None, validation_alias="codTipoLideranca")
    bloco: Texto = Field(None, validation_alias="siglaPartidoBloco")
    bloco_codigo: Inteiro = Field(None, validation_alias="codPartidoBloco")
    bloco_uri: Url = Field(None, validation_alias="uriPartidoBloco")


class Voto(Registro):
    """Voto de um deputado (`Votacao.votos`)."""

    voto: Texto = Field(None, validation_alias="tipoVoto")
    data: DataHora = Field(None, validation_alias="dataRegistroVoto")
    deputado_codigo: Inteiro = Field(None, validation_alias=AliasPath("deputado_", "id"))
    deputado_uri: Url = Field(None, validation_alias=AliasPath("deputado_", "uri"))
    deputado_nome: Texto = Field(None, validation_alias=AliasPath("deputado_", "nome"))
    deputado_partido: Texto = Field(None, validation_alias=AliasPath("deputado_", "siglaPartido"))
    deputado_partido_uri: Url = Field(None, validation_alias=AliasPath("deputado_", "uriPartido"))
    deputado_uf: Texto = Field(None, validation_alias=AliasPath("deputado_", "siglaUf"))
    deputado_legislatura: Inteiro = Field(None, validation_alias=AliasPath("deputado_", "idLegislatura"))
    deputado_foto: Url = Field(None, validation_alias=AliasPath("deputado_", "urlFoto"))
    deputado_email: Url = Field(None, validation_alias=AliasPath("deputado_", "email"))
