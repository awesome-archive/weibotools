# WeiboTools #

[@Timmy](http://weibo.com/zhu327)   [@ccbikai](http://weibo.com/ccbikai)

## 功能 ##

1. 新浪微博时间线与收藏夹生成rss;
2. 腾讯微博时间线与收藏夹生成rss;
3. instagram发发布图片同步到新浪微博,腾讯微博.

## 部署 ##
### 环境 ###

SAE(Sina App Engine) python tornado环境.

### 部署 ###

需要修改的文件:

    weibotools
        |--config.yaml
        |--conf.py
        
config.yaml

    ---
    name: pythonweibo
    version: 1
    accesskey: 

name字段改为SAE应用名称,accesskey字段改为SAE应用对应的accesskey值,该值在SAE应用管理界面可以找到.


conf.py

    # 新浪微博app参数
    SINA_CONF = {
            'app_key' : "",
            'app_secret' : "",
            'redirect_uri' : "",
            'access_token' : "",
            }

要使用功能1需要配置这段代码,字典里的前3个元为注册微博应用对应的内容,最后的access_token可以在
[API测试工具](http://open.weibo.com/tools/console)获取.这段配置完成后,功能1就可以正常使用了.

    # 腾讯微博app参数
    TENC_CONF = {
            'app_key' : "",
            'app_secret' : "",
            'callback_url' : "",
            'access_token' : "",
            'openid' : "",
            }


获取access_token和openid的python方法在added目录下的getqq.py脚本可以找到.

    # instagram app参数
    INST_CONF = {
            'access_token' : "",
            }

功能3配置比较复杂,首先用added下的get_access_token.py脚本获取access_token,修改subscribe.py脚本,注册回调url(/call).

## 开发 ##
### 结构 ###

    weibotools
        |--added          一些工具,部署不需要上传
        |--httplib2       instagram需要的模组  
        |--instagram      instagram官方python sdk
        |--conf.py        weibotools配置文件
        |--config.yaml    SAE的配置文件
        |--index.wgsi     tornado main文件
        |--qqweibo.py     腾讯微博sdk
        |--qqrss.xml      腾讯微博rss模版
        |--rss.xml        rss模版
        |--sina.py        新浪微博api简单封装
        |--sync.py        同步的核心逻辑
        |--tenc.py        腾讯微博api简单封装
        |--weibo.py       新浪微博sdk

### 依赖 ###

- 新浪微博sdk:[@michaelliao](https://github.com/michaelliao/sinaweibopy);
- 腾讯微博sdk:[@jinuljt](https://github.com/jinuljt/qqweibov2);
- IG(instagram) sdk:[@yibin001](https://github.com/yibin001/Instagram4sae).

### 设计 ###

#### 功能1 ####

/rss /fav url 收到get请求后,获取10条最新微博,tornado渲染模版,返回rss应答请求.

#### 功能2 ####

/qqrss /qqfav url 收到get请求后,获取10条最新微博,tornado渲染模版,返回rss应答请求.

#### 功能3 ###

IG用户上传1张图片,触发post到回调url /call,weibotools获取IG最新的图片,并发布到新浪微博.实时同步,基本无延时.

## 扩展 ##

自从有了[ifttt](http://ifttt.com)终于可以在墙内同步信息到墙外的信息了,
weibotools生成rss配合ifttt即可同步tweet到twiter,facebook,收藏夹rss可以同步到印象笔记.

## 问题 ##

SAE连接调用IG api可能超时,造成部分图片可能不能同步成功,这不是代码问题.
