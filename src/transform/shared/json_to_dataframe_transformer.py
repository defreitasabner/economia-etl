import pandas as pd

from src.transform.transformer_registry import TransformerRegistry
from src.transform.transformer import Transformer

@TransformerRegistry.register('json_to_dataframe')
class JsonToDataframeTransformer(Transformer):

    def transform(self, data: list[dict]) -> pd.DataFrame:
        return pd.json_normalize(data)
    
