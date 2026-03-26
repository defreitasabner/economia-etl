import pandas as pd
import pytest

from src.transform.shared.select_columns_transformer import SelectColumnsTransformer


def test_select_columns_transformer_seleciona_colunas_com_sucesso() -> None:
    selected_columns = ["data_reuniao", "numero_reuniao"]
    transformer = SelectColumnsTransformer(selected_columns)

    df = pd.DataFrame(
        [
            {"data_reuniao": "2025-01-29", "numero_reuniao": 1, "conteudo": "texto 1"},
            {"data_reuniao": "2025-03-19", "numero_reuniao": 2, "conteudo": "texto 2"},
        ]
    )

    resultado = transformer.transform(df)

    esperado = pd.DataFrame(
        [
            {"data_reuniao": "2025-01-29", "numero_reuniao": 1},
            {"data_reuniao": "2025-03-19", "numero_reuniao": 2},
        ]
    )
    pd.testing.assert_frame_equal(resultado, esperado)


def test_select_columns_transformer_lanca_erro_quando_coluna_nao_existe() -> None:
    selected_columns = ["data_reuniao", "coluna_inexistente"]
    transformer = SelectColumnsTransformer(selected_columns)

    df = pd.DataFrame(
        [
            {"data_reuniao": "2025-01-29", "numero_reuniao": 1},
        ]
    )

    with pytest.raises(KeyError):
        transformer.transform(df)
