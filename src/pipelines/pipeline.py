import json

from src.extract.base_extractor import BaseExtractor
from src.infrastructure.file_writer import FileWriter
from src.load.base_loader import BaseLoader


class Pipeline:
    def __init__(self, extractor: BaseExtractor, transformers: list, loader: BaseLoader, writer: FileWriter) -> None:
        self.__extractor = extractor
        self.__transformers = transformers
        self.__loader = loader
        self.__writer = writer

    def run(self) -> None:
        data, extract_metadata = self.__extractor.extract()
        for transformer in self.__transformers:
            data = transformer.transform(data)
        load_metadata = self.__loader.load(data)
        metadata = {
            'extract': extract_metadata,
            'load': load_metadata
        }
        self.__save_metadata(metadata)

    def __save_metadata(self, metadata: dict) -> None:
        metadata_path = metadata['load']['filepath'].replace('.json', '_metadata.json')
        self.__writer.write_json(metadata, metadata_path)




