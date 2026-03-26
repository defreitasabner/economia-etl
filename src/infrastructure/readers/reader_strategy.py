from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class ReaderStrategy(ABC):

    @abstractmethod
    def read(self, filepath: str | Path) -> list[dict] | pd.DataFrame:
        pass
