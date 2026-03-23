import pytest

from src.load.base_loader import BaseLoader


def test_base_loader_nao_pode_ser_instanciado() -> None:
    with pytest.raises(TypeError, match="load"):
        BaseLoader()

