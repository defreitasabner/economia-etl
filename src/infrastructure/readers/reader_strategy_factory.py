from src.infrastructure.readers.json_reader_strategy import JsonReaderStrategy
from src.infrastructure.readers.parquet_reader_strategy import ParquetReaderStrategy
from src.infrastructure.readers.reader_strategy import ReaderStrategy


class ReaderStrategyFactory:

    @staticmethod
    def create(storage_format: str) -> ReaderStrategy:
        if storage_format == 'json':
            return JsonReaderStrategy()
        if storage_format == 'parquet':
            return ParquetReaderStrategy()
        raise ValueError(f"Formato de leitura inválido: {storage_format}")
