from distutils.core import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'DadosAbertosBrasil',
  packages = ['DadosAbertosBrasil'],
  version = '0.1.1',
  license='MIT',
  description = 'Pacote Python para acesso a dados abertos e APIs do governo brasileiro.',
  long_description='''

**Dados Abertos Brasil** é uma iniciativa para facilitar o acesso a dados abertos e APIs do governo brasileiro.

É um pacote open-source para **Python** e **Pandas** e a forma mais simples de acessar dados de instituições como **IGBE**, **IPEA**, etc.

Atualmente o pacote Dados Abertos Brasil possui seis módulos em desenvolvimento:

- DadosAbertosBrasil.**[ibge](https://www.gustavofurtado.com/doc.html#SessaoIBGE)**
- DadosAbertosBrasil.**[ipea](https://www.gustavofurtado.com/doc.html#SessaoIPEA)**
- DadosAbertosBrasil.**[camara](https://www.gustavofurtado.com/doc.html#SessaoCamara)**
- DadosAbertosBrasil.**senado**
- DadosAbertosBrasil.**tse**
- DadosAbertosBrasil.**[favoritos](https://www.gustavofurtado.com/doc.html#SessaoFavoritos)**

### Sobre
- **[Página Oficial](https://www.gustavofurtado.com/dab.html)**
- **[Documentação](https://www.gustavofurtado.com/doc.html)**

### Instalação
```
pip install DadosAbertosBrasil
```

### Dependências
- **[pandas](https://pandas.pydata.org/)**
- **[requests](https://requests.readthedocs.io/en/master/)**

### Licença
- **[MIT](LICENSE)**

### Próximos Passos
- Módulo `senado`, similar ao módulo `camara`. Será necessário adicionar um package `xml`;
- Módulo `tse`, que utilizará o package `zipfile` para extrair os arquivos `.csv` do repositório do TSE;
- Substituição das funções do módulo `camara` por classes. Atualmente as funções capturam apenas dados dos últimos seis meses e da última legislatura;
- Expansão das funções de filtro e busca de séries, para facilitar encontrar a série desejada;
- Padronização dos nomes das colunas dos DataFrame para melhor interpretação do usuário e integração entre módulos;
- Adição constante de novas funções no módulo `favoritos`.

  ''',
  long_description_content_type='text/markdown', 
  author = 'Gustavo Furtado',
  author_email = 'gustavofurtado2@gmail.com',
  url = 'https://github.com/GusFurtado/DadosAbertosBrasil',
  download_url = 'https://github.com/GusFurtado/DadosAbertosBrasil/archive/0.1.1.tar.gz',
  keywords = ['brasil', 'ibge', 'ipea', 'camara', 'deputados', 'senado', 'senadores', 'tse', 'dados_abertos', 'dadosgovbr'],
  install_requires=[
          'pandas',
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Financial and Insurance Industry',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: Portuguese (Brazilian)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)