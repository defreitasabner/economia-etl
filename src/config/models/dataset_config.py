from typing import Any, Optional

from pydantic import BaseModel


class RequestConfig(BaseModel):
    url: str
    query_params: dict[str, Any]

class ExtractorParams(BaseModel):
    periodicidade_diaria: Optional[bool] = False
    request: RequestConfig

class ExtractorConfig(BaseModel):
    type: str
    params: ExtractorParams

class ExtractConfig(BaseModel):
    extractors: list[ExtractorConfig]

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

