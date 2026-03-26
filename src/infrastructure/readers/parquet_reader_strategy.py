from pathlib import Path

import pandas as pd

from src.infrastructure.readers.reader_strategy import ReaderStrategy


class ParquetReaderStrategy(ReaderStrategy):

    def read(self, filepath: str | Path) -> pd.DataFrame:
        if not str(filepath).endswith('.parquet'):
            raise ValueError("O filepath deve terminar com '.parquet'")
        return pd.read_parquet(filepath, engine = 'pyarrow')
