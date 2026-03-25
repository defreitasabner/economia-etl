from concurrent.futures import ThreadPoolExecutor
import logging
from datetime import datetime

import requests

from src.extract.extractor import Extractor
from src.core.extractor_registry import ExtractorRegistry


logger = logging.getLogger(__name__)

@ExtractorRegistry.register('comunicados')
class ComunicadosCopomExtractor(Extractor):
    """Extrator de comunicados do COPOM via API pública do Banco Central."""

    def __init__(self, config: dict) -> None:
        """Inicializa o extrator com a configuração da fonte COPOM.

        Args:
            config: Dicionário de configuração da extração contendo URLs
                e parâmetros padrão.
        """
        self.url_listar = config['url_listar']
        self.url_detalhes = config['url_detalhes']
        self.qtd_comunicados = config['qtd_comunicados']

    def extract(self) -> tuple[list[dict], dict]:
        """Extrai comunicados recentes do COPOM e seus detalhes.

        Returns:
            (dados, metadados):
                - Lista de dicionários com os detalhes dos comunicados.
                - Dicionário de metadados da extração, incluindo URL,
                    parâmetros de consulta, quantidade de registros e timestamp.
        """
        self.__validar_quantidade_comunicados(self.qtd_comunicados)

        comunicados, url = self.__extrair_comunicados(self.url_listar, self.qtd_comunicados)

        comunicados_detalhes = []
        if comunicados:
            with ThreadPoolExecutor(max_workers=min(4, len(comunicados))) as executor:
                comunicados_detalhes = list(
                    executor.map(
                        lambda comunicado: self.__extrair_comunicados_detalhes(
                            self.url_detalhes,
                            comunicado['nro_reuniao'],
                        ),
                        comunicados,
                    )
                )

        metadata = {
            'url': url,
            'query_params': {
                'quantidade': self.qtd_comunicados
            },
            'record_count': len(comunicados_detalhes),
            'extracted_at': datetime.now().isoformat()
        }
        logger.info(f"Extraídos {len(comunicados_detalhes)} comunicados do COPOM")
        return comunicados_detalhes, metadata

    def __validar_quantidade_comunicados(self, qtd_comunicados: int) -> None:
        """Valida a quantidade de comunicados a ser extraída.

        Args:
            qtd_comunicados: Quantidade de comunicados a ser extraída.

        Raises:
            ValueError: Se a quantidade de comunicados for menor ou igual a zero.
        """
        if qtd_comunicados <= 0:
            raise ValueError("A quantidade de comunicados deve ser maior que zero.")


    def __extrair_comunicados(self, url: str, qtd_comunicados: int) -> tuple[list[dict], str]:
        """Consulta a API para obter a lista de comunicados mais recentes.

        Args:
            url: URL da API para consulta dos comunicados.
            qtd_comunicados: Quantidade de comunicados a serem extraídos.

        Returns:
            (comunicados, url):
                - Lista de comunicados retornados pela API.
                - URL final da requisição (com query string).
        """
        query_params = {
            'quantidade': qtd_comunicados
        }
        response = requests.get(url, params = query_params, timeout = 5)
        logger.debug(f"Requisição GET para {url} com params {query_params} retornou status {response.status_code}")
        return response.json()['conteudo'], response.url

    def __extrair_comunicados_detalhes(self, url: str, nro_reuniao: str) -> dict:
        """Consulta a API para obter os detalhes de um comunicado do COPOM.

        Args:
            url: URL da API para consulta dos detalhes do comunicado.
            nro_reuniao: Número da reunião do comunicado.

        Returns:
            comunicados_detalhes: Dicionário com os detalhes do comunicado solicitado.
        """
        query_params = {
            'nro_reuniao': nro_reuniao
        }
        response = requests.get(url, params = query_params, timeout = 5)
        logger.debug(f"Requisição GET para {url} com params {query_params} retornou status {response.status_code}")
        return response.json()['conteudo'][0]
