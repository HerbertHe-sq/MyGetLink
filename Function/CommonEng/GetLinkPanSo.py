import urllib
from urllib import request

import requests
import re
import base64
import urllib

from http import cookiejar

#PanSouSou
class GetLinkPanSo:
    def __init__(self):
        self._baseUrl=''

    def SetBaseUrl(self,url):
        self._baseUrl = url


    def SearchMasterKey(self, key):
        all_list = []

        asc_str = urllib.parse.quote(key)
        for i in range(1,5):
            #url = "http://www.pansoso.com/zh/{0}_{1}".format(asc_str,i)
            url = self._baseUrl.format(asc_str, i)

            hearders = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Connection': 'keep-alive',
                'Host': 'www.pansoso.com',
                'Referer':'http://www.pansoso.com/',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
            }

            html = requests.get(url,headers=hearders)
            html.encoding='utf-8'

            match_str = re.findall('<div class="pss"><h2>(.*?)</h2>', html.text, re.S | re.I)
            for item in match_str:
                link_str = re.findall('<a href="(.*?)"', item, re.S | re.I)[0]
                name_str = re.findall('>(.*?)</a>', item, re.S | re.I)[0]
                dic_link={
                    'Name':name_str,
                    'Link':link_str
                }
                all_list.append(dic_link)
        return all_list

    def SearchPanLink(self,url):
        hearders = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'www.pansoso.com',
            'Referer': 'http://www.pansoso.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
        }

        html = requests.get(url, headers=hearders)
        html.encoding = 'utf-8'
        match_str = re.findall('<div class="down">(.*?)</div>', html.text, re.S | re.I)[0]
        match_str = re.findall('href="(.*?)"', match_str, re.S | re.I)[0]

        html_link = requests.get(match_str,headers=hearders)
        html_link.encoding='utf-8'

        match_str = re.findall('<div class="file">(.*?)</div>', html_link.text, re.S | re.I)
        for item in match_str:
            if item.find('href')>=0:
                match_link = re.findall('href="(.*?)"', item, re.S | re.I)
        temp_str=''
        code,link = self.EnterPanLink(match_link[0])
        temp_str='Status Code:'+str(code)+'\r\n'+link+'\r\n'+match_link[0]
        return temp_str

    def EnterPanLink(self,url):
        hearders = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'to.pansoso.com',
            'Upgrade-Insecure-Requests':'1',
            'Cookie':'UM_distinctid=16f63f923644aa-08056bd67cbbb98-4c302b7a-13c680-16f63f923652db',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
        }
        sp_str = url.split('?')[1]
        sp_str = sp_str.split('&')
        sp_str[0] = sp_str[0].replace('url=','')
        sp_str[1] = sp_str[1].replace('a=', '')
        data={
            'url':sp_str[0],
            'a':sp_str[1]
        }
        req = requests.get(url,headers=hearders,data=data,allow_redirects=False)
        if req.status_code==302:
            return req.status_code,req.headers['Location']
        else:
            return req.status_code,""


