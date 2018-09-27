import sys
import os
sys.path.append(os.path.abspath('../')) 
import unittest
import requests
import datetime

from youtube_api import YoutubeDataApi
from youtube_api.youtube_api_utils import *

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.channel_id = 'UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.date = '2018-03-14T20:53:14.000Z'
        cls.user_url = 'https://www.youtube.com/user/LastWeekTonight'
        cls.channel_url = 'https://www.youtube.com/channel/UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.video_id = '481YX6T9Xzs'
        cls.video_url = 'https://www.youtube.com/watch?v=481YX6T9Xzs'

    
    def test_upload_playlist_id(self):
        self.assertEqual(get_upload_playlist_id(self.channel_id), 'UU3XTzVzaHQEd30rQbuvCtTQ')
    
    def test_get_liked_playlist_id(self):
        self.assertEqual(get_liked_playlist_id(self.channel_id), 'LL3XTzVzaHQEd30rQbuvCtTQ')

    def test_parse_yt_datetime(self):
        self.assertEqual(parse_yt_datetime(self.date), datetime.datetime(2018, 3, 14, 20, 53, 14))
        
    def test_strip_video_id_from_url(self):
        self.assertEqual(strip_video_id_from_url(self.video_url), self.video_id)
        
    def test_is_user(self):
        self.assertTrue(is_user(self.user_url))
        self.assertFalse(is_user(self.channel_url))
        
    def test_get_url_from_video_id(self):
        self.assertEqual(get_url_from_video_id(self.video_id), video_url)

if __name__ == '__main__':
    unittest.main()