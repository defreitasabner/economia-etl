import pytest

from src.load.loader import Loader


def test_loader_nao_pode_ser_instanciado() -> None:
    with pytest.raises(TypeError, match="load"):
        Loader()

