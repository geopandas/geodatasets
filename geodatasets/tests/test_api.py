import os
from pathlib import Path

import pooch
import pytest
import geodatasets


def test_get_url():
    url = geodatasets.get_url("nybb")
    assert (
        url
        == "https://data.cityofnewyork.us/api/geospatial/tqmj-j8zm?method=export&format=Original"  # noqa
    )


@pytest.mark.request
def test_get_path():
    in_cache = pooch.os_cache("geodatasets").joinpath("nybb_22c.zip")
    if Path(in_cache).exists():
        os.remove(in_cache)

    assert Path(geodatasets.get_path("nybb")).exists()

    # cleanup
    os.remove(in_cache)


@pytest.mark.request
def test_fetch():
    # clear cache
    for data in ["airbnb.zip", "nybb_22c.zip", "nyc_neighborhoods.zip"]:
        in_cache = pooch.os_cache("geodatasets").joinpath(data)
        if Path(in_cache).exists():
            os.remove(in_cache)

    geodatasets.fetch("nybb")
    assert pooch.os_cache("geodatasets").joinpath("nybb_22c.zip").exists()

    geodatasets.fetch(["geoda airbnb", "geoda atlanta"])

    for data in ["airbnb.zip", "atlanta_hom.zip"]:
        assert pooch.os_cache("geodatasets").joinpath(data).exists()

    # cleanup
    for data in ["airbnb.zip", "nybb_22c.zip", "atlanta_hom.zip"]:
        in_cache = pooch.os_cache("geodatasets").joinpath(data)
        os.remove(in_cache)
