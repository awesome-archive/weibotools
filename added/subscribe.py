#-*- coding:utf-8 -*-

import sys
sys.path.append("..")

from instagram.client import InstagramAPI

# 注册IG app获取一下内容
client_id = ""
client_secret = ""

# 需要注册的回调url
callback_url = "http://demo/call"

api = InstagramAPI(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')

response = api.create_subscription(object='user', aspect='media', callback_url=callback_url)

print response