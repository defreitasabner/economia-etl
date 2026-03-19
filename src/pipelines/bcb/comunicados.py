import logging

from src.extract.bcb.comunicados_copom_extractor import ComunicadosCopomExtractor
from src.load.bronze_loader import BronzeLoader
from src.pipelines.pipeline import Pipeline
from src.utils.config import load_config


logger = logging.getLogger(__name__)


def extrair_comunicados_copom(qtd_comunicados: int | None = None) -> None:
    general_config = load_config('general.yaml')
    source_config = load_config(general_config['config']['sources']['bcb'])

    if qtd_comunicados:
        source_config['extract']['comunicados']['qtd_comunicados'] = qtd_comunicados
        logger.info(f"Quantidade de comunicados para extração definida via argumento: {qtd_comunicados}")
    else:
        logger.info(
            f"Quantidade de comunicados para extração definida via config: "
            f"{source_config['extract']['comunicados']['qtd_comunicados']}"
        )

    pipeline = Pipeline(
        extractor=ComunicadosCopomExtractor(
            config=source_config['extract']['comunicados'],
        ),
        transformers=[],
        loader=BronzeLoader(
            config=general_config['storage']['bronze'],
            source_name=source_config['source_name'],
            dataset_name=source_config['load']['bronze']['comunicados']['dataset_name'],
            partition_by=source_config['load']['bronze']['comunicados'].get('partition_by', []),
        ),
    )
    pipeline.run()
