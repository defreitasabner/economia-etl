import pandas as pd
import pytest

from src.infrastructure.readers.json_reader_strategy import JsonReaderStrategy
from src.infrastructure.readers.parquet_reader_strategy import ParquetReaderStrategy
from src.infrastructure.readers.reader_strategy_factory import ReaderStrategyFactory


def test_json_reader_strategy_read_retorna_lista_de_dict(tmp_path) -> None:
    filepath = tmp_path / "data.json"
    filepath.write_text('[{"id": 1, "valor": "a"}]')

    reader = JsonReaderStrategy()
    resultado = reader.read(filepath)

    assert resultado == [{"id": 1, "valor": "a"}]


def test_json_reader_strategy_read_lanca_erro_para_extensao_invalida(tmp_path) -> None:
    filepath = tmp_path / "data.txt"
    filepath.write_text('[{"id": 1}]')

    reader = JsonReaderStrategy()

    with pytest.raises(ValueError):
        reader.read(filepath)


def test_parquet_reader_strategy_read_retorna_dataframe(tmp_path) -> None:
    filepath = tmp_path / "data.parquet"
    esperado = pd.DataFrame([{"id": 1, "valor": "a"}])
    esperado.to_parquet(filepath, engine="pyarrow", index=False)

    reader = ParquetReaderStrategy()
    resultado = reader.read(filepath)

    pd.testing.assert_frame_equal(resultado, esperado)


def test_parquet_reader_strategy_read_lanca_erro_para_extensao_invalida(tmp_path) -> None:
    filepath = tmp_path / "data.csv"

    reader = ParquetReaderStrategy()

    with pytest.raises(ValueError):
        reader.read(filepath)


def test_reader_strategy_factory_create_json() -> None:
    reader = ReaderStrategyFactory.create("json")

    assert isinstance(reader, JsonReaderStrategy)


def test_reader_strategy_factory_create_parquet() -> None:
    reader = ReaderStrategyFactory.create("parquet")

    assert isinstance(reader, ParquetReaderStrategy)


def test_reader_strategy_factory_lanca_erro_para_formato_invalido() -> None:
    with pytest.raises(ValueError):
        ReaderStrategyFactory.create("csv")
