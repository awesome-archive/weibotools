#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qqweibo import APIClient

class Tenc(object):
    def __init__(self, app_key, app_secret, callback_url, access_token, openid):
        self.api = APIClient(app_key, app_secret, redirect_uri=callback_url)
        self.api.set_access_token(access_token, openid, "1521094035")
    
    def getTimeline(self, count):
        """ 获取用户当前发布的微博 """
        timeline = self.api.get.statuses__broadcast_timeline(format="json",pageflag=0,pagetime=0,lastid=0,contenttype=0,reqnum=count, type=1)
        
        return timeline.data
    
    def getFavorites(self, count):
        """ 获取用户当前收藏的微博 """
        favs = self.api.get.fav__list_t(format="json",pageflag=0,pagetime=0,lastid=0,reqnum=count)
        
        return favs.data
    
    def getUid(self):
        """ 获取当前用户UID """
        uid = self.api.get.user__info(format="json")
        
        return uid.data.name
    
    def getUser(self, name):
        """ 获取用户信息 """
        user = self.api.get.user__other_info(format="json",name=name)
        
        return user.data

    def postPic(self, content, pic_url, longitude='116.397717', latitude='39.903224'):
        if longitude==None or latitude==None:
            t = self.api.post.t__add_pic(content= content, pic=pic_url)
        else:
            t = self.api.post.t__add_pic(content= content, longitude=longitude, latitude=latitude, pic=pic_url)

        return t.id