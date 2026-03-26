from abc import ABC, abstractmethod

import pandas as pd


class Transformer(ABC):
    
    @abstractmethod
    def transform(self, data: list[dict] | pd.DataFrame) -> pd.DataFrame:
        pass

