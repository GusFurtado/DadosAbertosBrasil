'''
Módulo de funções de suporte aos pacotes principais.
'''



from datetime import date, datetime
from typing import Union



def parse_data(
        data: Union[date, str],
        modulo: str
    ) -> str:
    '''
    Padroniza o input de datas entre módulos.

    Parâmetros
    ----------
    data: datetime.date ou str
        Input a ser padronizado.
    modulo: str
        Módulo que o parser seja aplicado para selecionar a formatação
        adequada:
            - 'camara': API da Câmara dos Deputados;
            - 'senado': API do Senado Federal;
            - 'bacen': Consultas do Banco Central do Brasil.

    Atributos
    ---------
    str
        Data no formato adequado para o módulo escolhido.

    --------------------------------------------------------------------------
    '''
    data = str(data)
    if modulo == 'camara':
        return data
    elif modulo == 'senado':
        return data.replace('-', '')
    elif modulo == 'bacen':
        return f'{data[5:7]}-{data[8:10]}-{data[:4]}'




def parse_uf(uf:str) -> str:
    '''
    Converte os nomes dos estados em siglas padrões.
    Suporta abreviaturas, acentuação e case sensibility.

    Parametros
    ----------
    uf: str
        Nome ou sigla da UF.

    Retorna
    -------
    str
        String de dois caracteres maiúsculos que representam a sigla da
        Unidade Federativa desejada.
    '''
    
    UFS = {
        
        ('BR', 'BRASIL'): 'BR',
        
        # Região Norte
        ('AC', 'ACRE'): 'AC',
        ('AM', 'AMAZONAS'): 'AM',
        ('AP', 'AMAPA', 'AMAPÁ'): 'AP',
        ('PA', 'PARA', 'PARÁ'): 'PA',
        ('RO', 'RONDONIA', 'RONDÔNIA'): 'RO',
        ('RR', 'RORAIMA'): 'RR',
        ('TO', 'TOCANTINS'): 'TO',
        
        # Região Nordeste
        ('AL', 'ALAGOAS'): 'AL',
        ('BA', 'BAHIA'): 'BA',
        ('CE', 'CEARA', 'CEARÁ'): 'CE',
        ('MA', 'MARANHAO', 'MARANHÃO'): 'MA',
        ('PB', 'PARAIBA', 'PARAÍBA'): 'PB',
        ('PE', 'PERNAMBUCO'): 'PE',
        ('PI', 'PIAUI', 'PIAUÍ'): 'PI',
        ('RN', 'RIOGRANDEDONORTE'): 'RN',
        ('SE', 'SERGIPE'): 'SE',
        
        # Região Centro-Oeste
        ('DF', 'DISTRITOFEDERAL'): 'DF',
        ('GO', 'GOIAS', 'GOIÁS'): 'GO',
        ('MT', 'MATOGROSSO'): 'MT',
        ('MS', 'MATOGROSSODOSUL'): 'MS',
        
        # Região Sudeste
        ('ES', 'ESPIRITOSANTO', 'ESPÍRITOSANTO'): 'ES',
        ('MG', 'MINASGERAIS', 'MINAS'): 'MG',
        ('RJ', 'RIODEJANEIRO', 'RIO'): 'RJ',
        ('SP', 'SAOPAULO', 'SÃOPAULO'): 'SP',
        
        # Região Sul
        ('PR', 'PARANA', 'PARANÁ'): 'PR',
        ('RS', 'RIOGRANDEDOSUL'): 'RS',
        ('SC', 'SANTACATARINA'): 'SC',
    
    }
    
    mapping = {}
    for key in UFS:
        for value in key:
            mapping.update({value: UFS[key]})
    
    s = uf.upper().replace(' ', '')
    
    try:
        return mapping[s]
    except:
        raise TypeError('UF não encontrada.')



def parse_localidade(
        localidade: str,
        brasil = 1,
        on_error = 'raise'
    ) -> str:
    '''
    Verifica se o código da localidade é válido.

    Parametros
    ----------
    localidade: str ou int
        Código da localidade que se deseja verificar.
        Caso localidade == None, retorna o valor padrão do Brasil.
    brasil: default = 1
        Valor padrão para o Brasil.
    on_error: str (default = 'raise')
        - 'raise': Gera um erro quando o valor não for válido;
        - 'brasil': Retorna o valor Brasil quando o valor não for válido.

    Retorna
    -------
    str ou int
        Valor da localidade validado.
    '''

    if localidade is None:
        return brasil

    elif isinstance(localidade, int):
        return localidade

    elif isinstance(localidade, str):
        if localidade.isnumeric():
            return localidade

    if on_error == 'raise':
        raise AttributeError('O código da localidade não está em um formato numérico.')
    elif on_error == 'brasil':
        return brasil
    else:
        raise ValueError(
            "Valor incorreto para o argumento 'on_error':\n"
            "  - 'raise': Gera um erro quando o valor não for válido;\n"
            "  - 'brasil': Retorna o valor Brasil quando o valor não for válido."
        )