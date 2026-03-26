import json

import pandas as pd
import pytest

from src.infrastructure.writers.json_writer_strategy import JsonWriterStrategy
from src.infrastructure.writers.parquet_writer_strategy import ParquetWriterStrategy
from src.infrastructure.writers.writer_strategy_factory import WriterStrategyFactory


def test_json_writer_strategy_write_persiste_json(tmp_path) -> None:
    filepath = tmp_path / "data.json"
    data = [{"id": 1, "valor": "a"}]

    writer = JsonWriterStrategy()
    writer.write(data, filepath)

    with open(filepath, "r") as file:
        salvo = json.load(file)

    assert salvo == data


def test_json_writer_strategy_write_lanca_erro_para_extensao_invalida(tmp_path) -> None:
    filepath = tmp_path / "data.txt"

    writer = JsonWriterStrategy()

    with pytest.raises(ValueError, match="terminar com '.json'"):
        writer.write({"id": 1}, filepath)


def test_parquet_writer_strategy_write_persiste_parquet(tmp_path) -> None:
    filepath = tmp_path / "data.parquet"
    data = pd.DataFrame([{"id": 1, "valor": "a"}])

    writer = ParquetWriterStrategy()
    writer.write(data, filepath)

    resultado = pd.read_parquet(filepath, engine="pyarrow")
    pd.testing.assert_frame_equal(resultado, data)


def test_parquet_writer_strategy_write_lanca_erro_para_extensao_invalida(tmp_path) -> None:
    filepath = tmp_path / "data.csv"
    data = pd.DataFrame([{"id": 1}])

    writer = ParquetWriterStrategy()

    with pytest.raises(ValueError):
        writer.write(data, filepath)


def test_parquet_writer_strategy_write_lanca_erro_para_tipo_invalido(tmp_path) -> None:
    filepath = tmp_path / "data.parquet"

    writer = ParquetWriterStrategy()

    with pytest.raises(TypeError):
        writer.write([{"id": 1}], filepath)


def test_writer_strategy_factory_create_json() -> None:
    writer = WriterStrategyFactory.create("json")

    assert isinstance(writer, JsonWriterStrategy)


def test_writer_strategy_factory_create_parquet() -> None:
    writer = WriterStrategyFactory.create("parquet")

    assert isinstance(writer, ParquetWriterStrategy)


def test_writer_strategy_factory_lanca_erro_para_formato_invalido() -> None:
    with pytest.raises(ValueError):
        WriterStrategyFactory.create("csv")
