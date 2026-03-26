from pathlib import Path
from datetime import datetime


class FilePathBuilder:

    def __init__(self, base_path: str, domain: str, dataset: str, partition_by: list = None, storage_format: str = 'json') -> None:
        self.__tier_path = base_path
        self.__domain = domain
        self.__dataset = dataset
        self.__partition_by = partition_by or []
        self.__storage_format = storage_format

    def build_path(self) -> str:
        dir_path = self.__get_dir_path(
            tier_path = self.__tier_path,
            domain = self.__domain,
            dataset = self.__dataset
        )
        dir_path.mkdir(parents = True, exist_ok = True)
        filepath = self.__get_file_path(dir_path = dir_path, format = self.__storage_format)
        return str(filepath)

    def get_path(self) -> str:
        dir_path = self.__get_dir_path(
            tier_path = self.__tier_path,
            domain = self.__domain,
            dataset = self.__dataset
        )
        filepath = self.__get_file_path(dir_path = dir_path, format = self.__storage_format)
        if not filepath.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {filepath}")
        return str(filepath)

    def __get_dir_path(self, tier_path: str, domain: str, dataset: str) -> Path:
        return Path(tier_path) / domain / dataset
    
    def __get_file_path(self, dir_path: Path, format: str) -> Path:
        return dir_path / f'data.{format}'
    
