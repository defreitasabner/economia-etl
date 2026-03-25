from pathlib import Path

from src.infrastructure.file_path_builder import FilePathBuilder


def test_build_path_returns_expected_filepath(tmp_path: Path) -> None:
    builder = FilePathBuilder(
        storage_tier_path=str(tmp_path),
        domain="bcb",
        dataset="selic",
        storage_format="json",
    )

    filepath = builder.build_path()

    expected = tmp_path / "bcb" / "selic" / "data.json"
    assert filepath == str(expected)


def test_build_path_creates_directory_structure(tmp_path: Path) -> None:
    builder = FilePathBuilder(
        storage_tier_path=str(tmp_path),
        domain="bcb",
        dataset="atas",
    )

    filepath = builder.build_path()

    assert (tmp_path / "bcb" / "atas").is_dir()
    assert Path(filepath).parent == tmp_path / "bcb" / "atas"


def test_build_path_uses_default_json_format(tmp_path: Path) -> None:
    builder = FilePathBuilder(
        storage_tier_path=str(tmp_path),
        domain="bcb",
        dataset="comunicados",
    )

    filepath = builder.build_path()

    assert filepath.endswith("data.json")


def test_build_path_accepts_custom_storage_format(tmp_path: Path) -> None:
    builder = FilePathBuilder(
        storage_tier_path=str(tmp_path),
        domain="bcb",
        dataset="comunicados",
        storage_format="parquet",
    )

    filepath = builder.build_path()

    expected = tmp_path / "bcb" / "comunicados" / "data.parquet"
    assert filepath == str(expected)


def test_build_path_accepts_partition_by_without_changing_path(tmp_path: Path) -> None:
    builder = FilePathBuilder(
        storage_tier_path=str(tmp_path),
        domain="bcb",
        dataset="comunicados",
        partition_by=["ano", "mes"],
    )

    filepath = builder.build_path()

    expected = tmp_path / "bcb" / "comunicados" / "data.json"
    assert filepath == str(expected)
