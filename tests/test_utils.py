import sys
import os
sys.path.append('../')
import unittest
import requests
import datetime

from youtube_api import YoutubeDataApi
from youtube_api import youtube_api_utils as utils

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.channel_id = 'UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.upload_id = 'UU3XTzVzaHQEd30rQbuvCtTQ'
        cls.liked_id = 'LL3XTzVzaHQEd30rQbuvCtTQ'
        cls.date = '2018-03-14T20:53:14.000Z'
        cls.datetime_date = datetime.datetime(2018, 3, 14, 20, 53, 14)
        cls.user_url = 'https://www.youtube.com/user/LastWeekTonight'
        cls.channel_url = 'https://www.youtube.com/channel/UC3XTzVzaHQEd30rQbuvCtTQ'
        cls.video_id = '481YX6T9Xzs'
        cls.video_url = 'https://youtube.com/watch?v=481YX6T9Xzs'
        
    
    def test_get_upload_playlist_id(self):
        '''#Written by Megan Brown on 11/30/2018'''
        resp = utils.get_upload_playlist_id(self.channel_id)
        
        self.assertEqual(resp, self.upload_id)
        
    def test_get_liked_playlist_id(self):
        '''#Written by Megan Brown on 11/30/2018'''
        resp = utils.get_liked_playlist_id(self.channel_id)
        
        self.assertEqual(resp, self.liked_id)

    def test_parse_yt_datetime(self):
        ''' #Verified by Megan Brown on 11/30/2018'''
        resp = utils.parse_yt_datetime(self.date)
        self.assertEqual(resp, self.datetime_date)
        
if __name__ == '__main__':
    unittest.main()