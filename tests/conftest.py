# -*- coding: utf-8 -*-
import pytest
from youtube_api import YoutubeDataApi

# instantiate a YoutubeDataApi instance once per module
@pytest.fixture(scope="package")
def youtube_api():
    with pytest.raises(ValueError) as err_msg:
        yt = YoutubeDataApi('')
    assert 'No API key used to initate the class.' in str(err_msg.value)

    with pytest.raises(ValueError) as err_msg:
        yt = YoutubeDataApi('AIzaSyCtB2sDcJZTNscwWxLgVcT04V83KYR3')
    assert 'The API Key is invalid' in str(err_msg.value)

    return YoutubeDataApi('AIzaSyCtB2sDcJZTNscwWxLgVcT04V83KYR3gsI')
