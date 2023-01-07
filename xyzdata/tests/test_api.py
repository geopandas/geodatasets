import xyzdata
import os
import pooch
from pathlib import Path


def test_get_url():
    url = xyzdata.get_url("nybb")
    assert (
        url
        == "https://data.cityofnewyork.us/api/geospatial/tqmj-j8zm?method=export&format=Original"
    )


def test_get_path():
    in_cache = pooch.os_cache("xyzdata").joinpath("nybb_22c.zip")
    if Path(in_cache).exists():
        os.remove(in_cache)

    path = Path(xyzdata.get_path("nybb"))
    assert path.exists()

    os.remove(in_cache)
