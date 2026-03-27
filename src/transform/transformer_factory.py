from src.config.models.dataset_config import TransformerConfig
from src.transform.transformer import Transformer
from src.transform.transformer_registry import TransformerRegistry


class TransformerFactory:
    
    @staticmethod
    def create(transformer_config: TransformerConfig) -> Transformer:
        transformer_cls = TransformerRegistry.get(transformer_config.type)
        return transformer_cls(**transformer_config.params)

    @staticmethod
    def create_all(transformer_configs: list[TransformerConfig]) -> list[Transformer]:
        transformers = []
        for transformer_config in transformer_configs:
            transformer = TransformerFactory.create(transformer_config)
            transformers.append(transformer)
        return transformers
    
