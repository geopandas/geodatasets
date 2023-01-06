import importlib.resources

from . import json
from .lib import _load_json

json = importlib.resources.read_text(json, "providers.json")

data = _load_json(json)
