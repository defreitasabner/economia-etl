from src.load.loader_factory import LoaderFactory
from src.extract.extractor_registry import ExtractorRegistry
from src.pipelines.pipeline_factory import PipelineFactory
from src.read.reader_factory import ReaderFactory
from src.transform.transformer_factory import TransformerFactory
from src.transform.transformer_registry import TransformerRegistry
from src.utils.config import load_dataset_config, load_storage_config


def run_pipeline(domain_name: str, dataset_name: str, tier: str) -> None:
    ExtractorRegistry.auto_discover()
    TransformerRegistry.auto_discover()
    
    dataset_config = load_dataset_config(domain_name, dataset_name)
    storage_config = load_storage_config(tier)
    
    extractor = None
    if tier == 'bronze':
        extractor = ExtractorRegistry.get(name = dataset_name)(dataset_config['extract'])

    loader = LoaderFactory.create(
        tier = tier,
        output_path = storage_config['output_path'],
        domain = domain_name,
        dataset = dataset_name,
        output_format = storage_config['output_format'],
        partition_by = dataset_config['load'][tier]['partition_by']
    )

    reader = None
    if not tier == 'bronze':
        target_tier = 'bronze' if tier == 'silver' else 'silver'
        reader = ReaderFactory.create(
            tier = target_tier,
            input_path = storage_config['input_path'],
            domain = domain_name,
            dataset = dataset_name,
            partition_by = dataset_config['load'][target_tier]['partition_by'],
            format = storage_config['input_format']
        )

    transformers = []
    for transformer_config in dataset_config['transform']:
        transformer = TransformerFactory.create(transformer_config = transformer_config)
        transformers.append(transformer)

    pipeline = PipelineFactory.create(
        tier = tier,
        extractor = extractor,
        loader = loader,
        reader = reader,
        transformers = transformers
    )
    
    pipeline.run()

