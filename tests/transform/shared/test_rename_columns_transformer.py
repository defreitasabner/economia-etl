import pandas as pd

from src.transform.shared.rename_columns_transformer import RenameColumnsTransformer


def test_rename_columns_transformer_renomeia_colunas_com_sucesso() -> None:
    columns_to_rename = {
        "data_reuniao": "meeting_date",
        "numero_reuniao": "meeting_number",
    }
    transformer = RenameColumnsTransformer(columns_to_rename)

    df = pd.DataFrame(
        [
            {"data_reuniao": "2025-01-29", "numero_reuniao": 1},
            {"data_reuniao": "2025-03-19", "numero_reuniao": 2},
        ]
    )

    resultado = transformer.transform(df)

    assert list(resultado.columns) == ["meeting_date", "meeting_number"]
