from typing import Literal

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
    formato : {"pandas", "polars"}, default="pandas"
        Biblioteca usada nos DataFrames retornados pelas funções quando o
        argumento `formato` não é informado. Requer `polars` instalado para
        `"polars"` (`pip install DadosAbertosBrasil[polars]`).

    Examples
    --------
    >>> import DadosAbertosBrasil as dab
    >>> dab.config.verificar_certificado = False
    >>> dab.config.formato = "polars"

    """

    model_config = ConfigDict(validate_assignment=True, extra="forbid")

    verificar_certificado: bool = True
    formato: Literal["pandas", "polars"] = "pandas"

    def resolver_certificado(self, valor: bool | None) -> bool:
        """Retorna `valor` se informado, ou a configuração global."""
        return self.verificar_certificado if valor is None else valor

    def resolver_formato(self, valor: str | None) -> str:
        """Retorna `valor` se informado, ou o formato global."""
        return self.formato if valor is None else valor


config = Config()
