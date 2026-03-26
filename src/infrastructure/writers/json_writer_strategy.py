import json
from pathlib import Path

import pandas as pd

from src.infrastructure.writers.writer_strategy import WriterStrategy


class JsonWriterStrategy(WriterStrategy):

    def write(self, data: list[dict] | dict, filepath: str | Path) -> None:
        if not str(filepath).endswith('.json'):
            raise ValueError("O filepath deve terminar com '.json'")
        with open(filepath, 'w') as file:
            json.dump(data, file, indent = 4, ensure_ascii = False)