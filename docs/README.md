# Docs
By: Leon Yin<br>
Updated: 2018-09-12<br>

Docs are generated using sphinx and hosted in read the docs. Please download all dependencies in the `requirements.txt` file to generate docs.

the `conf.py` file is used to configure auto-generated API docs (via doc strings). It was created using `sphinx-quickstart`, this only really needs to be run once per project.

The directions to auto-generate docs are made with this function:<br>
```sphinx-apidoc -o source/ ../youtube_api/```

This also only needs to be run once!

Examples of how to use the code must be written in RST, stored in `source/usage/`, and referenced in the index.rst fil (see this [example](https://raw.githubusercontent.com/SMAPPNYU/youtube-data-api/master/docs/source/index.rst) for referencing usage/quickstart).

To build docs just use the make file,`make html`. This will populate or re-populate the `build` directory.


## Gotchas:
Spacing and new lines are extremely important for RST!

Read the docs's environment does not allow for C-packages. Many Python packages are optimized in Cython, we use mocking to fix this problem. When this is nto addressed the API docs are not properly generated on the read the docs site.
