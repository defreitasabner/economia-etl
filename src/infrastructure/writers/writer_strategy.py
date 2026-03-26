from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class WriterStrategy(ABC):

    @abstractmethod
    def write(self, data: list[dict] | dict | pd.DataFrame, filepath: str | Path) -> None:
        pass