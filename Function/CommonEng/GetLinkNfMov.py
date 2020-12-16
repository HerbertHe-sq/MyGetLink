import re
import urllib
from urllib.request import urlopen

import requests

#奈非影视
class GetLinkNfMov:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self,key):
        all_list = []
        headers={
            'Host': 'www.nfmovies.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': 'https://www.nfmovies.com/detail/?54169.html',
            'Connection': 'keep-alive'
        }
        asc_str = urllib.parse.quote(key)
        url = self._baseUrl+'/search.php?searchword=' + asc_str
        req = requests.get(url=url,headers=headers)
        match_str = re.findall('<ul.*? id="searchList">(.*?)</ul>',req.text,re.I|re.S)[0]
        match_list = re.findall('<li(.*?)</li>', match_str, re.I | re.S)
        for item in match_list:
            h_text = re.findall('<h4 class="title">(.*?)</h4>', item, re.I | re.S)[0]
            img_temp = re.findall('<div class="thumb">.*?<a.*?data-original="(.*?)">',item,re.I|re.S)[0]
            title = re.findall('>(.*?)</a>',h_text,re.I|re.S)[0]
            link = re.findall('href="(.*?)">',h_text,re.I|re.S)[0]
            dict_temp = {
                'MovName': title,
                'MovLink': self._baseUrl + link,
                'MovImg':self._baseUrl+img_temp
            }
            all_list.append(dict_temp)
        return all_list

    def SearchLink(self,dict_temp):
        all_link = []
        url = dict_temp['MovLink']

        headers = {
            'Host': 'www.nfmovies.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<div id="playlist(.*?)</ul>',req.text,re.I|re.S)
        for list_item in match_str:
            match_list = re.findall('<li>(.*?)</li>', list_item, re.I | re.S)
            for item in match_list:
                mov_title = re.findall('title=\'(.*?)\'', item, re.I | re.S)[0]
                mov_link = self._baseUrl+re.findall('href=\'(.*?)\'', item, re.I | re.S)[0]
                link = self.Search_M3U8Link(mov_link)

                dict_play = {
                    'Title': mov_title,
                    'PlayLink': urllib.parse.unquote(link)
                }
                all_link.append(dict_play)

        return all_link

    def Search_M3U8Link(self,url):
        req = requests.get(url=url)
        link = re.findall('var now=unescape\("(.*?)"\);', req.text, re.I | re.S)[0]
        return link

    # 获取图片
    def DownMovPicture(self, link):
        img = urlopen(link).read()
        return img