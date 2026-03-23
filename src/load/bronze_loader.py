import json
from pathlib import Path
from datetime import datetime


class BronzeLoader:
    
    def __init__(self, config: dict, source_name: str, dataset_name: str, partition_by: list[str] | None = None) -> None:
        self.storage_config = config
        self.source_name = source_name
        self.dataset_name = dataset_name
        self.partition_by = partition_by or []

    def load(self, data: list[dict], metadata: dict) -> None:
        ingest_date = datetime.now().strftime("%Y-%m-%d")
        source_dir_path = Path(
            self.storage_config['path'],
            self.source_name,
            self.dataset_name,
            f'ingest_date={ingest_date}'
        )
        for partition in self.partition_by:
            partition_value = metadata.get(partition)
            if partition_value:
                source_dir_path = source_dir_path / f"{partition}={partition_value}"
        source_dir_path.mkdir(parents = True, exist_ok = True)
        data_filepath = source_dir_path / f'{self.dataset_name}.json'
        with open(data_filepath, 'w') as file:
            json.dump(data, file, indent = 4, ensure_ascii = False)
        metadata['path'] = str(data_filepath)
        metadata_filepath = source_dir_path / f'{self.dataset_name}_metadata.json'
        with open(metadata_filepath, 'w') as file:
            json.dump(metadata, file, indent = 4, ensure_ascii = False)

