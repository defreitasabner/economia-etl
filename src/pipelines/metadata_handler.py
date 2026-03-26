from pathlib import Path
from src.infrastructure.writers.writer_strategy_factory import WriterStrategyFactory


class MetadataHandler:

    def __init__(self):
        self.__json_writer = WriterStrategyFactory.create(storage_format = 'json')

    def write_metadata(self, metadata: dict, data_output_path: str) -> None:
        metadata_output_path = str(Path(data_output_path).with_name('metadata.json'))
        self.__json_writer.write(data = metadata, filepath = metadata_output_path)

