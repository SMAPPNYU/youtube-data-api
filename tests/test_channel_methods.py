import sys
import os
sys.path.append('../')
import unittest
import requests

from youtube_api import YouTubeDataAPI
import youtube_api.youtube_api_utils as utils

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YouTubeDataAPI(cls.key)
        cls.channel_id = 'UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.channel_title = 'LastWeekTonight'

    def test_channel_id(self):
        '''written by Megan Brown on 11/30/2018'''
        resp = self.yt.get_channel_id_from_user(self.channel_title)
        self.assertEqual(resp, self.channel_id)
        

if __name__ == '__main__':
    unittest.main()