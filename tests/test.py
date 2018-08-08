import unittest
import sys
sys.path.append('youtube-data-api/youtube_api')
from youtube_api import YoutubeDataApi
from youtube_api_utils import *


class TestDataMethods(unittest.TestCase):
    def test_upload_playlist_id(self):
        self.assertEqual(get_upload_playlist_id('UC3XTzVzaHQEd30rQbuvCtTQ'), 'UU3XTzVzaHQEd30rQbuvCtTQ')

    def test_channel_id(self):
        self.assertEqual(yt.get_channel_id_from_user('LastWeekTonight'), 'UC3XTzVzaHQEd30rQbuvCtTQ')


if __name__ == '__main__':
    unittest.main()
