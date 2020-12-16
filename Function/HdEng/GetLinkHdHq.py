import urllib
from urllib.request import urlopen

import requests
import base64
import re

class GetLinkHdHq:
    def __init__(self):
        self._baseUrl=''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self, key):
        all_list = []
        asc_str = urllib.parse.quote(key)
        headers={
            "Host": "gaoqing.la",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        tag_url = self._baseUrl+asc_str
        req = requests.get(url=tag_url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<ul id="post_container" class="masonry clearfix">(.*?)</ul>',req.text,re.I|re.S)
        match_str = re.findall('<li class="post box row fixed-hight">.*?<div class="thumbnail">(.*?)</div>.*?</li>', match_str[0], re.I | re.S)

        for item in match_str:
            title_str = re.findall('title="(.*?)"',item,re.I|re.S)[0]
            url_str = re.findall('<a href="(.*?)"',item,re.I|re.S)[0]
            img = re.findall('<img src="(.*?)"',item,re.I|re.S)[0]
            if not 'http' in img:
                img = 'http://gaoqing.la' + img
            dict = {
                'MovieName':title_str,
                'MovieLink':url_str,
                'Img':img
            }
            all_list.append(dict)
        return all_list

    def SearchLinkBt(self, url):
        headers = {
            "Host": "gaoqing.la",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'

        match_link = re.findall('WEBRip.*?<a style.*?href="(.*?)"',req.text,re.I|re.S)
        if len(match_link)>0:
            match_title = re.findall('WEBRip.*?<a style.*?href=".*?>(.*?)</a></span></p>',req.text,re.I|re.S)
            dict = {
                'MovName':match_title[0],
                'MovLink':match_link[0]
            }
        else:
            dict={}
        return dict

    # 获取图片
    def DownMovPicture(self, link):
        img = urlopen(link).read()
        return img