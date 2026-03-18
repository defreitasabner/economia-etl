import yaml
from pathlib import Path


CONFIG_DIR_NAME = 'config'
CONFIG_DIR_PATH = Path(__file__).parent.parent.parent / CONFIG_DIR_NAME


def load_config(filepath: str) -> dict:
    """Carrega um arquivo de configuração YAML.

    Args:
        filepath: Caminho relativo do arquivo de configuração dentro do diretório CONFIG_DIR_PATH.

    Returns:
        configurações: Dicionário contendo as configurações carregadas do arquivo YAML.
    """
    with open(CONFIG_DIR_PATH / filepath, 'r') as file:
        return yaml.safe_load(file)
    
