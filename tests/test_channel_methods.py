import sys
import os
sys.path.append('../youtube-data-api/youtube_api')
import unittest
import requests

from youtube_api import YoutubeDataApi
from youtube_api_utils import *

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.channel_id = 'UC3XTzVzaHQEd30rQbuvCtTQ'

    def test_channel_id(self):
        self.assertEqual(self.yt.get_channel_id_from_user('LastWeekTonight'), self.channel_id)

    def test_upload_playlist_id(self):
        self.assertEqual(get_upload_playlist_id(self.channel_id), 'UU3XTzVzaHQEd30rQbuvCtTQ')
        

if __name__ == '__main__':
    unittest.main()