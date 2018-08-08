# -*- coding: utf-8 -*-
from youtube_api import YoutubeDataApi
from youtube_api import parsers as P
import pytest
import requests
from unittest import mock

@mock.patch('requests.get')
def test_verify(mock_request, youtube_api):
    mock_resp = requests.models.Response()
    mock_resp.status_code = 404
    mock_request.return_value = mock_resp

    assert youtube_api.verify_key() == False

def test_instance(youtube_api):
    assert isinstance(youtube_api, YoutubeDataApi)

def test_channel_id(youtube_api):
    id = youtube_api.get_channel_id_from_user('teamcoco')

    assert id == "UCi7GJNg51C3jgmYTUwqoUXA"

def test_video_metadata(youtube_api):
    api_call = youtube_api.get_video_metadata('a7KDbZ5VQ0E', parser=P.default)
    metadata = [{ "kind": "youtube#video",
    "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/KELXwMtT5O2GQeutrYy8ToTHAv4\"",
    "id": "a7KDbZ5VQ0E"}]
    print(api_call)

    assert metadata == api_call
