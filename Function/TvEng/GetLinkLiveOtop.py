import re
from urllib.request import urlopen

import requests

#10000top
class GetLinkLiveOtop:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMaster(self):
        all_list = []
        url = self._baseUrl
        headers={
            'Host': 'www.10000top.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding = 'gb2312'
        match_str = re.findall('<table.*?id="table3".*?>(.*?)</table>',req.text,re.I|re.S)[0]
        match_list = re.findall('<tr>(.*?)</tr>',match_str,re.I|re.S)
        for i in range(0,len(match_list)):
            if i>5:
                item = match_list[i]
                item_list = re.findall('<td.*?>(.*?)</td>',item,re.I|re.S)
                for item_s in item_list:
                    if '<p>' in item_s:
                        self._SearchList(item_s,all_list)
                    else:
                        try:
                            temp_link = re.findall('<a.*?href="(.*?)"',item_s,re.I|re.S)[0]
                            if not '#top' in temp_link:
                                if '<img' in item_s:
                                    temp_img = re.findall('<img.*?src="(.*?)"',item_s,re.I|re.S)[0]
                                else:
                                    temp_img = ''

                                if not 'http' in temp_link:
                                    temp_link = temp_link.replace('../','')
                                    temp_link = self._baseUrl+'/'+temp_link

                                if not 'http' in temp_img:
                                    temp_img = self._baseUrl+'/'+temp_img
                                dict_live = {
                                    'LiveLink':temp_link,
                                    'LiveImg':temp_img
                                }
                                all_list.append(dict_live)
                        except Exception as msg:
                            pass

        return all_list

    def _SearchList(self,html,list):
        match_str = re.findall('<p>(.*?)</p>',html,re.I|re.S)
        for item in match_str:
            if '<a' in item:
               temp_link = re.findall('<a.*?href="(.*?)"',item,re.I|re.S)[0]
               if not '#top' in temp_link:
                   if '<img' in item:
                       temp_img = re.findall('<img.*?src="(.*?)"', item, re.I | re.S)[0]
                   else:
                       temp_img = ''

                   if not 'http' in temp_link:
                       temp_link = temp_link.replace('../', '')
                       temp_link = self._baseUrl + '/' + temp_link

                   if not 'http' in temp_img:
                       temp_img = self._baseUrl + '/' + temp_img
                   dict_live = {
                       'LiveLink': temp_link,
                       'LiveImg': temp_img
                   }
                   list.append(dict_live)
        return list

    def GetM3U8Link(self,dict_live):
        url = dict_live['LiveLink']
        headers={
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
        link = ''
        if '<video src=' in req.text:
            link = re.findall('<video src="(.*?)"',req.text,re.I|re.S)[0]
        elif 'var videoUrl = "' in req.text:
            link = re.findall('var videoUrl = "(.*?)"', req.text, re.I | re.S)[0]
        else:
            pass
        return link

        # 下载图片
    def DownPicture(self, link):
        # link = 'http://supcache.haobobbs.cn/data/www.loldytt.org' + link
        img = urlopen(link).read()
        return img