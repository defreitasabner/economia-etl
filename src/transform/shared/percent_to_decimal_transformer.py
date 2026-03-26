import pandas as pd

from src.transform.transformer import Transformer
from src.transform.transformer_registry import TransformerRegistry


@TransformerRegistry.register('percent_to_decimal')
class PercentToDecimalTransformer(Transformer):
    def __init__(self, target_column: str, result_column: str):
        self.__target_column = target_column
        self.__result_column = result_column

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.__target_column not in data.columns:
            raise ValueError(f"Coluna '{self.__target_column}' não encontrada no DataFrame.")
        if data[self.__target_column].dtype not in [float, int]:
            try:
                data[self.__target_column] = pd.to_numeric(data[self.__target_column])
            except ValueError:
                raise ValueError(f"Coluna '{self.__target_column}' deve ser do tipo numérico.")
        data[self.__result_column] = data[self.__target_column] / 100
        return data

