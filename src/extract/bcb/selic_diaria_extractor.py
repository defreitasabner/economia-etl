import logging

import requests

from src.core.extractor_registry import ExtractorRegistry
from src.extract.extractor import Extractor


logger = logging.getLogger(__name__)


@ExtractorRegistry.register('selic')
class SelicDiariaExtractor(Extractor):

    def __init__(self, config: dict) -> None:
        self.__url = config['url']
        self.__formato = config['formato']
        self.__data_inicial = config['data_inicial']
        self.__data_final = config['data_final']

    def extract(self) -> tuple[list[dict], dict]:
        logger.info(f"Extraindo dados da SELIC diária: {self.__url}")
        query_params = {
            'formato': self.__formato,
            'dataInicial': self.__data_inicial,
            'dataFinal': self.__data_final
        }
        response = requests.get(self.__url, params = query_params)
        response.raise_for_status()
        data = response.json()
        metadata = {
            'url': response.url,
            'query_params': query_params,
            'record_count': len(data),
        }
        logger.info(f"Extração concluída. {len(data)} registros obtidos.")
        return data, metadata
    
