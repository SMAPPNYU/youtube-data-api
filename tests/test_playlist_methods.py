import sys
import os
sys.path.append('../youtube-data-api/youtube_api')
import unittest
import requests

from youtube_api import YoutubeDataApi

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.playlist_id = ''
