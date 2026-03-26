from typing import Dict, Type

from src.core.registry import Registry
from src.transform.transformer import Transformer


class TransformerRegistry(Registry):

    _registry: Dict[str, Type[Transformer]] = {}

