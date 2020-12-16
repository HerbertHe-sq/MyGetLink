import requests
import re
import os

#618G免费解析网
class VipChangeSoe:
    def __init__(self):
        self._baseUrl = ''
        self.httpSession = requests.session()

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterUrl(self,url):
        temp_url = self._baseUrl+url
        headers={
            'Host': 'jx.618g.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers'
        }
        data={
            'url':url
        }

        req = requests.get(url=self._baseUrl,headers = headers,params=data)
        req.encoding='utf-8'
        match_str = re.findall('src="(.*?)"></iframe>',req.text,re.I|re.S)[0]
        f_link,r_link = self._GetVideoLinkM3U8(match_str,req.url)
        all_link,end_url = self._GetVideoLinkSM3u8(f_link,r_link)
        return all_link,end_url

    def _GetVideoLinkM3U8(self,url,root_url):
        headers={
            'Host': 'jx.618g.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': root_url,
            'Upgrade-Insecure-Requests': '1',
            'TE': 'Trailers'
        }
        temp_url = url
        if not 'http' in url:
            temp_url = self._baseUrl+url
        elif '/m3u8' in url:
            temp_url = self._baseUrl + url
        else:
            print(temp_url)

        req = requests.get(url=temp_url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<video src="(.*?)"',req.text,re.I|re.S)[0]
        return match_str,req.url

    #获取所有ts文件路径
    def _GetVideoLinkSM3u8(self,url,root_url):
        list_data=[]
        headers={
            'Host': 'youku.cdn2-okzy.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            'Origin': 'https://jx.618g.com',
            'Connection': 'keep-alive',
            'Referer': root_url
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        if req.status_code==200:
            temp_str = req.text.split('\n')[2]
            link_str = req.url[:req.url.rfind('/')]+'/'+temp_str
        else:
            link_str = req.url

        req_link = requests.get(url=link_str)
        req_link.encoding = 'utf-8'

        end_url = req_link.url[:req_link.url.rfind('/')] + '/'
        if '/hls/index.m3u8' in req_link.text:
            temp_str_arr = req_link.text.split('\n')
            link_str = os.path.dirname(url)+'/'+temp_str_arr[2]
        else:
            match_list = re.findall(',(.*?)#EXTINF',req_link.text,re.I|re.S)
            for i in range(0,len(match_list)):
                name = match_list[i].replace('\n','')
                link = end_url+name
                dict_link={
                    'MovName':name,
                    'MovLink':link
                }
                list_data.append(dict_link)
        return list_data,link_str

    def GetUrlFile(self,url):
        try:
            req = self.httpSession.get(url=url,timeout=10)
        except Exception as msg:
            req = requests.get(url=url,verify=False,timeout=5)
        return req

    def GetStreamReq(self,url):
        req = requests.get(url=url,stream=True,verify=False)
        return req

    #返回头文件信息
    def GetStreamReqMsg(self,url):
        req_msg = requests.head(url=url,verify=False)
        return req_msg

    #自由设置headers
    def GetStreamReqHeader(self,url,headers):
        req= requests.get(url=url,headers=headers,verify=False)
        return req