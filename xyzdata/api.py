import pooch

from .data import data

flat = data.flatten()

registry = {value["filename"]: value["hash"] for value in flat.values()}
urls = {value["filename"]: value["url"] for value in flat.values()}

CACHE = pooch.create(
    path=pooch.os_cache("xyzdata"), base_url="", registry=registry, urls=urls
)


def get_url(name):
    """Short function for convenience

    Parameters
    ----------
    name : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    return data.query_name(name).url


def get_path(name):
    """Download file and get its local path

    Parameters
    ----------
    name : _type_
        _description_
    """
    return CACHE.fetch(data.query_name(name).filename)


def fetch(name):
    """_summary_

    Parameters
    ----------
    name : _type_
        _description_
    """
    if isinstance(name, str):
        name = [name]

    for n in name:
        _ = CACHE.fetch(data.query_name(n).filename)
