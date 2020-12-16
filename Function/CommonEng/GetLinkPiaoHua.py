import re
import urllib
from urllib.request import urlopen

import requests
import json


class GetLinkPiaoHua:
    def __init__(self):
        self._baseUrl=''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self,key):
        all_list = []
        url = self._baseUrl + '/plus/search.php'

        headers={
            'Host': 'www.piaohua.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        data={
            'kwtype':'0',
            'keyword':key,
            'searchtype':'影视搜索'
        }

        req = requests.get(url=url,headers=headers,params=data)
        req.encoding='utf-8'
        match_ul = re.findall('<ul class="ul-imgtxt2 row">(.*?)</ul>',req.text,re.I|re.S)
        match_list = re.findall('<li.*?>(.*?)</li>',match_ul[0],re.I|re.S)
        for item in match_list:
            title = re.findall('<h3>.*?<font color=\'red\'>(.*?)</em>.*?</h3>',item,re.I|re.S)[0].replace('<font color=\'red\'>','').replace('</font>','').replace('<em>','')
            img = re.findall('<img src="(.*?)"',item,re.I|re.S)[0]
            link = re.findall('<h3><a href="(.*?)"',item,re.I|re.S)[0]

            dict_temp = {
                'MovName': title,
                'MovLink': self._baseUrl + link,
                'MovImg': img
            }
            all_list.append(dict_temp)
        return all_list

    def SearchLink(self,dict_temp):
        all_link = []
        url = dict_temp['MovLink']

        req =requests.get(url=url)
        req.encoding = 'utf-8'
        if 'table' in req.text:
            match_tab = re.findall('<table.*?</table>',req.text,re.I|re.S)
            for item in match_tab:
                try:
                    link = re.findall('a href="(.*?)"', item, re.I | re.S)[0]
                    dict_play = {
                       'Title': '',
                       'PlayLink': urllib.parse.unquote(link)
                    }
                    all_link.append(dict_play)
                except:
                    pass
        else:
            match_div = re.findall('<div class="bot">(.*?)</div>', req.text, re.I | re.S)
            for item_tab in match_div:
                match_tab = re.findall('<a href="(.*?)"',item_tab, re.I | re.S)
                for item in match_tab:
                    item = item.replace('\r','')
                    dict_play = {
                       'Title': '',
                       'PlayLink': urllib.parse.unquote(item)
                    }
                    all_link.append(dict_play)
        return all_link

    # 获取图片
    def DownMovPicture(self, link):
        img = requests.get(url=link).content
        return img