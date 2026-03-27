import logging

import requests

from src.config.models.dataset_config import ExtractConfig
from src.extract.extractor_registry import ExtractorRegistry
from src.extract.extractor import Extractor


logger = logging.getLogger(__name__)


@ExtractorRegistry.register('selic')
class SelicDiariaExtractor(Extractor):

    def __init__(self, config: ExtractConfig) -> None:
        self.__url = f"{config.base_url}/{config.endpoints['data']}"
        self.__params = config.params

    def extract(self) -> tuple[list[dict], dict]:
        logger.info(f"Extraindo dados da SELIC diária: {self.__url}")
        query_params = {
            'formato': self.__params['formato'],
            'dataInicial': self.__params['data_inicial'],
            'dataFinal': self.__params['data_final']
        }
        response = requests.get(self.__url, params = query_params, timeout = 5)
        response.raise_for_status()
        data = response.json()
        metadata = {
            'url': response.url,
            'query_params': query_params,
            'record_count': len(data),
        }
        logger.info(f"Extração concluída. {len(data)} registros obtidos.")
        return data, metadata
    
