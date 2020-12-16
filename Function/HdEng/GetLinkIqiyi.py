import re
import urllib
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup

class GetLinkIqiyi:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self,key):
        all_list = []
        asc_str = urllib.parse.quote(key)
        url = self._baseUrl+'/q_'+asc_str
        headers={
            'Host': 'so.iqiyi.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

        data={
            'source':'history',
            'sr':'3997822823052301',
            'ssrt':'20201120090726667',
            'ssra':'e43a375f0784e52defe1127516824c29'
        }

        req = requests.get(url=url,headers=headers,params=data)
        req.encoding='utf-8'
        soup = BeautifulSoup(req.text, 'lxml')  # 选择lxml作为解析器
        temp = soup.find_all('div',class_='qy-search-result-item vertical-pic')
        try:
            for item in temp:
                title = item.find_all('a',class_='main-tit')[0]['title']
                img = item.find_all('img',class_='qy-mod-cover')[0]['src']
                if not 'http' in img:
                    img = 'http:'+img
                li_str = item.find_all('li')
                if len(li_str)>0:
                    mov_list = []
                    for li_item in li_str:
                        if 'title' in str(li_item):  #Herbert 201128
                            mov_title = li_item.find_all('a')[0]['title']
                            link = li_item.find_all('a')[0]['href']
                            if not 'http' in link:
                                link = 'http:'+link
                            dict_mov = {
                                'MovTitle':mov_title,
                                'MovLink':link
                            }
                            mov_list.append(dict_mov)
                    dict_mov_sum = {
                        'Title':title,
                        'Img':img,
                        'List':mov_list
                    }
                    all_list.append(dict_mov_sum)
        except Exception as msg:
            print(msg)
        return all_list

    # 获取图片
    def DownMovPicture(self, link):
        img = urlopen(link).read()
        return img