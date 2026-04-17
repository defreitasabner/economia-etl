import logging
from concurrent.futures import ThreadPoolExecutor
import math

import requests
from datetime import datetime, timedelta

from src.config.models.dataset_config import ExtractorConfig
from src.extract.extractor import Extractor
from src.extract.extractor_registry import ExtractorRegistry


logger = logging.getLogger(__name__)

@ExtractorRegistry.register('sgs')
class SgsExtractor(Extractor):

    def __init__(self, config: ExtractorConfig) -> None:
        self.__periodicidade_diaria = config.params.periodicidade_diaria
        self.__url = config.params.request.url
        self.__query_params = config.params.request.query_params

    def extract(self) -> tuple[list[dict], dict]:
        data_inicial = datetime.strptime(self.__query_params['dataInicial'], '%d/%m/%Y').date()
        data_final = datetime.strptime(self.__query_params['dataFinal'], '%d/%m/%Y').date()
        
        if data_inicial > data_final:
            raise ValueError("dataInicial deve ser anterior a dataFinal")
        
        anos_entre_datas = (data_final.year - data_inicial.year) + 1
        if self.__periodicidade_diaria and anos_entre_datas > 10:
            logger.info(f"Período entre dataInicial e dataFinal é de {anos_entre_datas} anos e é de periodicidade diária. Realizando extração em blocos de 10 anos para evitar timeouts.")
            qtd_blocos_10_anos = math.ceil(anos_entre_datas / 10)
            blocos_anos = list()
            for i in range(qtd_blocos_10_anos):
                bloco_data_inicial = datetime(data_inicial.year + (i * 10), 1, 1).date()
                bloco_data_final = datetime(data_inicial.year + (((i + 1) * 10) - 1), 12, 31).date()
                bloco = {
                    'data_inicial': bloco_data_inicial.strftime('%d/%m/%Y'),
                    'data_final': bloco_data_final.strftime('%d/%m/%Y')
                }
                blocos_anos.append(bloco)
            blocos_anos[0]['data_inicial'] = data_inicial.strftime('%d/%m/%Y')
            blocos_anos[-1]['data_final'] = data_final.strftime('%d/%m/%Y')
            with ThreadPoolExecutor(max_workers = min(4, len(blocos_anos))) as executor:
                responses = list(executor.map(lambda bloco: self.__request_data(
                    formato = self.__query_params['formato'],
                    data_inicial = bloco['data_inicial'],
                    data_final = bloco['data_final']
                ), blocos_anos))
            data = []
            for response in responses:
                data.extend(response.json())
            urls = [response.url for response in responses]
        
        else:
            logger.info(f"Período entre dataInicial e dataFinal é de {anos_entre_datas} anos, mas não é de periodicidade diária. Realizando extração em um único bloco.")
            response = self.__request_data(
                formato = self.__query_params['formato'],
                data_inicial = self.__query_params['dataInicial'],
                data_final = self.__query_params['dataFinal']
            )
            data = response.json()
            urls = [response.url]
        metadata = {
            'urls': urls,
            'query_params': self.__query_params,
            'record_count': len(data),
        }

        return data, metadata
    
    def __request_data(self, formato: str, data_inicial: str, data_final: str) -> requests.Response:
        query_params = {
            'formato': formato,
            'dataInicial': data_inicial,
            'dataFinal': data_final
        }
        response = requests.get(self.__url, params = query_params, timeout = 10)
        response.raise_for_status()
        return response