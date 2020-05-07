import sys
import os
sys.path.append('../')
import unittest
import requests
import datetime
from collections import OrderedDict

from youtube_api import YoutubeDataApi

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.video_id = 'gl1aHhXnN1k'
        cls.channel_id = 'UC9CoOnJkIBMdeijd9qYoT_g'
        #cls.vid_publish = datetime.datetime(2018, 11, 28, 10, 0, 3)
        cls.search_term = 'John Oliver'
        cls.list_of_videos = ['ximgPmJ9A5s','gl1aHhXnN1k']
        
    
    def test_video_metadata_valid(self):
        '''#written by Megan Brown on 11/30/2018'''
        resp = self.yt.get_video_metadata(self.video_id)
        
        self.assertEqual(resp['video_id'], self.video_id)
        self.assertEqual(resp['channel_id'], self.channel_id)
        #self.assertEqual(resp['video_publish_date'], self.vid_publish)
            
    
    def test_video_metadata_with_list_input(self):
        '''#written by Megan Brown on 11/30/2018'''
        resp = self.yt.get_video_metadata(self.list_of_videos)
        
        self.assertTrue(len(resp) == 2)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
    
    
    def test_video_metadata_with_invalid_list(self):
        '''#written by Megan Brown on 11/30/2018'''
        invalid_list_of_videos = self.list_of_videos
        invalid_list_of_videos.append('xxxxxxxx')
        
        resp = self.yt.get_video_metadata(invalid_list_of_videos)
        self.assertTrue(len(resp) == 2)
        
    
    def test_video_metadata_invalid_string(self):
        '''#written by Megan Brown on 11/30/2018'''
        resp = self.yt.get_video_metadata('xx')
        
        self.assertTrue(resp == [])
        

if __name__ == '__main__':
    unittest.main()