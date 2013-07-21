# -*- coding: utf-8 -*-

from conf import *
from sina import *
from tenc import *
from instagram.client import InstagramAPI
import pylibmc

__version__ = '0.1'
__author__ = 'zhu327'

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

def sina2tenc():
    """ 记录最新一条微博id到Memcache,比较id后同步到腾讯 """
    s = Sina(SINA_CONF['app_key'], SINA_CONF['app_secret'], SINA_CONF['redirect_uri'], SINA_CONF['access_token'])
    statuses = s.getTimeline(1)

    mc = pylibmc.Client()

    if statuses[0].id > mc.get("tid"):
        mc.set("tid", statuses[0].id)
        t = Tenc(TENC_CONF['app_key'], TENC_CONF['app_secret'], TENC_CONF['callback_url'], TENC_CONF['access_token'], TENC_CONF['openid'])
        if 'original_pic' in statuses[0].keys():
            if statuses[0].geo == None:
                t.postPic(statuses[0].text, statuses[0].original_pic)
            else:
                t.postPic(statuses[0].text, statuses[0].original_pic, longitude=statuses[0].geo.coordinates[1], latitude=statuses[0].geo.coordinates[0])
        else:
            if statuses[0].geo == None:
                t.postTweet(statuses[0].text)
            else:
                t.postTweet(statuses[0].text, longitude=statuses[0].geo.coordinates[1], latitude=statuses[0].geo.coordinates[0])

    return mc.get("tid")

def inst2sina(userid):
    """ 同步最新一条instagram状态到微博 """
    api = InstagramAPI(access_token=INST_CONF['access_token'])
    recent_media, next = api.user_recent_media(user_id=userid, count=1)
    # 验证request返回值正常，如果不正常，可能是access_token过期
    if recent_media['meta']['code'] == 200:
        s = Sina(SINA_CONF['app_key'], SINA_CONF['app_secret'], SINA_CONF['redirect_uri'], SINA_CONF['access_token'])
        
        if recent_media['data'][0]['location'] != None:
            if recent_media['data'][0]['caption']:
                id = s.postTweet(' '.join([recent_media['data'][0]['caption']['text'], recent_media['data'][0]['link']]), 
                recent_media['data'][0]['images']['standard_resolution']['url'], 
                lat=str(recent_media['data'][0]['location']['latitude']), long=str(recent_media['data'][0]['location']['longitude']))
            else:
                id = s.postTweet(recent_media['data'][0]['link'], recent_media['data'][0]['images']['standard_resolution']['url'], 
                lat=str(recent_media['data'][0]['location']['latitude']), long=str(recent_media['data'][0]['location']['longitude']))
        else:
            if recent_media['data'][0]['caption']:
                id = s.postTweet(' '.join([recent_media['data'][0]['caption']['text'], recent_media['data'][0]['link']]), 
                recent_media['data'][0]['images']['standard_resolution']['url'])
            else:
                id = s.postTweet(recent_media['data'][0]['link'], recent_media['data'][0]['images']['standard_resolution']['url'])
    else:
        return None
    return id