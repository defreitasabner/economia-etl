import logging


def configure_logging(debug: bool = False) -> None:
    """Configura o logging da aplicação.

    Args:
        debug: Se `True`, define o nível de logging como `DEBUG`. Caso contrário, `INFO`.
    """
    logging.basicConfig(
        level = logging.DEBUG if debug else logging.INFO,
        format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
