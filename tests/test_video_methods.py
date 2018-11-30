import sys
import os
sys.path.append('../youtube-data-api/youtube_api')
import unittest
import requests
import datetime

from youtube_api import YoutubeDataApi

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.video_id = 'RdjRMDADpcg'
        cls.channel_id = 'UC8-Th83bH_thdKZDJCrn88g'
        cls.vid_publish = datetime.datetime(2018, 11, 28, 10, 0, 3)
        cls.search_term = 'John Oliver'
        
    #written by Megan Brown on 11/30/2018
    def test_video_metadata_valid(self):
        resp = self.yt.get_video_metadata(self.video_id)
        
        self.assertEqual(resp['video_id'], self.video_id)
        self.assertEqual(resp['channel_id'], self.channel_id)
        self.assertEqual(resp['video_publish_date'], self.vid_publish)
        
    def test_search_for_video_method(self):
        resp = self.yt.search(self.search_term)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))

        

if __name__ == '__main__':
    unittest.main()