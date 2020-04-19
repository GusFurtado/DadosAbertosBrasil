# Dados Abertos Brasil

## **Documentação incompleta**

Dados Abertos Brasil é uma iniciativa para facilitar o acesso a dados abertos e APIs do governo brasileiro.

É um pacote open-source para Python e Pandas e a forma mais simples de acessar dados de instituições como IGBE , IPEA , etc.

Atualmente o pacote Dados Abertos Brasil possui quatro módulos:

1. DadosAbertosBrasil.**ibge**
2. DadosAbertosBrasil.**ipea**
3. DadosAbertosBrasil.**camara**
4. DadosAbertosBrasil.**favoritos**

---

# DadosAbertosBrasil.**ibge**

Módulo para captura dos dados abertos das APIs do IBGE.

- **Requer:** pandas e requests.

## def DadosAbertosBrasil.ibge.**nomes**(*nomes, sexo=None, localidade=None*)

Obtém a frequência de nascimentos por década para o(s) nome(s) consultado(s).

### Parâmetros:

- **nomes:** string ou lista de strings

Nome(s) que se deseja pesquisar

- **sexo:** (Opcional) 'M' ou 'F'

'M' se deseja pesquisar apenas por ocorrências do sexo masculino e 'F' se deseja pesquisar apenas por ocorrências do sexo feminino.

- **localidade:** (Opcional) int

Código da localidade que se deseja limitar a pesquisa.

Utilizar a função *DadosAbertosBrasil.ibge.localidades()* para consultar os códigos das localidades.

### Retorna:

- **pandas.DataFrame**, onde cada column é um dos nomes pesquisados e cada row é uma década.

### Exemplos:

Pesquisar pela frequência de nascimento de Maria e Ana:

	>>> ibge.nomes(['Maria', 'Ana'])
		PERIODO		ANA		MARIA
	0  	1930   		33395   336477
	1  	1930,1940	56160	749053
	2  	1940,1950  	101259  1487042
	3  	1950,1960  	183941  2476482
	4  	1960,1970  	292835  2495491
	5  	1970,1980  	421531  1616019
	6  	1980,1990  	529266  917968
	7  	1990,2000  	536302  544296
	8  	2000,2010  	935169  1111301

Pesquisar pela frequência de nascimentos de Maria no estado de São Paulo (código 35):

	>>> ibge.nomes('Maria', localidade=35)
		PERIODO 	MARIA
	0	1930   		65218
	1  	1930,1940  	150588
	2  	1940,1950  	313277
	3  	1950,1960  	541950
	4  	1960,1970  	487742
	5  	1970,1980  	252657
	6  	1980,1990  	105600
	7  	1990,2000	48444
	8  	2000,2010  	177756

### Documentação da API original:

https://servicodados.ibge.gov.br/api/docs/censos/nomes?versao=2#api-Nomes-nomeGet

---

## def DadosAbertosBrasil.ibge.**nomes_uf**(*nome*)

Obtém a frequência de nascimentos por UF para o nome consultado

### Parâmetros:

- **nome:** string

Nome que se deseja pesquisar

### Retorna:

- **pandas.DataFrame**, onde cada row é uma localidade (UF).

Contém três columns: Frequência de nascimento do nome pesquisado, população total da localidade e proporção de nascimentos por 100.000 habitantes.

Utilizar a função *DadosAbertosBrasil.ibge.localidades()* para consultar os códigos das localidades.

### Exemplos:

Pesquisar pela frequência de nascimento de Maria por UF:

	>>> ibge.nomes_uf('Maria')
				frequencia	populacao	proporcao
	localidade                                  
	11          72579    	1562409    	4645.33
	12          63172     	733559    	8611.71
	13          173034    	3483985    	4966.55
	14          20848     	450479    	4627.96
	15          472891    	7581051    	6237.80
	16          35298     	669526    	5272.09
	17          87040    	1383445    	6291.54
	21          574689    	6574789    	8740.80
	22          363139    	3118360   	11645.19
	23          967042    	8452381   	11441.06
	24          341940    	3168027   	10793.47
	25          423026    	3766528   	11231.19
	26          838534    	8796448    	9532.64
	27          321330    	3120494   	10297.41
	28          188619    	2068017    	9120.77
	29          766238   	14016906    5466.53
	31          1307650   	19597330    6672.59
	32          169081    	3514952    	4810.34
	33          752021   	15989929    4703.09
	35          2143232   	41262199    5194.18
	41          432175   	10444526    4137.81
	42          210558    	6248436    	3369.77
	43          322238   	10693929    3013.28
	50          100649    	2449024    	4109.76
	51          125984    	3035122    	4150.87
	52          314352    	6003788    	5235.89
	53          146770    	2570160    	5710.54

### Documentação da API original:

https://servicodados.ibge.gov.br/api/docs/censos/nomes?versao=2#api-Nomes-nomeGet

---

## def DadosAbertosBrasil.ibge.**nomes_ranking**(*decada=None, sexo=None, localidade=None*)

Obtém o ranking dos nomes segundo a frequência de nascimentos por década

### Parâmetros:

- **decada:** (Opcional) int

Década que se deseja limitar a pesquisa de nascimentos.

Deve estar no formato *AAAA*, sendo múltiplo de 10.

*Exemplos: 1930, 1980, 2000...*

- **sexo:** (Opcional) 'M' ou 'F'

'M' se deseja pesquisar apenas por ocorrências do sexo masculino e 'F' se deseja pesquisar apenas por ocorrências do sexo feminino.

- **localidade:** (Opcional) int

Código da localidade que se deseja limitar a pesquisa.

Utilizar a função *DadosAbertosBrasil.ibge.localidades()* para consultar os códigos das localidades.

### Retorna:

- **pandas.DataFrame**, com rows de 1 a 20 representando a posição no ranking.

Uma column para os nomes e uma para a frequência de nascimentos.

### Exemplos:

Pesquisar por nomes masculino com maior frequência de nascimentos no estado de São Paulo (código 35) na década de 1990:

	>>> ibge.nomes_ranking(decada=1990, sexo='M', localidade=35)
			 frequencia      nome
	ranking                      
	1             97066      JOSE
	2             86175   RODRIGO
	3             83805    RAFAEL
	4             64731     FABIO
	5             64642   LEANDRO
	6             61864    CARLOS
	7             61716     PAULO
	8             58724     TIAGO
	9             58472     ANDRE
	10            57261  ANDERSON
	11            55058  FERNANDO
	12            54797   MARCELO
	13            53907    MARCOS
	14            52614     BRUNO
	15            50907      JOAO
	16            48328    THIAGO
	17            46664    DANIEL
	18            46485   RICARDO
	19            45541     DIEGO
	20            38204   EDUARDO

### Documentação da API original:

https://servicodados.ibge.gov.br/api/docs/censos/nomes?versao=2#api-Ranking-rankingGet

---

## def DadosAbertosBrasil.ibge.**nomes_uf**(*nome*)

Obtém a frequência de nascimentos por UF para o nome consultado

### Parâmetros:

- **nome:** string

Nome que se deseja pesquisar

### Retorna:

- **pandas.DataFrame**, onde cada row é uma localidade (UF).

Contém três columns: Frequência de nascimento do nome pesquisado, população total da localidade e proporção de nascimentos por 100.000 habitantes.

Utilizar a função *DadosAbertosBrasil.ibge.localidades()* para consultar os códigos das localidades.

### Exemplos:

Pesquisar pela frequência de nascimento de Maria por UF:

	>>> ibge.nomes_uf('Maria')
				frequencia  populacao  proporcao
	localidade                                  
	11               72579    1562409    4645.33
	12               63172     733559    8611.71
	13              173034    3483985    4966.55
	14               20848     450479    4627.96
	15              472891    7581051    6237.80
	16               35298     669526    5272.09
	17               87040    1383445    6291.54
	21              574689    6574789    8740.80
	22              363139    3118360   11645.19
	23              967042    8452381   11441.06
	24              341940    3168027   10793.47
	25              423026    3766528   11231.19
	26              838534    8796448    9532.64
	27              321330    3120494   10297.41
	28              188619    2068017    9120.77
	29              766238   14016906    5466.53
	31             1307650   19597330    6672.59
	32              169081    3514952    4810.34
	33              752021   15989929    4703.09
	35             2143232   41262199    5194.18
	41              432175   10444526    4137.81
	42              210558    6248436    3369.77
	43              322238   10693929    3013.28
	50              100649    2449024    4109.76
	51              125984    3035122    4150.87
	52              314352    6003788    5235.89
	53              146770    2570160    5710.54

### Documentação da API original:

https://servicodados.ibge.gov.br/api/docs/censos/nomes?versao=2#api-Nomes-nomeGet

---

## def DadosAbertosBrasil.ibge.**localidades**()

Obtém o conjunto de distritos do Brasil.

### Parâmetros:

- Nenhum

### Retorna:

- **pandas.DataFrame**, contendo todos distritos, municípios, microrregiões, mesorregiões, UFs e regiões do Brasil.

### Exemplos:

Pesquisa completa por todos os distritos:

	>>> ibge.localidades()

### Documentação da API original:

https://servicodados.ibge.gov.br/api/docs/localidades?versao=1

---

## def DadosAbertosBrasil.ibge.**malha**(*localidade=''*)

Obtém a URL para a malha referente ao identificador da localidade.

### Parâmetros:

- **localidade:** (Opcional) int

Código da localidade que se deseja pesquisar. Caso omitido, assume o valor Brasil.

Utilizar a função *DadosAbertosBrasil.ibge.localidades()* para consultar os códigos das localidades.

### Retorna:

- **url** (string) para um arquivo .svg do mapa da região pesquisada.

### Exemplos:

Pesquisar pela malha referente a região Sudeste (código 3):

	>>> ibge.malha(3)
	'https://servicodados.ibge.gov.br/api/v2/malhas/3'
	
Pesquisar pela malha referente ao estado do Rio de Janeiro (código 33):

	>>> ibge.malha(33)
	'https://servicodados.ibge.gov.br/api/v2/malhas/33'

### Documentação da API original:

https://servicodados.ibge.gov.br/api/docs/malhas?versao=2

---

## def DadosAbertosBrasil.ibge.**populacao**(*projecao=None, localidade=None*)

Obtém a URL para a malha referente ao identificador da localidade.

### Parâmetros:

- **projecao:** (Opcional) 'populacao', 'nascimento' ou 'obito'.

Define que variável pesquisar. Se omitido, obtém um dictionary com todos os valores.

- **localidade:** (Opcional) int

Código da localidade que se deseja pesquisar. Caso omitido, assume o valor Brasil.

Utilizar a função *DadosAbertosBrasil.ibge.localidades()* para consultar os códigos das localidades.

### Retorna:

- **dict**, caso o campo 'projecao' seja omitido.
- **int**, contendo um valor estimado para população, nascimentos ou óbitos, caso o campo 'projecao' tenha um valor válido.

### Exemplos:

Pesquisar pela população total estimada do Brasil:

	>>> ibge.populacao(projecao='populacao')
	211406467
	
Pesquisar pela quantidade estimada de óbitos por ano no estado de São Paulo (código 35):

	>>> ibge.populacao(projecao='obito', localidade=35)
	45000
	
Pesquisar pelos dados de nascimento, óbitos e projeção populacional para o estado do Rio de Janeiro:

	>>> ibge.populacao(localidade=33)
	{'localidade': '33',
	 'horario': '19/04/2020 19:18:18',
	 'projecao': {'populacao': 17342454,
	  'periodoMedio': {'incrementoPopulacional': 317367,
	   'nascimento': 12000,
	   'obito': 45000}}}

### Documentação da API original:

https://servicodados.ibge.gov.br/api/docs/projecoes?versao=1
