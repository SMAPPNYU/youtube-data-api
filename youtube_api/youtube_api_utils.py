import sys
import json
import datetime
import requests
import html
from bs4 import BeautifulSoup, Comment
import re

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

    soup = BeautifulSoup(html_body, 'xml')
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
    if '/watch?v=' in url.lower():
        url_ = (url.split('&v=')[-1].split('/watch?v=')[-1].split('?')[0].split('&')[0])

    elif 'youtu.be' in url.lower():
        url_ = url[url.rindex('/') + 1:]
        if '?' in url_:
            url_ = url_[:url_.rindex('?')]
    else:
        url_ = None

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
    return channel_url.rstrip('/').replace('/featured', '').split('/')[-1]


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



