'''
Erros específicos dos módulos do DadosAbertosBrasil.
'''



class DAB_DataError(TypeError):
    '''
    Erro gerado quando o usuário insere um valor inválido para a data.
    '''



class DAB_LocalidadeError(TypeError):
    '''
    Erro gerado quando o usuário insere um valor inválido para a localidade.
    '''



class DAB_UFError(ValueError):
    '''
    Erro gerado quando o usuário insere um valor inválido para a UF.
    '''