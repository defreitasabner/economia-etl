from typing import Dict, Type

from src.extract.extractor import Extractor


class ExtractorRegistry:
    _registry: Dict[str, Type[Extractor]] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(extractor_cls: Type[Extractor]):
            if name in cls._registry:
                raise ValueError(f"Extrator com o nome '{name}' já está registrado.")
            cls._registry[name] = extractor_cls
            return extractor_cls
        return decorator
    
    @classmethod
    def get(cls, name: str) -> Type[Extractor]:
        if name not in cls._registry:
            raise ValueError(f"Extrator com o nome '{name}' não está registrado.")
        return cls._registry[name]