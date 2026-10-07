from pydantic import BaseModel, ConfigDict


class Config(BaseModel):
    """Configurações globais do pacote.

    Os valores podem ser alterados por atribuição direta e são validados na
    hora. Argumentos passados diretamente às funções têm precedência sobre
    estas configurações.

    Attributes
    ----------
    verificar_certificado : bool, default=True
        Verifica o certificado SSL das requisições. Defina como `False` em caso
        de falha na verificação do certificado.

    Examples
    --------
    >>> import DadosAbertosBrasil as dab
    >>> dab.config.verificar_certificado = False

    """

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    verificar_certificado: bool = True

    def resolver_certificado(self, valor: bool | None) -> bool:
        """Retorna `valor` se informado, ou a configuração global."""
        return self.verificar_certificado if valor is None else valor


config = Config()
