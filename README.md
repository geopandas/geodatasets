# geodatasets

Fetch links or download and cache spatial data example files.

The `geodatasets` contains an API on top of a JSON with metadata of externally hosted
datasets containing geospatial information useful for illustrative and educational
purposes.

See the documentation at [geodatasets.readthedocs.io/](https://geodatasets.readthedocs.io/).

## Install

From PyPI:

```sh
pip install geodatasets
```

or using `conda` or `mamba` from conda-forge:

```sh
conda install geodatasets -c conda-forge
```

The development version can be installed using `pip` from GitHub.

```sh
pip install git+https://github.com/geopandas/geodatasets.git
```

## How to use

The package comes with a database of datasets. To see all:

```py
In [1]: import geodatasets

In [2]: geodatasets.data
Out[2]:
{'geoda': {'airbnb': {'url': 'https://geodacenter.github.io/data-and-lab//data/airbnb.zip',
   'license': 'NA',
   'attribution': 'Center for Spatial Data Science, University of Chicago',
   'name': 'geoda.airbnb',
   'description': 'Airbnb rentals, socioeconomics, and crime in Chicago',
   'geometry_type': 'Polygon',
   'nrows': 77,
   'ncols': 21,
   'details': 'https://geodacenter.github.io/data-and-lab//airbnb/',
   'hash': 'a2ab1e3f938226d287dd76cde18c00e2d3a260640dd826da7131827d9e76c824',
   'filename': 'airbnb.zip'},
  'atlanta': {'url': 'https://geodacenter.github.io/data-and-lab//data/atlanta_hom.zip',
   'license': 'NA',
   'attribution': 'Center for Spatial Data Science, University of Chicago',
   'name': 'geoda.atlanta',
   'description': 'Atlanta, GA region homicide counts and rates',
   'geometry_type': 'Polygon',
   'nrows': 90,
   'ncols': 24,
   'details': 'https://geodacenter.github.io/data-and-lab//atlanta_old/',
   'hash': 'a33a76e12168fe84361e60c88a9df4856730487305846c559715c89b1a2b5e09',
   'filename': 'atlanta_hom.zip',
   'members': ['atlanta_hom/atl_hom.geojson']},
   ...
```

There is also a convenient top-level API. One to get only the URL:

```py
In [3]: geodatasets.get_url("geoda airbnb")
Out[3]: 'https://geodacenter.github.io/data-and-lab//data/airbnb.zip'
```

And one to get the local path. If the file is not available in the cache, it will be
downloaded first.

```py
In [4]: geodatasets.get_path('geoda airbnb')
Out[4]: '/Users/martin/Library/Caches/geodatasets/airbnb.zip'
```

You can also get all the details:

```py
In [5]: geodatasets.data.geoda.airbnb
Out[5]:
{'url': 'https://geodacenter.github.io/data-and-lab//data/airbnb.zip',
 'license': 'NA',
 'attribution': 'Center for Spatial Data Science, University of Chicago',
 'name': 'geoda.airbnb',
 'description': 'Airbnb rentals, socioeconomics, and crime in Chicago',
 'geometry_type': 'Polygon',
 'nrows': 77,
 'ncols': 21,
 'details': 'https://geodacenter.github.io/data-and-lab//airbnb/',
 'hash': 'a2ab1e3f938226d287dd76cde18c00e2d3a260640dd826da7131827d9e76c824',
 'filename': 'airbnb.zip'}
```

Or using the name query:

```py
In [6]: geodatasets.data.query_name('geoda airbnb')
Out[6]:
{'url': 'https://geodacenter.github.io/data-and-lab//data/airbnb.zip',
 'license': 'NA',
 'attribution': 'Center for Spatial Data Science, University of Chicago',
 'name': 'geoda.airbnb',
 'description': 'Airbnb rentals, socioeconomics, and crime in Chicago',
 'geometry_type': 'Polygon',
 'nrows': 77,
 'ncols': 21,
 'details': 'https://geodacenter.github.io/data-and-lab//airbnb/',
 'hash': 'a2ab1e3f938226d287dd76cde18c00e2d3a260640dd826da7131827d9e76c824',
 'filename': 'airbnb.zip'}
```

The whole structure `Bunch` class is based on a dictionary and can be flattened. If you want
to see all available datasets, you can use:

```py
In [7]: geodatasets.data.flatten().keys()
Out[7]: dict_keys(['geoda.airbnb', 'geoda.atlanta', 'geoda.cars', 'geoda.charleston1', 'geoda.charleston2', 'geoda.chicago_health', 'geoda.chicago_commpop', 'geoda.chile_labor', 'geoda.cincinnati', 'geoda.cleveland', 'geoda.columbus', 'geoda.grid100', 'geoda.groceries', 'geoda.guerry', 'geoda.health', 'geoda.health_indicators', 'geoda.hickory1', 'geoda.hickory2', 'geoda.home_sales', 'geoda.houston', 'geoda.juvenile', 'geoda.lansing1', 'geoda.lansing2', 'geoda.lasrosas', 'geoda.liquor_stores', 'geoda.malaria', 'geoda.milwaukee1', 'geoda.milwaukee2', 'geoda.ncovr', 'geoda.natregimes', 'geoda.ndvi', 'geoda.nepal', 'geoda.nyc', 'geoda.nyc_earnings', 'geoda.nyc_education', 'geoda.nyc_neighborhoods', 'geoda.orlando1', 'geoda.orlando2', 'geoda.oz9799', 'geoda.phoenix_acs', 'geoda.police', 'geoda.sacramento1', 'geoda.sacramento2', 'geoda.savannah1', 'geoda.savannah2', 'geoda.seattle1', 'geoda.seattle2', 'geoda.sids', 'geoda.sids2', 'geoda.south', 'geoda.spirals', 'geoda.stlouis', 'geoda.tampa1', 'geoda.us_sdoh', 'ny.bb', 'eea.large_rivers', 'naturalearth.land'])
```
