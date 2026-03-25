from src.infrastructure.file_path_builder import FilePathBuilder
from src.infrastructure.file_writer import FileWriter
from src.load.loader_factory import LoaderFactory
from src.pipelines.bronze_pipeline import BronzePipeline
from src.core.extractor_registry import ExtractorRegistry
from src.utils.config import load_dataset_config, load_storage_config


def run_pipeline(domain_name: str, dataset_name: str, tier: str) -> None:
    
    dataset_config = load_dataset_config(domain_name, dataset_name)
    storage_config = load_storage_config(tier)
    
    extractor = ExtractorRegistry.get(dataset_name)(dataset_config['extract'])

    writer = FileWriter()
    filepath_builder = FilePathBuilder(
        storage_tier_path = storage_config['path'],
        domain = domain_name,
        dataset = dataset_name,
        partition_by = dataset_config['load'][tier]['partition_by'],
        storage_format = storage_config['format']
    )
    loader = LoaderFactory.create(
        tier = tier,
        writer = writer,
        filepath_builder = filepath_builder
    )

    pipeline = BronzePipeline(
        extractor = extractor,
        loader = loader,
        writer = writer

    )
    pipeline.run()

