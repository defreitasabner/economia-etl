from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime

import requests

from src.extract.base_extractor import BaseExtractor


logger = logging.getLogger(__name__)

class AtasCopomExtractor(BaseExtractor):
    """Extrator de atas do COPOM via API pública do Banco Central."""
 
    def __init__(self, config: dict) -> None:
        """Inicializa o extrator com a configuração da fonte COPOM.

        Args:
            config: Dicionário de configuração da extração contendo base URL,
                endpoints e parâmetros padrão.
        """
        self.url_atas = f"{config['base_url']}/{config['endpoint_atas']}"
        self.url_atas_detalhes = f"{config['base_url']}/{config['endpoint_atas_detalhes']}"
        self.qtd_atas = config['default']['qtd_atas']
        
    def extract(self) -> tuple[list[dict], dict]:
        """Extrai atas recentes do COPOM e seus detalhes.

        Returns:
            (dados, metadados):
                - Lista de dicionários com os detalhes das atas.
                - Dicionário de metadados da extração, incluindo URL,
                    parâmetros de consulta, quantidade de registros e timestamp.
        """
        atas, url = self.__extrair_atas(self.url_atas, self.qtd_atas)
        atas_detalhes = []
        with ThreadPoolExecutor(max_workers = min(4, len(atas))) as executor:
            atas_detalhes = list(
                executor.map(
                    lambda ata: self.__extrair_atas_detalhes(self.url_atas_detalhes, ata['nroReuniao']), 
                    atas
                )
            )
        metadata = {
            'url': url,
            'query_params': {
                'quantidade': self.qtd_atas
            },
            'record_count': len(atas_detalhes),
            'extracted_at': datetime.now().isoformat()
        }
        logger.info(f"Extraídas {len(atas_detalhes)} atas do COPOM")
        return atas_detalhes, metadata

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
        query_params = {
            'quantidade': qtd_atas
        }
        response = requests.get(url, params = query_params, timeout = 5)
        logger.debug(f"Requisição GET para {url} com params {query_params} retornou status {response.status_code}")
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
        return response.json()['conteudo']
    
