from src.extract.extractor import Extractor
from src.load.loader import Loader
from src.pipelines.bronze_pipeline import BronzePipeline
from src.pipelines.metadata_handler import MetadataHandler
from src.pipelines.pipeline import Pipeline
from src.pipelines.silver_pipeline import SilverPipeline
from src.read.reader import Reader


class PipelineFactory:
    
    @staticmethod
    def create(tier: str, extractor: Extractor | None, loader: Loader, reader: Reader | None, transformers: list) -> Pipeline:
        
        if loader is None:
            raise ValueError("Loader é obrigatório para criação de pipeline.")
        
        metadata_handler = MetadataHandler()
        if tier == "bronze":
            if extractor is None:
                raise ValueError("Extractor é obrigatório para pipeline 'bronze'.")
            return BronzePipeline(
                extractor = extractor,
                loader = loader,
                metadata_handler = metadata_handler

            )
        elif tier == "silver":
            if reader is None:
                raise ValueError("Reader é obrigatório para pipeline 'silver'.")
            return SilverPipeline(
                bronze_reader = reader,
                transformers = transformers,
                loader = loader,
                metadata_handler = metadata_handler
            )
        elif tier == "gold":
            raise NotImplementedError("Pipeline para tier 'gold' ainda não implementada.")
        else:
            raise ValueError(f"Tier '{tier}' não suportada.")