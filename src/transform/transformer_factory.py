from src.transform.transformer import Transformer
from src.transform.transformer_registry import TransformerRegistry


class TransformerFactory:
    
    @staticmethod
    def create(transformer_config: dict) -> Transformer:
        transformer_name = transformer_config['type']
        params = {k: v for k, v in transformer_config.items() if k != 'type'}
        transformer_cls = TransformerRegistry.get(transformer_name)
        return transformer_cls(**params)
    
