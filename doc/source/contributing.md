# Contributing to `geodatasets`

Contributions to `geodatasets` are very welcome. They are likely to be accepted more
quickly if they follow these guidelines.

There are two main groups of contributions - adding new data sources and
contributions to the codebase and documentation.

## Data sources

If you want to add a new dataset, simply add its details to
`geodatasets/json/database.json`.

You can add a single `Dataset` or a `Bunch` of `Dataset`s. Use the following
schema to add a single dataset:

```json
{
  "dataset_name": {
        "url": "https://your-site.com/direct-link-to/my_file.zip",
        "license": "CC-0",
        "attribution": "University of Github",
        "name": "dataset_name",
        "description": "Contents of my file",
        "geometry_type": "Polygon",
        "nrows": 77,
        "ncols": 20,
        "details": "https://your-site.com/link-to-explanantion/",
        "hash": "a2ab1e3f938226d287dd76cde18c00e2d3a260640dd826da7131827d9e76c824",
        "filename": "my_file.zip"
    },
}
```

If you want to add a bunch of related datasets (e.g. different files from a single source),
you can group then within a `Bunch` using the following schema:

```json
{
  "provider_bunch_name": {
      "first_dataset_name": {
            "url": "https://your-site.com/direct-link-to/my_file.zip",
            "license": "CC-0",
            "attribution": "University of Github",
            "name": "dataset_name",
            "description": "Contents of my file",
            "geometry_type": "Polygon",
            "nrows": 77,
            "ncols": 20,
            "details": "https://your-site.com/link-to-explanantion/",
            "hash": "a2ab1e3f938226d287dd76cde18c00e2d3a260640dd826da7131827d9e76c824",
            "filename": "my_file.zip"
      },
      "second_dataset_name": {
            "url": "https://your-site.com/direct-link-to/my_file.zip",
            "license": "CC-0",
            "attribution": "University of Github",
            "name": "dataset_name",
            "description": "Contents of my file",
            "geometry_type": "Point",
            "nrows": 77,
            "ncols": 20,
            "details": "https://your-site.com/link-to-explanantion/",
            "hash": "a2ab1e3f938226d287dd76cde18c00e2d3a260640dd826da7131827d9e76c824",
            "filename": "my_file.zip",
            "members": ["use_only_this.geojson"]
      }
   },
}
```

It is mandatory to always specify at least `name`, `url`, `hash` and `filename`. `hash`
is a sha256 hash of the file to check that a user gets the expected file and a
`filename` specifies how the downloaded file will be called. Ensure that it has a correct
suffix. Don't forget to add any other custom attributes you'd like. Attribute `members` has
a specific meaning and specifies file (or files in case of ESRI Shapefile) that shall be
extracted from the archive and used.

## Code and documentation

At this stage of `geodatasets` development, the priorities are to define a simple,
usable, and stable API and to have clean, maintainable, readable code.

In general, `geodatasets` follows the conventions of the GeoPandas project where
applicable.

In particular, when submitting a pull request:

- All existing tests should pass. Please make sure that the test suite passes, both
  locally and on GitHub Actions. Status on GHA will be visible on a pull request. GHA
  are automatically enabled on your own fork as well. To trigger a check, make a PR to
  your own fork.
- Ensure that documentation has built correctly. It will be automatically built for each
  PR.
- New functionality should include tests. Please write reasonable tests for your code
  and make sure that they pass on your pull request.
- Classes, methods, functions, etc. should have docstrings and type hints. The first
  line of a docstring should be a standalone summary. Parameters and return values
  should be documented explicitly.
- Follow PEP 8 when possible. We use Black and Flake8 to ensure a consistent code format
  throughout the project. For more details see the [GeoPandas contributing
  guide](https://geopandas.readthedocs.io/en/latest/community/contributing.html).
- Imports should be grouped with standard library imports first, 3rd-party libraries
  next, and `geodatasets` imports third. Within each grouping, imports should be
  alphabetized. Always use absolute imports when possible, and explicit relative imports
  for local imports when necessary in tests.
- `geodatasets` supports Python 3.7+ only. When possible, do not introduce additional
  dependencies. If that is necessary, make sure they can be treated as optional.
