import pkgutil

from .lib import _load_json

database = pkgutil.get_data("geodatasets", "json/database.json")

data = _load_json(database)
