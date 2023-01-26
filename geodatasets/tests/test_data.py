from pathlib import Path

import pooch
import pytest

import geodatasets


@pytest.mark.request
@pytest.mark.parametrize("name", geodatasets.data.flatten())
def test_data_exists(name):
    dataset = geodatasets.data.query_name(name)
    path = pooch.retrieve(dataset["url"], known_hash=dataset["hash"])
    assert Path(path).exists()
