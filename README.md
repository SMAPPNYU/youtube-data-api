# Youtube Data API
<a href="https://badge.fury.io/py/youtube-data-api"><img src="https://badge.fury.io/py/youtube-data-api.svg" alt="PyPI version" height="18"></a>
<a href="https://travis-ci.com/SMAPPNYU/youtube-data-api"><img src="https://travis-ci.com/SMAPPNYU/youtube-data-api.svg?branch=master" alt="Build status" height="18"></a>
<a href='https://youtube-data-api.readthedocs.io/en/latest/?badge=latest'>
    <img src='https://readthedocs.org/projects/youtube-data-api/badge/?version=latest' alt='Documentation Status' />
</a>
<a href="https://doi.org/10.5281/zenodo.1414418"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.1414418.svg" alt="DOI"></a>



This is a Python client for the Python Data API. It was written to accomodate v3 of the API.

## Install

It is recommended to [install this module by using pip](https://pypi.org/project/youtube-data-api/):

```
pip install youtube-data-api
```

If you want to use it from source, you'll have to install the dependencies manually:

```
pip install -r requirements.txt
```

## Quickstart
In order to access the API, you'll need to get a [service key](https://developers.google.com/youtube/registering_an_application#Create_API_Keys) from the [Google Cloud Console](https://console.cloud.google.com/).

Once you have it you can use it to initiate the `YoutubeDataApi` class.
```
from youtube_api import YoutubeDataApi

api_key = 'AKAIXXXXXXXX'
yt = YoutubeDataApi(api_key)

yt.search('alexandria ocasio-cortez')
```

The `yt` object calls functions that automate the collection of data fields that are both visable and not-visable to everyday users.

Please refer to the [documentation](http://bit.ly/YouTubeDataAPI) for details.

## Testing
Static json files used for test are stored in `./tests/data`.
To test, command line input `make test`.


## Authors
Written by Leon Yin and Megan Brown

If you use this software in your research please cite it as:
```
@misc{leon_yin_2018_1414418,
  author       = {Leon Yin and
                  Megan Brown},
  title        = {SMAPPNYU/youtube-data-api},
  month        = sep,
  year         = 2018,
  doi          = {10.5281/zenodo.1414418},
  url          = {https://doi.org/10.5281/zenodo.1414418}
}
```
