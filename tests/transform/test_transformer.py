import pytest

from src.transform.transformer import Transformer


def test_transformer_nao_pode_ser_instanciado() -> None:
    with pytest.raises(TypeError, match="transform"):
        Transformer()
