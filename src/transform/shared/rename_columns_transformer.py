import pandas as pd

from src.transform.transformer_registry import TransformerRegistry
from src.transform.transformer import Transformer


@TransformerRegistry.register('rename_columns')
class RenameColumnsTransformer(Transformer):

    def __init__(self, columns_mapping: dict[str, str]):
        self.__columns_mapping = columns_mapping

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.rename(columns = self.__columns_mapping).copy()
    
