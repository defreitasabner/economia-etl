import pytest

from src.extract.extractor import Extractor


def test_extractor_nao_pode_ser_instanciado() -> None:
    with pytest.raises(TypeError, match="extract"):
        Extractor()
