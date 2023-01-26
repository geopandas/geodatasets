import pooch

from .data import data

flat = data.flatten()

registry = {value["filename"]: value["hash"] for value in flat.values()}
urls = {value["filename"]: value["url"] for value in flat.values()}

CACHE = pooch.create(
    path=pooch.os_cache("geodatasets"), base_url="", registry=registry, urls=urls
)


def get_url(name):
    """Get the URL from which the dataset can be fetched.

    ``name`` is queried using :meth:`~geodatasets.Bunch.query_name`, so it only needs to
    contain the same letters in the same order as the item's name irrespective
    of the letter case, spaces, dashes and other characters.

    No data is downloaded.

    Parameters
    ----------
    name : str
        Name of the data item. Formatting does not matter.

    Returns
    -------
    str
        link to the online dataset

    See also
    --------
    get_path

    Examples
    --------
    >>> geodatasets.get_url('GeoDa AirBnB')
    'https://geodacenter.github.io/data-and-lab//data/airbnb.zip'

    >>> geodatasets.get_url('geoda_airbnb')
    'https://geodacenter.github.io/data-and-lab//data/airbnb.zip'
    """
    return data.query_name(name).url


def get_path(name):
    """Get the absolute path to a file in the local storage.

    If it’s not in the local storage, it will be downloaded.

    ``name`` is queried using :meth:`~geodatasets.Bunch.query_name`, so it only needs to
    contain the same letters in the same order as the item's name irrespective
    of the letter case, spaces, dashes and other characters.

    Parameters
    ----------
    name : str
        Name of the data item. Formatting does not matter.

    See also
    --------
    get_url
    fetch

    Examples
    --------
    When it does not exist in the cache yet, it gets downloaded first:

    >>> path = geodatasets.get_path('GeoDa AirBnB')
    Downloading file 'airbnb.zip' from 'https://geodacenter.github.io/data-and-lab/\
/data/airbnb.zip' to '/Users/martin/Library/Caches/geodatasets'.
    >>> path
    '/Users/martin/Library/Caches/geodatasets/airbnb.zip'

    Every other call returns the path directly:

    >>> path2 = geodatasets.get_path("geoda_airbnb")
    >>> path2
    '/Users/martin/Library/Caches/geodatasets/airbnb.zip'
    """
    return CACHE.fetch(data.query_name(name).filename)


def fetch(name):
    """Download the data to the local storage.

    This is useful when it is expected that some data will be needed later but you
    want to avoid download at that time.

    ``name`` is queried using :meth:`~geodatasets.Bunch.query_name`, so it only needs to
    contain the same letters in the same order as the item's name irrespective
    of the letter case, spaces, dashes and other characters.

    Parameters
    ----------
    name : str, list
        Name of the data item(s). Formatting does not matter.

    See also
    --------
    get_path

    Examples
    --------
    >>> geodatasets.fetch('nybb')
    Downloading file 'nybb_22c.zip' from 'https://data.cityofnewyork.us/api/geospatial/\
tqmj-j8zm?method=export&format=Original' to '/Users/martin/Library/Caches/geodatasets'.

    >>> geodatasets.fetch(['geoda airbnb', 'geoda guerry'])
    Downloading file 'airbnb.zip' from 'https://geodacenter.github.io/data-and-lab//dat\
a/airbnb.zip' to '/Users/martin/Library/Caches/geodatasets'.
    Downloading file 'guerry.zip' from 'https://geodacenter.github.io/data-and-lab//dat\
a/guerry.zip' to '/Users/martin/Library/Caches/geodatasets'.

    """
    if isinstance(name, str):
        name = [name]

    for n in name:
        _ = CACHE.fetch(data.query_name(n).filename)
