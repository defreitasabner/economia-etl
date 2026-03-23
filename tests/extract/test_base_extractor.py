import pytest

from src.extract.base_extractor import BaseExtractor


def test_base_extractor_nao_pode_ser_instanciado() -> None:
    with pytest.raises(TypeError, match="extract"):
        BaseExtractor()
