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
    
def load_dataset_config(domain: str, dataset: str) -> dict:
    """Carrega as configurações de uma fonte de dados específica.

    Args:
        domain: O domínio da fonte de dados (ex: 'economia', 'financeiro').
        dataset: O nome do dataset específico dentro do domínio.

    Returns:
        configurações: Dicionário contendo as configurações da fonte de dados específica.
    """
    return load_config(f"domains/{domain}/{dataset}.yaml")

def load_storage_config(tier: str) -> dict:
    """Carrega as configurações de armazenamento para um nível específico.

    Args:
        tier: O nível de armazenamento (ex: 'bronze', 'silver', 'gold').

    Returns:
        configurações: Dicionário contendo as configurações de armazenamento para o nível específico.
    """
    return load_config('storage.yaml')[tier]
