import sys
import json
import datetime
import requests
import html
import tldextract
from bs4 import BeautifulSoup, Comment
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
    '_text_from_html',
    'parse_yt_datetime',
    'strip_video_id_from_url',
    'get_upload_playlist_id',
    'get_liked_playlist_id',
    'is_user',
    'strip_youtube_id',
    'get_channel_id_from_custom_url',
    'get_url_from_video_id'
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

def _text_from_html(html_body):
    '''
    Gets clean text from html.
    '''
    def _tag_visible(element):
        '''Gets the text elements we're interested in'''
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    soup = BeautifulSoup(html_body, 'html.parser')
    raw_text = soup.findAll(text=True)
    visible_text = filter(_tag_visible, raw_text)
    text = u" ".join(t.strip() for t in visible_text)
    text = re.sub(r"[\n\t]", ' ', text)
    text = re.sub(r'<.+?>', '', text)
    text = html.unescape(text)
    text = ' '.join(text.split())

    return text


def parse_yt_datetime(date_str):
    '''
    Parses a date string returned from YouTube's API into a Python datetime.
    '''
    date = None
    if date_str:
        try:
            date = datetime.datetime.strptime(date_str,"%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            pass
    return date

def strip_video_id_from_url(url):
    '''Strips the video_id from YouTube URL.'''

    domain = tldextract.extract(url).registered_domain
    url_ = None
        
    if 'youtu.be' in domain:
        url_ = url[url.rindex('/') + 1:]
        if '?' in url_:
            url_ = url_[:url_.rindex('?')]
    elif "youtube.com" in domain and "embed" in url:
        url_ = url.rpartition("/")[-1].partition("?")[0]
    elif "youtube.com" in domain and "attribution_link" in url:
        u = urlparse(url)
        
        # Get and parse the query string, which will look like:
        #. a=--oPiH1x0pU&u=%2Fwatch%3Fv%3DHR1Ta25HkBM%26feature%3Dshare
        q = parse_qs(u.query)
        
        # Now we have a decoded query string, e.g., 'u':['/watch?v=HR1Ta25HkBM&feature=share']
        if ( 'u' in q ):
            # Parse like it was a normal /watch url
            q = parse_qs(urlparse(q['u'][0]).query)
            if ( 'v' in q ):
                url_ = q['v'][0]
            elif ( 'video_id' in q ):
                url_ = q['video_id'][0]
    elif "youtube.com" in domain:
        u = urlparse(url)
        q = parse_qs(u.query)
        if ( 'v' in q ):
            url_ = q['v'][0]
        elif ( 'video_id' in q ):
            url_ = q['video_id'][0]

    return url_


def get_upload_playlist_id(channel_id):
    '''Given a channel_id, returns the user uploaded playlist id.'''
    playlist_id = 'UU' + channel_id[2:]
    return playlist_id


def get_liked_playlist_id(channel_id):
    '''Given a channel_id, returns the user liked playlist id.'''
    playlist_id = 'LL' + channel_id[2:]
    return playlist_id


def is_user(channel_url):
    '''
    Checks if url is channel or user
    '''
    if 'youtube.com/user/' in channel_url:
        return True
    elif 'youtube.com/channel/' in channel_url:
        return False
    else:
        raise Exception("Didn't recognize url {}".format(channel_url))


def strip_youtube_id(channel_url):
    '''
    From a URL returns the YT ID.
    '''
    return (channel_url.rstrip('/').replace('/featured', '')
                       .split('/')[-1].split('#')[0])

def get_channel_id_from_custom_url(url):
    '''
    Gets channel id from a url of a custom url IE: http://youtube.com/stefbot
    returns a channel_id IE: UCuMo0RRtnNDuMB8DV5stEag
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    class_ = ('yt-uix-button yt-uix-button-size-default '
              'yt-uix-button-subscribe-branded '
              'yt-uix-button-has-icon no-icon-markup '
              'yt-uix-subscription-button yt-can-buffer')
    channel_id = soup.find('button', class_=class_).get('data-channel-external-id')
    return channel_id

def get_url_from_video_id(video_id):
    '''
    Given a video id, this function returns the full URL.
    '''
    url = "https://youtube.com/watch?v={}".format(video_id)
    return url



