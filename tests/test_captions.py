import sys
import os
sys.path.append('../youtube-data-api/youtube_api')
import unittest
import requests
from collections import OrderedDict

from youtube_api import YoutubeDataApi

class TestVideo(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.yt = YoutubeDataApi(cls.key)
        cls.video_id = 'wmxDZeh8W34'
        cls.video_id_list = ['wmxDZeh8W34', 'PIXQdfiRZNk','nvEFb_dWJdQ']
        cls.fake_vid = '99999999999'
        
    def test_valid_caption(self):
        resp = self.yt.get_captions(self.video_id)
        
        self.assertEqual(type(resp), OrderedDict)
        self.assertEqual(type(resp['video_id']), str)
        
    def test_list_of_captions(self):
        resp = self.yt.get_captions(self.video_id_list)
        
        self.assertEqual(type(resp), list)
        self.assertEqual(type(resp[0]['video_id']), str)
        

    
if __name__ == '__main__':
    unittest.main()
    