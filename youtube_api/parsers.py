import json
import sys
import datetime
from collections import OrderedDict

if sys.version_info[0] == 2:
    from collections import Iterable
else:
    from collections.abc import Iterable

from youtube_api.youtube_api_utils import parse_yt_datetime

"""
This script contains the parsers for the raw json responses
from the API. Use `raw_json` to return the output as-is.
"""

__all__ = ['raw_json',
           'parse_video_metadata',
           'parse_channel_metadata',
           'parse_rec_video_metadata',
           'parse_video_url',
           'parse_subscription_descriptive',
           'parse_featured_channels',
           'parse_comment_metadata',
           'parse_playlist_metadata',
           'parse_caption_track']

def raw_json(item):
    '''
    Returns the raw json output from the API.
    '''
    return item

def raw_json_with_datetime(item):
    '''
    Returns the raw json output from the API.
    '''
    item['collection_date'] = datetime.datetime.now().strftime('%Y-%m-%d')
    return item

def parse_video_metadata(item):
    '''
    Parses and processes raw output and returns video_id, channel_title, channel_id, video_publish_date, video_title, video_description, video_category, video_view_count, video_comment_count, video_like_count, video_dislike_count, video_thumbnail, video_tags, collection_date.

    :params item: json document
    :type item: dict

    :returns: parsed dictionary
    :rtype: dict
    '''
    if not isinstance(item, dict):
        return dict()

    tags = item["snippet"].get('tags')
    if isinstance(tags, Iterable):
        video_tags =  '|'.join(tags)
    else:
        video_tags = ''

    video_meta = {
        "video_id" : item['id'],
        "channel_title" : item["snippet"].get("channelTitle"),
        "channel_id" : item["snippet"].get("channelId"),
        "video_publish_date" : parse_yt_datetime(item["snippet"].get("publishedAt")),
        "video_title" : item["snippet"].get("title"),
        "video_description" : item["snippet"].get("description"),
        "video_category" : item["snippet"].get("categoryId"),
        "video_view_count" : item["statistics"].get("viewCount"),
        "video_comment_count" : item["statistics"].get("commentCount"),
        "video_like_count" : item["statistics"].get("likeCount"),
        "video_dislike_count" : item["statistics"].get("dislikeCount"),
        "video_thumbnail" : item["snippet"]["thumbnails"]["high"]["url"],
        "video_tags" :  video_tags,
        "collection_date" : datetime.datetime.now()
    }

    return video_meta


def parse_video_url(item):
    '''
    Parses and processes raw output and returns publish_date, video_id, channel_id, collection_date
    
    :params item: json document
    :type item: dict

    :returns: parsed dictionary
    :rtype: dict
    '''
    if not isinstance(item, dict):
        return dict()

    publish_date = item['snippet'].get('publishedAt')
    publish_date = parse_yt_datetime(publish_date)
    video_id = item['snippet']['resourceId'].get('videoId')
    channel_id = item['snippet'].get('channelId')

    return {
        "video_id" : video_id,
        "channel_id" : channel_id,
        "publish_date" : publish_date,
        "collection_date" : datetime.datetime.now()
    }


def parse_channel_metadata(item):
    '''
    Parses and processes raw output and returns channel_id, title, account_creatation_date, keywords, description, view_count, video_count, subscription_count, playlist_id_likes, playlist_id_uploads, topic_ids, country, collection_date.
    
    :params item: json document
    :type item: dict

    :returns: parsed dictionary
    :rtype: dict
    '''
    if not isinstance(item, dict):
        return dict()

    topic = item.get('topicDetails')
    if topic:
        topic = '|'.join(topic.get('topicCategories'))

    channel_meta = {
        "channel_id" : item['id'],
        "title" : item["snippet"].get("title"),
        "account_creation_date" : parse_yt_datetime(item["snippet"].get("publishedAt")),
        "keywords" : item['brandingSettings']['channel'].get('keywords'),
        "description" : item["snippet"].get("description"),
        "view_count" : item["statistics"].get("viewCount"),
        "video_count" : item["statistics"].get("videoCount"),
        "subscription_count" : item["statistics"].get("subscriberCount"),
        "playlist_id_likes" : item['contentDetails']['relatedPlaylists'].get('likes'),
        "playlist_id_uploads" : item['contentDetails']['relatedPlaylists'].get('uploads'),
        "topic_ids" : topic,
        "country" : item['snippet'].get('country'),
        "collection_date" : datetime.datetime.now()
    }

    return channel_meta


def parse_subscription_descriptive(item):
    '''
    Parses and processes raw output and returns subscription_title, subscription_channel_id, subscription_kind, subscription_publish_date, collection_date.

    
    :params item: json document
    :type item: dict

    :returns: parsed dictionary
    :rtype: dict
    '''
    if not isinstance(item, dict):
        return dict()

    sub_meta = {
        "subscription_title" : item['snippet']['title'],
        "subscription_channel_id" : item['snippet']['resourceId'].get('channelId'),
        "subscription_kind" : item['snippet']['resourceId'].get('kind'),
        "subscription_publish_date" : parse_yt_datetime(item['snippet'].get('publishedAt')),
        "collection_date" : datetime.datetime.now()
    }

    return sub_meta


def parse_featured_channels(item):
    '''
    Parses and processes raw output and returns a dictionary where the key is the channel_id and the key is a list of channel URLs.
    
    :params item: json document
    :type item: dict

    :returns: parsed dictionary
    :rtype: dict
    '''
    if not isinstance(item, dict):
        return dict()

    d = {}
    d[item['id']] = item['brandingSettings']['channel'].get('featuredChannelsUrls', [])
    return d


def parse_playlist_metadata(item):
    '''
    Parses and processes raw output and returns playlist_name, playlist_id, playlist_publish_date, playlist_n_videos, channel_id, channel_name, collection_date.
    
    :params item: json document
    :type item: dict

    :returns: parsed dictionary
    :rtype: dict

    '''
    if not isinstance(item, dict):
        return dict()

    playlist_meta = {
        "playlist_name" : item['snippet'].get('title'),
        "playlist_id" : item['id'],
        "playlist_publish_date" : parse_yt_datetime(item['snippet'].get('publishedAt')),
        "playlist_n_videos" : item['contentDetails'].get('itemCount'),
        "channel_id" : item['snippet'].get('channelId'),
        "channel_name" : item['snippet'].get('channelTitle'),
        "collection_date" : datetime.datetime.now()
    }

    return playlist_meta


def parse_comment_metadata(item):
    '''
    Parses and processes raw output and returns video_id, commenter_channel_url,  commenter_channel_display_name, comment_id, comment_like_count, comment_publish_date, text, commenter_rating, comment_parent_id, collection_date.
    
    :params item: json document
    :type item: dict

    :returns: parsed dictionary
    :rtype: dict
    '''
    if not isinstance(item, dict):
        return dict()

    if item['snippet'].get('topLevelComment'):
        save = item['snippet']
        item = item['snippet']['topLevelComment']

    comment_meta = {
        "video_id" : item["snippet"].get("videoId"),
        "commenter_channel_url" : item["snippet"].get("authorChannelUrl"),
        "commenter_channel_id" : item['snippet'].get('authorChannelId', dict()).get('value', None),
        "commenter_channel_display_name" : item['snippet'].get('authorDisplayName'),
        "comment_id" : item.get("id"),
        "comment_like_count" : item["snippet"].get("likeCount"),
        "comment_publish_date" : parse_yt_datetime(item["snippet"].get("publishedAt")),
        "text" : item["snippet"].get("textDisplay"),
        "commenter_rating" : item["snippet"].get("viewerRating"),
        "comment_parent_id" : item["snippet"].get("parentId"),
        "collection_date" : datetime.datetime.now()
    }
    try:
        comment_meta['reply_count'] = save.get('totalReplyCount')
    except:
        comment_meta['reply_count'] = item.get('totalReplyCount')

    return comment_meta


def parse_rec_video_metadata(item):
    '''
    Parses and processes raw output and returns video_id, channel_title, channel_id, video_publish_date, video_title, video_description, video_category, video_thumbnail, collection_date.
    
    :params item: json document
    :type item: dict

    :returns: parsed dictionary
    :rtype: dict
    '''
    if not isinstance(item, dict):
        return dict()

    video_meta = {
        "video_id" : item['id'].get('videoId'),
        "channel_title" : item["snippet"].get("channelTitle"),
        "channel_id" : item["snippet"].get("channelId"),
        "video_publish_date" : parse_yt_datetime(item["snippet"].get("publishedAt")),
        "video_title" : item["snippet"].get("title"),
        "video_description" : item["snippet"].get("description"),
        "video_category" : item["snippet"].get("categoryId"),
        "video_thumbnail" : item["snippet"]["thumbnails"]["high"]["url"],
        "collection_date" : datetime.datetime.now()
    }

    return video_meta

def parse_caption_track(item):
    '''
    Returns the video_id, captions and collection_date.
    
    :params item: json document
    :type item: dict

    :returns: parsed dictionary
    :rtype: dict
    '''

    #TODO: convert known errors into an error message.

    caption_meta = {
        "video_id" : item['video_id'],
        "caption" : item['caption'],
        "collection_date" : item['collection_date']
    }

    return caption_meta
