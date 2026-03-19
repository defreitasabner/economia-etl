import logging

from src.extract.bcb.atas_copom_extractor import AtasCopomExtractor
from src.load.bronze_loader import BronzeLoader
from src.pipelines.pipeline import Pipeline
from src.utils.config import load_config


logger = logging.getLogger(__name__)

def extrair_atas_copom(qtd_atas: int | None = None) -> None:
    general_config = load_config('general.yaml')
    source_config = load_config(general_config['config']['sources']['bcb'])

    if qtd_atas:
        source_config['extract']['atas']['qtd_atas'] = qtd_atas
        logger.info(f"Quantidade de atas para extração definida via argumento: {qtd_atas}")
    else:
        logger.info(f"Quantidade de atas para extração definida via config: {source_config['extract']['atas']['qtd_atas']}")
    
    pipeline = Pipeline(
        extractor = AtasCopomExtractor(
            config = source_config['extract']['atas'],
        ),
        transformers = [],
        loader = BronzeLoader(
            config = general_config['storage']['bronze'],
            source_name = source_config['source_name'],
            dataset_name = source_config['load']['bronze']['atas']['dataset_name'],
            partition_by = source_config['load']['bronze']['atas'].get('partition_by', [])
        )
    )
    pipeline.run()

