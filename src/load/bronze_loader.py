from datetime import datetime

from src.infrastructure.file_path_builder import FilePathBuilder
from src.infrastructure.writers.writer_strategy import WriterStrategy
from src.load.loader import Loader


class BronzeLoader(Loader):
    
    def __init__(self, writer_strategy: WriterStrategy, filepath_builder: FilePathBuilder) -> None:
        self.__filepath_builder = filepath_builder
        self.__writer_strategy = writer_strategy

    def load(self, data: list[dict]) -> dict:
        filepath = self.__filepath_builder.build_path()
        self.__writer_strategy.write(data, filepath)
        metadata = {
            'filepath': str(filepath),
            'loaded_at': datetime.now().strftime("%Y-%m-%d")
        }
        return metadata

