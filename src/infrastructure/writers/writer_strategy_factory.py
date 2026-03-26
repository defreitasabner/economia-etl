from src.infrastructure.writers.json_writer_strategy import JsonWriterStrategy
from src.infrastructure.writers.parquet_writer_strategy import ParquetWriterStrategy
from src.infrastructure.writers.writer_strategy import WriterStrategy


class WriterStrategyFactory:

    @staticmethod
    def create(storage_format: str) -> WriterStrategy:
        if storage_format == 'json':
            return JsonWriterStrategy()
        if storage_format == 'parquet':
            return ParquetWriterStrategy()
        raise ValueError(f"Formato de escrita inválido: {storage_format}")