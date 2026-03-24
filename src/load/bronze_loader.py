import json
from pathlib import Path
from datetime import datetime

from src.infrastructure.file_writer import FileWriter


class BronzeLoader:
    
    def __init__(self, storage_config: dict, domain_name: str, dataset_name: str, partition_by: list[str], writer: FileWriter) -> None:
        self.__storage_config = storage_config
        self.__domain_name = domain_name
        self.__dataset_name = dataset_name
        self.__partition_by = partition_by
        self.__writer = writer

    def load(self, data: list[dict]) -> dict:
        ingest_date = datetime.now().strftime("%Y-%m-%d")
        source_dir_path = Path(
            self.__storage_config['path'],
            self.__domain_name,
            self.__dataset_name,
            f'ingest_date={ingest_date}'
        )
        source_dir_path.mkdir(parents = True, exist_ok = True)
        data_filepath = source_dir_path / f'{self.__dataset_name}.json'
        self.__writer.write_json(data, data_filepath)
        metadata = {
            'filepath': str(data_filepath),
            'loaded_at': ingest_date
        }
        return metadata

