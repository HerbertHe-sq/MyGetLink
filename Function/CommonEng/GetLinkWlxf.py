import re
from urllib.request import urlopen

import requests

#下载荔枝网的外来媳妇本地郎
class GetLinkWlxf:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self):
        all_list = []
        url = self._baseUrl
        headers={
            'Host': 'v.gdtv.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.GetReqData(url, headers, all_list)  # 使用递归-直到访问完成
        return all_list




    #获取当前页数据并且下一页地址
    def GetReqData(self,url,headers,list):
        next_url = ''
        # 访问首页
        req = requests.get(url=url, headers=headers)
        req.encoding = 'utf-8'
        if '>下一页</a>' in req.text:
            next_match_str = re.findall('<div class="article-page">(.*?)</div>',req.text,re.I|re.S)[0]#
            next_match_list = re.findall('<a href=".*?">.*?</a>', next_match_str, re.I | re.S)
            for item in next_match_list:
                if '下一页' in item:
                    next_url = re.findall('<a href="(.*?)"', item, re.I | re.S)[0]
        match_str = re.findall('<div class="gvlist">(.*?)</ul>', req.text, re.I | re.S)
        match_list = re.findall('<li>(.*?)</li>', match_str[0], re.I | re.S)
        for item in match_list:
            title = re.findall('title="(.*?)">.*?<img', item, re.I | re.S)[0]
            link = re.findall('href="(.*?)".*?<img', item, re.I | re.S)[0]
            img = re.findall('<img.*?src="(.*?)"', item, re.I | re.S)[0]
            title = title.replace('：','_').replace('（','(').replace('）',')')
            dict_mov = {
                'MovName': title,
                'MovLink': link,
                'MovImg': img
            }
            list.append(dict_mov)
        if next_url != '':
            self.GetReqData(next_url,headers,list)
        return next_url

    def SearchLink(self,dict_mov):
        url = dict_mov['MovLink']
        headers={
            'Host':'v.gdtv.cn',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate',
            #'Referer':'http://v.gdtv.cn/zj/wlxfbdl/?pp=',
            'Connection':'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        link = re.findall('<input type="hidden" name="m3u8" id="m3u8"  value="(.*?)"',req.text,re.I|re.S)[0]
        return link

    # 获取图片
    def DownMovPicture(self, link):
        img = urlopen(link).read()
        return img