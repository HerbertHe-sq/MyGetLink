import urllib
from urllib.request import urlopen

import requests
import re

#80s手机电影网
class GetLinkEs:
    def __init__(self):
        self._baseUrl = 'http://www.y80s.com/movie/search/'
        self._elementUrl='http://www.y80s.com'

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SetEleUrl(self,url):
        self._elementUrl = url

    def SearchMasterKey(self, key):
        all_list = []

        asc_str = urllib.parse.quote(key)
        tag_key = urllib.parse.quote('搜索')

        data={
            'search_typeid':'1',
            'skey':asc_str,
            'input':tag_key
        }

        my_headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'www.y80s.com',
            'Referer':'http://www.y80s.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
        }

        #发送post数据
        req_post = requests.post(self._baseUrl,data=data,headers=my_headers)
        req_post.encoding='utf-8'

        match_str_all = re.findall('<ul class="me1 clearfix">(.*?)</ul>',req_post.text,re.I|re.S)
        match_list_all = re.findall('<li>(.*?)</li>',match_str_all[0],re.I|re.S)
        for item in match_list_all:
            temp_href = re.findall('<h3 class="h3">(.*?)</h3>', item, re.I | re.S)
            temp_href = re.findall('<a href="(.*?)">', temp_href[0], re.I | re.S)
            temp_title = re.findall('title="(.*?)">', item, re.I | re.S)
            temp_tip = re.findall('<span class="tip" >(.*?)</span>', item, re.I | re.S)[0].replace(' ','').replace('\n','')
            temp_img = re.findall('_src="(.*?)"', item, re.I | re.S)
            dic_item = {
                'MovName':temp_title[0]+'-'+temp_tip,
                'Link':temp_href[0],
                'Img':temp_img[0]
            }
            all_list.append(dic_item)
        return all_list

    def SearchLinkBt(self, dic_dat):
        all_link = []
        my_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'www.y80s.com',
            'Referer': dic_dat['Link'],
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'X-Requested-With':'XMLHttpRequest'
        }

        #<span class="dlb_link_link" onclick="get_dllist(
        myurl=self._elementUrl+dic_dat['Link']  #+'/bd-2'
        req_fg = requests.get(myurl, headers=my_headers)
        req_fg.encoding = 'utf-8'

        link_url = myurl
        if req_fg.text.find('<span class="dlb_link_link" onclick="get_dllist')>=0:
            match_fg_str = re.findall('<span class="dlb_link_link" onclick="get_dllist\((.*?)\)">', req_fg.text, re.S | re.I)[0]
            str_arr = match_fg_str.split(',')
            str_arr[0] = str_arr[0].replace('\'','')#获取hd/bd标志
            link_url=myurl + '/{0}-{1}'.format(str_arr[0], str_arr[1])

        html = requests.get(link_url, headers=my_headers)
        html.encoding = 'utf-8'  # 解析编码
        match_str = re.findall('<ul class="dllist1"(.*?)</ul>', html.text, re.S | re.I)[0]
        match_str = re.findall('<span class="dlname nm">(.*?)</span>', match_str, re.S | re.I)
        for item in match_str:
            temp_str = re.findall('thunderHref=".*?</a>', item, re.S | re.I)[0]
            temp_str_name = re.findall('>(.*?)</a>', temp_str, re.S | re.I)[0]
            temp_str_link = re.findall('thunderHref="(.*?)"', temp_str, re.S | re.I)[0]
            dic_link = {
                'Name': temp_str_name,
                'ThunderLink': temp_str_link
            }
            all_link.append(dic_link)
        return all_link

    # 获取图片
    def DownMovPicture(self, link):
        img = urlopen(link).read()
        return img