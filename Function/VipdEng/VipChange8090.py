import os
import re
import requests
import base64
import time
import json

class VipChange8090:
    def __init__(self):
        self._baseUrl=''
        self._rootUrl = ''
        self._interUrl=''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SetRootUrl(self,url):
        self._rootUrl = url

    def SetInterFace(self,url):
        self._interUrl = url

    def _SearchApiUrl(self,url):
        headers={
            'Host': '8090.ylybz.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.8090g.cn/?url='+url,
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'TE': 'Trailers'
        }
        data = {
            'url':url
        }
        req = requests.get(url=self._interUrl,headers=headers,params=data)
        req.encoding='utf-8'
        match_str = re.findall('\$.post\(.*?},',req.text,re.I|re.S)
        tag_url =  re.findall('post\("(.*?)",',match_str[0],re.I|re.S)[0]
        js_str = re.findall('{.*?}',match_str[0],re.I|re.S)[0]
        dict_detail = {
            'tag_url':tag_url,
            'url':re.findall('\'url\':\'(.*?)\'',js_str,re.I|re.S)[0],
            'referer':re.findall('\'referer\':\'(.*?)\'',js_str,re.I|re.S)[0],
            'time': re.findall('\'time\':\'(.*?)\'', js_str, re.I | re.S)[0]
        }
        return dict_detail




    def SearchMaster(self,url):
        all_list = []
        #dict_detail = self._SearchApiUrl(url)
        tag_url = 'https://8090.gdkaman.com/?url='+url
        headers={
            'Host': '8090.gdkaman.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://8090.gdkaman.com',
            'Connection': 'keep-alive'
        }

        data={
            'url': url,
            'referer': str(base64.b64encode(tag_url.encode('utf-8')),'utf-8'),
            'ref': '0',
            'time': str(self._GetUtcTime()),
            'type': '',
            'other': str(base64.b64encode(url.encode('utf-8')),'utf-8'),
            'ios': ''
        }
        #req = requests.post(url=self._interUrl+'/'+dict_detail['tag_url'],headers=headers,data=data)
        req = requests.post(url=self._baseUrl, headers=headers, data=data)
        js_ele = json.loads(req.text)
        if 'http' in js_ele['url']:
            video_url = js_ele['url']
        elif '//cdn.'in js_ele['url']:
            video_url ='http:'+ js_ele['url']
        else:
            temp = base64.b64decode(str(js_ele['url']))
            video_url = re.findall('.x00.x83W(.*?)\'',str(temp),re.I|re.S)[0]
        if not 'http' in video_url:
            video_url = 'https:' +video_url
        if not (('sochy.tcdn.qq.com' in video_url) or ('om.tc.qq.com' in video_url) or ('?vkey=' in video_url) or ('.mp4' in video_url)):
            list = self._GetAllLink(video_url,url)
            all_list = self._GetM3U8FromList(list)
        return all_list,video_url

    def _GetAllLink(self,url,root_url):
        list = []
        headers={
            'Host': 'cdn.oss-cn.aliyuncs.com.gms-lighting.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            #'Accept-Encoding': 'gzip, deflate, br',
            'Origin': self._rootUrl,
            'Connection': 'keep-alive',
            'Referer': 'https://8090.ylybz.cn/jiexi/?url='+root_url
        }
        if 'cdn.oss-cn.aliyuncs.com' in url:
            req = requests.get(url=url,headers=headers)
        else:
            req = requests.get(url=url)
        req.encoding = 'utf-8'
        if 'http' in req.text:  # 兼容特殊网站
            if 'ts?' in req.text:
                match_str = re.findall('(http.*?.ts.*?)#EXTINF', req.text, re.I | re.S)
            elif 'ts' in req.text:
                match_str = re.findall('http.*?.ts', req.text, re.I | re.S)
            elif 'jpg' in req.text:
                match_str = re.findall('http.*?.jpg', req.text, re.I | re.S)
            else:
                match_str = ''
        else:
            match_str = re.findall(',.*?.ts', req.text, re.I | re.S)
        for item in match_str:
            temp = item.replace(',\n', '')
            temp = temp.replace('\n', '')
            temp_key = temp[0:temp.rfind('/')]

            if temp_key in url:
                root_url = url.split(temp_key)
                list.append(root_url[0].replace(',\n', '') + temp)
            else:
                list.append(temp)
        return list

    # 筛选链接
    def _GetM3U8FromList(self, list):
        all_list = []
        for item in list:
            if '.ts?' in item:
                file_name = re.findall('(.*?.ts)',os.path.basename(item),re.I|re.S)[0]
                dict_file = {
                    'MovName': file_name.replace('\n', ''),
                    'MovLink': item.replace('\r', '')
                }
                all_list.append(dict_file)
            elif ('.ts' in item) or ('.jpg' in item):
                file_name = os.path.basename(item)
                dict_file = {
                    'MovName': file_name.replace('\n', ''),
                    'MovLink': item.replace('\n', '')
                }
                all_list.append(dict_file)
        return all_list

    def _GetUtcTime(self):
        time_stamp = int(time.time())
        return time_stamp