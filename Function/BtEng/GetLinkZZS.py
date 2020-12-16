import urllib

import requests
import re
import json

class GetLinkZZS:
    def __init__(self):
        self._baseUrl=''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    #关键字搜索
    def SearchMasterKey(self,key):
        list_data = []
        asc_str = urllib.parse.quote(key)
        url = self._baseUrl+'search?wd='+asc_str

        headers={
            'Host': 'zhongzi8.xyz',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': self._baseUrl,
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        html = req.text

        if '<li class="last_p">' in html:
            page_count = int(re.findall('<li class="last_p">.*?page=(.*?)">Last</a>',html,re.S|re.I)[0])

            #限制爬取页数
            if page_count>20:
                page_count=20
            for i in range(1,page_count):
                temp_url = url + '&sort=rel&page='+str(i)
                temp_req = requests.get(url=temp_url, headers=headers)
                temp_req.encoding = 'utf-8'
                temp_html = temp_req.text
                match_str = re.findall('<li class="media">(.*?)</li>', temp_html, re.I | re.S)
                for item in match_str:
                    bt_name = re.findall('<a.*?title="(.*?)"', item, re.I | re.S)[0]
                    bt_link = re.findall('<a.*?href="(.*?)"', item, re.I | re.S)[0]
                    dict_bt = {
                        'BtName': bt_name,
                        'BtLink': bt_link,
                        'BtRootUrl':url
                    }
                    list_data.append(dict_bt)
        else:
            match_str = re.findall('<li class="media">(.*?)</li>', html, re.I | re.S)
            for item in match_str:
                bt_name = re.findall('<a.*?title="(.*?)"', item, re.I | re.S)[0]
                bt_link = re.findall('<a.*?href="(.*?)"', item, re.I | re.S)[0]
                dict_bt = {
                    'BtName': bt_name,
                    'BtLink': bt_link,
                    'BtRootUrl': url
                }
                list_data.append(dict_bt)
        return list_data

    def SearchLink(self,dict_data):
        headers={
            'Host': 'zhongzi8.xyz',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': dict_data['BtRootUrl'],
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }

        url = self._baseUrl+dict_data['BtLi' \
                                      'nk']

        req = requests.get(url=url,headers=headers)
        req.encoding = 'utf-8'
        try:
            match_str = re.findall('<div class="bt-opt"><a href="(.*?)" id="down-url"',req.text,re.I|re.S)[0]
        except Exception as msg:
            match_str = msg
        return match_str