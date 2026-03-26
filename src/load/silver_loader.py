from datetime import datetime

import pandas as pd

from src.infrastructure.writers.writer_strategy import WriterStrategy
from src.load.loader import Loader
from src.infrastructure.file_path_builder import FilePathBuilder


class SilverLoader(Loader):

    def __init__(self, writer_strategy: WriterStrategy, filepath_builder: FilePathBuilder):
        self.__writer_strategy = writer_strategy
        self.__path_builder = filepath_builder

    def load(self, data: pd.DataFrame) -> dict:
        filepath = self.__path_builder.build_path()
        self.__writer_strategy.write(data, filepath)
        return {
            'filepath': filepath,
            'loaded_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }