import re
import time
import urllib
import requests
import json
from bs4 import BeautifulSoup

#爬取腾讯视频播放网址
class GetLinkTenv:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self,key):
        all_list = []
        asc_str = urllib.parse.quote(key)
        url = self._baseUrl+'/x/search/?q='+asc_str
        headers={
            'Host': 'v.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers'
        }

        req = requests.get(url=url,headers=headers)
        soup = BeautifulSoup(req.text, 'lxml')  # 选择lxml作为解析器
        temp = soup.find_all('div', class_='wrapper_main')
        soup_list = temp[0].find_all('div',class_='result_item')
        for item in soup_list:
            try:
                temp_all_link = item.find_all('div',class_='_playlist')
                if len(temp_all_link)>0:
                    result_link = temp_all_link[0].find_all('div', class_='result_episode_list')
                    js_str = result_link[0].attrs['r-props'].replace('\n','').replace('\t','')
                    match_js_str = re.findall('{(.*?)}',js_str,re.I|re.S)[0]
                    dict_param = {
                        'id':re.findall('id: \'(.*?)\'',match_js_str,re.I|re.S)[0],
                        'dataType': re.findall('dataType: \'(.*?)\'', match_js_str, re.I | re.S)[0],
                        'videoType': re.findall('videoType: \'(.*?)\'', match_js_str, re.I | re.S)[0],
                        'initRange': re.findall('initRange: \'(.*?)\'', match_js_str, re.I | re.S)[0],
                        'playsrc': re.findall('playsrc: \'(.*?)\'', match_js_str, re.I | re.S)[0],
                        'Title': re.findall('title: \'(.*?)\'', match_js_str, re.I | re.S)[0],
                        'Referer':url
                    }
                    all_list.append(dict_param)
                else:
                    pass
            except Exception as msg:
                print(msg)
        return all_list

    def SetMovLink(self,tag_dict):
        all_list = []
        url = 'https://s.video.qq.com/get_playsource'
        headers={
            'Host': 's.video.qq.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer':tag_dict['Referer'],
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache'
        }

        data={
            'id': tag_dict['id'],
            'plat': '2',
            'type': '4',
            'range': tag_dict['initRange'],
            'data_type': tag_dict['dataType'],
            'video_type': tag_dict['videoType'],
            'plname': tag_dict['playsrc'],
            'otype': 'json',
            'uid': '7e893595-83e9-434a-80ac-1ce192b39596',
            'callback': '_jsonp_0_3cef',
            '_t': str(self._GetUtcTime())
        }

        req = requests.get(url=url,headers=headers,params=data)
        js_str = re.findall('\((.*?)\)',req.text,re.I|re.S)
        js_ele = json.loads(js_str[0])
        count = int(js_ele['PlaylistItem']['totalEpisode'])
        for i in range(0,count):
            js_video = js_ele['PlaylistItem']['videoPlayList'][i]
            dict_video = {
                'MovId':js_video['id'],
                'MovTitle':js_video['episode_number'],
                'MovLink':urllib.parse.unquote(js_video['playUrl']),
                'MovImg':js_video['pic']
            }
            all_list.append(dict_video)
        return all_list


    #获取13位时间戳
    def _GetUtcTime(self):
        time_stamp = int(time.time()*1000)
        return time_stamp