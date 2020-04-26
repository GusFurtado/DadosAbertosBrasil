import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='Dados Abertos Brasil',
    version="0.0.1",
    author='Gustavo Furtado da Silva',
    author_email='gustavofurtado2@gmail.com',
    description='Pacote Python para acesso a dados abertos e APIs do governo brasileiro.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GusFurtado/DadosAbertosBrasil",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)