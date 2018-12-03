'''
Last Updated: 11/30/2018

Tests the initialization of the YoutubeDataApi

TO DO
=====


Functions Tested
================
def __init__(self, key, api_version='3')
def verify_key(self)
                                  

DONE 
====
* __init__
* verifiy_key

'''

import sys
import os
sys.path.append('../')
import unittest
from unittest.mock import patch
import requests

from youtube_api import YoutubeDataApi

class TestAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.key = os.environ.get('YT_KEY')
        cls.wrong_key = 'xxxxxxxxx'
        cls.yt = YoutubeDataApi(cls.key)

    #Verified by Megan Brown on 11/30/2018
    def test_init(self):
        with self.assertRaisesRegex(ValueError, 'No API key used to initate the class.'):
            yt = YoutubeDataApi('')

        with self.assertRaisesRegex(ValueError, 'The API Key is invalid'):
            yt = YoutubeDataApi(self.wrong_key)

    #verified by Megan Brown on 11/30/2018
    @patch('requests.get')
    def test_verify(self, mock_request):
        mock_resp = requests.models.Response()
        mock_resp.status_code = 404
        mock_request.return_value = mock_resp

        self.assertEqual(self.yt.verify_key(), False)

if __name__ == '__main__':
    unittest.main()
