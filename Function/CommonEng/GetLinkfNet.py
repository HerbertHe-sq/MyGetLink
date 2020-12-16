import json
import re
import urllib
from urllib.request import urlopen
from urllib.request import urlretrieve

import requests



class GetLinkfNet:
    def __init__(self):
        self._baseUrl='http://www.415.net'

    def SetBaseUrl(self,url):
        self._baseUrl=url

    def SearchMasterKey(self,key):
        all_list = []

        asc_str = urllib.parse.quote(key)
        url=self._baseUrl+'/search-index-keyword-{0}.htm'.format(key)
        req = requests.get(url)
        req.encoding='utf-8'

        match_list = re.findall('<a target="_blank"(.*?)</a>',req.text,re.I|re.S)
        for item in match_list:
            match_url=re.findall('href="(.*?)"',item,re.I|re.S)[0]
            match_name = re.findall('>(.*?)$',item,re.I|re.S)[0]
            match_name = match_name.replace('<span class="red">','')
            match_name = match_name.replace('</span>', '')
            dict_detail={
                'BtName':match_name,
                'BtUrl':match_url
            }
            all_list.append(dict_detail)
        return all_list

    def SearchLinkBt(self, url):
        req = requests.get(url)
        req.encoding = 'utf-8'
        try:
            match_img = re.findall('<div.*?class="message">.*?<img src="(.*?)"',req.text,re.I|re.S)
        except:
            match_img = re.findall('<div.*?class="message">.*?<img .*?src="(.*?)"', req.text, re.I | re.S)
        match_url = re.findall('<div class="attachlist">.*?<a href="(.*?)" class="ajaxdialog"',req.text,re.I|re.S)

        js_str = requests.get(match_url[0])
        js_ele = json.loads(js_str.text)
        match_url = re.findall('window.open\(\'(.*?)\'\)', js_ele['message']['body'], re.I | re.S)

        dict={
            'BtImg':match_img[0],
            'BtUrl':match_url[0]
        }

        return dict

    # 获取图片
    def DownMovPicture(self, link):
        req =requests.get(link)
        img = req.content
        #img = urlopen(link).read()
        return img

    # 下载文件
    def DownLoadTor(self, path, url, up_bar):
        urlretrieve(url, path + '.torrent', up_bar)
