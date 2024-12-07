import pandas as pd

from .._utils.get_data import get_data


def get_ipea_data(path: str) -> pd.DataFrame:
    """Captura e formata dados deste módulo.

    Parameters
    ----------
    path : str
        Parâmetros da coleta.

    Returns
    -------
    pandas.core.frame.DataFrame

    """

    values = get_data(endpoint="http://www.ipeadata.gov.br/api/odata4/", path=path)
    return pd.DataFrame(values["value"])
