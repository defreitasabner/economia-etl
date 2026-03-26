import pandas as pd
from bs4 import BeautifulSoup

from src.transform.transformer_registry import TransformerRegistry
from src.transform.transformer import Transformer


@TransformerRegistry.register('html_to_text')
class HtmlToTextTransformer(Transformer):

    def __init__(self, target_column: str, result_column: str, target_html_id: str | None = None) -> None:
        self.__target_column = target_column
        self.__target_html_id = target_html_id
        self.__result_column = result_column
    
    def transform(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.__target_html_id:
            data[self.__result_column] = data[self.__target_column].map(
                lambda x: BeautifulSoup(x, 'html.parser').find(id = self.__target_html_id).text
            )
        else:
            data[self.__result_column] = data[self.__target_column].map(
                lambda x: BeautifulSoup(x, 'html.parser').text
            )
        return data
    
