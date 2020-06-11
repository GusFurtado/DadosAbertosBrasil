from distutils.core import setup
setup(
  name = 'DadosAbertosBrasil',
  packages = ['DadosAbertosBrasil'],
  version = '0.1',
  license='MIT',
  description = 'Pacote Python para acesso a dados abertos e APIs do governo brasileiro.',
  author = 'Gustavo Furtado',
  author_email = 'gustavofurtado2@gmail.com',
  url = 'https://github.com/GusFurtado/DadosAbertosBrasil',
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['pandas', 'api', 'brasil', 'ibge', 'ipea', 'camara', 'requests', 'dados_abertos', 'dadosgovbr'],
  install_requires=[
          'pandas',
          'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)