import pandas as pd

from src.transform.shared.json_to_dataframe_transformer import JsonToDataframeTransformer


def test_json_to_dataframe_transformer_converte_lista_de_dict_para_dataframe() -> None:
    transformer = JsonToDataframeTransformer()

    data = [
        {"id": 1, "nome": "Ata 1", "objeto": {"chave": "valor"}},
        {"id": 2, "nome": "Ata 2", "objeto": {"chave": "valor"}},
    ]

    resultado = transformer.transform(data)

    esperado = pd.DataFrame(
        [
            {"id": 1, "nome": "Ata 1", "objeto.chave": "valor"},
            {"id": 2, "nome": "Ata 2", "objeto.chave": "valor"},
        ]
    )
    pd.testing.assert_frame_equal(resultado, esperado)
