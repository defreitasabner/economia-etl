import requests
from datetime import datetime

from src.config.models.dataset_config import ExtractorConfig
from src.extract.extractor import Extractor
from src.extract.extractor_registry import ExtractorRegistry


@ExtractorRegistry.register('sgs')
class SgsExtractor(Extractor):

    def __init__(self, config: ExtractorConfig) -> None:
        self.__url = config.params.request.url
        self.__query_params = config.params.request.query_params

    def extract(self) -> tuple[list[dict], dict]:
        data_inicial = datetime.strptime(self.__query_params['dataInicial'], '%d/%m/%Y').date()
        data_final = datetime.strptime(self.__query_params['dataFinal'], '%d/%m/%Y').date()
        if data_inicial > data_final:
            raise ValueError("dataInicial deve ser anterior a dataFinal")
        response = requests.get(self.__url, params=self.__query_params, timeout=10)
        response.raise_for_status()
        data = response.json()
        metadata = {
            'url': response.url,
            'query_params': self.__query_params,
            'record_count': len(data),
        }
        return data, metadata
