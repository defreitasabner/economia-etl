from datetime import datetime

import pandas as pd

from src.infrastructure.file_writer import FileWriter
from src.load.loader import Loader
from src.infrastructure.file_path_builder import FilePathBuilder


class SilverLoader(Loader):

    def __init__(self, writer: FileWriter, filepath_builder: FilePathBuilder):
        self.__writer = writer
        self.__path_builder = filepath_builder

    def load(self, data: pd.DataFrame) -> dict:
        filepath = self.__path_builder.build_path()
        self.__writer.write_parquet(data, filepath)
        return {
            'filepath': filepath,
            'loaded_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }