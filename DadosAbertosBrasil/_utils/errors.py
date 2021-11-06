"""Erros específicos dos módulos do DadosAbertosBrasil.

"""



class DAB_DataError(TypeError):
    """Erro gerado quando o usuário insere um valor inválido para a data.

    """



class DAB_InputError(ValueError):
    """Erro gerado quando o usuário insere um valor inválido para um argumento.
    
    """



class DAB_LocalidadeError(TypeError):
    """Erro gerado quando o usuário insere um valor inválido para a localidade.

    """



class DAB_MoedaError(ValueError):
    """Erro gerado quando o usuário insere um valor inválido para uma moeda.

    """



class DAB_UFError(ValueError):
    """Erro gerado quando o usuário insere um valor inválido para a UF.

    """



class DAB_DeprecationError(DeprecationWarning):
    """Erro gerado quando o usuário chama uma função depreciada.
    
    """