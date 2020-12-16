import requests
import re
import base64
import json

class NationalAnalysis:
    def __init__(self):
        self._baseUrl=''

    def SetBaseUrl(self,url):
        self._baseUrl = url


    def FindEngineUrl(self):
        list_dat=[]
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection':'keep-alive',
            'Host':'qmaile.com',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
        }

        req = requests.get(self._baseUrl,headers=headers)
        req.encoding='utf-8'

        if req.status_code== 200:
            match_str = re.findall('<select class="form-control input-lg" id="jk">(.*?)</select>',req.text,re.S|re.I)
            match_url_list = re.findall('<option value="(.*?)"',match_str[0],re.S|re.I)
            match_name_list = re.findall('selected="">(.*?)</option>', match_str[0], re.S | re.I)

            for i in range(len(match_name_list)):
                dict_temp={
                    'EngName':match_name_list[i],
                    'EngUrl':match_url_list[i]
                }
                list_dat.append(dict_temp)

        return list_dat

    def ConvertLink(self):
        pass

    #获取引擎1地址
    def EngineVip_1(self,tag_url):
        url='https://8090.ylybz.cn/jiexi2019/api.php'
        headers={
            'Host': '8090.ylybz.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://8090.ylybz.cn',
            'Connection': 'keep-alive',
            'Referer': 'https://8090.ylybz.cn/jiexi2019/?url='+tag_url
        }

        data={
            'url':tag_url,
            'referer':str(base64.b64encode(('https://www.8090g.cn/?url=' + tag_url).encode('utf-8')), 'utf-8'),
            'ref':'0',
            'time':'1579828783',
            'type':'',
            'other':str(base64.b64encode(tag_url.encode('utf-8')), 'utf-8'),
            'ios':''
        }

        req = requests.post(url=url,headers=headers,data=data,verify=False)
        js_ele = json.loads(req.text)

        return js_ele
