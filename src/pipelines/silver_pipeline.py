from src.read.bronze_reader import BronzeReader
from src.load.loader import Loader
from src.pipelines.metadata_handler import MetadataHandler
from src.pipelines.pipeline import Pipeline


class SilverPipeline(Pipeline):
    def __init__(self, 
        bronze_reader: BronzeReader,
        transformers: list, 
        loader: Loader, 
        metadata_handler: MetadataHandler
    ) -> None:
        self.__bronze_reader = bronze_reader
        self.__transformers = transformers
        self.__loader = loader
        self.__metadata_handler = metadata_handler

    def run(self):
        data = self.__bronze_reader.read()
        for transformer in self.__transformers:
            data = transformer.transform(data)
        load_metadata = self.__loader.load(data)
        #TODO: Melhorar metadados: transformações aplicadas e talvez puxar metadados da bronze layer também
        metadata = {
            'input_path': self.__bronze_reader.get_path(),
            'load': load_metadata
        }
        self.__metadata_handler.write_metadata(metadata, load_metadata['filepath'])


