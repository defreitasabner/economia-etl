from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests

from src.config.models.dataset_config import ExtractorConfig
from src.extract.extractor import Extractor
from src.extract.extractor_registry import ExtractorRegistry


@ExtractorRegistry.register('copom_detail')
class CopomDetailExtractor(Extractor):
    def __init__(self, config: ExtractorConfig, list_data: list[dict]) -> None:
        self.__url = config.params.request.url
        self.__list_data = list_data

    def extract(self) -> tuple[list[dict], dict]:
        result: list[dict] = []
        if self.__list_data:
            with ThreadPoolExecutor(max_workers=min(4, len(self.__list_data))) as executor:
                result = list(executor.map(self.__extract_details, self.__list_data))

        metadata = {
            'url': self.__url,
            'query_params': {},
            'record_count': len(result),
            'extracted_at': datetime.now().isoformat(),
        }
        return result, metadata

    def __extract_details(self, item: dict) -> dict:
        nro_reuniao = item.get('nroReuniao') or item.get('nro_reuniao')
        if nro_reuniao is None:
            raise ValueError('Não foi encontrado o número da reunião.')

        query_params = {
            'nro_reuniao': nro_reuniao,
        }
        response = requests.get(self.__url, params = query_params, timeout = 5)
        response.raise_for_status()
        return response.json()['conteudo'][0]