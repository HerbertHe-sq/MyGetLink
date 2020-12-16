import requests
import re

class GetLinkLiveIVI:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMaster(self):
        list_data = []
        url = self._baseUrl
        headers={
            'Host': 'ivi.bupt.edu.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding = 'utf-8'
        match_str = re.findall('<div class="2u.*?>(.*?)</div>',req.text,re.I|re.S)
        for item in match_str:
            title = re.findall('<p>(.*?)</p>',item,re.I|re.S)[0]
            mobile_link = re.findall('&nbsp;.*?<a class="icon1" href="(.*?)"',item,re.I|re.S)[0]
            pc_link = re.findall('</p>.*?<a class="icon1" href=".*?channel=(.*?)"',item,re.I|re.S)[0]
            dict_link = {
                'LiveTitle':title,
                'PCLink':self._baseUrl+'/hls/'+pc_link+'.m3u8',
                'MobileLink':self._baseUrl+mobile_link
            }
            list_data.append(dict_link)

        return list_data