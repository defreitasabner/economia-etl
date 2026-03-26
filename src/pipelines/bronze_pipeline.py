from src.extract.extractor import Extractor
from src.load.loader import Loader
from src.pipelines.metadata_handler import MetadataHandler
from src.pipelines.pipeline import Pipeline


class BronzePipeline(Pipeline):
    def __init__(self, extractor: Extractor, loader: Loader, metadata_handler: MetadataHandler) -> None:
        self.__extractor = extractor
        self.__loader = loader
        self.__metadata_handler = metadata_handler

    def run(self) -> None:
        data, extract_metadata = self.__extractor.extract()
        load_metadata = self.__loader.load(data)
        metadata = {
            'extract': extract_metadata,
            'load': load_metadata
        }
        self.__metadata_handler.write_metadata(metadata, load_metadata['filepath'])




