# -*- coding: utf-8 -*-
import pytest
import os
from .config import key
from youtube_api import YoutubeDataApi

# instantiate a YoutubeDataApi instance once per module
@pytest.fixture(scope="package")
def youtube_api():
    print('Calling conftest')

    wrong_key = key[:-1]

    with pytest.raises(ValueError) as err_msg:
        yt = YoutubeDataApi('')
    assert 'No API key used to initate the class.' in str(err_msg.value)

    with pytest.raises(ValueError) as err_msg:
        yt = YoutubeDataApi(wrong_key)
    assert 'The API Key is invalid' in str(err_msg.value)

    return YoutubeDataApi(key)
