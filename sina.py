#!/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo import APIClient
from urllib2 import urlopen

__version__ = '0.1'
__author__ = 'zhu327'

""" 调用微博SDK，对微博相关接口进行简单封装 """

class Sina(object):
    def __init__(self, app_key, app_secret, redirect_uri, access_token):
        """ 初始化微博参数 """
        self.client = APIClient(app_key=app_key, app_secret=app_secret, redirect_uri=redirect_uri)
        self.client.set_access_token(access_token, 1521094035)
    
    def getTimeline(self, count):
        """ 获取用户当前发布的微博 """
        timeline = self.client.statuses.user_timeline.get(count=count, feature=1)
        
        return timeline.statuses
    
    def getFavorites(self, count):
        """ 获取用户当前收藏的微博 """
        favorites = self.client.favorites.get(count=count)
        
        return favorites.favorites
    
    def getUid(self):
        """ 获取当前用户UID """
        uid = self.client.account.get_uid.get()
        
        return uid.uid
    
    def getUser(self, uid):
        """ 获取用户信息 """
        usr = self.client.users.show.get(uid=uid)
        
        return usr
    
    def postTweet(self, status, url, lat=None, long=None):
        """ 
        发送带图片微博,instagram留用
        新浪屏蔽了upload_url_text的非认证用户使用，所以只好自己取数据用upload
        """
        data = urlopen(url)
        if lat == None or long ==None:
            t = self.client.statuses.upload.post(status=status, pic=data)
        else:
            t = self.client.statuses.upload.post(status=status, pic=data, lat=lat, long=long)
        return t.id