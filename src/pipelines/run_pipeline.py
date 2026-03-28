from src.config.config import Config
from src.extract.extractor_factory import ExtractorFactory
from src.load.loader_factory import LoaderFactory
from src.extract.extractor_registry import ExtractorRegistry
from src.pipelines.pipeline_factory import PipelineFactory
from src.read.reader_factory import ReaderFactory
from src.transform.transformer_factory import TransformerFactory
from src.transform.transformer_registry import TransformerRegistry


def run_pipeline(domain_name: str, dataset_name: str, tier: str) -> None:
    ExtractorRegistry.auto_discover()
    TransformerRegistry.auto_discover()
    
    config = Config()
    storage_config = config.read_storage_config().get_tier(tier)
    dataset_config = config.read_dataset_config(domain_name, dataset_name)
    
    extractor = None
    if tier == 'bronze':
        extractor = ExtractorFactory.create(dataset_config.extract)

    loader = LoaderFactory.create(
        tier = tier,
        output_path = storage_config.output_path,
        domain = domain_name,
        dataset = dataset_name,
        output_format = storage_config.output_format,
        partition_by = dataset_config.load.partition_by
    )

    reader = None
    if not tier == 'bronze':
        target_tier = 'bronze' if tier == 'silver' else 'silver'
        reader = ReaderFactory.create(
            tier = target_tier,
            input_path = storage_config.input_path,
            domain = domain_name,
            dataset = dataset_name,
            partition_by = dataset_config.load.partition_by,
            format = storage_config.input_format
        )

    transformers = TransformerFactory.create_all(dataset_config.transform.transformers)

    pipeline = PipelineFactory.create(
        tier = tier,
        extractor = extractor,
        loader = loader,
        reader = reader,
        transformers = transformers
    )
    
    pipeline.run()

