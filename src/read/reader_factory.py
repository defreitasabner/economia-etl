from src.infrastructure.file_path_builder import FilePathBuilder
from src.infrastructure.readers.reader_strategy_factory import ReaderStrategyFactory
from src.read.bronze_reader import BronzeReader
from src.read.reader import Reader


class ReaderFactory:
    
    @staticmethod
    def create(tier: str, input_path: str, domain: str, dataset: str, partition_by: list, format: str) -> Reader:
        reader_strategy = ReaderStrategyFactory.create(storage_format = format)
        path_builder = FilePathBuilder(
            base_path = input_path,
            domain = domain,
            dataset = dataset,
            partition_by = partition_by,
            storage_format = format
        )

        if tier == 'bronze':
            return BronzeReader(filepath_builder = path_builder, reader_strategy = reader_strategy)
        elif tier == 'silver':
            raise NotImplementedError("Reader para tier 'silver' ainda não implementado.")
        else:
            raise ValueError(f"Tier '{tier}' não é suportada para leitura.")

