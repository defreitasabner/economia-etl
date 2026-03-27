from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime

import requests

from src.config.models.dataset_config import ExtractConfig
from src.extract.extractor import Extractor
from src.extract.extractor_registry import ExtractorRegistry


logger = logging.getLogger(__name__)


@ExtractorRegistry.register('comunicados')
class ComunicadosCopomExtractor(Extractor):
    """Extrator de comunicados do COPOM via API publica do Banco Central."""

    def __init__(self, config: ExtractConfig) -> None:
        """Inicializa o extrator com a configuracao da fonte COPOM."""
        self.__url_list = f"{config.base_url}/{config.endpoints['list']}"
        self.__url_details = f"{config.base_url}/{config.endpoints['detail']}"
        self.__params = config.params

    def extract(self) -> tuple[list[dict], dict]:
        """Extrai comunicados recentes do COPOM e seus detalhes."""
        self.__validate_params(self.__params)

        comunicados, url = self.__extrair_comunicados(self.__url_list)

        comunicados_detalhes = []
        if comunicados:
            with ThreadPoolExecutor(max_workers=min(4, len(comunicados))) as executor:
                comunicados_detalhes = list(
                    executor.map(
                        lambda comunicado: self.__extrair_comunicados_detalhes(
                            self.__url_details,
                            comunicado['nro_reuniao'],
                        ),
                        comunicados,
                    )
                )

        metadata = {
            'url': url,
            'query_params': self.__params,
            'record_count': len(comunicados_detalhes),
            'extracted_at': datetime.now().isoformat(),
        }
        logger.info(f"Extraidos {len(comunicados_detalhes)} comunicados do COPOM")
        return comunicados_detalhes, metadata

    def __validate_params(self, params: dict) -> None:
        """Valida a quantidade de comunicados a ser extraida."""
        quantidade = params.get('quantidade', 0)
        if quantidade <= 0:
            raise ValueError("A quantidade de comunicados deve ser maior que zero.")

    def __extrair_comunicados(self, url: str) -> tuple[list[dict], str]:
        """Consulta a API para obter a lista de comunicados mais recentes."""
        response = requests.get(url, params=self.__params, timeout=5)
        logger.debug(
            "Requisicao GET para %s com params %s retornou status %s",
            url,
            self.__params,
            response.status_code,
        )
        return response.json()['conteudo'], response.url

    def __extrair_comunicados_detalhes(self, url: str, nro_reuniao: str) -> dict:
        """Consulta a API para obter os detalhes de um comunicado do COPOM."""
        query_params = {
            'nro_reuniao': nro_reuniao,
        }
        response = requests.get(url, params=query_params, timeout=5)
        logger.debug(
            "Requisicao GET para %s com params %s retornou status %s",
            url,
            query_params,
            response.status_code,
        )
        return response.json()['conteudo'][0]
