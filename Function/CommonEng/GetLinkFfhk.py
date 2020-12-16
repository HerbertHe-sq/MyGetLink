import re
from urllib.request import urlopen

import requests
import urllib


class GetLinkFfhk:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url


    def SearchMasterKey(self,key):
        all_list = []

        asc_str = urllib.parse.quote(key)
        url = self._baseUrl+'/index.php?s=vod-search-name'

        headers={
            'Host': 'www.55hk.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Content-Length': '21',
            'Origin': self._baseUrl,
            'Connection': 'keep-alive',
            'Referer': self._baseUrl+'/',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

        data={
            'wd':asc_str
        }

        req = requests.post(url=url,headers=headers,data=data)
        req.encoding='utf-8'
        match_str = re.findall('<li class="mb">(.*?)</li>',req.text,re.I|re.S)
        for item in match_str:
            title = re.findall('<a class="li-hv" href=".*?title="(.*?)"',item,re.I|re.S)
            link = re.findall('<a class="li-hv" href="(.*?)"', item, re.I | re.S)
            img = re.findall('data-original="(.*?)"', item, re.I | re.S)
            dict_temp={
                'MovName':title[0],
                'MovLink': self._baseUrl+link[0],
                'MovImg': img[0]
            }
            all_list.append(dict_temp)
        return all_list

    def SearchLink(self,dict_mov):
        url = dict_mov['MovLink']
        headers={
            'Host': 'www.55hk.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'http://www.55hk.net/index.php?s=vod-search-name',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<ul class="urlli">(.*?)</ul>',req.text,re.I|re.S)
        all_link = []
        for item in match_str:
            link = re.findall('href=\'(.*?)\'', item, re.I | re.S)
            id = re.findall('target="_self" id="(.*?)"', item, re.I | re.S)
            title = re.findall('<a title=\'(.*?)\'', item, re.I | re.S)
            for i in range(0,len(title)):
                dict_play={
                    'ID':id[i],
                    'Title':title[i],
                    'Link':self._baseUrl+link[i]
                }
                all_link.append(dict_play)

        #获取链接
        for item in all_link:
            temp_link = self._GetLinkM3U8(url,item['Link'])
            item['PlayLink'] = temp_link.replace('\/','/')

        return all_link

    def _GetLinkM3U8(self,root_url,link):
        headers={
            'Host': 'www.55hk.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': root_url,
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }

        req = requests.get(url=link,headers=headers)
        req.encoding='utf-8'
        match_link = re.findall('var cms_player = {"url":"(.*?)"',req.text,re.I|re.S)
        return match_link[0]

    # 获取图片
    def DownMovPicture(self, link):
        img = urlopen(link).read()
        return img
