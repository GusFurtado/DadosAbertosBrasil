import json
from bs4 import BeautifulSoup
import pandas as pd
import requests



# CONSTANTES

URL = r'https://pt.wikipedia.org/wiki/Lista_de_governadores_das_unidades_federativas_do_Brasil'

COLS = {
    'Unidade federativa': 'uf',
    'Governador.1': 'nome',
    'No cargo': 'periodo',
    'Partido': 'partido',
    'Mandato (ano da eleição)': 'ano_eleicao',
    'Cargo anterior': 'cargo_anterior',
    'Vice-governador': 'vice_governador'
}

MESES = {
    'janeiro': '01',
    'fevereiro': '02',
    'março': '03',
    'abril': '04',
    'maio': '05',
    'junho': '06',
    'julho': '07',
    'agosto': '08',
    'setembro': '09',
    'outubro': '10',
    'novembro': '11',
    'dezembro': '12'
}



# FUNÇÕES

def apply_periodo(texto:str) -> str:
    texto = texto.replace('º', '')
    texto = texto.split(' de ')
    dia = f'0{texto[0]}'[-2:]
    mes = MESES[texto[1].lower()]
    ano = texto[2][:4]
    return f'{ano}-{mes}-{dia}'

def apply_vice(x:str) -> str:
    if x.startswith('—'):
        return None
    else:
        return x.split('1')[0].split('[')[0].strip()



# REQUEST TABELA

r = requests.get(URL)
soup = BeautifulSoup(r.text)
table = soup.find_all('table')[0]
df = pd.read_html(str(table))[0]



# LIMPAR TABELA

df['Unidade federativa'] = df['Unidade federativa'].apply(lambda x: x.split('(')[0])

df = df[list(COLS.keys())]
df.rename(columns=COLS, inplace=True)
df = df.groupby('uf').last()

df['nome_completo'] = df.nome.apply(lambda x: x.split('(')[-1].split(')')[0])
df.nome = df.nome.apply(lambda x: x.split('(')[0].strip())

df['mandato_inicio'] = df.periodo.apply(lambda x: apply_periodo(x.split('–')[0]))
df['mandato_fim'] = df.periodo.apply(lambda x: apply_periodo(x.split('–')[1]))

df['partido_sigla'] = df.partido.apply(lambda x: x.split('(')[-1].split(')')[0])
df.partido = df.partido.apply(lambda x: x.split('(')[0].strip())

df.ano_eleicao = df.ano_eleicao.apply(lambda x: x.split('(')[-1].split(')')[0])
df.ano_eleicao = df.ano_eleicao.apply(lambda x: None if x=='1' else int(x))

df.vice_governador = df.vice_governador.apply(apply_vice)

df.cargo_anterior = df.cargo_anterior.str.replace('(', ' (')

df = df[[
    'nome',
    'nome_completo',
    'ano_eleicao',
    'mandato_inicio',
    'mandato_fim',
    'partido',
    'partido_sigla',
    'cargo_anterior',
    'vice_governador'
]]



# SALVAR JSON

data = df.to_json(orient='index')
with open('data/governadores.json', 'w') as f:
    json.dump(data, f)
