import pandas as pd

from .._utils.get_data import get_data


def get_bacen_data(path: str, params: dict = None) -> pd.DataFrame:
    data = get_data(
        endpoint="https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/",
        path=path,
        params=params,
    )
    return pd.DataFrame(data["value"])
