import base64
from urllib.request import urlopen

import requests
import re
import time


#乐视直播网
class GetLinkLiveLS:
    def __init__(self):
        self._baseSeaUrl = ''
        self._baseUrl=''
        self._baseSigUrl=''

    def SetSigUrl(self,url):
        self._baseSigUrl=url

    def SetBaseUrl(self,url):
        self._baseUrl=url

    def SetBaseSeaUrl(self,url):
        self._baseSeaUrl = url

    def SearchPlace(self):
        all_addr_list = []
        headers={
            'Host': 'www.leshitya.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=self._baseSeaUrl,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<ul class="dhs">(.*?)</ul>',req.text,re.I|re.S)
        match_list = re.findall('<li><a.*?</li>',match_str[0],re.I|re.S)
        for match_item in match_list:
            title = re.findall('title="(.*?)"',match_item,re.I|re.S)
            link = re.findall('href="(.*?)"',match_item,re.I|re.S)
            dict_addr={
                'AddrName':title[0],
                'AddrLink':link[0]
            }
            if not '/tv/' in link[0]:
                all_addr_list.append(dict_addr)

        #match_local_str = re.findall('<div id="content_jr">(.*?)</div>',req.text,re.I|re.S)
        match_local_list = re.findall('<dd class="title">(.*?)</dd>',req.text,re.I|re.S)
        for match_item in match_local_list:
            title = re.findall('title="(.*?)"', match_item, re.I | re.S)
            link = re.findall('href="(.*?)"', match_item, re.I | re.S)
            dict_addr = {
                'AddrName':title[0],
                'AddrLink':link[0]
            }
            all_addr_list.append(dict_addr)
        return all_addr_list

    #获取频道
    def SearchTvProgram(self, dict_addr):
        all_live_list = []
        url = self._baseUrl+dict_addr['AddrLink']
        headers = {
            'Host': 'www.leshitya.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'

        match_str = re.findall('<dd class="title">(.*?)</dd>',req.text, re.I | re.S)
        for match_item in match_str:
            title = re.findall('title="(.*?)"', match_item, re.I | re.S)
            link = re.findall('href="(.*?)"', match_item, re.I | re.S)
            dict_tv_list = {
                'LiveTitle': title[0],
                'LiveLink': link[0],
            }
            all_live_list.append(dict_tv_list)
        return all_live_list

    def SearchTvLink(self, dict_live):
        list_link = []
        url = self._baseUrl+dict_live['LiveLink']
        headers = {
            'Host': 'www.leshitya.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<iframe.*?src="(.*?)"',req.text,re.I|re.S)[0]

        #分情况进行特殊处理
        if 'http://list.leshitya.com' in match_str:
            link = self._GetLinkM3U8_SingleSp1(match_str)
            if '&autoPlay=true' in link:
                link = link.replace('&autoPlay=true','')
            dict_link = {
                'LiveTitle': 'Unknow Source',
                'LiveLink': link
            }
            list_link.append(dict_link)
        elif 'mini.meitiantv.com' in match_str:
            self._GetLinkM3U8_SingleSp2(match_str)
        else:
            all_link,flag = self._GetAllSignal(match_str,url)
            if flag:
                for item in all_link:
                    link = self._GetLinkM3U8(item,url)
                    dict_link={
                        'LiveTitle':item['SigName'],
                        'LiveLink':link
                    }
                    list_link.append(dict_link)
            else:
                link = self._GetLinkM3U8_Sigle(match_str,url)
                dict_link = {
                    'LiveTitle': 'Unknow Source',
                    'LiveLink': link
                }
                list_link.append(dict_link)
        return list_link


    def _GetAllSignal(self,url,root_url):
        list_link = []
        flag = True
        headers={
            'Host': 'mukgu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': root_url,
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        if '</select>' in req.text:
            match_str = re.findall('<select(.*?)</select>',req.text,re.I|re.S)
            match_list = re.findall('<option.*?</option>', match_str[0], re.I | re.S)
            for match_item in match_list:
                title = re.findall('>(.*?)</option>', match_item, re.I | re.S)[0]
                link = re.findall('value="(.*?)"', match_item, re.I | re.S)[0]
                if not '/' in link:
                    link = '/'+link
                link = self._baseSigUrl+link
                dict_sig={
                    'SigName': title,
                    'SigLink':link
                }
                list_link.append(dict_sig)
            flag = True
        else:
            flag = False
        return list_link,flag

    #获取连接
    def _GetLinkM3U8(self,dict_sig,root_url):
        list_link = []
        headers = {
            'Host': 'mukgu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': root_url,
            'Upgrade-Insecure-Requests': '1'
        }
        req = requests.get(url=dict_sig['SigLink'], headers=headers)
        req.encoding = 'utf-8'
        if 'jwplayer' in req.text:
            match_str = re.findall('jwplayer\(.*?\).setup\((.*?)\);',req.text,re.I|re.S)
            if 'file:\'' in match_str[0]:
                match_link = re.findall('file:\'(.*?)\',', match_str[0], re.I | re.S)[0]
            else:
                match_link = re.findall('file:"(.*?)",', match_str[0], re.I | re.S)[0]
        else:
            match_str = re.findall('<iframe class=videoplayer src="(.*?)"', req.text, re.I | re.S)
            match_link = match_str[0]

        return match_link

    #单一信号源
    def _GetLinkM3U8_Sigle(self,url,root_url):
        headers = {
            'Host': 'mukgu.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': root_url,
            'Upgrade-Insecure-Requests': '1'
        }
        req = requests.get(url=url, headers=headers)
        req.encoding = 'utf-8'
        if 'jwplayer' in req.text:
            match_str = re.findall('jwplayer\(.*?\).setup\((.*?)\);',req.text,re.I|re.S)
            if 'file:\'' in match_str[0]:
                match_link = re.findall('file:\'(.*?)\',', match_str[0], re.I | re.S)[0]
            else:
                match_link = re.findall('file:"(.*?)",', match_str[0], re.I | re.S)[0]
        else:
            match_str = re.findall('<iframe class=videoplayer src="(.*?)"', req.text, re.I | re.S)
            match_link = match_str[0]

        return match_link

    #单一特殊情况
    def _GetLinkM3U8_SingleSp1(self,url):
        link_str=''
        headers={
            'Host': 'list.leshitya.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        html = req.text

        #分情况解析
        if '<embed' in html:
           match_str = re.findall('<embed.*?src="(.*?)".*?>',html,re.I|re.S)[0]
           if 'vurl' in match_str:
               match_str = match_str.split('vurl=')[1]
           link_str = match_str
        elif '<!DOCTYPE html>' in html and 'showPlayer' in html:
            match_str = re.findall('onload = showPlayer\(\'(.*?)\',',html,re.I|re.S)[0]
            link_str = match_str
        elif '<!DOCTYPE html>' in html and 'var fa=' in html:
            match_str = re.findall('var fa=\'(.*?)\';', html, re.I | re.S)[0]
            link_str = match_str
        elif '<object' in html:
            match_str = re.findall('ipadUrl(.*?);}],',html, re.I | re.S)
            match_str = re.findall(':&quot;(.*?)&quot;}]', match_str[0], re.I | re.S)
            link_str = match_str[0]
        elif '<iframe' in html:
            match_str = re.findall('﻿<iframe src="(.*?)"', html, re.I | re.S)[0]
            link_str = match_str
        else:
            print(html)

        return link_str


    # 单一特殊情况
    def _GetLinkM3U8_SingleSp2(self, url):
        pass