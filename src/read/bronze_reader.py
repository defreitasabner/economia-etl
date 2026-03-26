from yaml.reader import Reader

from src.infrastructure.file_path_builder import FilePathBuilder
from src.infrastructure.readers.reader_strategy import ReaderStrategy


class BronzeReader(Reader):

    def __init__(self, filepath_builder: FilePathBuilder, reader_strategy: ReaderStrategy) -> None:
        self.__filepath_builder = filepath_builder
        self.__reader_strategy = reader_strategy

    def get_path(self) -> str:
        return self.__filepath_builder.get_path()

    def read(self):
        filepath = self.__filepath_builder.get_path()
        return self.__reader_strategy.read(filepath)
