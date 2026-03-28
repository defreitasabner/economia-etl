from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

import requests

from src.config.models.dataset_config import ExtractorConfig
from src.extract.extractor import Extractor
from src.extract.extractor_registry import ExtractorRegistry


@ExtractorRegistry.register('comunicados_detail')
class ComunicadoDetailExtractor(Extractor):
    def __init__(self, config: ExtractorConfig, comunicados: list[dict]) -> None:
        self.__url = config.params.request.url
        self.__comunicados = comunicados

    def extract(self) -> tuple[list[dict], dict]:
        comunicados_detalhes: list[dict] = []
        if self.__comunicados:
            with ThreadPoolExecutor(max_workers=min(4, len(self.__comunicados))) as executor:
                comunicados_detalhes = list(executor.map(self.__extract_comunicado_detail, self.__comunicados))

        metadata = {
            'url': self.__url,
            'query_params': {},
            'record_count': len(comunicados_detalhes),
            'extracted_at': datetime.now().isoformat(),
        }
        return comunicados_detalhes, metadata

    def __extract_comunicado_detail(self, comunicado: dict) -> dict:
        nro_reuniao = comunicado.get('nro_reuniao')
        if nro_reuniao is None:
            raise ValueError('Comunicado sem identificador de reunião.')

        query_params = {
            'nro_reuniao': nro_reuniao,
        }
        response = requests.get(self.__url, params=query_params, timeout=5)
        response.raise_for_status()
        return response.json()['conteudo'][0]
