'''
Funções para padronização de parâmetros entre os módulos.
'''



from datetime import date
from typing import Union

from . import errors



def data(
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



def uf(
        uf: str,
        extintos: bool = False
    ) -> str:
    '''
    Converte os nomes dos estados em siglas padrões.
    Suporta abreviaturas, acentuação e case sensibility.

    Parametros
    ----------
    uf: str
        Nome ou sigla da UF.
    extintos: bool (default=None)
        !!! AINDA NÃO IMPLEMENTADO !!!
        Permitir as UFs extintas:
            - 20: Fernando de Noronha / FN
            - 34: Guanabara / GB

    Retorna
    -------
    str
        String de dois caracteres maiúsculos que representam a sigla da
        Unidade Federativa desejada.

    --------------------------------------------------------------------------
    '''

    UFS = {
        '1': 'BR',
        '11': 'RO',
        '12': 'AC',
        '13': 'AM',
        '14': 'RR',
        '15': 'PA',
        '16': 'AP',
        '17': 'TO',
        '21': 'MA',
        '22': 'PI',
        '23': 'CE',
        '24': 'RN',
        '25': 'PB',
        '26': 'PE',
        '27': 'AL',
        '28': 'SE',
        '29': 'BA',
        '31': 'MG',
        '32': 'ES',
        '33': 'RJ',
        '35': 'SP',
        '41': 'PR',
        '42': 'SC',
        '43': 'RS',
        '50': 'MS',
        '51': 'MT',
        '52': 'GO',
        '53': 'DF',
        'BRASIL': 'BR',
        'ACRE': 'AC',
        'ALAGOAS': 'AL',
        'AMAZONAS': 'AM',
        'AMAPA': 'AP',
        'AMAPÁ': 'AP',
        'BAHIA': 'BA',
        'CEARA': 'CE',
        'CEARÁ': 'CE',
        'DISTRITOFEDERAL': 'DF',
        'ESPIRITOSANTO': 'ES',
        'ESPÍRITOSANTO': 'ES',
        'GOIAS': 'GO',
        'GOIÁS': 'GO',
        'MARANHAO': 'MA',
        'MARANHÃO': 'MA',
        'MATOGROSSO': 'MT',
        'MATOGROSSODOSUL': 'MS',
        'MINASGERAIS': 'MG',
        'MINAS': 'MG',
        'PARA': 'PA',
        'PARÁ': 'PA',
        'PARAIBA': 'PB',
        'PARAÍBA': 'PB',
        'PARANA': 'PR',
        'PARANÁ': 'PR',
        'PERNAMBUCO': 'PE',
        'PIAUI': 'PI',
        'PIAUÍ': 'PI',
        'RIODEJANEIRO': 'RJ',
        'RIO': 'RJ',
        'RIOGRANDEDONORTE': 'RN',
        'RIOGRANDEDOSUL': 'RS',
        'RONDONIA': 'RO',
        'RONDÔNIA': 'RO',
        'RORAIMA': 'RR',
        'SAOPAULO': 'SP',
        'SÃOPAULO': 'SP',
        'SANTACATARINA': 'SC',
        'SERGIPE': 'SE',
        'TOCANTINS': 'TO'
    }

    EXTINTOS = {
        '20': 'FN',
        '34': 'GB',
        'FERNANDODENORONHA': 'FN',
        'GUANABARA': 'GB'
    }
    
    uf = str(uf).upper().replace(' ', '')

    if uf in UFS.values():
        return uf
    else:
        try:
            return UFS[uf]
        except KeyError:
            raise errors.UFError(
                "UF incorreta.\n"
                "Insira uma das 27 UFs válidas."
            )



def localidade(
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

    --------------------------------------------------------------------------
    '''

    if localidade is None:
        return brasil

    elif isinstance(localidade, int):
        return localidade

    elif isinstance(localidade, str):
        if localidade.isnumeric():
            return localidade

    if on_error == 'raise':
        raise errors.LocalidadeError('O código da localidade não está em um formato numérico.')
    elif on_error == 'brasil':
        return brasil
    else:
        raise errors.LocalidadeError(
            "Valor incorreto para o argumento `on_error`:\n"
            "  - 'raise': Gera um erro quando o valor não for válido;\n"
            "  - 'brasil': Retorna o valor Brasil quando o valor não for válido."
        )