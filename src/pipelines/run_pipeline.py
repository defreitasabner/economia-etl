from src.infrastructure.file_writer import FileWriter
from src.load.bronze_loader import BronzeLoader
from src.pipelines.pipeline import Pipeline
from src.core.extractor_registry import ExtractorRegistry
from src.utils.config import load_dataset_config, load_config


def run_pipeline(domain_name: str, dataset_name: str, tier: str) -> None:
    dataset_config = load_dataset_config(domain_name, dataset_name)
    extractor = ExtractorRegistry.get(dataset_name)(dataset_config['extract'])

    file_writer = FileWriter()
    storage_config = load_config('storage.yaml')
    loader = BronzeLoader(
        storage_config = storage_config['bronze'],
        domain_name = domain_name,
        dataset_name = dataset_name,
        partition_by = dataset_config['load']['bronze']['partition_by'],
        writer = file_writer
    )

    pipeline = Pipeline(
        extractor = extractor,
        transformers = [],
        loader = loader,
        writer = file_writer

    )
    pipeline.run()