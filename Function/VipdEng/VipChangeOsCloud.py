import base64
import json
import time
import requests

class VipChangeOsCloud:
    def __init__(self):
        self._baseUrl=''
        self._rootUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SetRootUrl(self,url):
        self._rootUrl = url

    def SearchMaster(self, url):
        all_list = []
        video_url = ''
        tag_url = self._baseUrl
        headers={
            'Host': '1717.ntryjd.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://1717.ntryjd.net',
            'Connection': 'keep-alive'
        }

        referer_t = 'https://www.1717yun.com/beiyong/?url='+url
        referer_t = str(base64.b64encode(referer_t.encode('utf-8')),'utf-8')
        data={
            'url':url,
            'referer': referer_t,
            'ref': '0',
            'time': str(self._GetUtcTime()),
            'type': '',
            'other':str(base64.b64encode(url.encode('utf-8')),'utf-8'),
            'ios': ''
        }
        req = requests.post(url=tag_url,headers=headers,data=data)
        req.encoding='utf-8'
        js_ele = json.loads(req.text)
        if (js_ele['code']==200) or (js_ele['code']=='200'):
            if 'http' in js_ele['url']:
                video_url = js_ele['url']
        else:
            video_url='Get link failed!'
        return all_list,video_url


    def _GetUtcTime(self):
        time_stamp = int(time.time())
        return time_stamp