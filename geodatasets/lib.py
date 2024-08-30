"""
Utilities to support geodatasets

Heavily based on top of geodatasets (Copyright (c) 2021, GeoPandas) licensed
under BSD 3-clause
"""
from __future__ import annotations

import json
import uuid
from typing import Callable

import pooch

GEOMETRY_TYPES = ["POINT", "LINESTRING", "POLYGON", "MIXED"]
QUERY_NAME_TRANSLATION = str.maketrans({x: "" for x in "., -_/"})


class Bunch(dict):
    """A dict with attribute-access

    :class:`Bunch` is used to store :class:`Dataset` objects.
    """

    def __getattr__(self, key):
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(key)

    def __dir__(self):
        return self.keys()

    def _repr_html_(self, inside=False):
        children = ""
        for key in self.keys():
            if isinstance(self[key], Dataset):
                obj = "geodatasets.Dataset"
            else:
                obj = "geodatasets.Bunch"
            uid = str(uuid.uuid4())
            children += f"""
            <li class="xyz-child">
                <input type="checkbox" id="{uid}" class="xyz-checkbox"/>
                <label for="{uid}">{key} <span>{obj}</span></label>
                <div class="xyz-inside">
                    {self[key]._repr_html_(inside=True)}
                </div>
            </li>
            """

        style = "" if inside else f"<style>{CSS_STYLE}</style>"
        html = f"""
        <div>
        {style}
            <div class="xyz-wrap">
                <div class="xyz-header">
                    <div class="xyz-obj">geodatasets.Bunch</div>
                    <div class="xyz-name">{len(self)} items</div>
                </div>
                <div class="xyz-details">
                    <ul class="xyz-collapsible">
                        {children}
                    </ul>
                </div>
            </div>
        </div>
        """

        return html

    def flatten(self) -> dict:
        """Return the nested :class:`Bunch` collapsed into the one level dictionary.

        Dictionary keys are :class:`Dataset` names (e.g. ``geoda.airbnb``)
        and its values are :class:`Dataset` objects.

        Returns
        -------
        flattened : dict
            dictionary of :class:`Dataset` objects
        """

        flat = {}

        def _get_items(item):
            if isinstance(item, Dataset):
                flat[item.name] = item
            else:
                for prov in item.values():
                    _get_items(prov)

        _get_items(self)

        return flat

    def query_name(self, name: str) -> Dataset:
        """Return :class:`Dataset` based on the name query

        Returns a matching :class:`Dataset` from the :class:`Bunch` if the ``name``
        contains the same letters in the same order as the item's name irrespective
        of the letter case, spaces, dashes and other characters.
        See examples for details.

        Parameters
        ----------
        name : str
            Name of the data item. Formatting does not matter.

        Returns
        -------
        match: Dataset
        """
        xyz_flat_lower = {
            k.translate(QUERY_NAME_TRANSLATION).lower(): v
            for k, v in self.flatten().items()
        }
        name_clean = name.translate(QUERY_NAME_TRANSLATION).lower()
        if name_clean in xyz_flat_lower:
            return xyz_flat_lower[name_clean]

        raise ValueError(f"No matching item found for the query '{name}'.")

    def filter(
        self,
        keyword: str | None = None,
        name: str | None = None,
        geometry_type: str | None = None,
        function: Callable[[Dataset], bool] = None,
    ) -> Bunch:
        """Return a subset of the :class:`Bunch` matching the filter conditions

        Each :class:`Dataset` within a :class:`Bunch` is checked against one or
        more specified conditions and kept if they are satisfied or removed if at least
        one condition is not met.

        Parameters
        ----------
        keyword : str (optional)
            Condition returns ``True`` if ``keyword`` string is present in any string
            value in a :class:`Dataset` object.
            The comparison is not case sensitive.
        name : str (optional)
            Condition returns ``True`` if ``name`` string is present in
            the name attribute of :class:`Dataset` object.
            The comparison is not case sensitive.
        geometry_type : str (optional)
            Condition returns ``True`` if :meth:`Dataset.geometry_type` is
            matches the ``geometry_type``.
            Possible options are ``["Point", "LineString", "Polygon", "Mixed"]``.
            The comparison is not case sensitive.
        function : callable (optional)
            Custom function taking :class:`Dataset` as an argument and returns
            bool. If ``function`` is given, other parameters are ignored.

        Returns
        -------
        filtered : Bunch

        Examples
        --------
        >>> from geodatasets import data

        You can filter all Point datasets:

        >>> points = data.filter(geometry_type="Point")

        Or all datasets with ``chicago`` in the name:

        >>> chicago_datasets = data.filter(name="chicago")

        You can use keyword search to find all datasets in a CSV format:

        >>> csv_datasets = data.filter(keyword="csv")

        You can combine multiple conditions to find datasets based with ``chicago`` in
        name of Polygon geometry type:

        >>> chicago_polygons = data.filter(name="chicago", geometry_type="Polygon")

        You can also pass custom function that takes :class:`Dataset` and returns
        boolean value. You can then find all datasets with ``nrows`` smaller than
        100:

        >>> def small_data(dataset):
        ...    if hasattr(dataset, "nrows") and dataset.nrows < 100:
        ...        return True
        ...    return False
        >>> small = data.filter(function=small_data)
        """

        def _validate(dataset, keyword, name, geometry_type):
            cond = []

            if keyword is not None:
                keyword_match = False
                for v in dataset.values():
                    if isinstance(v, str) and keyword.lower() in v.lower():
                        keyword_match = True
                        break
                cond.append(keyword_match)

            if name is not None:
                name_match = False
                if name.lower() in dataset.name.lower():
                    name_match = True
                cond.append(name_match)

            if geometry_type is not None:
                geom_type_match = False
                if (
                    dataset.geometry_type.upper()
                    == geometry_type.translate(QUERY_NAME_TRANSLATION).upper()
                ):
                    geom_type_match = True
                cond.append(geom_type_match)

            return all(cond)

        def _filter_bunch(bunch, keyword, name, geometry_type, function):
            new = Bunch()
            for key, value in bunch.items():
                if isinstance(value, Dataset):
                    if function is None:
                        if _validate(
                            value,
                            keyword=keyword,
                            name=name,
                            geometry_type=geometry_type,
                        ):
                            new[key] = value
                    else:
                        if function(value):
                            new[key] = value

                else:
                    filtered = _filter_bunch(
                        value,
                        keyword=keyword,
                        name=name,
                        geometry_type=geometry_type,
                        function=function,
                    )
                    if filtered:
                        new[key] = filtered

            return new

        return _filter_bunch(
            self,
            keyword=keyword,
            name=name,
            geometry_type=geometry_type,
            function=function,
        )


class Dataset(Bunch):
    """
    A dict with attribute-access and that
    can be called to update keys
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required = ["name", "url", "hash", "filename"]
        missing = []
        for el in required:
            if el not in self.keys():
                missing.append(el)
        if len(missing) > 0:
            msg = (
                f"The attributes {required} "
                f"are required to initialise "
                f"a `Dataset`. Please provide values for: "
                f'`{"`, `".join(missing)}`'
            )
            raise AttributeError(msg)

    def __call__(self, **kwargs) -> Dataset:
        new = Dataset(self)  # takes a copy preserving the class
        new.update(kwargs)
        return new

    def copy(self, **kwargs) -> Dataset:
        new = Dataset(self)  # takes a copy preserving the class
        return new

    @property
    def path(self) -> str:
        """Get the absolute path to a file in the local storage.

        If it’s not in the local storage, it will be downloaded.

        For Datasets containing multiple files, the archive is automatically extracted.

        Returns
        -------
        str
            loacal path
        """
        from .api import CACHE

        if "members" in self.keys():
            unzipped_files = CACHE.fetch(
                self.filename, processor=pooch.Unzip(members=self.members)
            )
            if len(unzipped_files) == 1:
                return unzipped_files[0]
            elif len(unzipped_files) > 1:  # shapefile
                return [f for f in unzipped_files if f.endswith(".shp")][0]
            else:
                raise

        return CACHE.fetch(self.filename)

    def _repr_html_(self, inside=False):
        item_info = ""
        for key, val in self.items():
            if key != "name":
                item_info += f"<dt><span>{key}</span></dt><dd>{val}</dd>"

        style = "" if inside else f"<style>{CSS_STYLE}</style>"
        html = f"""
        <div>
        {style}
            <div class="xyz-wrap">
                <div class="xyz-header">
                    <div class="xyz-obj">geodatasets.Dataset</div>
                    <div class="xyz-name">{self.name}</div>
                </div>
                <div class="xyz-details">
                    <dl class="xyz-attrs">
                        {item_info}
                    </dl>
                </div>
            </div>
        </div>
        """

        return html


def _load_json(f):
    data = json.loads(f)

    items = Bunch()

    for item_name in data.keys():
        item = data[item_name]

        if "url" in item.keys():
            items[item_name] = Dataset(item)
        else:
            items[item_name] = Bunch({i: Dataset(item[i]) for i in item})

    return items


CSS_STYLE = """
/* CSS stylesheet for displaying geodatasets objects in Jupyter.*/
.xyz-wrap {
    --xyz-border-color: var(--jp-border-color2, #ddd);
    --xyz-font-color2: var(--jp-content-font-color2, rgba(128, 128, 128, 1));
    --xyz-background-color-white: var(--jp-layout-color1, white);
    --xyz-background-color: var(--jp-layout-color2, rgba(128, 128, 128, 0.1));
}

html[theme=dark] .xyz-wrap,
body.vscode-dark .xyz-wrap,
body.vscode-high-contrast .xyz-wrap {
    --xyz-border-color: #222;
    --xyz-font-color2: rgba(255, 255, 255, 0.54);
    --xyz-background-color-white: rgba(255, 255, 255, 1);
    --xyz-background-color: rgba(255, 255, 255, 0.05);

}

.xyz-header {
    padding-top: 6px;
    padding-bottom: 6px;
    margin-bottom: 4px;
    border-bottom: solid 1px var(--xyz-border-color);
}

.xyz-header>div {
    display: inline;
    margin-top: 0;
    margin-bottom: 0;
}

.xyz-obj,
.xyz-name {
    margin-left: 2px;
    margin-right: 10px;
}

.xyz-obj {
    color: var(--xyz-font-color2);
}

.xyz-attrs {
    grid-column: 1 / -1;
}

dl.xyz-attrs {
    padding: 0 5px 0 5px;
    margin: 0;
    display: grid;
    grid-template-columns: 135px auto;
    background-color: var(--xyz-background-color);
}

.xyz-attrs dt,
dd {
    padding: 0;
    margin: 0;
    float: left;
    padding-right: 10px;
    width: auto;
}

.xyz-attrs dt {
    font-weight: normal;
    grid-column: 1;
}

.xyz-attrs dd {
    grid-column: 2;
    white-space: pre-wrap;
    word-break: break-all;
}

.xyz-details ul>li>label>span {
    color: var(--xyz-font-color2);
    padding-left: 10px;
}

.xyz-inside {
    display: none;
}

.xyz-checkbox:checked~.xyz-inside {
    display: contents;
}

.xyz-collapsible li>input {
    display: none;
}

.xyz-collapsible>li>label {
    cursor: pointer;
}

.xyz-collapsible>li>label:hover {
    color: var(--xyz-font-color2);
}

ul.xyz-collapsible {
    list-style: none!important;
    padding-left: 20px!important;
}

.xyz-checkbox+label:before {
    content: '►';
    font-size: 11px;
}

.xyz-checkbox:checked+label:before {
    content: '▼';
}

.xyz-wrap {
    margin-bottom: 10px;
}
"""
