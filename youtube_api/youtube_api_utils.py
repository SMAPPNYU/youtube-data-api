import sys
import json
import datetime
import requests
import re
import signal

from urllib.parse import urlparse
from urllib.parse import parse_qs

'''
This contains utilities used by other functions in the YoutubeDataApi class, as well as a few convenience functions for data analysis.
'''

__all__ = [
    '_chunker',
    '_load_response',
    'parse_yt_datetime',
    'get_upload_playlist_id',
    'get_liked_playlist_id',
]

class TimeoutError(Exception):
    pass

class timeout:
    def __init__(self, seconds=1, error_message='Timeout'):
        self.seconds = seconds
        self.error_message = error_message
    def handle_timeout(self, signum, frame):
        raise TimeoutError(self.error_message)
    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)
    def __exit__(self, type, value, traceback):
        signal.alarm(0)

def _chunker(l, chunksize):
    """Yield successive ``chunksize``-sized chunks from l."""
    for i in range(0, len(l), chunksize):
        yield l[i:i + chunksize]

def _load_response(response):
    '''
    Loads the response to json, and checks for errors.
    '''
    
    response.raise_for_status()
    response_json = json.loads(response.text)

    return response_json


def parse_yt_datetime(date_str):
    '''
    Parses a date string returned from YouTube's API into a Python datetime.
    '''
    date = None
    if date_str:
        try:
            date = datetime.datetime.strptime(date_str,"%Y-%m-%dT%H:%M:%S.%fZ")
            date = datetime.datetime.timestamp(date)
        except:
            try:
                date = datetime.datetime.strptime(date_str,"%Y-%m-%dT%H:%M:%SZ")
                date = datetime.datetime.timestamp(date)
            except:
                pass
    return date

def get_upload_playlist_id(channel_id):
    '''Given a channel_id, returns the user uploaded playlist id.'''
    playlist_id = 'UU' + channel_id[2:]
    return playlist_id


def get_liked_playlist_id(channel_id):
    '''Given a channel_id, returns the user liked playlist id.'''
    playlist_id = 'LL' + channel_id[2:]
    return playlist_id
