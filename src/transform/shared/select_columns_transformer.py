import pandas as pd

from src.transform.transformer_registry import TransformerRegistry
from src.transform.transformer import Transformer


@TransformerRegistry.register('select_columns')
class SelectColumnsTransformer(Transformer):

    def __init__(self, columns: list[str]):
        self.__columns = columns

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        missing_columns = [column for column in self.__columns if column not in df.columns]
        if missing_columns:
            raise KeyError(f'Não foi possível encontrar a(s) coluna(s): {missing_columns}')
        return df[self.__columns].copy()
    
