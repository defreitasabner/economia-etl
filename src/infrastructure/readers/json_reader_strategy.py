import json
from pathlib import Path

from src.infrastructure.readers.reader_strategy import ReaderStrategy


class JsonReaderStrategy(ReaderStrategy):

    def read(self, filepath: str | Path) -> list[dict]:
        if not str(filepath).endswith('.json'):
            raise ValueError("O filepath deve terminar com '.json'")
        with open(filepath, 'r') as file:
            return json.load(file)
