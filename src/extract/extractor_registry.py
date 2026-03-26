import importlib
import pkgutil
from pathlib import Path
from typing import Dict, Type

from src.core.registry import Registry
from src.extract.extractor import Extractor


class ExtractorRegistry(Registry):
    
    _registry: Dict[str, Type[Extractor]] = {}


