import json
from pathlib import Path

import pandas as pd

class FileWriter:

    def write_json(self, data: list[dict], filepath: str | Path) -> None:
        if not str(filepath).endswith('.json'):
            raise ValueError("O filepath deve terminar com '.json'")
        with open(filepath, 'w') as file:
            json.dump(data, file, indent = 4, ensure_ascii = False)

    def write_parquet(self, data: pd.DataFrame, filepath: str | Path) -> None:
        if not str(filepath).endswith('.parquet'):
            raise ValueError("O filepath deve terminar com '.parquet'")
        data.to_parquet(filepath, engine = 'pyarrow', index = False)

