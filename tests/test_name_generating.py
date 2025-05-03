import os

from utils import get_unique_filename


def test_returns_original_filename_if_not_exists(tmp_path):
    file_path = get_unique_filename("config", "xml", str(tmp_path))
    assert file_path == os.path.join(tmp_path, "config.xml")


def test_returns_next_available_filename(tmp_path):
    (tmp_path / "config.xml").write_text("test")

    file_path = get_unique_filename("config", "xml", str(tmp_path))
    assert file_path == os.path.join(tmp_path, "config(1).xml")


def test_skips_existing_indexed_files(tmp_path):
    (tmp_path / "config.xml").write_text("original")
    (tmp_path / "config(1).xml").write_text("v1")
    (tmp_path / "config(2).xml").write_text("v2")

    file_path = get_unique_filename("config", "xml", str(tmp_path))
    assert file_path == os.path.join(tmp_path, "config(3).xml")


def test_handles_different_extensions_independently(tmp_path):
    (tmp_path / "config.xml").write_text("irrelevant")

    file_path = get_unique_filename("config", "json", str(tmp_path))
    assert file_path == os.path.join(tmp_path, "config.json")
