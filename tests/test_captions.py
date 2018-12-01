'''
Last Updated: 11/30/2018

Tests the parameters for the `get_captions` method in the YoutubeDataApi

TO DO
=====
* parser

Functions Tested
================
def get_captions(self, video_id, lang_code='en', parser=P.parse_caption_track, **kwargs)

PARAMS TESTED
=============
* video_id
* lang_code

'''
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
        cls.fake_vid = '12345'
        
    #Verified by Megan Brown on 11/30/2018
    def test_valid_caption(self):
        resp = self.yt.get_captions(self.video_id)

        self.assertEqual(type(resp), OrderedDict)
        self.assertEqual(type(resp['video_id']), str)

    #Verified by Megan Brown on 11/30/2018
    def test_valid_list_of_captions(self):
        resp = self.yt.get_captions(self.video_id_list)

        self.assertEqual(type(resp), list)
        self.assertEqual(type(resp[0]['video_id']), str)

    #Written by Megan Brown on 11/30/2018
    def test_invalid_short_caption(self):
        with self.assertRaises(Exception):
            resp = self.yt.get_captions(self.fake_vid)

    '''
    #Written by Megan Brown on 11/30/2018
    def test_list_of_captions_with_invalid_string(self):
        resp = self.yt.get_captions(self.video_id_list)

        self.assertEqual(type(resp), list)
        self.assertEqual(type(resp[0]['video_id']), str)'''



if __name__ == '__main__':
    unittest.main()
