'''
Erros específicos dos módulos do DadosAbertosBrasil.
'''



class LocalidadeError(TypeError):
    '''
    Erro gerado quando o usuário insere um valor inválido para a localidade.
    '''


class UFError(ValueError):
    '''
    Erro gerado quando o usuário insere um valor inválido para a UF.
    '''