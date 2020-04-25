# Dados Abertos Brasil

### **(Documentação incompleta)**

Dados Abertos Brasil é uma iniciativa para facilitar o acesso a dados abertos e APIs do governo brasileiro.

É um pacote open-source para Python e Pandas e a forma mais simples de acessar dados de instituições como IGBE, IPEA , etc.

Atualmente o pacote Dados Abertos Brasil possui quatro módulos:

- DadosAbertosBrasil.[ibge](https://github.com/GusFurtado/DadosAbertosBrasil#dadosabertosbrasilibge)
- DadosAbertosBrasil.**ipea**
- DadosAbertosBrasil.**camara**
- DadosAbertosBrasil.**favoritos**

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
  - ibge.[Agregados]()
  - ibge.[Metadados]()
  - ibge.[referencias]()
  - ibge.[Sidra]()

### def DadosAbertosBrasil.ibge.**nomes**(*nomes, sexo=None, localidade=None*)

Obtém a frequência de nascimentos por década para o(s) nome(s) consultado(s).

##### *Parâmetros:*

- **nomes:** string ou lista de strings

Nome(s) que se deseja pesquisar

- **sexo:** (Opcional) 'M' ou 'F'

'M' se deseja pesquisar apenas por ocorrências do sexo masculino e 'F' se deseja pesquisar apenas por ocorrências do sexo feminino.

- **localidade:** (Opcional) int

Código da localidade que se deseja limitar a pesquisa.

Utilizar a função `DadosAbertosBrasil.ibge.localidades()` para consultar os códigos das localidades.

##### *Retorna:*

- **pandas.DataFrame**, onde cada column é um dos nomes pesquisados e cada row é uma década.

##### *Exemplos:*

Pesquisar pela frequência de nascimento de Maria e Ana:

```pycon
>>> ibge.nomes(['Maria', 'Ana'])
	PERIODO	      ANA    MARIA
0  	1930   		33395   336477
1  	1930,1940	56160   749053
2  	1940,1950  101259  1487042
3  	1950,1960  183941  2476482
4  	1960,1970  292835  2495491
5  	1970,1980  421531  1616019
6  	1980,1990  529266   917968
7  	1990,2000  536302   544296
8  	2000,2010  935169  1111301
```

Pesquisar pela frequência de nascimentos de Maria no estado de São Paulo (código 35):

```pycon
>>> ibge.nomes('Maria', localidade=35)
	PERIODO     MARIA
0	1930   	    65218
1  	1930,1940  150588
2  	1940,1950  313277
3  	1950,1960  541950
4  	1960,1970  487742
5  	1970,1980  252657
6  	1980,1990  105600
7  	1990,2000   48444
8  	2000,2010  177756
```

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

Utilizar a função `DadosAbertosBrasil.ibge.localidades()` para consultar os códigos das localidades.

##### *Exemplos:*

Pesquisar pela frequência de nascimento de Maria por UF:

```pycon
>>> ibge.nomes_uf('Maria')
           frequencia  populacao  proporcao
localidade                                  
11              72579    1562409    4645.33
12              63172     733559    8611.71
13             173034    3483985   	4966.55
14              20848     450479   	4627.96
15             472891    7581051   	6237.80
...               ...        ...        ...
```

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

- **sexo:** (Opcional) 'M' ou 'F'

'M' se deseja pesquisar apenas por ocorrências do sexo masculino e 'F' se deseja pesquisar apenas por ocorrências do sexo feminino.

- **localidade:** (Opcional) int

Código da localidade que se deseja limitar a pesquisa.

Utilizar a função `DadosAbertosBrasil.ibge.localidades()` para consultar os códigos das localidades.

##### *Retorna:*

- **pandas.DataFrame**, com rows de 1 a 20 representando a posição no ranking.

Uma column para os nomes e uma para a frequência de nascimentos.

##### *Exemplos:*

Pesquisar por nomes masculino com maior frequência de nascimentos no estado de São Paulo (código 35) na década de 1990:

```pycon
>>> ibge.nomes_ranking(decada=1990, sexo='M', localidade=35)
		 frequencia      nome
ranking                      
1             97066      JOSE
2             86175   RODRIGO
3             83805    RAFAEL
4             64731     FABIO
5             64642   LEANDRO
...             ...       ...
```

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

Utilizar a função `DadosAbertosBrasil.ibge.localidades()` para consultar os códigos das localidades.

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

- **projecao:** (Opcional) 'populacao', 'nascimento' ou 'obito'.

Define que variável pesquisar. Se omitido, obtém um dictionary com todos os valores.

- **localidade:** (Opcional) int

Código da localidade que se deseja pesquisar. Caso omitido, assume o valor Brasil.

Utilizar a função `DadosAbertosBrasil.ibge.localidades()` para consultar os códigos das localidades.

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

# **SIDRA**

O SIDRA (Sistema IBGE de Recuperação Automática) permite consultar todo catalogo de dados armazenados no Banco de Tabelas Estatísticas do IBGE.

Por ser um sistema completo e robusto, foram desenvolvidos os seguintes objetos para facilitar a consulta:

- ibge.[Agregados]()
- ibge.[Metadados]()
- ibge.[referencias]()
- ibge.[Sidra]()

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

- **index:** (Opcional) True ou False.

True para definir o id do agregado como index do DataFrame. Caso omitido, assume o valor False.

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
                                                 agregado_nome  pesquisa_id                pesquisa_nome  
agregado_id                                                                  
1            Receita operacional líquida e subvenções das e...           PY   Pesquisa Anual de Serviços  
2            População ocupada de 15 anos e mais por setor ...           PE   Pesquisa Mensal de Emprego  
3            População ocupada de 15 anos e mais por posiçã...           PE   Pesquisa Mensal de Emprego  
4            Taxa de desemprego aberto - semana por sexo (s...           PE   Pesquisa Mensal de Emprego  
5            Taxa de desemprego aberto - semana por setor d...           PE   Pesquisa Mensal de Emprego
...                                                        ...          ...                          ...
```

Obter lista de pesquisas realizadas:

```pycon
>>> agreg = ibge.Agregados()
>>> agreg.pesquisas
   pesquisa_id 	                           pesquisa_nome
0 	        CL 	            Cadastro Central de Empresas
1 	        CA 	                      Censo Agropecuário
2 	        ME 	Censo Comum do Mercosul, Bolívia e Chile
3 	        CD 	                       Censo Demográfico
4 	        CM 	                   Contagem da População
...        ...                                       ...
```

Obter agregados da Pesquisa Mensal de Empregos (PE) contendo a palavra 'desemprego' no título:

```pycon
>>> agreg = ibge.Agregados()
>>> agreg.filtrar(pesquisa='PE', contendo='desemprego')
	                                              agregado_nome  pesquisa_id               pesquisa_nome
agregado_id 			
4 	          Taxa de desemprego aberto - semana por sexo (s...           PE  Pesquisa Mensal de Emprego
5 	          Taxa de desemprego aberto - semana por setor d...           PE  Pesquisa Mensal de Emprego
13 	          Taxa de desemprego aberto - semana (série ence...           PE  Pesquisa Mensal de Emprego
14 	          Taxa de desemprego aberto - 30 dias (série enc...           PE  Pesquisa Mensal de Emprego
```

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

```
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

  - 'A' ou 'assuntos' para obter a base de referências de assuntos;
  - 'C' ou 'classificacoes' para obter a base de referências de classificações;
  - 'P' ou 'periodos' para obter a base de referências de períodos;
  - 'E' ou 'periodicidades' para obter a base de referências de periodicidades;
  - 'V' ou 'variaveis' para obter a base de referências de variáveis;
  - 'N', 'T', 'niveis_geograficos' ou 'territorios' para obter a base de referências de níveis geográficos;

- **index:** (Opcional) True ou False.

True para definir o id da referência como index do DataFrame. Caso omitido, assume o valor False.

##### *Retorna:*

- **DataFrame**, contendo todos as referências e códigos.

##### *Exemplos:*

Pesquisar pela base de referências de periodicidades ('E'):

```pycon
>>> ibge.referencias('E')
 	id 	 literal
0 	P1 	 Anual
1 	P8 	 Semestral
2 	P9 	 Trimestral
3 	P5 	 Mensal
4 	P13  Trimestral móvel
```
	
Pesquisar pela base de referências de assuntos ('A'), utilizando o id do assunto como index do DataFrame:

```pycon
>>> ibge.referencias('A', index=True)
 	 literal
id 	
148  Abastecimento de água
70   Abate de animais
110  Acesso a esgotamento sanitário
147  Acesso à internet
107  Acesso a serviço de coleta de lixo doméstico
146  Acesso a serviços de telefonia
...  ...
```

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

```
# Importar módulo IBGE:
>>> from DadosAbertosBrasil import ibge

# Encontrar o agregado desejado:
>>> agreg = ibge.Agregados()
>>> agreg.filtrar(contendo='Óbitos fetais')

                                                 agregado_nome  pesquisa_id                   pesquisa_nome
agregado_id 			
2990         Óbitos fetais, ocorridos no ano, por mês do re...           RC  Estatísticas do Registro Civil
2991         Óbitos fetais, ocorridos no ano, por mês do re...           RC  Estatísticas do Registro Civil
2992         Óbitos fetais, ocorridos no ano, por mês do re...           RC  Estatísticas do Registro Civil

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

```
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

```
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
