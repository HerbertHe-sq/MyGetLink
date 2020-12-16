import re
import requests
import urllib
import urllib.request
import urllib.error
import base64

from urllib.request import urlopen

#www.22tu.cc迅播
class GetLinkXplay:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self, key):
        all_list = []
        asc_str = urllib.parse.quote(key)
        url = self._baseUrl

        data={
            'wd':asc_str,
            'submit':'%E6%90%9C+%E7%B4%A2' #搜+索
        }

        headers={
            "Host": "www.22tu.cc",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            #"Content-Type": "application/x-www-form-urlencoded",
            "Origin": "http://www.22tu.cc",
            "Connection": "keep-alive",
            "Referer": "http://www.22tu.cc/",
            "Upgrade-Insecure-Requests": "1"
        }

        req = requests.post(url=url,data=data,headers=headers)
        req.encoding='utf-8'

        match_str = re.findall('<ul class="mlist">(.*?)</ul>',req.text,re.S|re.I)
        match_list = re.findall('<li>.*?<a(.*?)</a>.*?</li>', match_str[0], re.S | re.I)
        for item in match_list:
            link = re.findall('href="(.*?)"',item,re.I|re.S)[0]
            title = re.findall('title="(.*?)"',item,re.I|re.S)[0]
            img = re.findall('<img src="(.*?)"',item,re.I|re.S)[0]
            if not 'http' in img:
                img = 'http://www.22tu.cc'+img
            dict={
                'MovieName':title,
                'Link':link,
                'Img':img
            }
            all_list.append(dict)
        return all_list

    def SearchLinkBt(self, url):
        all_link = []
        all_play_link = []
        my_url = 'http://www.22tu.cc'+url

        headers={
            "Host": "www.22tu.cc",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }

        req = requests.get(url=my_url,headers=headers)
        req.encoding='utf-8'
        if '<ul class="downurl down-list">' in req.text:
            match_str = re.findall('<ul class="downurl down-list">(.*?)</ul>',req.text,re.I|re.S)
            match_str = re.findall('<li class="down-item">(.*?)</li>', match_str[0], re.I | re.S)
            for item in match_str:
                temp_name = re.findall('source-url=".*?">(.*?)</a>',item,re.I|re.S)[0]
                d_url = re.findall('<a href="(.*?)"',item,re.I|re.S)[0]
                s_url = re.findall('source-url="(.*?)"',item,re.I|re.S)[0]
                temp_str = 'AA' + d_url + 'ZZ'
                temp_str = base64.b64encode(temp_str.encode('utf-8'))
                temp_str = "thunder://" + str(temp_str, 'utf-8')
                dict_down={
                    'MovName':temp_name,
                    'DownUrl':temp_str,
                    'SourceUrl':s_url
                }
                all_link.append(dict_down)

        match_play_str = re.findall('<div class="play-list">(.*?)</div>',req.text,re.I|re.S)
        match_play_str = re.findall('<a(.*?)</a>', match_play_str[0], re.I | re.S)
        for item in match_play_str:
            if not 'href="' in item:
                p_url = re.findall('href=\'(.*?)\'',item,re.I|re.S)[0]
                title = re.findall('title=\'(.*?)\'',item,re.I|re.S)[0]
            else:
                p_url = re.findall('href="(.*?)"', item, re.I | re.S)[0]
                title = re.findall('title="(.*?)"', item, re.I | re.S)[0]
            dict_play = {
                'MovieMode':title,
                'PlayUrl':'http://www.22tu.cc'+p_url
            }
            all_play_link.append(dict_play)
        return all_link,all_play_link