import pandas as pd

from src.transform.shared.html_to_text_transformer import HtmlToTextTransformer


def test_html_to_text_transformer_com_target_html_id_extrai_texto_do_elemento() -> None:
    transformer = HtmlToTextTransformer(
        target_column="html",
        result_column="texto",
        target_html_id="alvo",
    )

    df = pd.DataFrame(
        [
            {"html": "<div id='alvo'>Ata 1</div><div id='outro'>Ignorar</div>"},
            {"html": "<div id='alvo'>Ata 2</div><p>Ignorar</p>"},
        ]
    )

    resultado = transformer.transform(df.copy())

    esperado = pd.DataFrame(
        [
            {"html": "<div id='alvo'>Ata 1</div><div id='outro'>Ignorar</div>", "texto": "Ata 1"},
            {"html": "<div id='alvo'>Ata 2</div><p>Ignorar</p>", "texto": "Ata 2"},
        ]
    )
    pd.testing.assert_frame_equal(resultado, esperado)


def test_html_to_text_transformer_sem_target_html_id_extrai_todo_texto() -> None:
    transformer = HtmlToTextTransformer(
        target_column="html",
        result_column="texto",
    )

    df = pd.DataFrame(
        [
            {"html": "<div>Ata 1</div>"},
            {"html": "<p>Ata 2</p>"},
        ]
    )

    resultado = transformer.transform(df.copy())

    esperado = pd.DataFrame(
        [
            {"html": "<div>Ata 1</div>", "texto": "Ata 1"},
            {"html": "<p>Ata 2</p>", "texto": "Ata 2"},
        ]
    )
    pd.testing.assert_frame_equal(resultado, esperado)
