<div align="center">
  <img src="https://raw.githubusercontent.com/GusFurtado/DadosAbertosBrasil/master/assets/logo.png"><br>
</div>

---

Dados Abertos Brasil é uma iniciativa para facilitar o acesso a dados abertos e APIs do governo brasileiro.

É um pacote open-source para Python e Pandas e a forma mais simples de acessar dados de instituições como IGBE, IPEA , etc.

Atualmente o pacote Dados Abertos Brasil possui quatro módulos:

- DadosAbertosBrasil.[ibge](https://github.com/GusFurtado/DadosAbertosBrasil#dadosabertosbrasilibge)
- DadosAbertosBrasil.[ipea](https://github.com/GusFurtado/DadosAbertosBrasil#dadosabertosbrasilipea)
- DadosAbertosBrasil.[camara](https://github.com/GusFurtado/DadosAbertosBrasil#dadosabertosbrasilcamara)
- DadosAbertosBrasil.[favoritos](https://github.com/GusFurtado/DadosAbertosBrasil#dadosabertosbrasilfavoritos)

### Dependências
- [pandas](https://pandas.pydata.org/)
- [requests](https://requests.readthedocs.io/en/master/)

### Licença
- [MIT](LICENSE)

---

# DadosAbertosBrasil.**ibge**

Módulo para captura dos dados abertos das APIs do IBGE.

- ibge.[nomes](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilibgenomesnomes-sexonone-localidadenone)
- ibge.[nomes_uf](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilibgenomes_ufnome)
- ibge.[nomes_ranking](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilibgenomes_rankingdecadanone-sexonone-localidadenone)
- ibge.[localidades](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilibgelocalidades)
- ibge.[malha](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilibgemalhalocalidade)
- ibge.[populacao](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilibgepopulacaoprojecaonone-localidadenone)
- [SIDRA](https://github.com/GusFurtado/DadosAbertosBrasil#sidra)
  - ibge.[Agregados](https://github.com/GusFurtado/DadosAbertosBrasil#class-dadosabertosbrasilibgeagregadosindexfalse)
  - ibge.[Metadados](https://github.com/GusFurtado/DadosAbertosBrasil#class-dadosabertosbrasilibgemetadadosagregado)
  - ibge.[referencias](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilibgereferenciascod-indexfalse)
  - ibge.[Sidra](https://github.com/GusFurtado/DadosAbertosBrasil#class-dadosabertosbrasilibgesidraagregadonone-periodosnone-variaveisnone-localidadesn1-all-classificacoesnone)

Importe o módulo com `from DadosAbertosBrasil import ibge`

### def DadosAbertosBrasil.ibge.**nomes**(*nomes, sexo=None, localidade=None*)

Obtém a frequência de nascimentos por década para o(s) nome(s) consultado(s).

##### *Parâmetros:*

- **nomes:** string ou lista de strings

Nome(s) que se deseja pesquisar

- **sexo:** (Opcional) `'M'` ou `'F'`

`'M'` se deseja pesquisar apenas por ocorrências do sexo masculino e `'F'` se deseja pesquisar apenas por ocorrências do sexo feminino.

- **localidade:** (Opcional) int

Código da localidade que se deseja limitar a pesquisa.

Utilizar a função `ibge.localidades()` para consultar os códigos das localidades.

##### *Retorna:*

- **pandas.DataFrame**, onde cada column é um dos nomes pesquisados e cada row é uma década.

##### *Exemplos:*

Pesquisar pela frequência de nascimento de Maria e Ana:

```pycon
>>> ibge.nomes(['Maria', 'Ana'])
```

|  |PERIODO  |ANA   |MARIA  |
|:-|--------:|-----:|------:|
|0 |1930   	 |33395 |336477 |
|1 |1930,1940|56160 |749053 |
|2 |1940,1950|101259|1487042|
|3 |1950,1960|183941|2476482|
|4 |1960,1970|292835|2495491|
|5 |1970,1980|421531|1616019|
|6 |1980,1990|529266|917968 |
|7 |1990,2000|536302|544296 |
|8 |2000,2010|935169|1111301|

Pesquisar pela frequência de nascimentos de Maria no estado de São Paulo (código 35):

```pycon
>>> ibge.nomes('Maria', localidade=35)
```

|  |PERIODO  |ANA   |
|:-|--------:|-----:|
|0 |1930   	 |65218 |
|1 |1930,1940|150588|
|2 |1940,1950|313277|
|3 |1950,1960|541950|
|4 |1960,1970|487742|
|5 |1970,1980|252657|
|6 |1980,1990|105600|
|7 |1990,2000|48444 |
|8 |2000,2010|177756|

##### *Documentação da API original:*

https://servicodados.ibge.gov.br/api/docs/censos/nomes?versao=2#api-Nomes-nomeGet

---

### def DadosAbertosBrasil.ibge.**nomes_uf**(*nome*)

Obtém a frequência de nascimentos por UF para o nome consultado

##### *Parâmetros:*

- **nome:** string

Nome que se deseja pesquisar

##### *Retorna:*

- **pandas.DataFrame**, onde cada row é uma localidade (UF).

Contém três columns: Frequência de nascimento do nome pesquisado, população total da localidade e proporção de nascimentos por 100.000 habitantes.

Utilizar a função `ibge.localidades()` para consultar os códigos das localidades.

##### *Exemplos:*

Pesquisar pela frequência de nascimento de Maria por UF:

```pycon
>>> ibge.nomes_uf('Maria')
```

|localidade|frequencia|populacao|proporcao|
|:---------|---------:|--------:|--------:|
|11        |72579     |1562409  |4645.33  |
|12        |63172     |733559   |8611.71  |
|13        |173034    |3483985  |4966.55  |
|14        |20848     |450479   |4627.96  |
|15        |472891    |7581051  |6237.80  |
|...       |...       |...      |...      |

##### *Documentação da API original:*

https://servicodados.ibge.gov.br/api/docs/censos/nomes?versao=2#api-Nomes-nomeGet

---

### def DadosAbertosBrasil.ibge.**nomes_ranking**(*decada=None, sexo=None, localidade=None*)

Obtém o ranking dos nomes segundo a frequência de nascimentos por década

##### *Parâmetros:*

- **decada:** (Opcional) int

Década que se deseja limitar a pesquisa de nascimentos.

Deve estar no formato *AAAA*, sendo múltiplo de 10.

*Exemplos: 1930, 1980, 2000...*

- **sexo:** (Opcional) `'M'` ou `'F'`

`'M'` se deseja pesquisar apenas por ocorrências do sexo masculino e `'F'` se deseja pesquisar apenas por ocorrências do sexo feminino.

- **localidade:** (Opcional) int

Código da localidade que se deseja limitar a pesquisa.

Utilizar a função `ibge.localidades()` para consultar os códigos das localidades.

##### *Retorna:*

- **pandas.DataFrame**, com rows de 1 a 20 representando a posição no ranking.

Uma column para os nomes e uma para a frequência de nascimentos.

##### *Exemplos:*

Pesquisar por nomes masculino com maior frequência de nascimentos no estado de São Paulo (código 35) na década de 1990:

```pycon
>>> ibge.nomes_ranking(decada=1990, sexo='M', localidade=35)
```

|ranking|frequencia|nome   |
|:------|---------:|------:|
|1      |97066     |JOSE   |
|2      |86175     |RODRIGO|
|3      |83805     |RAFAEL |
|4      |64731     |FABIO  |
|5      |64642     |LEANDRO|
|...    |...       |...    |

##### *Documentação da API original:*

https://servicodados.ibge.gov.br/api/docs/censos/nomes?versao=2#api-Ranking-rankingGet

---

### def DadosAbertosBrasil.ibge.**localidades**()

Obtém o conjunto de distritos do Brasil.

##### *Parâmetros:*

- Nenhum

##### *Retorna:*

- **pandas.DataFrame**, contendo todos distritos, municípios, microrregiões, mesorregiões, UFs e regiões do Brasil.

##### *Exemplos:*

Pesquisa completa por todos os distritos:

```pycon
>>> ibge.localidades()
```

##### *Documentação da API original:*

https://servicodados.ibge.gov.br/api/docs/localidades?versao=1

---

### def DadosAbertosBrasil.ibge.**malha**(*localidade=''*)

Obtém a URL para a malha referente ao identificador da localidade.

##### *Parâmetros:*

- **localidade:** (Opcional) int

Código da localidade que se deseja pesquisar. Caso omitido, assume o valor Brasil.

Utilizar a função `ibge.localidades()` para consultar os códigos das localidades.

##### *Retorna:*

- **url** (string) para um arquivo .svg do mapa da região pesquisada.

##### *Exemplos:*

Pesquisar pela malha referente a região Sudeste (código 3):

```pycon
>>> ibge.malha(3)
'https://servicodados.ibge.gov.br/api/v2/malhas/3'
```
	
Pesquisar pela malha referente ao estado do Rio de Janeiro (código 33):

```pycon
>>> ibge.malha(33)
'https://servicodados.ibge.gov.br/api/v2/malhas/33'
```

##### *Documentação da API original:*

https://servicodados.ibge.gov.br/api/docs/malhas?versao=2

---

### def DadosAbertosBrasil.ibge.**populacao**(*projecao=None, localidade=None*)

Obtém a URL para a malha referente ao identificador da localidade.

##### *Parâmetros:*

- **projecao:** (Opcional) `'populacao'`, `'nascimento'` ou `'obito'`.

Define que variável pesquisar. Se omitido, obtém um dictionary com todos os valores.

- **localidade:** (Opcional) int

Código da localidade que se deseja pesquisar. Caso omitido, assume o valor Brasil.

Utilizar a função `ibge.localidades()` para consultar os códigos das localidades.

##### *Retorna:*

- **dict**, caso o campo 'projecao' seja omitido.
- **int**, contendo um valor estimado para população, nascimentos ou óbitos, caso o campo 'projecao' tenha um valor válido.

##### *Exemplos:*

Pesquisar pela população total estimada do Brasil:

```pycon
>>> ibge.populacao(projecao='populacao')
211406467
```
	
Pesquisar pela quantidade estimada de óbitos por ano no estado de São Paulo (código 35):

```pycon
>>> ibge.populacao(projecao='obito', localidade=35)
45000
```
	
Pesquisar pelos dados de nascimento, óbitos e projeção populacional para o estado do Rio de Janeiro:

```pycon
>>> ibge.populacao(localidade=33)
{'localidade': '33',
 'horario': '19/04/2020 19:18:18',
 'projecao': {'populacao': 17342454,
  'periodoMedio': {'incrementoPopulacional': 317367,
   'nascimento': 12000,
   'obito': 45000}}}
```

##### *Documentação da API original:*

https://servicodados.ibge.gov.br/api/docs/projecoes?versao=1

---

### def DadosAbertosBrasil.ibge.**coordenadas**()

Obtém as coordenadas de todas as localidades brasileiras.

##### *Parâmetros:*

- **Nenhum**

##### *Retorna:*

- **pandas.DataFrame** contendo latitude, longitude e altitude de bairros, distritos e povoados brasileiros.

##### *Exemplos:*

Pesquisar pelas coordenadas de todos os setores de Joinville:

```pycon
>>> l = ibge.coordenadas()
>>> l[l.NM_MUNICIPIO == 'JOINVILLE']
```

|     |GM_PONTO|ID   |CD_GEOCODIGO   |TIPO  |CD_GEOCODBA |NM_BAIRRO     |CD_GEOCODSD|NM_SUBDISTRITO|CD_GEOCODDS|NM_DISTRITO|...|NM_MESO          |NM_UF         |CD_NIVEL|CD_CATEGORIA|NM_CATEGORIA|NM_LOCALIDADE     |LONG      |LAT       |ALT      |GM_PONTO_sk |
|:----|-------:|----:|--------------:|-----:|-----------:|-------------:|----------:|-------------:|----------:|----------:|--:|----------------:|-------------:|-------:|-----------:|-----------:|-----------------:|---------:|---------:|--------:|-----------:|
|18796|NaN     |18797|420910205000001|URBANO|4.209102e+11|Centro        |42091020500|NaN           |420910205  |JOINVILLE  |...|NORTE CATARINENSE|SANTA CATARINA|1       |5 	      |CIDADE      |JOINVILLE         |-48.849409|-26.304518|10.296596|1J6SeWA.76m-|
|18797|NaN     |18798|420910205000488|URBANO|4.209102e+11|Espinheiros   |42091020500|NaN           |420910205  |JOINVILLE  |...|NORTE CATARINENSE|SANTA CATARINA|6       |3 	      |AUI         |ESPINHEIROS       |-48.799454|-26.217098|4.518122 |1J6SeU*vQ:X-|
|18798|NaN     |18799|420910205000490|URBANO|4.209102e+11|Vila Cubatão  |42091020500|NaN           |420910205  |JOINVILLE  |...|NORTE CATARINENSE|SANTA CATARINA|6       |2 	      |AUI         |VILA CUBATÃO      |-48.770058|-26.281902|14.757318|1J6SeUwSrXDp|
|18799|NaN     |18800|420910205000498|URBANO|4.209102e+11|Morro do Meio |42091020500|NaN           |420910205  |JOINVILLE  |...|NORTE CATARINENSE|SANTA CATARINA|6       |5 	      |AUI         |MORRO DO MEIO     |-48.897157|-26.332775|17.335947|1J6Sevu.:L6f|
|18800|NaN     |18801|420910205000506|URBANO|4.209102e+11|Jardim Paraíso|42091020500|NaN           |420910205  |JOINVILLE  |...|NORTE CATARINENSE|SANTA CATARINA|6       |1 	      |AUI         |JARDIM PARAÍSO    |-48.808627|-26.217094|5.828033 |1J6SeU)vR6j>|
|18801|NaN     |18802|420910205000543|RURAL |NaN         |NaN           |42091020500|NaN           |420910205  |JOINVILLE  |...|NORTE CATARINENSE|SANTA CATARINA|3       |2 	      |POVOADO     |MORRO DO AMARAL   |-48.776351|-26.304859|3.824058 |1J6SeYA,]ecp|
|18802|NaN     |18803|420910205000739|RURAL |NaN         |NaN           |42091020500|NaN           |420910205  |JOINVILLE  |...|NORTE CATARINENSE|SANTA CATARINA|3       |5 	      |POVOADO     |VIGORELLI         |-48.766511|-26.224330|1.000000 |1J6SeU4grE+f|
|18803|NaN     |18804|420910210000001|URBANO|4.209102e+11|Pirabeiraba   |42091021000|NaN           |420910210  |PIRABEIRABA|...|NORTE CATARINENSE|SANTA CATARINA|2       |10 	      |VILA        |PIRABEIRABA       |-48.908392|-26.206492|25.135213|1J6SeQXucW^-|
|18804|NaN     |18805|420910210000034|RURAL |NaN         |NaN           |42091021000|NaN           |420910210  |PIRABEIRABA|...|NORTE CATARINENSE|SANTA CATARINA|3       |3 	      |POVOADO     |ESTRADA DO OESTE 1|-48.880583|-26.193152|20.269465|1J6SeRlD;LYf|
|18805|NaN     |18806|420910210000036|RURAL |NaN         |NaN           |42091021000|NaN           |420910210  |PIRABEIRABA|...|NORTE CATARINENSE|SANTA CATARINA|3       |4 	      |POVOADO     |ESTRADA DO OESTE 2|-48.880570|-26.195625|22.273426|1J6SeRlT@jKp|

##### *Documentação da API original:*

ftp://geoftp.ibge.gov.br/organizacao_do_territorio/estrutura_territorial/localidades/

---

# **SIDRA**

O SIDRA (Sistema IBGE de Recuperação Automática) permite consultar todo catalogo de dados armazenados no Banco de Tabelas Estatísticas do IBGE.

Por ser um sistema completo e robusto, foram desenvolvidos os seguintes objetos para facilitar a consulta:

- ibge.[Agregados](https://github.com/GusFurtado/DadosAbertosBrasil#class-dadosabertosbrasilibgeagregadosindexfalse)
- ibge.[Metadados](https://github.com/GusFurtado/DadosAbertosBrasil#class-dadosabertosbrasilibgemetadadosagregado)
- ibge.[referencias](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilibgereferenciascod-indexfalse)
- ibge.[Sidra](https://github.com/GusFurtado/DadosAbertosBrasil#class-dadosabertosbrasilibgesidraagregadonone-periodosnone-variaveisnone-localidadesn1-all-classificacoesnone)

Utilize a seguinte metodologia para encontrar a tabela (agregado) que procura:

1. Estude a [aplicação oficial](https://sidra.ibge.gov.br/home/ipca/brasil) e/ou o [Query Builder](https://servicodados.ibge.gov.br/api/docs/agregados?versao=3#api-bq) do SIDRA para entender o sistema;
2. Crie um objeto`ibge.Agregados` que contém o catálogo completo de pesquisas e agregados;
3. Filtre o objeto `.Agregados` utilizando o método `.filtrar` para facilitar a busca pela agregado desejado;
4. Com o código do agregado em mãos, crie um objeto `ibge.Metadados` inserindo o código do agregado como parâmetro;
5. Explore os atributos do seu objeto `.Metadados` para identificar as variáveis, classificações e outros parâmetros necessários para sua pesquisa no SIDRA;
6. Crie um objeto `ibge.Sidra`. Ele funcionará como o [Query Builder](https://servicodados.ibge.gov.br/api/docs/agregados?versao=3#api-bq).
7. Insira os parâmetros identificados pelo `.Metadados` no seu objeto `.Sidra` através dos argumentos `.__init__` ou retroalimentando os atributos do objeto.
8. Chame o método `.rodar` para obter a série de dados.

---

### class DadosAbertosBrasil.ibge.**Agregados**(*index=False*)

Obtém o conjunto de agregados, agrupados pelas respectivas pesquisas.

##### *Parâmetros:*

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id do agregado como index do DataFrame. Caso omitido, assume o valor `False`.

##### *Atributos:*

- **.dados**

Exibe um DataFrame dos agregados agrupados por pesquisa.

- **.pesquisas**

Exibe um DataFrame das lista de pesquisas realizadas.

##### *Métodos:*

- **.filtrar(pesquisa=None, contendo=None, excluindo=None)**

Filtra o DataFrame de `.dados`.

  - Parâmetros:
  
    - **pesquisa:** (Opcional) string
	  Código de duas letras maiúsculas representando a pesquisa realizada.
	  Utilize esse campo para retornar apenas os agregados desta pesquisa.
	  Utilize o atributo `.pesquisas` para obter as referências das pesquisas.
	
	- **contendo:** (Opcional) string
	  Obtenha apenas agregados que contenham este parâmetro no nome.
	
	- **excluindo:** (Opcional) string
	  Filtre agregados que contenham esse parâmetro no nome.
	
  - Retorna:
  
    - **DataFrame**, com os filtros aplicados no DataFrame de `.dados`.

##### *Exemplos:*

Obter todos os agregados, com o código do agregado como index do DataFrame:

```pycon
>>> agreg = ibge.Agregados(index=True)
>>> agreg.dados
```

|agregado_id|agregado_nome                                    |pesquisa_id|pesquisa_nome             |
|:----------|------------------------------------------------:|----------:|-------------------------:|
|1          |Receita operacional líquida e subvenções das e...|PY         |Pesquisa Anual de Serviços|
|2          |População ocupada de 15 anos e mais por setor ...|PE         |Pesquisa Mensal de Emprego|
|3          |População ocupada de 15 anos e mais por posiçã...|PE         |Pesquisa Mensal de Emprego|
|4          |Taxa de desemprego aberto - semana por sexo (s...|PE         |Pesquisa Mensal de Emprego|
|5          |Taxa de desemprego aberto - semana por setor d...|PE         |Pesquisa Mensal de Emprego|
|...        |...                                              |...        |...                       |

Obter lista de pesquisas realizadas:

```pycon
>>> agreg = ibge.Agregados()
>>> agreg.pesquisas
```

|   |pesquisa_id|pesquisa_nome                           |
|:--|----------:|---------------------------------------:|
|0  |CL 	    |Cadastro Central de Empresas            |
|1  |CA 	    |Censo Agropecuário                      |
|2  |ME 	    |Censo Comum do Mercosul, Bolívia e Chile|
|3  |CD 	    |Censo Demográfico                       |
|4  |CM 	    |Contagem da População                   |
|...|...        |...                                     |

Obter agregados da Pesquisa Mensal de Empregos (PE) contendo a palavra 'desemprego' no título:

```pycon
>>> agreg = ibge.Agregados()
>>> agreg.filtrar(pesquisa='PE', contendo='desemprego')
```

|agregado_id|agregado_nome                                    |pesquisa_id|pesquisa_nome             |
|:----------|------------------------------------------------:|----------:|-------------------------:|
|4 	        |Taxa de desemprego aberto - semana por sexo (s...|PE         |Pesquisa Mensal de Emprego|
|5 	        |Taxa de desemprego aberto - semana por setor d...|PE         |Pesquisa Mensal de Emprego|
|13 	    |Taxa de desemprego aberto - semana (série ence...|PE         |Pesquisa Mensal de Emprego|
|14 	    |Taxa de desemprego aberto - 30 dias (série enc...|PE         |Pesquisa Mensal de Emprego|

##### *Documentação da API original:*

https://servicodados.ibge.gov.br/api/docs/agregados?versao=3

---

### class DadosAbertosBrasil.ibge.**Metadados**(*agregado*)

Obtém os metadados do agregado pesquisado.

##### *Parâmetros:*

- **agregado:** int

Código do agregado que se deseja consultar.

Utilize `ibge.Agregados` para encontrar o código do agregado desejado.

##### *Atributos:*

- **.dados:**

Obtém um dictionary com todos os metadados do agregado pesquisado.

- **.id:**

Obtém o id do agregado pesquisado.

- **.nome:**

Obtém no nome completo do agregado pesquisado.

- **.assunto:**

Obtém o assunto do agregado pesquisado.

Utilize em conjunto com a função `ibge.referencias(cod='A')` para obter a referência dos assuntos.

- **.periodos:**

Obtém um dictionary contendo informações do período do agregado pesquisado, incluindo a frequência, o início e o fim da amostra de dados.

Utilize em conjunto com a função `ibge.referencias(cod='P')` para obter a referência dos períodos.

- **.localidades:**

Obtém um dictionary contendo os parâmetros de localidade do agregado pesquisa.

Utilize em conjunto com a função `ibge.referencias(cod='N')` para obter a referência dos níveis territoriais.

- **.variaveis:**

Obtém uma lista de dictionaries de todas as variáveis do agregado pesquisado, incluindo id, nome e unidade das variáveis.

Utilize em conjunto com a função `ibge.referencias(cod='V')` para obter a referência das variáveis. 

- **.classificacoes:**

Obtém uma lista de dictionaries de todas as classificações do agregado pesquisado, incluindo id, nome e uma lista de categorias das classificações.

Utilize em conjunto com a função `ibge.referencias(cod='C')` para obter a referência das classificações. 

##### *Exemplos:*

Explorar os metadados do agregado número 2991:

```pycon
>>> meta = ibge.Metadados(2991)

>>> meta.nome
'Óbitos fetais, ocorridos no ano, por mês do registro, sexo, local de nascimento, número de nascidos por parto, idade da mãe na ocasião do parto e lugar do registro'

>>> meta.assunto
'Óbitos fetais'

>>> meta.periodos
{'frequencia': 'anual', 'inicio': 2003, 'fim': 2018}

>>> meta.localidades
{'Administrativo': ['N1', 'N2', 'N8', 'N9', 'N6', 'N14', 'N7', 'N13', 'N3'],
 'Especial': [],
 'IBGE': []}
 
 >>> meta.variaveis
 [{'id': 225,
  'nome': 'Número de óbitos fetais ocorridos e registrados no ano',
  'unidade': 'Unidades',
  'sumarizacao': ['nivelTerritorial']},
 {'id': 1000225,
  'nome': 'Número de óbitos fetais ocorridos e registrados no ano - percentual do total geral',
  'unidade': '%',
  'sumarizacao': []}]
  
  >>> meta.classificacoes
  [{'id': 236,
  'nome': 'Mês do registro',
  'sumarizacao': {'status': True, 'excecao': []},
  'categorias': [{'id': 0, 'nome': 'Total', 'unidade': None, 'nivel': 0},
   {'id': 5337, 'nome': 'Janeiro', 'unidade': None, 'nivel': 1},
   {'id': 5338, 'nome': 'Fevereiro', 'unidade': None, 'nivel': 1},
   ...
   ]},
 {'id': 2,
  'nome': 'Sexo',
  'sumarizacao': {'status': True, 'excecao': []},
  'categorias': [{'id': 0, 'nome': 'Total', 'unidade': None, 'nivel': 0},
   {'id': 4, 'nome': 'Homens', 'unidade': None, 'nivel': 1},
   {'id': 5, 'nome': 'Mulheres', 'unidade': None, 'nivel': 1},
   ...
   ]},
 {'id': 237,
  'nome': 'Local do nascimento',
  'sumarizacao': {'status': True, 'excecao': []},
  'categorias': [{'id': 0, 'nome': 'Total', 'unidade': None, 'nivel': 0},
   {'id': 5349, 'nome': 'Hospital', 'unidade': None, 'nivel': 1},
   {'id': 5350, 'nome': 'Domicílio', 'unidade': None, 'nivel': 1},
   ...
   ]},
 {'id': 238,
  'nome': 'Número de nascidos por parto',
  'sumarizacao': {'status': True, 'excecao': []},
  'categorias': [{'id': 0, 'nome': 'Total', 'unidade': None, 'nivel': 0},
   {'id': 5352, 'nome': 'Um', 'unidade': None, 'nivel': 1},
   {'id': 5353, 'nome': 'Dois', 'unidade': None, 'nivel': 1},
   ...
   ]},
 {'id': 240,
  'nome': 'Idade da mãe na ocasião do parto',
  'sumarizacao': {'status': True, 'excecao': []},
  'categorias': [{'id': 0, 'nome': 'Total', 'unidade': None, 'nivel': 0},
   {'id': 5370, 'nome': 'Menos de 15 anos', 'unidade': None, 'nivel': 1},
   {'id': 5414, 'nome': '15 a 19 anos', 'unidade': None, 'nivel': 1},
   ...
   ]},
 {'id': 261,
  'nome': 'Duração da gestação em semanas',
  'sumarizacao': {'status': True, 'excecao': []},
  'categorias': [{'id': 0, 'nome': 'Total', 'unidade': None, 'nivel': 0},
   {'id': 104318, 'nome': 'Menos de 22 semanas', 'unidade': None, 'nivel': 1},
   {'id': 104319, 'nome': '22 a 27 semanas', 'unidade': None, 'nivel': 1},
   ...
   ]}]
```

##### *Documentação da API original:*

https://servicodados.ibge.gov.br/api/docs/agregados?versao=3#api-Metadados-agregadosAgregadoMetadadosGet

---

### def DadosAbertosBrasil.ibge.**referencias**(*cod, index=False*)

Obtém uma base de códigos para utilizar como argumento na busca do SIDRA.

##### *Parâmetros:*

- **cod:** string

Define qual referência pesquisar. É possível utilizar um dos seguintes valores:

  - `'A'` ou `'assuntos'` para obter a base de referências de assuntos;
  - `'C'` ou `'classificacoes'` para obter a base de referências de classificações;
  - `'P'` ou `'periodos'` para obter a base de referências de períodos;
  - `'E'` ou `'periodicidades'` para obter a base de referências de periodicidades;
  - `'V'` ou `'variaveis'` para obter a base de referências de variáveis;
  - `'N'`, `'T'`, `'niveis_geograficos'` ou `'territorios'` para obter a base de referências de níveis geográficos;

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id da referência como index do DataFrame. Caso omitido, assume o valor `False`.

##### *Retorna:*

- **DataFrame**, contendo todos as referências e códigos.

##### *Exemplos:*

Pesquisar pela base de referências de periodicidades ('E'):

```pycon
>>> ibge.referencias('E')
```

|  |id |literal         |
|:-|--:|---------------:|
|0 |P1 |Anual           |
|1 |P8 |Semestral       |
|2 |P9 |Trimestral      |
|3 |P5 |Mensal          |
|4 |P13|Trimestral móvel|
	
Pesquisar pela base de referências de assuntos ('A'), utilizando o id do assunto como index do DataFrame:

```pycon
>>> ibge.referencias('A', index=True)
```

|id |literal                                     |
|:--|-------------------------------------------:|
|148|Abastecimento de água                       |
|70 |Abate de animais                            |
|110|Acesso a esgotamento sanitário              |
|147|Acesso à internet                           |
|107|Acesso a serviço de coleta de lixo doméstico|
|146|Acesso a serviços de telefonia              |
|...|...                                         |

---

### class DadosAbertosBrasil.ibge.**Sidra**(*agregado=None, periodos=None, variaveis=None, localidades={'N1': 'all'}, classificacoes=None*)

Classe para obter dados do SIDRA - Sistema IBGE de Recuperação Automática.

##### *Parâmetros:*

- **agregado:** (Opcional) int

Código da tabela (agregado) que será consultada.

Utilize `ibge.Agregados` para encontrar o agregado que deseja.

- **periodos:** (Opcional) list ou int

Períodos nos quais se limitará a consulta.

Utilize `ibge.Metadados(agregado).periodos` para ver os períodos disponíves para o agregado escolhido.

Utilize `ibge.referencias('P')` para encontrar o código de referência destes períodos.

- **variaveis:** (Opcional) list ou int

Lista dos códigos das variáveis que se dejesa consultar.

Utilize `ibge.Metadados(agregado).variaveis` para ver as variáveis disponíves para o agregado escolhido.

Utilize `ibge.referencias('V')` para encontrar o código de referência destas variáveis.

- **self.localidades:** (Opcional) dict

Dictionary de níveis territoriais por códigos dos territórios que se deseja limitar a consulta.

Utilize `ibge.Metadados(agregado).localidades` para ver os níveis territoriais disponíves para o agregado escolhido.

Utilize `ibge.referencias('N')` para encontrar o código de referência destes níveis.

Utilize `ibge.localidades()` para listar todas as localidades disponíveis.

- **self.classificacoes:** (Opcional) dict

Dictionaty de códigos da classificações por códigos das categorias que se deseja consultar.

Utilize `ibge.Metadados(agregado).classificacoes` para ver as classificações e categorias disponíves para o agregado escolhido.

Utilize `ibge.referencias('C')` para encontrar o código de referência destas classificações.

##### *Atributos:*

Os atributos são os mesmos que os parâmetros.

Eles podem ser adicionados tanto pela função `__init__` quando a class é criada, quanto alimentando os atributos posteriormente.

- **agregado**
- **periodos**
- **variaveis**
- **localidades**
- **classificacoes**

##### *Métodos:*

- **.query()**

Obtém uma string contendo a URL da API com os parâmetros alimentados.

Utilize esta URL para obter o arquivo `.json` da consulta diretamente.

  - Parâmetros:
  
    - **Nenhum**

  - Retorna:
  
    - **str**, contendo a URL da consulta.

- **.rodar()**

Obtém o resultado da consulta em função dos parâmetros alimentados no objeto SIDRA.

  - Parâmetros:
  
    - **Nenhum**

  - Retorna:
  
    - **nested dict**, contendo os valores das séries separados pelas categorias e variáveis consultados.

##### *Exemplos:*

Criar o número de óbitos fetais nos estados de São Paulo e Rio de Janeiro, nos anos de 2017 e 2018, separados por idade da mãe e sexo, por unidades e por porcentagem:

1. Pesquisar parâmetros:

```pycon
# Importar módulo IBGE:
>>> from DadosAbertosBrasil import ibge

# Encontrar o agregado desejado:
>>> agreg = ibge.Agregados()
>>> agreg.filtrar(contendo='Óbitos fetais')
```

|agregado_id |agregado_nome                                    |pesquisa_id|pesquisa_nome                 |
|:-----------|------------------------------------------------:|----------:|-----------------------------:|
2990         |Óbitos fetais, ocorridos no ano, por mês do re...|RC         |Estatísticas do Registro Civil|
2991         |Óbitos fetais, ocorridos no ano, por mês do re...|RC         |Estatísticas do Registro Civil|
2992         |Óbitos fetais, ocorridos no ano, por mês do re...|RC         |Estatísticas do Registro Civil|

```pycon
# Obter os metadados do agregado para encontrar os parâmetros necessários para o objeto Sidra
>>> meta = ibge.Metadados(2991)
>>> print('Períodos:')
>>> print(m.periodos)
>>> print('\nVariáveis:')
>>> print(m.variaveis)
>>> print('\nLocalidades:')
>>> print(m.localidades)
>>> print('\nClassificações:')
>>> print(m.classificacoes)

Períodos:
{'frequencia': 'anual', 'inicio': 2003, 'fim': 2018}

Variáveis:
[{'id': 225, 'nome': 'Número de óbitos fetais ocorridos e registrados no ano', 'unidade': 'Unidades', 'sumarizacao': ['nivelTerritorial']}, {'id': 1000225, 'nome': 'Número de óbitos fetais ocorridos e registrados no ano - percentual do total geral', 'unidade': '%', 'sumarizacao': []}]

Localidades:
{'Administrativo': ['N1', 'N2', 'N8', 'N9', 'N6', 'N14', 'N7', 'N13', 'N3'], 'Especial': [], 'IBGE': []}

Classificações:
[{'id': 236, 'nome': 'Mês do registro', 'sumarizacao': {'status': True, 'excecao': []}, 'categorias': [{'id': 0, 'nome': 'Total', 'unidade': None, 'nivel': 0}, {'id': 5337, 'nome': 'Janeiro', 'unidade': None, 'nivel': 1}, {'id': 5338, 'nome': 'Fevereiro', 'unidade': None, 'nivel': 1}, {'id': 5339, 'nome': 'Março', 'unidade': None, 'nivel': 1}, {'id': 5340, 'nome': 'Abril', 'unidade': None, 'nivel': 1}, ...
```

2. Criar objeto SIDRA, alimentar com parâmetros e rodar query:

```pycon
# Método 1:
>>> obitos = ibge.Sidra()
>>> obitos.agregado = 2991
>>> obitos.periodos = [2017, 2018]
>>> obitos.variaveis = [225, 1000225]
>>> obitos.localidades = {'N3': [33, 35]}
>>> obitos.classificacoes = {2: [4, 5], 240: 'all'}
>>> res = obitos.rodar()

# Método 2:
>>> res = ibge.Sidra(agregado=2991, periodos=[2017, 2018], variaveis=[225, 1000225], localidades={'N3':[33, 35]}, classificacoes={2:[4, 5], 240:'all'}).rodar()
```

3. Abrindo o dictionary até chegar em um valor específico:

```pycon
# Variáveis escolhidas em obitos.variaveis:
# 0 para 'Unidades' e 1 para 'Percentual'.
>>> var_id = 0

# Informações da variável:
# 'id', 'variavel', 'unidade' ou 'resultados'
>>> var_info = 'resultados'

# Combinação de classificações:
# Todas as combinações possíveis de 0 a 92:
>>> class_id = 0

# Informações da classificação:
# 'classificacoes' ou 'series'
>>> class_info = 'series'

# Localidades escolhidas em obitos.localidades:
# 0 para 'Rio de Janeiro' e 1 para 'São Paulo'.
>>> loc_id = 0

# Informações da localidade:
# 'localidade' ou 'serie'
>>> loc_info = 'serie'

# Períodos escolhidos em obitos.periodos:
# '2017' ou '2018'. Note que é necessário ser tipo 'str', não 'int'.
>>> per = '2018'

>>> valor = res[var_id][var_info][class_id][class_info][loc_id][loc_info][per]

# Ou...
>>> valor = res[0]['resultados'][0]['series'][0]['serie']['2018']

# Ver valor
>>> valor
'1377'
```

##### *Documentação da API original:*

https://servicodados.ibge.gov.br/api/docs/agregados?versao=3#api-bq

---

# DadosAbertosBrasil.**ipea**

Módulo para captura dos dados abertos das APIs do Ipeadata.

- ipea.[series](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilipeaseriescodnone-valorestrue)
- ipea.[temas](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilipeatemascodnone)
- ipea.[paises](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilipeapaisescodnone)
- ipea.[territorios](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilipeaterritorioscodnone-nivelnone)
- ipea.[nivel_territoriais](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilipeaniveis_territoriais)

Importe o módulo com `from DadosAbertosBrasil import ipea`

---

### def DadosAbertosBrasil.ipea.**series**(*cod=None, valores=True*)

Registros de metadados de todas as séries disponíveis para consulta.

##### *Parâmetros:*

- **cod:** (Opcional) str

Código da série que se deseja pesquisar.

Caso o valor seja omitido, um DataFrame com todas as séries é retornado.

O código é o campo `SERNOME` do DataFrame de séries.

- **valores:** (Opcional) `True` ou `False`

`True` para obter os valores da série.

`False` para obter as informações sobre a série.

Este argumento é ignorado caso não seja fornecido um código de série.

##### *Retorna:*

- **pandas.DataFrame** contendo a lista completa de séries disponíveis, caso `cod == None`
- **pandas.DataFrame** contendo os valores da série, caso `valores == True`
- **pandas.DataFrame** contendo as informações da série, caso `valores == False`

##### *Exemplos:*

Pesquisar por todas as séries contendo o termo 'Gini':

```pycon
>>> s = ipea.series()
>>> s[s.SERNOME.str.contains('Gini')]
```

|    |BASNOME       |FNTNOME                                       |FNTSIGLA|FNTURL         |MULNOME|PAICODIGO|PERNOME |SERATUALIZACAO               |SERCODIGO |SERCOMENTARIO                                    |SERNOME                                        |SERNUMERICA|SERSTATUS|TEMCODIGO|UNINOME|
|:---|-------------:|---------------------------------------------:|-------:|--------------:|------:|--------:|-------:|----------------------------:|---------:|------------------------------------------------:|----------------------------------------------:|----------:|--------:|--------:|------:|
|6967|Macroeconômico|Instituto de Pesquisa Econômica Aplicada(IPEA)|IPEA    |www.ipea.gov.br|None   |BRA      |Anual   |2016-01-06T19:33:38-02:00    |DISOC_RDCG|Mede o grau de desigualdade na distribuição da...|Renda - desigualdade - coeficiente de Gini     |True       |I        |15       |-      |
|7543|Social        |Instituto de Pesquisa Econômica Aplicada(IPEA)|IPEA    |www.ipea.gov.br|None   |None     |Decenal |2009-04-20T15:58:01.41-03:00 |GINIC1    |Mede o grau de desigualdade existente na distr...|Renda - desigualdade - índice de Gini - brancos|True       |None     |30       |-      |
|7544|Social        |Instituto de Pesquisa Econômica Aplicada(IPEA)|IPEA    |www.ipea.gov.br|None   |None     |Decenal |2009-04-20T15:58:01.443-03:00|GINIC2    |Mede o grau de desigualdade existente na distr...|Renda - desigualdade - índice de Gini - negros |True       |None     |30       |-      |
|7589|Social        |Instituto de Pesquisa Econômica Aplicada(IPEA)|IPEA    |www.ipea.gov.br|None   |None     |Anual   |2016-01-07T16:09:04.52-02:00 |PGINI     |Mede o grau de desigualdade na distribuição da...|Renda - desigualdade - coeficiente de Gini     |True       |None     |30       |-      |

Capturar dados anuais do coeficiente de Gini (código 'DISOC_RDCG'):

```pycon
>>> ipea.series('DISOC_RDCG')
```

| 	|NIVNOME|SERCODIGO |TERCODIGO|VALDATA                  |VALVALOR|
|:--|------:|---------:|--------:|------------------------:|-------:|
|0  |       |DISOC_RDCG|         |1976-01-01T00:00:00-02:00|0.622740|
|1  |       |DISOC_RDCG|         |1977-01-01T00:00:00-02:00|0.624648|
|2  |       |DISOC_RDCG|         |1978-01-01T00:00:00-02:00|0.603907|
|3  |       |DISOC_RDCG|         |1979-01-01T00:00:00-02:00|0.593121|
|...|...    |...       |...      |...                      |...     |

##### *Documentação da API original:*

http://www.ipeadata.gov.br/api/

---

### def DadosAbertosBrasil.ipea.**temas**(*cod=None*)

Registros de todos os temas cadastrados.

##### *Parâmetros:*

- **cod:** (Opcional) int

Código do tema.

Caso o valor seja omitido, um DataFrame com todas os temas é retornado.

O código é o campo `TEMCODIGO` do DataFrame de séries.

##### *Retorna:*

- **pandas.DataFrame** contendo a lista completa de temas disponíveis. Cada row é um tema e as columns são os códigos dos temas, dos temas-pai e os nomes dos temas.

##### *Exemplos:*

Pesquisar por todos os temas disponíveis:

```pycon
>>> ipea.temas()
```

|   |TEMCODIGO|TEMCODIGO_PAI|TEMNOME              |
|:--|--------:|------------:|--------------------:|
|0  |28       |NaN          |Agropecuária         |
|1  |23       |NaN          |Assistência social   |
|2  |10       |NaN          |Balanço de pagamentos|
|3  |7        |NaN          |Câmbio               |
|4  |5        |NaN          |Comércio exterior    |
|...|...      |...          |...                  |

##### *Documentação da API original:*

http://www.ipeadata.gov.br/api/

---

### def DadosAbertosBrasil.ipea.**paises**(*cod=None*)

Registros de todos os países cadastrados.

##### *Parâmetros:*

- **cod:** (Opcional) str

Código de três letras maiúsculas do país.

Caso o valor seja omitido, um DataFrame com todas os países é retornado.

O código é o campo `PAICODIGO` do DataFrame de séries.

##### *Retorna:*

- **pandas.DataFrame** contendo a lista completa de países. Cada row é um país e as columns são os códigos e os nomes completos dos países.

##### *Exemplos:*

Pesquisar por todos os países disponíveis:

```pycon
>>> ipea.paises()
```

|   |PAICODIGO|PAINOME       |
|:--|--------:|-------------:|
|0  |ZAF      |África do Sul |
|1  |DEU      |Alemanha      |
|2  |LATI     |América Latina|
|3  |AGO      |Angola        |
|4  |SAU      |Arábia Saudita|
|...|...      |...           |

##### *Documentação da API original:*

http://www.ipeadata.gov.br/api/

---

### def DadosAbertosBrasil.ipea.**territorios**(*cod=None, nivel=None*)

Registros de todos os territórios brasileiros cadastrados, categorizados por nível territorial.

##### *Parâmetros:*

- **cod:** (Opcional) int ou str

Código do território pesquisado.

Deve ser usado em conjunto com o parâmetro `nivel`

Caso pelo menos um dos dois seja omitido, um DataFrame com todos os territórios brasileiros é retornado.

O código é o campo `TERCODIGO` do DataFrame de séries.

Utilize a função do módulo IBGE `ibge.localidades()` para auxiliar na busca pelos códigos dos territórios.

- **nivel:** (Opcional) str

Nome do nível geográfico do território pesquisado.

Deve ser usado em conjunto com o parâmetro `cod`

Caso pelo menos um dos dois seja omitido, um DataFrame com todos os territórios brasileiros é retornado.

O código é o campo `NIVNOME` do DataFrame de séries.

##### *Retorna:*

- **pandas.DataFrame** contendo a lista completa de territórios brasileiros. Cada row é um território e as columns são o código, o nome, o nível e a área do território.

##### *Exemplos:*

Pesquisar por todos os territórios chamados 'São Paulo':

```pycon
>>> t = ipea.territorios
>>> t[t.TERNOME == 'São Paulo']
```

|     |NIVAMC|NIVNOME      |TERAREA |TERCAPITAL|TERCODIGO|TERNOME  |TERNOMEPADRAO| 	
|:----|-----:|------------:|-------:|---------:|--------:|--------:|------------:|
|0    |False |Estados      |248808.8|False     |35       |São Paulo|SAO PAULO    |
|12247|False |Microrregiões|2355.7  |False     |35061    |São Paulo|SAO PAULO    |
|14002|True  |AMC 91-00    |1528.5  |False     |355030   |São Paulo|SAO PAULO    |
|14003|True  |AMC 70-00    |1528.5  |False     |355030   |São Paulo|SAO PAULO    |
|14004|False |Municípios   |1528.5  |True      |3550308  |São Paulo|SAO PAULO    |

Pesquisar pelo estado de São Paulo (código 35):

```pycon
>>> ipea.territorios(35, 'Estados')
```

|  |NIVAMC|NIVNOME|TERAREA |TERCAPITAL|TERCODIGO|TERNOME  |TERNOMEPADRAO| 	
|:-|-----:|------:|-------:|---------:|--------:|--------:|------------:|
|0 |False |Estados|248808.8|False     |35       |São Paulo|SAO PAULO    |

Pesquisar pela cidade de São Paulo (código 3550308):

```pycon
>>> ipea.territorios(3550308, 'Municípios')
```

|  |NIVAMC|NIVNOME   |TERAREA|TERCAPITAL|TERCODIGO|TERNOME  |TERNOMEPADRAO| 	
|:-|-----:|---------:|------:|---------:|--------:|--------:|------------:|
|0 |False |Municípios|1528.8 |True      |3550308  |São Paulo|SAO PAULO    |

##### *Documentação da API original:*

http://www.ipeadata.gov.br/api/

---

### def DadosAbertosBrasil.ipea.**niveis_territoriais**()

Lista dos possíveis níveis territoriais.

##### *Parâmetros:*

- **Nenhum**

##### *Retorna:*

- **list de str** contendo as descrições por extenso dos níveis territoriais.

##### *Exemplos:*

Capturar a lista de descrições de níveis territoriais:

```pycon
>>> ipea.niveis_territoriais()

['',
 'Brasil',
 'Regiões',
 'Estados',
 'Municípios',
 'AMC 91-00',
 'Microrregiões',
 'Mesorregiões',
 'AMC 20-00',
 'AMC 40-00',
 'AMC 60-00',
 'AMC 70-00',
 'AMC 1872-00',
 'Área metropolitana',
 'Estado/RM']
```

##### *Documentação da API original:*

http://www.ipeadata.gov.br/api/

---

# DadosAbertosBrasil.**camara**

Pacote para captura dos dados abertos da Câmara dos Deputados do Brasil

- camara.[blocos](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamarablocoscodnone-indexfalse)
- camara.[deputados](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamaradeputadoscodnone-serieinformacoes-indexfalse)
- camara.[eventos](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamaraeventoscodnone-serieinformacoes-indexfalse)
- camara.[frentes](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamarafrentescodnone-serieinformacoes-indexfalse)
- camara.[legislaturas](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamaralegislaturascodnone-serieinformacoes-indexfalse)
- camara.[orgaos](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamaraorgaoscodnone-serieinformacoes-indexfalse)
- camara.[partidos](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamarapartidoscodnone-serieinformacoes-indexfalse)
- camara.[proposicoes](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamaraproposicoescodnone-serieinformacoes-indexfalse)
- camara.[votacoes](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamaravotacoescodnone-serieinformacoes-indexfalse)
- camara.[referencias](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamarareferenciasfuncao-indexfalse)
- camara.[filtrar_deputados](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilcamarafiltrar_deputadossexonone-ufnone-partidonone-contendonone-excluindonone-indexfalse)

Importe o módulo com `from DadosAbertosBrasil import camara`

---

### def DadosAbertosBrasil.camara.**blocos**(*cod=None, index=False*)

Obtém dados sobre os blocos partidários.

Nas atividades parlamentares, partidos podem se juntar em blocos partidários. Quando associados, os partidos passam a trabalhar como se fossem um "partidão", com um só líder e um mesmo conjunto de vice-líderes.

Os blocos só podem existir até o fim da legislatura em que foram criados: na legislatura seguinte, os mesmos partidos, se associados, formam um novo bloco.

##### *Parâmetros:*

- **cod**: (Opcional) int

Insira o id do bloco partidário para obter mais informações sobre ele.

Caso esse campo seja omitido, retorna uma lista com todos os blocos partidários.

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id do bloco partidário como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista com todos os blocos partidários, caso `cod == None`.
- **dict**, contendo detalhes do bloco partidário, caso `cod` seja o id do bloco.

##### *Exemplos:*

Obter detalhes do bloco 575:

```pycon
>>> camara.blocos(575)

{'id': '575',
 'uri': 'https://dadosabertos.camara.leg.br/api/v2/blocos/575',
 'nome': 'PL, PP, PSD, MDB, DEM, SOLIDARIEDADE, PTB, PROS, AVANTE',
 'idLegislatura': '56'}
```

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**deputados**(*cod=None, serie='informacoes', index=False*)

Obtém a lista ou informações dos deputados.

##### *Parâmetros:*

- **cod**: (Opcional) int

Insira o id do(a) deputado(a) para obter mais informações sobre ele(a).

Caso esse campo seja omitido, retorna uma lista com todos os deputados da atual legislatura.

- **serie**: string

Insira um dos campos abaixo para obter mais informações sobre o(a) deputado(a).

  - `'informacoes'`: Informações detalhadas sobre um deputado específico;
  - `'despesas'`: As despesas com exercício parlamentar do deputado;
  - `'discursos'`: Os discursos feitos por um deputado em eventos diversos;
  - `'eventos'`: Uma lista de eventos com a participação do parlamentar;
  - `'frentes'`: As frentes parlamentares das quais um deputado é integrante;
  - `'orgaos'`: Os órgãos dos quais um deputado é integrante.
  
Esse campo é ignorado caso `cod == None`

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id do(a) deputado(a) como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista com todos os deputados, caso `cod == None`. Cada row é um deputado e as columns são o nome, partido, estado, e-mail, legislatura atual e a URL da foto no site da câmara.
- **dict**, contendo detalhes da série escolhida sobre o(a) deputado(a), caso `cod` seja o id do(a) deputado(a).

##### *Exemplos:*

Obter a lista de deputados da atual legislatura:

```pycon
>>> camara.deputados(index=True)
```

|id    |email                           |idLegislatura|nome           |siglaPartido|siglaUf|urlFoto                                           |
|:-----|-------------------------------:|------------:|--------------:|-----------:|------:|-------------------------------------------------:|
|204554|dep.abiliosantana@camara.leg.br |56           |Abílio Santana |PL          |BA     |https://www.camara.leg.br/internet/deputado/ba... |
|204521|dep.abouanni@camara.leg.br      |56           |Abou Anni      |PSL         |SP     |https://www.camara.leg.br/internet/deputado/ba... |
|204379|dep.acaciofavacho@camara.leg.br |56           |Acácio Favacho |PROS        |AP     |https://www.camara.leg.br/internet/deputado/ba... |
|204560|dep.adolfoviana@camara.leg.br   |56           |Adolfo Viana   |PSDB        |BA     |https://www.camara.leg.br/internet/deputado/ba... |
|204528|dep.adrianaventura@camara.leg.br|56           |Adriana Ventura|NOVO        |SP     |https://www.camara.leg.br/internet/deputado/ba... |
|...   |...                             |...          |...            |...         |...    |...                                               |


Obter a lista de frentes que o deputado Rodrigo Maia (código 74693) participa:

```pycon
>>> camara.deputados(cod=74693, serie='frentes')

[{'id': 54180,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/frentes/54180',
  'titulo': 'Frente Parlamentar Mista em Defesa do Cinema e do Audiovisual Brasileiros',
  'idLegislatura': 56},
 {'id': 54165,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/frentes/54165',
  'titulo': 'Frente Parlamentar de Defesa e Valorização da Produção Nacional de Uvas, Vinhos, Espumantes e seus Derivados',
  'idLegislatura': 56},
  ...]
```

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**eventos**(*cod=None, serie='informacoes', index=False*)

Obtém a lista ou informações dos eventos ocorridos ou previstos nos diversos órgãos da Câmara.

##### *Parâmetros:*

- **cod**: (Opcional) int

Insira o id do evento para obter mais informações sobre ele.

Caso esse campo seja omitido, retorna uma lista com todos os eventos da Câmara.

- **serie**: string

Insira um dos campos abaixo para obter mais informações sobre o evento.

  - `'informacoes'`: Informações detalhadas sobre um evento específico;
  - `'deputados'`: Os deputados participantes de um evento específico;
  - `'orgaos'`: Lista de órgãos organizadores do evento;
  - `'pauta'`: Lista de proposições que foram ou deverão ser avaliadas em um evento de caráter deliberativo;
  - `'votacoes'`: Informações detalhadas de votações sobre um evento específico.

Esse campo é ignorado caso `cod == None`

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id do evento como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista com todos os eventos da Câmara, caso `cod == None`. Cada row é um evento e as columns são os horários, descrições, orgãos, locais e a situação do evento.
- **dict**, contendo detalhes da série escolhida sobre o evento, caso `cod` seja o id do evento.

##### *Exemplos:*

Obter a lista de todos os eventos ocorridos ou previstos na Câmara:

```pycon
>>> camara.eventos(index=True)
```

|id   |dataHoraFim     |dataHoraInicio  |descricao                                        |descricaoTipo      |localCamara                                      |...|
|:----|---------------:|---------------:|------------------------------------------------:|------------------:|------------------------------------------------:|--:|
|59588|2020-05-04T23:25|2020-05-04T13:55|Sessão Deliberativa Extraordinária (VIRTUAL)     |Sessão Deliberativa|{'nome': 'Plenário da Câmara dos Deputados', '...|...|
|59591|2020-05-04T13:37|2020-05-04T11:30|Situação dos Hospitais no Rio de Janeiro...      |Outro Evento       |{'nome': None, 'predio': None, 'sala': None, '...|...|
|59592|2020-05-05T14:22|2020-05-05T11:30|Instituições de Longa Permanência para Idosos\...|Reunião Técnica    |{'nome': 'Anexo II, Plenário 03', 'predio': No...|...|
|59593|2020-05-05T18:06|2020-05-05T15:00|Requisição Administrativa de Leitos\r\n Reuniã...|Reunião Técnica    |{'nome': None, 'predio': None, 'sala': None, '...|...|
|...  |...             |...             |...                                              |...                |...                                              |...|


Obter a lista de deputados presentes no evento 59588:

```pycon
>>> camara.eventos(cod=59588, serie='deputados')

[{'id': 66179,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/66179',
  'nome': 'Norma Ayub',
  'siglaPartido': 'DEM',
  'uriPartido': 'https://dadosabertos.camara.leg.br/api/v2/partidos/36769',
  'siglaUf': 'ES',
  'idLegislatura': 56,
  'urlFoto': 'https://www.camara.leg.br/internet/deputado/bandep/66179.jpg',
  'email': 'dep.normaayub@camara.leg.br'},
 {'id': 66828,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/66828',
  'nome': 'Fausto Pinato',
  'siglaPartido': 'PP',
  'uriPartido': 'https://dadosabertos.camara.leg.br/api/v2/partidos/37903',
  'siglaUf': 'SP',
  'idLegislatura': 56,
  'urlFoto': 'https://www.camara.leg.br/internet/deputado/bandep/66828.jpg',
  'email': 'dep.faustopinato@camara.leg.br'},
  ...]
```

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**frentes**(*cod=None, serie='informacoes', index=False*)

Obtém a lista ou informações das frentes parlamentares, um agrupamento oficial de parlamentares em torno de um determinado tema ou proposta.

As frentes existem até o fim da legislatura em que foram criadas, e podem ser recriadas a cada legislatura. Algumas delas são compostas por deputados e senadores

##### *Parâmetros:*

- **cod**: (Opcional) int

Insira o id da frente parlamentar para obter mais informações sobre ela.

Caso esse campo seja omitido, retorna uma lista com todos as frentes parlamentares.

- **serie**: string

Insira um dos campos abaixo para obter mais informações sobre a frente parlamentar.

  - `'informacoes'`: Informações detalhadas sobre uma frente parlamentar;
  - `'membros'`: Os deputados que participam de uma frente parlamentar.

Esse campo é ignorado caso `cod == None`

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id da frente como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista com todas as frentes parlamentares, caso `cod == None`. Cada row é uma frente parlamentar e as columns são o nome da frente e a legislatura que ela pertence.
- **dict**, contendo detalhes da série escolhida sobre a frente parlamentar, caso `cod` seja o id do frente.

##### *Exemplos:*

Obter a lista de todas frentes parlamentares:

```pycon
>>> camara.frentes(index=True)
```

|id   |idLegislatura|titulo                                           |
|:----|------------:|------------------------------------------------:|
|54251|56           |Frente Parlamentar Mista para Implantação do P...|
|54248|56           |Frente Parlamentar em Defesa da Democratização...|
|54249|56           |Frente Parlamentar em Defesa dos Profissionais...|
|54250|56           |Frente Parlamentar em Apoio ao Ecoturismo - EC...|
|54231|56           |Frente Parlamentar Mista de Segurança Contra I...|
|...  |...          |...                                              |

Obter os deputados membros da Frente Parlamentar Brasil-Rússia (código 54246):

```pycon
>>> camara.frentes(cod=54246, serie='membros')

[{'id': 204511,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/204511',
  'nome': 'David Soares',
  'siglaPartido': 'DEM',
  'uriPartido': 'https://dadosabertos.camara.leg.br/api/v2/partidos/36769',
  'siglaUf': 'SP',
  'idLegislatura': 56,
  'urlFoto': 'https://www.camara.leg.br/internet/deputado/bandep/204511.jpg',
  'email': None,
  'titulo': 'Coordenador',
  'codTitulo': 14,
  'dataInicio': None,
  'dataFim': None},
 {'id': 68720,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/68720',
  'nome': 'Fábio Henrique',
  'siglaPartido': 'PDT',
  'uriPartido': 'https://dadosabertos.camara.leg.br/api/v2/partidos/36786',
  'siglaUf': 'SE',
  'idLegislatura': 56,
  'urlFoto': 'https://www.camara.leg.br/internet/deputado/bandep/68720.jpg',
  'email': None,
  'titulo': 'Membro',
  'codTitulo': 1004,
  'dataInicio': None,
  'dataFim': None},
  ...]
```

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**legislaturas**(*cod=None, serie='informacoes', index=False*)

Obtém a lista ou informações das legislaturas.

Legislatura é o nome dado ao período de trabalhos parlamentares entre uma eleição e outra.

##### *Parâmetros:*

- **cod**: (Opcional) int

Insira o id da legislatura para obter mais informações sobre ela.

Caso esse campo seja omitido, retorna uma lista com a data de início e fim das legislaturas.

- **serie**: string

Insira um dos campos abaixo para obter mais informações sobre o evento.

  - `'informacoes'`: Informações extras sobre uma determinada legislatura da Câmara;
  - `'membros'`: Quais deputados fizeram parte da Mesa Diretora em uma legislatura.

Esse campo é ignorado caso `cod == None`

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id da legislatura como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista com todas os períodos das legislaturas, caso `cod == None`. Cada row é uma legislatura e as columns são a data de início e a data de fim.
- **dict**, contendo detalhes da série escolhida sobre a legislatura, caso `cod` seja o id da legislatura.

##### *Exemplos:*

Obter a lista dos períodos das legislaturas:

```pycon
>>> camara.legislaturas(index=True)
```

|id   |dataFim   |dataInicio|
|:----|---------:|---------:|
|56   |2023-01-31|2019-02-01|
|55   |2019-01-31|2015-02-01|
|54   |2015-01-31|2011-02-01|
|53   |2011-01-31|2007-02-01|
|52   |2007-01-31|2003-02-01|
|...  |...       |...       |

Obter os deputados membros da mesa diretora da legislatura 55:

```pycon
>>> camara.legislaturas(cod=55, serie='mesa')

[{'id': 141430,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/141430',
  'nome': 'FELIPE BORNIER',
  'siglaPartido': 'PSD',
  'uriPartido': 'https://dadosabertos.camara.leg.br/api/v2/partidos/36763',
  'siglaUf': 'RJ',
  'idLegislatura': 55,
  'urlFoto': 'https://www.camara.leg.br/internet/deputado/bandep/141430.jpg',
  'email': None,
  'dataInicio': '2015-02-01',
  'dataFim': '2017-02-02',
  'titulo': '2º Secretário',
  'codTitulo': '6'},
 {'id': 160633,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/160633',
  'nome': 'MANDETTA',
  'siglaPartido': 'DEM',
  'uriPartido': 'https://dadosabertos.camara.leg.br/api/v2/partidos/36769',
  'siglaUf': 'MS',
  'idLegislatura': 55,
  'urlFoto': 'https://www.camara.leg.br/internet/deputado/bandep/160633.jpg',
  'email': None,
  'dataInicio': '2015-02-01',
  'dataFim': '2017-02-02',
  'titulo': '1º Suplente de Secretário',
  'codTitulo': '9'},
  ...]
```

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**orgaos**(*cod=None, serie='informacoes', index=False*)

Obtém a lista ou informações das comissões e outros órgãos legislativos da Câmara.

##### *Parâmetros:*

- **cod**: (Opcional) int

Insira o id do órgão legislativo para obter mais informações sobre ele.

Caso esse campo seja omitido, retorna uma lista com todos os órgãos.

- **serie**: string

Insira um dos campos abaixo para obter mais informações sobre o órgão legislativo.

  - `'informacoes'`: Informações detalhadas sobre um órgão da Câmara;
  - `eventos`: Os eventos ocorridos ou previstos em um órgão legislativo;
  - `membros`: Lista de cargos de um órgão e parlamentares que os ocupam;
  - `votacoes`: Informações detalhadas sobre votações de um órgão da Câmara.

Esse campo é ignorado caso `cod == None`

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id do órgão legislativo como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista com todos os órgãos legislativos, caso `cod == None`. Cada row é um órgão e as columns são identificadores, tipos e descrições dos órgãos.
- **dict**, contendo detalhes da série escolhida sobre o órgão legislativo, caso `cod` seja o id do órgão.

##### *Exemplos:*

Obter a lista dos órgãos legislativos:

```pycon
>>> camara.orgaos(index=True)
```

|id |apelido                    |codTipoOrgao|nome                                 |sigla     |tipoOrgao                        |
|:--|--------------------------:|-----------:|------------------------------------:|---------:|--------------------------------:|
|4  |Mesa Diretora              |1           |Mesa Diretora da Câmara dos Deputados|MESA      |Comissão Diretora                |
|51 |Judiciário                 |50000       |Judiciário                           |Judiciário|Órgão do Poder Judiciário        |
|57 |MINISTÉRIO PÚBLICO DA UNIÃO|81007       |MINISTÉRIO PÚBLICO DA UNIÃO          |MPU       |MPU - Ministério Público da União|
|60 |PRESIDÊNCIA DA REPÚBLICA   |30000       |Presidência da República             |PR        |Órgão do Poder Executivo         |
|78 |Senado Federal             |40000       |Senado Federal                       |SF        |Órgão do Poder Legislativo       |
|...|...                        |...         |...                                  |...       |...                              |

Obter informações do conselho de ministros (código 301):

```pycon
>>> camara.orgaos(cod=301, serie='informacoes')

{'id': 301,
 'uri': 'https://dadosabertos.camara.leg.br/api/v2/orgaos/301',
 'sigla': 'CM',
 'nome': 'CONSELHO DE MINISTROS',
 'apelido': 'CONSELHO DE MINISTROS',
 'codTipoOrgao': 12000,
 'tipoOrgao': 'Órgão da Câmara dos Deputados',
 'dataInicio': None,
 'dataInstalacao': None,
 'dataFim': None,
 'dataFimOriginal': None,
 'casa': '',
 'sala': None,
 'urlWebsite': None}
```

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**partidos**(*cod=None, serie='informacoes', index=False*)

Obtém a lista ou informações dos partidos políticos que têm parlamentares em exercício na Câmara.

##### *Parâmetros:*

- **cod**: (Opcional) int

Insira o id do partido político para obter mais informações sobre ele.

Caso esse campo seja omitido, retorna uma lista com todos os partidos.

- **serie**: string

Insira um dos campos abaixo para obter mais informações sobre o partido.

  - `'informacoes'`: Informações detalhadas sobre um partido político;
  - `membros`: Uma lista dos parlamentares de um partido durante um período.

Esse campo é ignorado caso `cod == None`

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id do partido como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista com todos os partidos políticos, caso `cod == None`. Cada row é um partido e as columns são o nome e a sigla deles.
- **dict**, contendo detalhes da série escolhida sobre o partido político, caso `cod` seja o id do partido.

##### *Exemplos:*

Obter a lista dos partidos com parlamentares em exercício:

```pycon
>>> camara.partidos(index=True)
```

|id   |nome                            |sigla    |
|:----|-------------------------------:|--------:|
|36898|Avante                          |AVANTE   |
|37905|Cidadania                       |CIDADANIA|
|37902|Democracia Cristã               |DC       |
|36769|Democratas                      |DEM      |
|36899|Movimento Democrático Brasileiro|MDB      |
|...  |...                             |...      |

Obter a lista de parlamentares do partido NOVO (código 37901) em exercício na Câmara:

```pycon
>>> camara.orgaos(cod=301, serie='informacoes')

[{'id': 204528,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/204528',
  'nome': 'Adriana Ventura',
  'siglaPartido': 'NOVO',
  'uriPartido': 'https://dadosabertos.camara.leg.br/api/v2/partidos/37901',
  'siglaUf': 'SP',
  'idLegislatura': 56,
  'urlFoto': 'https://www.camara.leg.br/internet/deputado/bandep/204528.jpg',
  'email': 'dep.adrianaventura@camara.leg.br'},
 {'id': 204516,
  'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/204516',
  'nome': 'Alexis Fonteyne',
  'siglaPartido': 'NOVO',
  'uriPartido': 'https://dadosabertos.camara.leg.br/api/v2/partidos/37901',
  'siglaUf': 'SP',
  'idLegislatura': 56,
  'urlFoto': 'https://www.camara.leg.br/internet/deputado/bandep/204516.jpg',
  'email': 'dep.alexisfonteyne@camara.leg.br'},
  ...]
```

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**proposicoes**(*cod=None, serie='informacoes', index=False*)

Obtém a lista ou informações sobre projetos de lei, resoluções, medidas provisórias, emendas, pareceres e todos os outros tipos de proposições na Câmara.

##### *Parâmetros:*

- **cod**: (Opcional) int

Insira o id da proposição para obter mais informações sobre ela.

Caso esse campo seja omitido, retorna uma lista com as proposições mais recentes.

- **serie**: string

Insira um dos campos abaixo para obter mais informações sobre a proposição.

  - `'informacoes'`: Informações detalhadas sobre uma proposição específica;
  - `autores`: Lista pessoas e/ou entidades autoras de uma proposição;
  - `relacionadas`: Uma lista de proposições relacionadas a uma em especial;
  - `temas`: Lista de áreas temáticas de uma proposição;
  - `tramitacoes`: O histórico de passos na tramitação de uma proposta;
  - `votacoes`: Informações detalhadas de votações sobre uma proposição específica.

Esse campo é ignorado caso `cod == None`

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id da proposição como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista com as proposições mais recentes, caso `cod == None`. Cada row é uma proposição e as columns são os identificadores e descrições da proposição.
- **dict**, contendo detalhes da série escolhida sobre a proposição, caso `cod` seja o id da proposição.

##### *Exemplos:*

Obter a lista com as proposições mais recentes:

```pycon
>>> camara.proposicoes(index=True)
```

|id    |ano |codTipo|ementa                                           |numero|siglaTipo|
|:-----|---:|------:|------------------------------------------------:|-----:|--------:|
|17915 |2000|139    |Dispõe sobre a jornada de trabalho dos Enferme...|2295  |PL       |
|45377 |2002|139    |Dispõe sobre a vigilância e o controle da qual...|6222  |PL       |
|327888|2006|139    |Altera o art. 109 do Decreto-Lei nº 2.848, de ...|7220  |PL       |
|345103|2007|139    |Dispõe sobre o Estatuto do Nascituro e dá outr...|478   |PL       |
|351367|2007|146    |Solicita a instauração de procedimento de fisc...|7     |REP      |
|...   |... |...    |...                                              |...   |...      |

Obter a lista de autores da PL 478 (código 345103):

```pycon
>>> camara.proposicoes(cod=345103, serie='autores')

[{'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/74059',
  'nome': 'Luiz Bassuma',
  'codTipo': 10000,
  'tipo': 'Deputado',
  'ordemAssinatura': 1,
  'proponente': 1},
 {'uri': 'https://dadosabertos.camara.leg.br/api/v2/deputados/141469',
  'nome': 'Miguel Martini',
  'codTipo': 10000,
  'tipo': 'Deputado',
  'ordemAssinatura': 2,
  'proponente': 1}]
```

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**votacoes**(*cod=None, serie='informacoes', index=False*)

Obtém a lista ou informações sobre as votações ocorridas em eventos dos diversos órgãos da Câmara.

##### *Parâmetros:*

- **cod**: (Opcional) int

Insira o id da votação para obter mais informações sobre ela.

Caso esse campo seja omitido, retorna uma lista com as votações mais recentes.

- **serie**: string

Insira um dos campos abaixo para obter mais informações sobre a votação.

  - `'informacoes'`: Informações detalhadas sobre uma votação da Câmara;
  - `orientacoes`: O voto recomendado pelas lideranças aos seus deputados em uma votação;
  - `votos`: Como cada parlamentar votou em uma votação nominal e aberta.

Esse campo é ignorado caso `cod == None`

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id da votação como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista com as votações mais recentes, caso `cod == None`. Cada row é uma votação e as columns são descrições e horários da votação.
- **dict**, contendo detalhes da série escolhida sobre a votação, caso `cod` seja o id da votação.

##### *Exemplos:*

Obter a lista com as votações mais recentes:

```pycon
>>> camara.votacoes(index=True)
```

|id        |aprovacao|data      |dataHoraRegistro   |descricao                                        |proposicaoObjeto|siglaOrgao|
|:---------|--------:|---------:|------------------:|------------------------------------------------:|---------------:|---------:|
|2236213-78|1.0      |2020-05-08|2020-05-08T17:39:53|Aprovada a Redação Final assinada pelo Relator...|None            |PLEN      |
|2236213-77|0.0      |2020-05-08|2020-05-08T17:37:43|Rejeitada a Emenda nº 14.                        |None            |PLEN      |
|2236213-74|1.0      |2020-05-08|2020-05-08T16:44:41|Aprovada a Emenda n° 12.                         |None            |PLEN      |
|2236213-70|NaN      |2020-05-08|2020-05-08T15:42:07|Mantido o texto.                                 |None            |PLEN      |
|2236213-68|NaN      |2020-05-08|2020-05-08T15:41:32|Mantido o texto.                                 |None            |PLEN      |
|...       |...      |...       |...                |...                                              |...             |...       |

Obter as informações da votação de código '2236213-74':

```pycon
>>> camara.votacoes(cod='2236213-74', serie='informacoes')

{'id': '2236213-74',
 'uri': 'https://dadosabertos.camara.leg.br/api/v2/votacoes/2236213-74',
 'data': '2020-05-08',
 'dataHoraRegistro': '2020-05-08T16:44:41',
 'siglaOrgao': 'PLEN',
 'uriOrgao': 'https://dadosabertos.camara.leg.br/api/v2/orgaos/180',
 'idOrgao': 180,
 'uriEvento': 'https://dadosabertos.camara.leg.br/api/v2/eventos/59601',
 'idEvento': 59601,
 'descricao': 'Aprovada a Emenda n° 12.',
 'aprovacao': 1,
 'descUltimaAberturaVotacao': 'Votação do DTQ 5: Bloco PP: destaque da emenda de Plenário nº 12 apresentada à MP 915/2019, com vistas a sua inclusão no texto. (161, II)',
 'dataHoraUltimaAberturaVotacao': '2020-05-08T15:47:05',
 'ultimaApresentacaoProposicao': {'dataHoraRegistro': '2020-04-30T13:14:53',
  'descricao': 'Apresentação do Projeto de Lei de Conversão n. 9/2020, pelo Deputado Rodrigo de Castro (PSDB-MG), que: "[EMENTA!]".',
  'uriProposicaoCitada': 'https://dadosabertos.camara.leg.br/api/v2/proposicoes/2250966'},
 'efeitosRegistrados': [],
 'objetosPossiveis': [{'id': 2250884,
   'uri': 'https://dadosabertos.camara.leg.br/api/v2/proposicoes/2250884',
   'siglaTipo': 'EMP',
   'codTipo': 873,
   'numero': 1,
   'ano': 2020,
   'ementa': ''},
  {'id': 2251874,
   'uri': 'https://dadosabertos.camara.leg.br/api/v2/proposicoes/2251874',
   'siglaTipo': 'ERD',
   'codTipo': 872,
   'numero': 1,
   'ano': 2020,
   'ementa': 'Emenda de redação à MPV 915/2019.'},
   ...
```

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**referencias**(*funcao, index=False*)

Obtém a lista de dados ou parâmetros utilizados no módulo `camara`.

##### *Parâmetros:*

- **funcao**: string

Lista de referências a ser buscada.

Pode ser um dos seguintes valores:

  - `codSituacaoDeputados`: As possíveis situações de exercício parlamentar de um deputado;
  - `siglaUF`: As siglas e nomes dos estados e do Distrito Federal;
  - `codSituacaoEvento`: As possíveis situações para eventos;
  - `codTipoEvento`: Os tipos de eventos realizados na Câmara;
  - `codSituacaoOrgao`: As situações em que órgãos podem se encontrar;
  - `codTipoOrgao`: Os tipos de órgãos que existem na Câmara;
  - `codSituacaoProposicao`: Os possíveis estados de tramitação de uma proposição;
  - `codTema`: Os vários tipos de temas existentes;
  - `codTipoAutor`: Entidades que podem ser autoras de proposições;
  - `codTipoTramitacao`: Os vários tipos de tramitação existentes;
  - `siglaTipo`: Os vários tipos de proposições existentes;
  - `situacoesDeputado`: As possíveis situações de exercício parlamentar de um deputado;
  - `situacoesEvento`: As possíveis situações para eventos;
  - `situacoesOrgao`: As situações em que órgãos podem se encontrar;
  - `situacoesProposicao`: Os possíveis estados de tramitação de uma proposição;
  - `tiposAutor`: Entidades que podem ser autoras de proposições;
  - `tiposEvento`: Os tipos de eventos realizados na Câmara;
  - `tiposOrgao`: Os tipos de órgãos que existem na Câmara;
  - `tiposProposicao`: Os vários tipos de proposições existentes;
  - `tiposTramitacao`: Os vários tipos de tramitação existentes;
  - `uf`: As siglas e nomes dos estados e do Distrito Federal.

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id da referência como index do DataFrame. Caso omitido, assume o valor `False`.

##### *Retorna:*

- **pandas.DataFrame**, contendo identificados e descrições da função buscada.

##### *Exemplos:*

Obter a lista de unidades da federação:

```pycon
>>> camara.referencias('uf')
```

|   |cod|descricao|nome     |sigla|
|:--|--:|--------:|--------:|----:|
|0  |6  |         |ACRE     |AC   |
|1  |14 |         |ALAGOAS  |AL   |
|2  |4  |         |AMAZONAS |AM   |
|3  |2  |         |AMAPÁ    |AP   |
|4  |16 |         |BAHIA    |BA   |
|...|...|...      |...      |...  |

Obter a lista de tipos de autores, colocando o código do tipo como índice do DataFrame:

```pycon
>>> camara.referencias('codTipoAutor', index=True)
```

|cod|descricao|nome                             |sigla|
|:--|--------:|--------------------------------:|----:|
|1  |         |COMISSÃO DIRETORA                |     |
|2  |         |COMISSÃO PERMANENTE              |     |
|3  |         |COMISSÃO ESPECIAL                |     |
|4  |         |COMISSÃO PARLAMENTAR DE INQUÉRITO|     |
|5  |         |COMISSÃO EXTERNA                 |     |
|...|...      |...                              |...  |

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

### def DadosAbertosBrasil.camara.**filtrar_deputados**(*sexo=None, uf=None, partido=None, contendo=None, excluindo=None, index=False*)

Obtém a lista de deputados em atividade parlamentar, com filtros.

Essa função será depreciada e integrada a função `camara.deputados`.

##### *Parâmetros:*

- **sexo**: (Opcional) `M` ou `F`

Filtre deputados por sexo masculino (`M`) ou feminino (`F`).

- **uf**: (Opcional) string

Filtre deputados por unidade da federação. Esse campo deve ser a sigla de duas letras maiúsculas que representa a UF.

- **partido**: (Opcional) string

Filtre deputados por partido polítido. Esse campo deve ser a sigla do partido.

- **contendo**: (Opcional)

Selecione deputados cujo nome contenha essa string.

- **excluindo**: (Opcional)

Remova deputados cujo nome contenha essa string.

- **index:** (Opcional) `True` ou `False`.

`True` para definir o id do(a) deputado(a) como index do DataFrame. Caso omitido, assume o valor `False`.

Esse campo é ignorado caso um id seja fornecido no campo `cod`.

##### *Retorna:*

- **pandas.DataFrame**, contendo uma lista filtrada de deputados. Cada row é um deputado e as columns são o nome, partido, estado, e-mail, legislatura atual e a URL da foto no site da câmara.

##### *Exemplos:*

Obter a lista de deputados do partido MDB, de Santa Catarina e sexo masculino:

```pycon
>>> camara.filtrar_deputados(sexo='M', partido='MDB', uf='SC')
```

|  |email                                   |id    |idLegislatura|nome                    |siglaPartido|siglaUf|urlFoto                                           |
|:-|---------------------------------------:|-----:|------------:|-----------------------:|-----------:|------:|-------------------------------------------------:|
|0 |dep.carloschiodini@camara.leg.br        |204361|56           |Carlos Chiodini         |MDB         |SC     |https://www.camara.leg.br/internet/deputado/ba... |
|1 |dep.celsomaldaner@camara.leg.br         |141405|56           |Celso Maldaner          |MDB         |SC     |https://www.camara.leg.br/internet/deputado/ba... |
|2 |dep.rogeriopeninhamendonca@camara.leg.br|160651|56           |Rogério Peninha Mendonça|MDB         |SC     |https://www.camara.leg.br/internet/deputado/ba... |

Obter a lista de deputados contendo `Campos` no nome, porém não contendo `Jefferson`. Colocar o código do deputado como index do DataFrame:

```pycon
>>> camara.filtrar_deputados(contendo='Campos', excluindo='Jefferson', index=True)
```

|id    |email                        |idLegislatura|nome          |siglaPartido|siglaUf|urlFoto                                           |
|:-----|----------------------------:|------------:|-------------:|-----------:|------:|-------------------------------------------------:|
|74366 |dep.joaocampos@camara.leg.br |56           |João Campos   |REPUBLICANOS|GO     |https://www.camara.leg.br/internet/deputado/ba... |
|204429|dep.joaohcampos@camara.leg.br|56           |João H. Campos|PSB         |PE     |https://www.camara.leg.br/internet/deputado/ba... |

##### *Documentação da API original:*

https://dadosabertos.camara.leg.br/swagger/api.html

---

# DadosAbertosBrasil.**favoritos**

Algumas funções selecionadas que não fazer parte dos módulos principais.

- favoritos.[moedas](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilfavoritosmoedas)
- favoritos.[cambio](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilfavoritoscambiomoedasusd-data_inicial01-01-2000-data_finalnone-indexfalse)
- favoritos.[ipca](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilfavoritosipcaindexfalse)
- favoritos.[catalogo](https://github.com/GusFurtado/DadosAbertosBrasil#def-dadosabertosbrasilfavoritoscatalogo)

Importe o módulo com `from DadosAbertosBrasil import favoritos`

---

### def DadosAbertosBrasil.favoritos.**moedas**()

Nomes e símbolos das principais moedas internacionais.

##### *Parâmetros:*

- **Nenhum**

##### *Retorna:*

- **pandas.DataFrame**, onde cada row é uma moeda e as três columns são o nome completo, a sigla de três letras e o tipo da moeda.

  - Tipo A: Moeda cuja paridade é expressa em quantidade de moeda por uma unidade de dólar.
  - Tipo B: Moeda cuja paridade é expressa em quantidade de dólar, por uma unidade de moeda.

##### *Exemplos:*

Obtém a lista das principais moedas:

```pycon
>>> favoritos.moedas()
```

|  |Nome                    |Símbolo|Tipo|
|:-|-----------------------:|------:|---:|
|0 |Dólar australiano       |AUD    |B   |
|1 |Dólar canadense         |CAD    |A   |
|2 |Franco suíço            |CHF    |A   |
|3 |Coroa dinamarquesa      |DKK    |A   |
|4 |Euro                    |EUR    |B   |
|5 |Libra Esterlina         |GBP    |B   |
|6 |Iene                    |JPY    |A   |
|7 |Coroa norueguesa        |NOK    |A   |
|8 |Coroa sueca             |SEK    |A   |
|9 |Dólar dos Estados Unidos|USD    |A   |

##### *Documentação da API original:*

https://dadosabertos.bcb.gov.br/dataset/taxas-de-cambio-todos-os-boletins-diarios/resource/9d07b9dc-c2bc-47ca-af92-10b18bcd0d69?inner_span=True

---

### def DadosAbertosBrasil.favoritos.**cambio**(*moedas='USD', data_inicial='01-01-2000', data_final=None, index=False*)

Obtém as taxas de câmbio das principais moedas internacionais por período.

##### *Parâmetros:*

- **moedas:** (Opcional) string ou lista de strings

Moeda(s) que se deseja pesquisar.

Assume `'USD'` (dólar americano) como valor padrão.

As siglas das moedas são as mesmas da consulta `favoritos.moedas()`.

- **data_inicial:** (Opcional) string no formato `MM-DD-AAAA`

Data inicial da consulta.

Assume `01-01-2000` como valor padrão.

- **data_final:** (Opcional) string no formato `MM-DD-AAAA`

Data final da consulta.

Caso valor seja omitido (`None`), a data final da consulta será `datetime.datetime.today()` (a data do hoje, segundo o sistema).

- **index:** (Opcional) `True` ou `False`.

`True` para definir a data da cotação como index do DataFrame. Caso omitido, assume o valor `False`.

##### *Retorna:*

- **pandas.DataFrame**, onde cada row é um valor da cotação em um datetime específico e cada column é uma moeda consultada.

##### *Exemplos:*

Pesquisar pela cotação do euro a partir de 01/01/2020 até o dia de hoje:

```pycon
>>> favoritos.cambio('EUR', data_inicial='01-01-2020')
```

|   |Data                   |EUR   |
|:--|----------------------:|-----:|
|0  |2020-01-02 13:11:10.762|4.5051|
|1  |2020-01-03 13:06:22.606|4.5247|
|2  |2020-01-06 13:03:22.271|4.5384|
|3  |2020-01-07 13:06:14.601|4.5513|
|4  |2020-01-08 13:03:56.075|4.5235|
|...|...                    |...   |

Pesquisar as cotações do dólar americano e do dólar canadense do dia 15/01/2020 até o dia 20/01/2020, usando a data como index do DataFrame:

```pycon
>>> favoritos.cambio(['USD', 'CAD'], data_inicial='01-15-2020', data_final='01-20-2020', index=True)
```

|Data      |USD   |CAD   |
|:---------|-----:|-----:|
|2020-01-15|4.1622|3.1906|
|2020-01-16|4.1726|3.1996|
|2020-01-17|4.1837|3.2044|
|2020-01-20|4.1829|3.2036|

##### *Documentação da API original:*

https://dadosabertos.bcb.gov.br/dataset/taxas-de-cambio-todos-os-boletins-diarios/resource/b31299d9-7fe6-45ca-ac88-a03273ff280f?inner_span=True

---

### def DadosAbertosBrasil.favoritos.**ipca**(*index=False*)

Obtém o valor mensal do índice IPCA, a partir de Janeiro de 1992.

Apesar do que o índice IPCA também pode ser obtido nos módulos `DadosAbertosBrasil.ibge` e `DadosAbertosBrasil.ipea`, esta função obtem o índice através da API do Banco Central do Brasil e permite uma consulta simples sem necessidade de especificar outros parâmetros.

##### *Parâmetros:*

- **index:** (Opcional) `True` ou `False`.

`True` para definir a data como index do DataFrame. Caso omitido, assume o valor `False`.

##### *Retorna:*

- **pandas.DataFrame**, onde cada row é uma data de referência e a column principal é o valor do índice IPCA em relação àquele mês.

##### *Exemplos:*

Captura o índice IPCA mensal do Banco Central:

```pycon
>>> favoritos.ipca()
```

|   |Data      |IPCA Mensal|
|:--|---------:|----------:|
|0  |1992-01-01|26.18      |
|1  |1992-01-02|22.40      |
|2  |1992-01-03|21.25      |
|3  |1992-01-04|18.96      |
|4  |1992-01-05|25.52      |
|...|...       |...        |

##### *Documentação da API original:*

https://dadosabertos.bcb.gov.br/dataset/4448-indice-de-precos-ao-consumidor-amplo-ipca---nao-comercializaveis

---

### def DadosAbertosBrasil.favoritos.**catalogo**()

Obtém o catálogo de iniciativas oficiais de dados abertos no Brasil

##### *Parâmetros:*

- **Nenhum**

##### *Retorna:*

- **pandas.DataFrame**, onde cada row é uma API de dados abertos no Brasil e as columns são o título, a URL, o município, a UF, a esfera (Estadual, Municipal ou Federal), o poder (Executivo ou Legislativo) e a solução (CKAN, Interna ou ArcGIS) da API.

##### *Exemplos:*

Obtém o catalogo de iniciativas de dados abertos no Brasil:

```pycon
>>> favoritos.catalogo()
```

|   |Título                        |URL                                               |Município|UF |Esfera   |Poder      |Solução|
|:--|-----------------------------:|-------------------------------------------------:|--------:|--:|--------:|----------:|------:|
|0  |Alagoas em dados e informações|http://dados.al.gov.br/                           |NaN      |AL |Estadual |Executivo  |CKAN   |
|1  |Fortaleza Dados Abertos       |http://dados.fortaleza.ce.gov.br/                 |Fortaleza|CE |Municipal|Executivo  |CKAN   |
|2  |Dados abertos – TCM-CE        |http://api.tcm.ce.gov.br/                         |NaN      |CE |Estadual |Legislativo|Interna|
|3  |Dados abertos Distrito Federal|http://dados.df.gov.br/                           |NaN      |DF |Estadual |Executivo  |CKAN   |
|4  |Dados abertos – Governo do ES |https://transparencia.es.gov.br/DadosAbertos/B... |NaN      |ES |Estadual |Executivo  |Interna|
|...|...                           |...                                               |...      |...|...      |...        |...    |

##### *Documentação da API original:*

https://github.com/dadosgovbr/catalogos-dados-brasil

---

# Em breve...

Nossos próximos passos serão:
- Módulo `senado`, similar ao módulo `camara`. Será necessário adicionar um package `xml`;
- Adição de parâmetros de busca para dados históricos no módulo `camara`. Atualmente só são listados os dados mais recentes;
- Expansão das funções de filtro e busca de séries, para facilitar encontrar a série desejada;
- Integrar as funções `camara.deputados` e `camara.filtrar_deputados` em uma só através da adição de novos argumentos na primeira função;
- Padronização dos nomes das colunas dos DataFrame para melhor interpretação do usuário e integração entre módulos;
- Adição constante de novas funções no módulo `favoritos`.

---