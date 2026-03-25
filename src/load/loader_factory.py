

from src.infrastructure.file_path_builder import FilePathBuilder
from src.infrastructure.file_writer import FileWriter
from src.load.bronze_loader import BronzeLoader
from src.load.loader import Loader
from src.load.silver_loader import SilverLoader


class LoaderFactory:

    @staticmethod
    def create(tier: str, writer: FileWriter, filepath_builder: FilePathBuilder) -> Loader:
        if tier == 'bronze':
            return BronzeLoader(
                writer = writer,
                filepath_builder = filepath_builder
            )
        elif tier == 'silver':
            return SilverLoader(
                writer = writer,
                filepath_builder = filepath_builder
            )
        else:
            raise ValueError(f"Tier inválido: {tier}")
        
