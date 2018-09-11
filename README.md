# Youtube Data API
This is a Python client for the Python Data API. It was written to accomodate v3 of the API.<br>

It differs from other packages because it provides a versitile way to parse raw json outputs, and it is optimized for analysis-- IE all the functions in this package are to G=

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
In order to access the API, you'll need to get a [service key](https://developers.google.com/youtube/registering_an_application#Create_API_Keys) from the [Google Developer's Console]( Google Developers Console).

Once you have it you can use it to initiate the `YoutubeDataApi` class.
```
from youtube_api import YoutubeDataApi

api_key = 'AKAIXXXXXXXX'
yt = YoutubeDataApi(api_key)

yt.search('alexandria ocasio-cortez')
```

The `yt` object calls functions that automate the collection of data fields that are both visable and not-visable to everyday users.

Please refer to the documentation for details.

## Testing
Static json files used for test are stored in `./tests/data`.
To test, command line input `make test`.

Written by Leon Yin and Megan Brown
