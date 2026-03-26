import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Type

from src.extract.extractor import Extractor


class ExtractorRegistry:
    _registry: Dict[str, Type[Extractor]] = {}

    @classmethod
    def auto_discover(cls) -> None:
        extract_root = Path(__file__).resolve().parents[1] / "extract"
        base_package = "src.extract"

        for module_info in pkgutil.walk_packages(
            [str(extract_root)],
            prefix=f"{base_package}."
        ):
            module_name = module_info.name
            if module_name.endswith(".__init__"):
                continue

            importlib.import_module(module_name)

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