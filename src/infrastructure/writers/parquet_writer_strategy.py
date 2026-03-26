from pathlib import Path

import pandas as pd

from src.infrastructure.writers.writer_strategy import WriterStrategy


class ParquetWriterStrategy(WriterStrategy):

    def write(self, data: pd.DataFrame, filepath: str | Path) -> None:
        if not str(filepath).endswith('.parquet'):
            raise ValueError("O filepath deve terminar com '.parquet'")
        if not isinstance(data, pd.DataFrame):
            raise TypeError('ParquetWriterStrategy espera um pandas DataFrame como entrada.')
        data.to_parquet(filepath, engine = 'pyarrow', index = False)