import logging

from src.extract.copom_extractor import CopomExtractor
from src.load.bronze_loader import BronzeLoader
from src.pipelines.pipeline import Pipeline
from src.utils.config import load_config


logger = logging.getLogger(__name__)

def extrair_atas_copom(qtd_atas: int | None = None) -> None:
    general_config = load_config('general.yaml')
    source_config = load_config('sources/copom.yaml')

    if qtd_atas:
        source_config['extract']['default']['qtd_atas'] = qtd_atas
        logger.info(f"Quantidade de atas para extração definida via argumento: {qtd_atas}")
    else:
        logger.info(f"Quantidade de atas para extração definida via config: {source_config['extract']['default']['qtd_atas']}")
    
    pipeline = Pipeline(
        extractor = CopomExtractor(
            config = source_config['extract'],
        ),
        transformers = [],
        loader = BronzeLoader(
            config = general_config['storage']['bronze'],
            source_name = source_config['source_name'],
            dataset_name = source_config['load']['bronze']['dataset_name'],
            partition_by = source_config['load']['bronze'].get('partition_by', [])
        )
    )
    pipeline.run()

