'''
Last Updated: 11/30/2018

Tests the parameters for the channel methods in the YoutubeDataApi

TO DO
=====
* get_video_metadata_gen
    * parser
    * part
    
* get_video_metadata
    * parser
    * part
    
* get_video_comments
    * video_id
    * get_replies
    * max_results
    * next_page_token
    * parser
    * part
    
* get_recommended_videos
    * video_id
    * max_results
    * parser


Functions Tested
================
def get_video_metadata_gen(self, video_id, parser=P.parse_video_metadata,
                               part=['statistics','snippet'],  **kwargs)
                               
def get_video_metadata(self, video_id, parser=P.parse_video_metadata, part=['statistics','snippet'],  **kwargs)

def get_video_comments(self, video_id, get_replies=True,
                           max_results=None, next_page_token=False,
                           parser=P.parse_comment_metadata, part = ['snippet'],
                           **kwargs)
                           
def get_recommended_videos(self, video_id, max_results=5,
                               parser=P.parse_rec_video_metadata,
                               **kwargs)
                                               

DONE 
====
* get_video_metadata
    * video_id

* get_video_metadata_gen
    * video_id

'''

import sys
import os
sys.path.append('../youtube-data-api/')
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
        cls.video_id = 'RdjRMDADpcg'
        cls.channel_id = 'UC8-Th83bH_thdKZDJCrn88g'
        cls.vid_publish = datetime.datetime(2018, 11, 28, 10, 0, 3)
        cls.search_term = 'John Oliver'
        cls.list_of_videos = ['ximgPmJ9A5s','RdjRMDADpcg']
        
    #written by Megan Brown on 11/30/2018
    def test_video_metadata_valid(self):
        resp = self.yt.get_video_metadata(self.video_id)
        
        self.assertEqual(resp['video_id'], self.video_id)
        self.assertEqual(resp['channel_id'], self.channel_id)
        self.assertEqual(resp['video_publish_date'], self.vid_publish)
            
    #written by Megan Brown on 11/30/2018
    def test_video_metadata_with_list_input(self):
        resp = self.yt.get_video_metadata(self.list_of_videos)
        
        self.assertTrue(len(resp) == 2)
        
        for item in resp:
            self.assertTrue('video_id' in list(item.keys()))
            self.assertTrue('video_title' in list(item.keys()))
            self.assertTrue('channel_title' in list(item.keys()))
    
    #written by Megan Brown on 11/30/2018
    def test_video_metadata_with_invalid_list(self):
        invalid_list_of_videos = self.list_of_videos
        invalid_list_of_videos.append('xxxxxxxx')
        
        resp = self.yt.get_video_metadata(invalid_list_of_videos)
        self.assertTrue(len(resp) == 2)
        
    #written by Megan Brown on 11/30/2018
    def test_video_metadata_invalid_string(self):
        resp = self.yt.get_video_metadata('xx')
        
        self.assertTrue(resp == [])
        

if __name__ == '__main__':
    unittest.main()