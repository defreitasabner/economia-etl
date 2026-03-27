from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime

import requests

from src.config.models.dataset_config import ExtractConfig
from src.extract.extractor import Extractor
from src.extract.extractor_registry import ExtractorRegistry


logger = logging.getLogger(__name__)


@ExtractorRegistry.register('atas')
class AtasCopomExtractor(Extractor):
    """Extrator de atas do COPOM via API pública do Banco Central."""
 
    def __init__(self, config: ExtractConfig) -> None:
        """Inicializa o extrator com a configuração da fonte COPOM.

        Args:
            config: Configuração de extração contendo base URL,
                endpoints e parâmetros padrão.
        """
        self.__url_list = f"{config.base_url}/{config.endpoints['list']}"
        self.__url_details = f"{config.base_url}/{config.endpoints['detail']}"
        self.__params = config.params
        
    def extract(self) -> tuple[list[dict], dict]:
        """Extrai atas recentes do COPOM e seus detalhes.

        Returns:
            (dados, metadados):
                - Lista de dicionários com os detalhes das atas.
                - Dicionário de metadados da extração, incluindo URL,
                    parâmetros de consulta, quantidade de registros e timestamp.
        """
        self.__validate_params(self.__params)
        atas, url = self.__extrair_atas(self.__url_list, self.__params)

        atas_detalhes = []
        if atas:
            with ThreadPoolExecutor(max_workers = min(4, len(atas))) as executor:
                atas_detalhes = list(
                    executor.map(
                        lambda ata: self.__extrair_atas_detalhes(self.__url_details, ata['nroReuniao']), 
                        atas
                    )
                )

        metadata = {
            'url': url,
            'query_params': {
                'quantidade': self.__params
            },
            'record_count': len(atas_detalhes),
            'extracted_at': datetime.now().isoformat()
        }
        logger.info(f"Extraídas {len(atas_detalhes)} atas do COPOM")
        return atas_detalhes, metadata

    def __validate_params(self, params: dict) -> None:
        """Valida a quantidade de atas a ser extraída.

        Args:
            params: Parâmetros de consulta contendo a quantidade de atas a ser extraída.

        Raises:
            ValueError: Se a quantidade de atas for negativa ou zero.
        """
        quantidade = params.get('quantidade', 0)
        if quantidade <= 0:
            raise ValueError(f"A quantidade de atas deve ser um número positivo. Valor fornecido: {quantidade}")

    def __extrair_atas(self, url: str, qtd_atas: int) -> tuple[list[dict], str]:
        """Consulta a API para obter a lista de atas mais recentes.

        Args:
            url: URL da API para consulta das atas.
            qtd_atas: Quantidade de atas a serem extraídas.

        Returns:
            (atas, url):
                - Lista de atas retornadas pela API.
                - URL final da requisição (com query string).
        """
        response = requests.get(url, params = self.__params, timeout = 5)
        logger.debug(f"Requisição GET para {url} com params {self.__params} retornou status {response.status_code}")
        return response.json()['conteudo'], response.url
    
    def __extrair_atas_detalhes(self, url: str, nro_reuniao: int) -> dict:
        """Consulta a API para obter os detalhes de uma reunião do COPOM.

        Args:
            url: URL da API para consulta dos detalhes da ata.
            nro_reuniao: Número identificador da reunião.

        Returns:
            atas_detalhes: Dicionário com os detalhes da ata da reunião solicitada.
        """
        query_params = {
            'nro_reuniao': nro_reuniao
        }
        response = requests.get(url, params = query_params, timeout = 5)
        logger.debug(f"Requisição GET para {url} com params {query_params} retornou status {response.status_code}")
        return response.json()['conteudo'][0]
    
