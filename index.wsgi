# -*- coding: utf-8 -*-

#import tornado.ioloop
import tornado.web
from sync import *
import json

# 以下为SAE需要
import os
os.environ['disable_fetchurl'] = True

class SinaTlRss(tornado.web.RequestHandler):
    def get(self):
        tl = sinaTlRss()
        self.set_header("Content-Type", "application/xml; charset=UTF-8")
        self.render("rss.xml", statuses=tl[0], user=tl[1], appkey=tl[2])

class SinaFavRss(tornado.web.RequestHandler):
    def get(self):
        fav = sinaFavRss()
        self.set_header("Content-Type", "application/xml; charset=UTF-8")
        self.render("rss.xml", statuses=fav[0], user=fav[1], appkey=fav[2])

class Sina2Tenc(tornado.web.RequestHandler):
    def get(self):
        id = sina2tenc()
        self.write(str(id))

class CallBack(tornado.web.RequestHandler):
    def get(self):
        self.write(self.get_argument("hub.challenge", "no response"))

    def post(self):
        data = json.loads(self.request.body)
        for d in data:
            if d['object'] == u"user":
                id = inst2sina(d['object_id'])
        self.write("sync ok")


application = tornado.web.Application([
    (r"/rss", SinaTlRss),
    (r"/fav", SinaFavRss),
    (r"/sync", Sina2Tenc),
    (r"/call", CallBack),
    (r"/", tornado.web.RedirectHandler, dict(url="http://instagram.sinaapp.com/rss")),
], debug=True)

#if __name__ == "__main__":
#    application.listen(8888)
#    tornado.ioloop.IOLoop.instance().start()
