import re
import urllib
import urllib.request
import urllib.error
import time
import json

from urllib.request import urlopen

#盘搜搜
class GetLinkPan:
    def __init__(self):
        self._baseUrl = "http://www.pansou.com"

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self,key):
        list_all = []
        asc_str = urllib.parse.quote(key)
        url = self._baseUrl+'/?q={0}'.format(asc_str)
        html = urlopen(url).read().decode()
        match_str = re.findall('function _getData(.*?)function _combine',html,re.I|re.S)
        match_str = re.findall('.*?({.*}).*',str(match_str),re.I|re.S)
        match_str = re.findall(r'ajax.*?,.*url:(.*?),', str(match_str), re.I | re.S)
        match_str = re.findall(r'http.*?[a-zA-Z_]+', str(match_str), re.I | re.S)
        if match_str:
            first_url = self.GetKeyWordUrl(match_str[0],1,asc_str)
            list_count = self.GetResourceCount(first_url)
            for i in range(1,list_count):
                time.sleep(2)
                temp_url = self.GetKeyWordUrl(match_str[0],i,asc_str)
                temp_list = self.GetListDat(temp_url)
                list_all.extend(temp_list)
        return list_all

    def GetKeyWordUrl(self,url,page,key):
        t1 = self.GetUTCTime()           #分别获取时间
        asc_str = urllib.parse.quote(key)
        t2 = self.GetUTCTime()
        new_url = url+'?callback=jQuery17209849051853487387_{0}&q={1}&p={2}&_={3}'.format(t1,asc_str,str(page),t2)
        return new_url

    def GetResourceCount(self,url):
        js_str = urlopen(url).read().decode()
        match_str = re.findall('.*?({.*}).*',js_str,re.I|re.S)
        js_selector = json.loads(match_str[0])
        return int(int(js_selector['list']['count'])/10)

    def GetListDat(self,url):
        list_all = []
        js_str = urlopen(url).read().decode()
        match_str = re.findall('.*?({.*}).*', js_str, re.I | re.S)
        js_selector = json.loads(match_str[0])
        my_list = js_selector['list']['data']
        for item in my_list:
            dict = {
                'Title':item['title'],
                'Link': item['link'],
                'BLink': item['blink'],
            }
            list_all.append(dict)
        return list_all


    #获取UTC时间
    def GetUTCTime(self):
        total_sec = str(time.time()).replace('.', '')
        total_sec = total_sec[0:12]
        return total_sec