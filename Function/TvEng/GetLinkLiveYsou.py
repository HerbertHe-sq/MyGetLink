import re
import requests
import json

class GetLinkLiveYsou:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchPlace(self):
        all_list = []
        self._AddSpPalce(all_list)

        url = self._baseUrl
        headers={
            'Host': 'www.yunsosuo.cc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<div class="pg-list-panel">.*?<ul>(.*?)</ul>',req.text,re.I|re.S)[0]
        match_list = re.findall('<a class.*?</a>',match_str,re.I|re.S)
        for item in match_list:
            title = re.findall('>(.*?)</a>',item,re.I|re.S)[0].replace('&nbsp;','').replace(' ','')
            link = re.findall('href="(.*?)"',item,re.I|re.S)[0]
            if not 'http' in link:
                link = self._baseUrl+link
            dict_place = {
                'PlaceName':title,
                'PlaceLink':link
            }
            all_list.append(dict_place)
        return all_list


    def _AddSpPalce(self,list):
        dict_place_1 = {
            'PlaceName': '央视频道',
            'PlaceLink': self._baseUrl+'/cctv/'
        }
        dict_place_2 = {
            'PlaceName': '卫视频道',
            'PlaceLink': self._baseUrl + '/tv/'
        }
        list.append(dict_place_1)
        list.append(dict_place_2)

    #搜索电视节目
    def SearchTvProgram(self,dict_place):
        all_list = []
        url = dict_place['PlaceLink']
        headers={
            'Host': 'www.yunsosuo.cc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<dd class="title"><a(.*?)</a>',req.text,re.I|re.S)
        for item in match_str:
            title = re.findall('title="(.*?)"',item,re.I|re.S)[0]
            link = re.findall('href="(.*?)"',item,re.I|re.S)[0]
            if not 'http' in link:
                link = self._baseUrl+link
            dict_prog = {
                'LiveTitle':title,
                'LiveLink':link,
                'RootUrl':url
            }
            all_list.append(dict_prog)
        return all_list

    def GetM3U8Link(self,dict_temp):
        all_list = []
        url = dict_temp['LiveLink']
        req = requests.get(url=url)
        req.encoding='utf-8'
        link = re.findall('<iframe.*?src="(.*?)".*?</iframe>',req.text,re.I|re.S)[0]
        live_link = self._GetPlayUrl(link)
        if ('?vurl' in live_link) and ('&amp' in live_link):
            live_link = re.findall('\?vurl=(.*?)&amp',live_link,re.I|re.S)[0]
        return live_link

    def _GetPlayUrl(self,url):
        req = requests.get(url=url)
        req.encoding = 'utf-8'
        html = req.text
        if '本频道无信号' in html:
            link = '本频道无信号'
        else:
            if 'open_win' in html:
                link = re.findall('open_win\(\'(.*?)\'\)',html,re.I|re.S)[0]
            elif 'window.open(' in html:
                list = re.findall('window.open\(\'(.*?)\'', html, re.I | re.S)
                if len(list)>0:
                    link = list[len(list)-1]
            elif 'showPlayer' in html:
               link = re.findall('window.onload = showPlayer\(\'(.*?)\'', html, re.I | re.S)[0]
            elif 'xmlhttp' in html: #特殊匹配湖北卫视
                js_link = re.findall('var url = \'(.*?)\'', html, re.I | re.S)[0]
                req_js = requests.get(url=js_link)
                js_ele = json.loads(req_js.text)
                link = js_ele['body']['urlInfo']['url']
            elif '<embed' in html:
                link = re.findall('<embed.*?src="(.*?)"', html, re.I | re.S)[0]
            elif 'var fa' in html:   #特殊匹配兵团卫视
                link = re.findall('var fa=\'(.*?)\'', html, re.I | re.S)[0]
            elif '﻿<object type="' in html:
                pass
            else:
                tag_link = re.findall('<iframe.*?src="(.*?)".*?</iframe>', html, re.I | re.S)[0]
                try:
                    link = self._GetPlayUrl(tag_link)
                    if 'htm' in link:
                        link = self._GetSpM3U8Link(link)
                except:
                    link = tag_link
        return link

    #获取特殊链接
    def _GetSpM3U8Link(self,url):
        link = ''
        if '10000top' in url:
            headers = {
                'Host': 'www.10000top.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'http://www.10000top.com/'
            }
            req = requests.get(url=url,headers=headers)
            req.encoding = 'utf-8'
            if '<video src=' in req.text:
                link = re.findall('<video src="(.*?)"',req.text,re.I|re.S)[0]
            elif 'var videoUrl = "' in req.text:
                link = re.findall('var videoUrl = "(.*?)"', req.text, re.I | re.S)[0]
            else:
                pass
        return link