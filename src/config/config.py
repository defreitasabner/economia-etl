from pathlib import Path

import yaml

from src.config.models.dataset_config import DatasetConfig
from src.config.models.storage_config import StorageConfig


class Config:

    def __init__(self):
        self.__config_dir_path = Path(__file__).parent.parent.parent / "config"
        
    def read_storage_config(self) -> StorageConfig:
        config = None
        with open(self.__config_dir_path / 'storage.yaml', 'r') as f:
            config = yaml.safe_load(f)
        storage_config = StorageConfig(**config)
        return storage_config

    def read_dataset_config(self, domain: str, dataset: str) -> DatasetConfig:
        config = None
        with open(self.__config_dir_path / 'domains' / domain / f'{dataset}.yaml', 'r') as f:
            config = yaml.safe_load(f)
        dataset_config = DatasetConfig(**config)
        return dataset_config
    
