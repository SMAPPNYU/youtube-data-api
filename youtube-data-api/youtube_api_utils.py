import os
import sys
import json
import time
import logging
import warnings
import datetime
import requests
import html
from bs4 import BeautifulSoup, Comment
import re
import numpy as np

def verify_key(key):
    dummy_http = ("https://www.googleapis.com/youtube/v3/playlists"
                     "?part=id&id=UC_x5XG1OV2P6uZZ5FSM9Ttw&"
                     "key={}&maxResults=2".format(key))
    dummy_request = requests.get(dummy_http)

    try:
        dummy_request.raise_for_status()
        return True
    except:
        return False


def log(msg, verbose=1):
    '''
    Defaults to print,
    Will be silent it verbose = 0,
    Will write to a logger if verbose = 1
    '''
    if verbose == 1:
        print(msg)
    elif verbose == 2:
        logger = logging.getLogger(__name__)
        logger.info(msg)
    else:
        pass


def load_response(response, verbose=1, handle_error=True):
    '''
    Loads the response to json, and checks for errors.
    '''
    try:
        response_json = json.loads(response.text)
    except Exception as e:
        log(e, verbose)
        log(response, verbose)
        return False
    try:
        response.raise_for_status()
    except:
        if handle_error:
            response_json = error_handler(response_json, verbose)
        else:
            sys.exit()

    return response_json


def error_handler(error, verbose=1):
    '''
    Parses errors if the request raised a status.
    '''
    reasons = []
    for e in error['error']['errors']:
        reasons.append(e['reason'])

    if 'keyInvalid' in reasons:
        warnings.warn("Bad Key!")
        log(error, verbose)
        sys.exit()
    if 'dailyLimitExceeded' in reasons:
        log(error, verbose)
        raise Exception("Daily API Limit Exceeded!")
        sys.exit()
    elif 'limitExceeded' in reasons:
        warnings.warn("API quota exceeded, sleeping for an hour!")
        log(error, verbose)
        sys.exit()
        #time.sleep(60 * 60)
    elif 'quotaExceeded' in reasons:
        warnings.warn("API quota exceeded, sleeping for an hour!")
        log(error, verbose)
        sys.exit()
        #time.sleep(60 * 60)
    elif 'badRequest' in reasons:
        warnings.warn("Bad Request!")
        log(error, verbose)
    elif 'subscriptionForbidden' in reasons:
        warnings.warn("Viewing subscriptions are forbidden for this user!")
    elif 'commentsDisabled' in reasons:
        warnings.warn("User has disabled comments on this video!")
        log(error, verbose)
    elif 'videoNotFound' in reasons:
        warnings.warn("The video was not found!")
        log(error, verbose)
    elif 'processingFailure' in reasons:
        warnings.warn("There was a processing failure!")
        log(error, verbose)
    elif 'playlistNotFound' in reasons:
        warnings.warn("This playlist does not exist!")
        log(error, verbose)
    else:
        warnings.warn("An unexpected error!")
        log(error, verbose)
        sys.exit()



def handle_caption_error(error, verbose=1):
    if isinstance(error, AttributeError):
        log("The attribute for your language could not be found", verbose)
    else:
        log("An unexpected error!", verbose)
    return False

def parse_yt_datetime(date_str):
    date = None
    if date_str:
        try:
            date = datetime.datetime.strptime(date_str,"%Y-%m-%dT%H:%M:%S.%fZ")
        except:
            pass
    return date

def strip_video_id_from_url(url):
    '''Strips a URL from youtube to a video_id'''

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
    url = "https://youtube.com/watch?v={}".format(video_id)
    return url

def text_from_html(html_body):
    '''
    Gets clean text from html.
    '''
    def tag_visible(element):
        '''Gets the text elements we're interested in'''
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True

    soup = BeautifulSoup(html_body, 'xml')
    raw_text = soup.findAll(text=True)
    visible_text = filter(tag_visible, raw_text)
    text = u" ".join(t.strip() for t in visible_text)
    text = re.sub(r"[\n\t]", ' ', text)
    text = re.sub(r'<.+?>', '', text)
    text = html.unescape(text)
    text = ' '.join(text.split())

    return text
