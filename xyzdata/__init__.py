from .api import get_path, get_url, fetch  # noqa
from .data import data  # noqa
from .lib import Bunch, DataItem  # noqa

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("xyzdata")
except PackageNotFoundError:  # noqa
    # package is not installed
    pass
