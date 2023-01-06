# xyzdata

Fetch links or download and cache spatial data example files.

## Install

While in the development, use `pip` from GitHub.

```sh
pip install git+https://github.com/martinfleis/xyzdata.git
```

## How to use

The package comes with a database of datasets. To see all:

```py
In [1]: import xyzdata

In [2]: xyzdata.data
Out[2]:
{'geoda': {'airbnb': {'url': 'https://geodacenter.github.io/data-and-lab//data/airbnb.zip',
   'license': 'CC-0',
   'attribution': 'GeoDa Data and Lab',
   'name': 'geoda.airbnb',
   'description': 'Airbnb rentals, socioeconomics, and crime in Chicago',
   'nrows': 77,
   'ncols': 20,
   'details': 'https://geodacenter.github.io/data-and-lab//airbnb/',
   'hash': 'a2ab1e3f938226d287dd76cde18c00e2d3a260640dd826da7131827d9e76c824',
   'filename': 'airbnb.zip'},
  'atlanta': {'url': 'https://geodacenter.github.io/data-and-lab//data/atlanta_hom.zip',
   'license': 'CC-0',
   'attribution': 'GeoDa Data and Lab',
   'name': 'geoda.atlanta',
   'description': 'Atlanta, GA region homicide counts and rates',
   'nrows': 90,
   'ncols': 23,
   'details': 'https://geodacenter.github.io/data-and-lab//atlanta_old/',
   'hash': 'missing',
   'filename': 'atlanta_hom.zip'},
   ...
```

You can get all the details exactly as you would with `xyzservices`. Only `query_name`
and `flatten` methods are available.

```py
In [3]: xyzdata.data.geoda.airbnb
Out[3]:
{'url': 'https://geodacenter.github.io/data-and-lab//data/airbnb.zip',
 'license': 'CC-0',
 'attribution': 'GeoDa Data and Lab',
 'name': 'geoda.airbnb',
 'description': 'Airbnb rentals, socioeconomics, and crime in Chicago',
 'nrows': 77,
 'ncols': 20,
 'details': 'https://geodacenter.github.io/data-and-lab//airbnb/',
 'hash': 'a2ab1e3f938226d287dd76cde18c00e2d3a260640dd826da7131827d9e76c824',
 'filename': 'airbnb.zip'}
```

Query:

```py
In [4]: xyzdata.data.query_name('geoda airbnb')
Out[4]:
{'url': 'https://geodacenter.github.io/data-and-lab//data/airbnb.zip',
 'license': 'CC-0',
 'attribution': 'GeoDa Data and Lab',
 'name': 'geoda.airbnb',
 'description': 'Airbnb rentals, socioeconomics, and crime in Chicago',
 'nrows': 77,
 'ncols': 20,
 'details': 'https://geodacenter.github.io/data-and-lab//airbnb/',
 'hash': 'a2ab1e3f938226d287dd76cde18c00e2d3a260640dd826da7131827d9e76c824',
 'filename': 'airbnb.zip'}
```

There is also convenient top-level API. One to get only the URL:

```py
In [6]: xyzdata.get_url("geoda airbnb")
Out[6]: 'https://geodacenter.github.io/data-and-lab//data/airbnb.zip'
```

And one to get the local path. If the file is not available in the cache, it will be
downloaded first.

```py
In [7]: xyzdata.get_path('geoda airbnb')
Out[7]: '/Users/martin/Library/Caches/xyzdata/airbnb.zip'
```
