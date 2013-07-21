#!/usr/bin/env python
# -*- coding: utf-8 -*-

from qqweibo import APIClient

class Tenc(object):
    def __init__(self, app_key, app_secret, callback_url, access_token, openid):
        self.api = APIClient(app_key, app_secret, redirect_uri=callback_url)
        self.api.set_access_token(access_token, openid, "1521094035")

    def postTweet(self, content, longitude=None, latitude=None):
        if longitude==None or latitude==None:
            self.api.post.t__add(content=content)
        else:
            self.api.post.t__add(content=content, longitude=longitude, latitude=latitude)

        return

    def postPic(self, content, pic_url, longitude=None, latitude=None):
        if longitude==None or latitude==None:
            self.api.post.t__add_pic_url(content=content, pic_url=pic_url)
        else:
            self.api.post.t__add_pic_url(content=content, 
                longitude=longitude, latitude=latitude, pic_url=pic_url)

        return
