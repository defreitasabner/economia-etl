from typing import Dict, Type

from src.extract.base_extractor import BaseExtractor


class ExtractorRegistry:
    _registry: Dict[str, Type[BaseExtractor]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(extractor_cls: Type[BaseExtractor]):
            if name in cls._registry:
                raise ValueError(f"Extrator com o nome '{name}' já está registrado.")
            cls._registry[name] = extractor_cls
            return extractor_cls
        return decorator
    
    @classmethod
    def get(cls, name: str) -> Type[BaseExtractor]:
        if name not in cls._registry:
            raise ValueError(f"Extrator com o nome '{name}' não está registrado.")
        return cls._registry[name]