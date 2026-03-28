from datetime import datetime

import requests

from src.config.models.dataset_config import ExtractorConfig
from src.extract.extractor import Extractor
from src.extract.extractor_registry import ExtractorRegistry


@ExtractorRegistry.register('copom_list')
class CopomListExtractor(Extractor):
    def __init__(self, config: ExtractorConfig) -> None:
        self.__url = config.params.request.url
        self.__query_params = config.params.request.query_params

    def extract(self) -> tuple[list[dict], dict]:
        self.__validate_params()
        response = requests.get(self.__url, params=self.__query_params, timeout=5)
        response.raise_for_status()
        result = response.json().get('conteudo', [])

        metadata = {
            'url': response.url,
            'query_params': self.__query_params,
            'record_count': len(result),
            'extracted_at': datetime.now().isoformat(),
        }
        return result, metadata

    def __validate_params(self) -> None:
        quantidade = self.__query_params.get('quantidade', 0)
        if quantidade <= 0:
            raise ValueError(
                f"A quantidade deve ser um número positivo. Valor fornecido: {quantidade}"
            )