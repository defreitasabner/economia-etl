import argparse

from src.pipelines.bcb.atas import extrair_atas_copom


def register_commands(domain_parsers: argparse._SubParsersAction) -> None:
    """Registra os comandos do domínio COPOM.

    Args:
        domain_parsers: Coleção de subcomandos do parser principal.
    """
    parser_bcb = domain_parsers.add_parser('bcb', help='Pipelines do domínio BCB')
    dataset_parsers = parser_bcb.add_subparsers(dest='dataset', required=True)

    parser_atas = dataset_parsers.add_parser('atas', help='Pipelines do dataset atas')
    tier_parsers = parser_atas.add_subparsers(dest='tier', required=True)

    parser_bronze = tier_parsers.add_parser('bronze', help='Extrai atas do COPOM para a camada bronze')
    parser_bronze.add_argument(
        '--qtd-atas',
        type = int,
        default = None,
        help = 'Quantidade de atas para extração (sobrescreve o valor do config)',
    )
    parser_bronze.set_defaults(handler=_run_copom_atas_bronze)


def _run_copom_atas_bronze(args: argparse.Namespace) -> None:
    extrair_atas_copom(qtd_atas=args.qtd_atas)
