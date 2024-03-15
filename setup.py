from setuptools import setup
from os import path


def get_long_description():
    """Extrai o texto do `README.md` para o `long_description`.

    Returns
    -------
    str
        Descrição do pacote.

    """

    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, "README.md"), encoding="utf-8") as file:
        return file.read()


def get_version():
    """Obtém o número da versão do pacote salvo no `__init__.py`.

    Returns
    -------
    str
        Número da versão do pacote.

    """

    with open("DadosAbertosBrasil/__init__.py") as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("__version__"):
                return line.split('"')[1]
        raise RuntimeError("Versão não encontrada.")


setup(
    name="DadosAbertosBrasil",
    packages=[
        "DadosAbertosBrasil",
        "DadosAbertosBrasil._utils",
        "DadosAbertosBrasil._ibge",
    ],
    version=get_version(),
    license="MIT",
    description="Pacote Python para acesso a dados abertos e APIs do governo brasileiro.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Gustavo Furtado",
    author_email="gustavofurtado2@gmail.com",
    url="https://github.com/GusFurtado/DadosAbertosBrasil",
    download_url=f"https://github.com/GusFurtado/DadosAbertosBrasil/archive/{get_version()}.tar.gz",
    keywords=[
        "brasil",
        "ibge",
        "ipea",
        "ipeadata",
        "camara",
        "deputados",
        "senado",
        "senadores",
        "bacen",
        "bcb",
        "bancocentral",
        "dadosabertos",
        "dadosgovbr",
    ],
    install_requires=[
        "pandas",
        "requests",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Portuguese (Brazilian)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
