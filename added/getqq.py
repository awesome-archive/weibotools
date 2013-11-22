#-*- coding:utf-8 -*-

import sys
sys.path.append("..")

from conf import *

""" 参考http://wiki.open.t.qq.com/index.php/OAuth2.0%E9%89%B4%E6%9D%83 """

url1 = "https://open.t.qq.com/cgi-bin/oauth2/authorize?client_id=%s&response_type=code&redirect_uri=%s"
        % (TENC_CONF['app_key'], TENC_CONF['callback_url'])

print "访问该url并记录openid=OPENID"
print url1

url2 = "https://open.t.qq.com/cgi-bin/oauth2/access_token?client_id=%s&client_secret=%s&redirect_uri=%s&grant_type=authorization_code&code=CODE"
        % (TENC_CONF['app_key'], TENC_CONF['app_secret'], TENC_CONF['callback_url'])

print "访问该url并记录accesstoken"
print url2