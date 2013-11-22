# -*- coding: utf-8 -*-

from conf import *
from sina import *
from tenc import *
from instagram.client import InstagramAPI
import pylibmc
import time

__version__ = '0.1'
__author__ = 'ccbikai'

""" 同步逻辑函数实现 """

def sinaTlRss():
    """ 获取微博timeline，并处理为rss.xml模版所需格式 """
    s = Sina(SINA_CONF['app_key'], SINA_CONF['app_secret'], SINA_CONF['redirect_uri'], SINA_CONF['access_token'])

    statuses = s.getTimeline(RSS_COUNT)
    for tweet in statuses:
        time = tweet.created_at.split(' ')
        tweet.created_at = ' '.join([time[2],time[1],time[5],time[3],time[4]])

    uid = s.getUid()
    user = s.getUser(uid)
    appkey = SINA_CONF['app_key']

    return statuses, user, appkey

    
def sinaFavRss():
    """ 获取微博收藏，并处理为rss.xml模版所需格式 """
    s = Sina(SINA_CONF['app_key'], SINA_CONF['app_secret'], SINA_CONF['redirect_uri'], SINA_CONF['access_token'])

    statuses = s.getFavorites(RSS_COUNT)
    tweets = []
    for tweet in statuses:
        time = tweet.favorited_time.split(' ')
        tweet.status.created_at = ' '.join([time[2],time[1],time[5],time[3],time[4]])
        tweets.append(tweet.status)

    uid = s.getUid()
    user = s.getUser(uid)
    appkey = SINA_CONF['app_key']

    return tweets, user, appkey

def tencTlRss():
    """ 获取微博timeline，并处理为rss.xml模版所需格式 """
    t = Tenc(TENC_CONF['app_key'], TENC_CONF['app_secret'], TENC_CONF['callback_url'], TENC_CONF['access_token'], TENC_CONF['openid'])

    data = t.getTimeline(RSS_COUNT)
    name = t.getUid()
    user = t.getUser(name)
    appkey = TENC_CONF['app_key']
    
    return data, user, appkey

def tencFavRss():
    """ 获取微博收藏，并处理为rss.xml模版所需格式 """
    t = Tenc(TENC_CONF['app_key'], TENC_CONF['app_secret'], TENC_CONF['callback_url'], TENC_CONF['access_token'], TENC_CONF['openid'])

    data = t.getFavorites(RSS_COUNT)
    name = t.getUid()
    user = t.getUser(name)
    appkey = TENC_CONF['app_key']

    return data, user, appkey

def inst2sina(userid):
    """ 同步最新一条instagram状态到微博 """
    api = InstagramAPI(access_token=INST_CONF['access_token'])
    recent_media, next = api.user_recent_media(user_id=userid, count=1)
    # 验证request返回值正常，如果不正常，可能是access_token过期
    if recent_media['meta']['code'] == 200:
        s = Sina(SINA_CONF['app_key'], SINA_CONF['app_secret'], SINA_CONF['redirect_uri'], SINA_CONF['access_token'])
        
        if recent_media['data'][0]['location'] != None:
            if recent_media['data'][0]['caption']:
                id = s.postTweet(' '.join([recent_media['data'][0]['caption']['text'],recent_media['data'][0]['link']," #instagram#"]), 
                recent_media['data'][0]['images']['standard_resolution']['url'], 
                lat=str(recent_media['data'][0]['location']['latitude']), long=str(recent_media['data'][0]['location']['longitude']))
            else:
                id = s.postTweet(recent_media['data'][0]['link'], recent_media['data'][0]['images']['standard_resolution']['url'], 
                lat=str(recent_media['data'][0]['location']['latitude']), long=str(recent_media['data'][0]['location']['longitude']))
        else:
            if recent_media['data'][0]['caption']:
                id = s.postTweet(' '.join([recent_media['data'][0]['caption']['text'], recent_media['data'][0]['link']," #instagram#"]), 
                recent_media['data'][0]['images']['standard_resolution']['url'])
            else:
                id = s.postTweet(recent_media['data'][0]['link'], recent_media['data'][0]['images']['standard_resolution']['url'])
    else:
        return None
    return id

def inst2tenc(userid):
    """ 同步最新一条instagram状态到腾讯微博 """
    api = InstagramAPI(access_token=INST_CONF['access_token'])
    recent_media, next = api.user_recent_media(user_id=userid, count=1)
    # 验证request返回值正常，如果不正常，可能是access_token过期
    if recent_media['meta']['code'] == 200:
        t = Tenc(TENC_CONF['app_key'], TENC_CONF['app_secret'], TENC_CONF['callback_url'], TENC_CONF['access_token'], TENC_CONF['openid'])
   
        if recent_media['data'][0]['location'] != None:
            if recent_media['data'][0]['caption']:
                id = t.postPic(' '.join([recent_media['data'][0]['caption']['text'],recent_media['data'][0]['link']," #instagram#"]), 
                recent_media['data'][0]['images']['standard_resolution']['url'], 
                lat=str(recent_media['data'][0]['location']['latitude']), long=str(recent_media['data'][0]['location']['longitude']))
            else:
                id = t.postPic(recent_media['data'][0]['link'], recent_media['data'][0]['images']['standard_resolution']['url'], 
                lat=str(recent_media['data'][0]['location']['latitude']), long=str(recent_media['data'][0]['location']['longitude']))
        else:
            if recent_media['data'][0]['caption']:
                id = t.postPic(' '.join([recent_media['data'][0]['caption']['text'], recent_media['data'][0]['link']," #instagram#"]), 
                recent_media['data'][0]['images']['standard_resolution']['url'])
            else:
                id = t.postPic(recent_media['data'][0]['link'], recent_media['data'][0]['images']['standard_resolution']['url'])
    else:
        return None
    return id