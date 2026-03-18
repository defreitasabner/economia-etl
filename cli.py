import argparse

from src.utils import log
from src.cli.commands import copom


def main():
    parser = argparse.ArgumentParser(description = 'Executar ETL pipeline')
    domain_parsers = parser.add_subparsers(dest = 'domain', required = True)

    copom.register_commands(domain_parsers)

    args = parser.parse_args()
    log.configure_logging(debug = False)
    args.handler(args)


if __name__ == '__main__':
    main()
