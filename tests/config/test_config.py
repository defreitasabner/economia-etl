from src.config.config import Config
from src.config.models.dataset_config import DatasetConfig
from src.config.models.storage_config import StorageConfig


def test_read_storage_config_retorna_modelo_storage_config(tmp_path) -> None:
    config_file = tmp_path / "storage.yaml"
    config_file.write_text(
        """
bronze:
  output_path: data/bronze
  output_format: json
silver:
  input_path: data/bronze
  input_format: json
  output_path: data/silver
  output_format: parquet
""".strip()
    )

    config = Config()
    config._Config__config_dir_path = tmp_path

    storage_config = config.read_storage_config()

    assert isinstance(storage_config, StorageConfig)
    assert storage_config.bronze.output_path == "data/bronze"
    assert storage_config.silver.output_format == "parquet"


def test_read_dataset_config_retorna_modelo_dataset_config(tmp_path) -> None:
    dataset_file = tmp_path / "domains" / "bcb" / "selic.yaml"
    dataset_file.parent.mkdir(parents=True)
    dataset_file.write_text(
        """
extract:
  base_url: https://api.example.com
  endpoints:
    data: dados/serie/bcdata.sgs.11/dados
  params:
    formato: json
    data_inicial: 01/01/2020
    data_final: 31/12/2025
transform:
  transformers:
    - type: json_to_dataframe
      params: {}
load:
  partition_by: []
""".strip()
    )

    config = Config()
    config._Config__config_dir_path = tmp_path

    dataset_config = config.read_dataset_config("bcb", "selic")

    assert isinstance(dataset_config, DatasetConfig)
    assert dataset_config.extract.base_url == "https://api.example.com"
    assert dataset_config.transform.transformers[0].type == "json_to_dataframe"