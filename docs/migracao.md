# Migração do 2.x para o 3.0

O DadosAbertosBrasil 3.0 padroniza o retorno de todas as funções, torna o pandas opcional e traz o
módulo [`wiki`](referencia/wiki.md). Esta página lista o que muda e como adaptar o seu código.

A versão 2.3 avisa (com `DeprecationWarning` e `DABFormatoWarning`) quase tudo o que está aqui. Rodar o
seu código na 2.3 com os avisos visíveis é a forma mais rápida de achar o que precisa mudar:

```bash
python -W default::DeprecationWarning seu_script.py
```

## Resumo

| Tema | 2.x | 3.0 |
|---|---|---|
| Python | 3.10 ou superior | 3.11 ou superior |
| pandas | dependência obrigatória | extra opcional: `pip install DadosAbertosBrasil[pandas]` |
| Retorno sem `formato` | DataFrame pandas | `"json"` (lista de registros), com `DABFormatoWarning` uma vez por sessão |
| `formato="json"` | JSON original da API | registros normalizados, com os nomes das colunas do DataFrame |
| JSON original da API | `formato="json"` | `formato="bruto"` |
| Modelos Pydantic | — | `formato="pydantic"` |
| `formato="url"` | URL sem os parâmetros | URL completa, com a query string |
| Dados da Wikipedia | `uf` lia `ufs.json` e `governadores.json` | módulo `wiki` |
| Exceções | `DAB_UFError`, `DAB_InputError`... | `DABUFError`, `DABInputError`..., com base comum `DABError` |

## Formato padrão e pandas opcional

`pip install DadosAbertosBrasil` não instala mais o pandas. Para continuar recebendo DataFrames:

```bash
pip install "DadosAbertosBrasil[pandas]"      # ou [polars]
```

```python
import DadosAbertosBrasil as dab

dab.config.formato = "pandas"    # o comportamento do 2.x; silencia o DABFormatoWarning
```

Sem `formato` no argumento nem em `dab.config.formato`, as funções retornam `"json"`: uma lista de
dicionários com os mesmos campos e tipos das colunas do DataFrame (datas como `datetime.date`,
números como `int` e `float`). O tipo de retorno deixa de depender do que está instalado.

O aviso tem categoria própria, que pode ser filtrada:

```python
import warnings
warnings.filterwarnings("ignore", category=dab.DABFormatoWarning)
```

### Tipos das colunas

Os nomes das colunas dos DataFrames são os mesmos do 2.x. Os tipos agora vêm dos modelos de cada
função e são iguais em pandas, polars e `"json"`:

- inteiros e booleanos usam os tipos com valores ausentes do pandas (`Int64` e `boolean`);
- datas viram `datetime64` no pandas e `Date`/`Datetime` no polars em todas as funções (no 2.x, as
  séries do IPEA vinham como objetos `date` e algumas colunas de data ficavam como texto);
- valores que eram texto por engano (como `valor` nas séries do SGS) viram números;
- `bacen.serie` e os atalhos de `favoritos` sobre ela sempre têm a coluna `datafim`, vazia quando a
  série não tem fim de período;
- a coluna `orgaos` de `camara.lista_eventos` e afins é sempre uma lista de códigos (no 2.x era um
  número quando havia um órgão só).

Um valor da API que não corresponde ao modelo (sinal de que a API mudou) não interrompe a consulta:
gera `DABValidacaoWarning` e o valor fica como veio.

### `formato="pydantic"`

Devolve uma lista de modelos Pydantic, um por registro, definidos em `<modulo>.modelos`
(`camara.modelos.Deputado`, `wiki.modelos.Governador`...). Útil para type checking e autocomplete.

## Funções removidas

Viram stubs que levantam `DABFuncaoRemovidaError` com o motivo. Os stubs saem de vez numa versão
futura do 3.x, anunciada nas notas de versão.

| Função | Motivo | Alternativa |
|---|---|---|
| `favoritos.perfil_eleitorado` | dados eleitorais deixaram de fazer parte do pacote | nenhuma |
| `ibge.coordenadas` | o arquivo de coordenadas de setores e bairros saiu do repositório de dados | coordenadas de municípios: `wiki.municipios()` (é outro dado) |
| `bacen.expectativas("instituicoes")` | o conjunto não existe mais na API do Banco Central | nenhuma |

`ibge.populacao` continua no pacote, mas a API de projeções do IBGE que ela usa responde 404 (já no
2.x). `UF.populacao` e `UF.densidade` passaram a usar a estimativa da tabela 6579 do SIDRA.

## Nomes renomeados

Os nomes antigos continuam funcionando com `DeprecationWarning` e saem numa versão futura do 3.x.

| 2.x | 3.0 |
|---|---|
| `senado.lista_legislatura` | `senado.lista_legislaturas` |
| `senado.lista_uso_palavra` | `senado.lista_tipos_uso_palavra` |
| `DAB_DataError` | `DABDataError` |
| `DAB_InputError` | `DABInputError` |
| `DAB_LocalidadeError` | `DABLocalidadeError` |
| `DAB_MoedaError` | `DABMoedaError` |
| `DAB_UFError` | `DABUFError` |
| `camara.Votacao.data_regitro` | `data_registro` |
| `camara.Frente.id_sitacao` | `id_situacao` |
| `camara.Orgao.urlWebsite` | `website` |

`DAB_DeprecationError`, que não era usado pelo pacote, foi removido. Todas as exceções herdam de
`DABError` e continuam herdando de `ValueError` ou `TypeError`, como antes.

## Classes de objeto

`camara.Deputado(cod)`, `camara.Partido(cod)`, `senado.Senador(cod)` e as demais mantêm a interface:
o construtor busca os dados, `dados` guarda o JSON original e os atributos têm os mesmos nomes. Os
atributos agora têm tipo (datas como `date`, códigos como `int`) e o novo atributo `registro` guarda o
modelo Pydantic validado.

## Módulo `uf` e dados da Wikipedia

- `UF` e `Governador` leem do novo módulo [`wiki`](referencia/wiki.md). A interface de `UF` é a mesma,
  com os atributos novos `wikidata`, `artigo`, `registro` e a propriedade `prefeito`.
- `Governador.nome_completo` não existe mais; há `artigo` (título do artigo na Wikipedia) e
  `interino`.
- Os arquivos de dados vêm do repositório
  [DadosAbertosBrasil-wiki](https://github.com/GusFurtado/DadosAbertosBrasil-wiki) (antigo
  `dab_assets`), num envelope com `schema_version`, `gerado_em`, `licenca` e `fontes`. Veja
  `wiki.metadados()`.

O 2.3 lê do branch congelado `2.x` desse repositório e continua funcionando. Versões 2.2 ou
anteriores, que liam da `main`, deixam de funcionar nas funções que usavam esses arquivos (`uf`,
`favoritos.perfil_eleitorado` e `ibge.coordenadas`).

## Outras mudanças

- Endpoints do IPEA, do Senado e do SIDRA usam HTTPS (o SIDRA mudou para `apisidra.ibge.gov.br`).
- Cache local opcional para dados que mudam pouco: `dab.config.cache = True` (veja
  [Configuração](referencia/configuracao.md)).
- Correções que mudam resultados: `senado.lista_legislaturas` passa a trazer UF e datas de exercício
  (antes saíam vazias); `senado.Senador.profissoes` e `camara.Evento.orgaos` passam a trazer os dados
  certos; `favoritos.salario_minimo(tipo="ppc")` passa a funcionar.

## Versões do Python

O 3.0 suporta Python 3.11 a 3.14. O Python 3.10 chegou ao fim do suporte em outubro de 2026; quem
precisar dele pode fixar `DadosAbertosBrasil<3`.
