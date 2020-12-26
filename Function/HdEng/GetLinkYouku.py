import urllib
from urllib import request

import requests
from http import cookiejar

class GetLinkYouku:
    def __init__(self):
        self._baseUrl = ''
        self._searchUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SetSearchUrl(self,url):
        self._searchUrl = url

    def SearchMasterKey(self,key):
        all_list = []
        asc_str = urllib.parse.quote(key)
        url = self._searchUrl.format(key)

        data={
            'searchfrom':'1'
        }

        headers = {
            'Host': 'so.youku.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

        self._GetCookie()

        req = requests.get(url=url,params=data,headers=headers)
        req.encoding = 'utf-8'
        print(req.text)

    def _GetCookie(self):
        dic_cookie = {}
        # 声明一个CookieJar对象实例来保存cookie
        cookie = cookiejar.CookieJar()
        # 利用urllib.request库的HTTPCookieProcessor对象来创建cookie处理器,也就CookieHandler
        handler = request.HTTPCookieProcessor(cookie)
        # 通过CookieHandler创建opener
        opener = request.build_opener(handler)
        opener.addheaders=[
        ('Host', 'www.youku.com'), #注意修改host,不用也行
        ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'),
        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
        ('Accept-Language', 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'),
        ('Accept-Encoding', 'gzip, deflate, br'),
        ('Connection', 'keep-alive')
        ]
        # 此处的open方法打开网页
        response = opener.open(self._baseUrl)
        # 打印cookie信息
        for item in cookie:
            dic_cookie[item.name] = item.value

        return dic_cookie, cookie