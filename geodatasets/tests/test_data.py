import geopandas as gpd
import pandas as pd
import pytest

import geodatasets


@pytest.mark.request
@pytest.mark.parametrize("name", geodatasets.data.flatten())
def test_data_exists(name):
    dataset = geodatasets.data.query_name(name)
    gdf = gpd.read_file(geodatasets.get_path(name), engine="pyogrio")
    assert isinstance(gdf, pd.DataFrame)
    assert gdf.shape == (dataset.nrows, dataset.ncols)
    if not (
        ".csv" in dataset.filename
        or (
            hasattr(dataset, "members")
            and any(".csv" in member for member in dataset.members)
        )
    ):
        assert gdf.geom_type.str.endswith(dataset.geometry_type).all()
