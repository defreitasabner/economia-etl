from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests

from src.config.models.dataset_config import ExtractorConfig
from src.extract.extractor import Extractor
from src.extract.extractor_registry import ExtractorRegistry


@ExtractorRegistry.register('atas_detail')
class AtaDetailExtractor(Extractor):
    def __init__(self, config: ExtractorConfig, atas: list[dict]) -> None:
        self.__url = config.params.request.url
        self.__atas = atas

    def extract(self) -> tuple[list[dict], dict]:
        atas_detalhes: list[dict] = []
        if self.__atas:
            with ThreadPoolExecutor(max_workers=min(4, len(self.__atas))) as executor:
                atas_detalhes = list(executor.map(self.__extract_ata_detail, self.__atas))

        metadata = {
            'url': self.__url,
            'query_params': {},
            'record_count': len(atas_detalhes),
            'extracted_at': datetime.now().isoformat(),
        }
        return atas_detalhes, metadata

    def __extract_ata_detail(self, ata: dict) -> dict:
        nro_reuniao = ata.get('nroReuniao') or ata.get('nro_reuniao')
        if nro_reuniao is None:
            raise ValueError('Ata sem identificador de reunião.')

        query_params = {
            'nro_reuniao': nro_reuniao,
        }
        response = requests.get(self.__url, params=query_params, timeout=5)
        response.raise_for_status()
        return response.json()['conteudo'][0]