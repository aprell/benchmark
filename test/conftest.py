import pytest

from pathlib import Path


@pytest.fixture
def test_dir():
    return Path(__file__).parent


@pytest.fixture
def config_input_dir(test_dir):
    return test_dir / "config.input"


@pytest.fixture(autouse=True)
def chdir_test(test_dir, monkeypatch):
    monkeypatch.chdir(test_dir)
