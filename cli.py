import argparse

from src.utils import log
from src.pipelines.run_pipeline import run_pipeline


def main():
    parser = argparse.ArgumentParser(description = 'Executar ETL pipeline')
    parser.add_argument('--debug', action = 'store_true', help = 'Habilitar modo debug para logging detalhado')
    parser.add_argument('--domain', type = str, required = True, help = 'Domínio para execução do pipeline')
    parser.add_argument('--dataset', type = str, required = True, help = 'Dataset para execução do pipeline')
    parser.add_argument('--tier', type = str, required = True, help = 'Camada para execução do pipeline (ex: bronze, silver, gold)')


    args = parser.parse_args()
    log.configure_logging(debug = args.debug)

    run_pipeline(domain_name = args.domain, dataset_name = args.dataset, tier = args.tier)

if __name__ == '__main__':
    main()
