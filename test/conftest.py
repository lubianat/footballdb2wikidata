import pytest
from pathlib import Path


@pytest.fixture
def sample_football_text():
    sample_path = Path(__file__).parent.joinpath("sample.txt")

    return sample_path.read_text()
