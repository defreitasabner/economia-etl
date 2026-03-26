import pandas as pd

from src.transform.transformer import Transformer
from src.transform.transformer_registry import TransformerRegistry


@TransformerRegistry.register("text_to_date")
class TextToDateTransformer(Transformer):
    def __init__(self, target_column: str, text_format: str):
        self.__target_column = target_column
        self.__text_format = text_format

    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        data[self.__target_column] = pd.to_datetime(data[self.__target_column], format = self.__text_format).dt.date
        return data