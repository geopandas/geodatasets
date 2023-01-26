# geodatasets

Fetch links or download and cache spatial data example files.

## Install

While in the development, use `pip` from GitHub.

```sh
pip install git+https://github.com/martinfleis/geodatasets.git
```

## How to use

The package comes with a database of datasets. To see all:

```py
In [1]: import geodatasets

In [2]: geodatasets.data
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

There is also convenient top-level API. One to get only the URL:

```py
In [3]: geodatasets.get_url("geoda airbnb")
Out[3]: 'https://geodacenter.github.io/data-and-lab//data/airbnb.zip'
```

And one to get the local path. If the file is not available in the cache, it will be
downloaded first.

```py
Out[4]: '/Users/martin/Library/Caches/geodatasets/airbnb.zip'
In [4]: geodatasets.get_path('geoda airbnb')
```

You can also get all the details:

```py
In [5]: geodatasets.data.geoda.airbnb
Out[5]:
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

Or using the name query:

```py
In [6]: geodatasets.data.query_name('geoda airbnb')
Out[6]:
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
