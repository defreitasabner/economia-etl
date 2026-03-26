from src.infrastructure.file_path_builder import FilePathBuilder
from src.infrastructure.writers.writer_strategy import WriterStrategy
from src.infrastructure.writers.writer_strategy_factory import WriterStrategyFactory
from src.load.bronze_loader import BronzeLoader
from src.load.loader import Loader
from src.load.silver_loader import SilverLoader


class LoaderFactory:

    @staticmethod
    def create(tier: str, output_path: str, domain: str, dataset: str, output_format: str, partition_by: str) -> Loader:
        writer_strategy = WriterStrategyFactory.create(storage_format = output_format)
        filepath_builder = FilePathBuilder(
            base_path = output_path,
            domain = domain,
            dataset = dataset,
            partition_by = partition_by,
            storage_format = output_format
        )
        if tier == 'bronze':
            return BronzeLoader(
                writer_strategy = writer_strategy,
                filepath_builder = filepath_builder
            )
        elif tier == 'silver':
            return SilverLoader(
                writer_strategy = writer_strategy,
                filepath_builder = filepath_builder
            )
        elif tier == 'gold':
            raise NotImplementedError("Loader para tier 'gold' ainda não implementado.")
        else:
            raise ValueError(f"Tier inválido: {tier}")
        
