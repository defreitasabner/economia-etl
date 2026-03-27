from typing import Any

from pydantic import BaseModel


class ExtractConfig(BaseModel):
    base_url: str
    endpoints: dict[str, str]
    params: dict[str, Any]

class TransformerConfig(BaseModel):
    type: str
    params: dict[str, Any]

class TransformConfig(BaseModel):
    transformers: list[TransformerConfig]

class LoadConfig(BaseModel):
    partition_by: list[str]

class DatasetConfig(BaseModel):
    extract: ExtractConfig
    transform: TransformConfig
    load: LoadConfig

