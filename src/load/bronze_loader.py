from pathlib import Path
from datetime import datetime

from src.infrastructure.file_path_builder import FilePathBuilder
from src.infrastructure.file_writer import FileWriter
from src.load.loader import Loader


class BronzeLoader(Loader):
    
    def __init__(self, writer: FileWriter, filepath_builder: FilePathBuilder) -> None:
        self.__filepath_builder = filepath_builder
        self.__writer = writer

    def load(self, data: list[dict]) -> dict:
        filepath = self.__filepath_builder.build_path()
        self.__writer.write_json(data, filepath)
        metadata = {
            'filepath': str(filepath),
            'loaded_at': datetime.now().strftime("%Y-%m-%d")
        }
        return metadata

