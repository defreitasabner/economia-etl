import json
from pathlib import Path

class FileWriter:

    def write_json(self, data: list[dict], filepath: str | Path) -> None:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent = 4, ensure_ascii = False)

