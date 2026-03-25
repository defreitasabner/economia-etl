from pathlib import Path
from datetime import datetime


class FilePathBuilder:

    def __init__(self, storage_tier_path: str, domain: str, dataset: str, partition_by: list = None, storage_format: str = 'json') -> None:
        self.__tier_path = storage_tier_path
        self.__domain = domain
        self.__dataset = dataset
        self.__partition_by = partition_by or []
        self.__storage_format = storage_format

    def build_path(self) -> str:
        dir_path = Path(self.__tier_path) / self.__domain / self.__dataset
        dir_path.mkdir(parents = True, exist_ok = True)
        filepath = dir_path / f"data.{self.__storage_format}"
        return str(filepath)
    
