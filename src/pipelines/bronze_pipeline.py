import json

from src.extract.extractor import Extractor
from src.infrastructure.file_writer import FileWriter
from src.load.loader import Loader
from src.pipelines.pipeline import Pipeline


class BronzePipeline(Pipeline):
    def __init__(self, extractor: Extractor, loader: Loader, writer: FileWriter) -> None:
        self.__extractor = extractor
        self.__loader = loader
        self.__writer = writer

    def run(self) -> None:
        data, extract_metadata = self.__extractor.extract()
        load_metadata = self.__loader.load(data)
        metadata = {
            'extract': extract_metadata,
            'load': load_metadata
        }
        self.__save_metadata(metadata)

    def __save_metadata(self, metadata: dict) -> None:
        metadata_path = metadata['load']['filepath'].replace('data.json', 'metadata.json')
        self.__writer.write_json(metadata, metadata_path)




