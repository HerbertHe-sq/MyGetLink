import base64
from urllib.request import urlopen

import requests
import re
import math
import time


#66直播网
class GetLinkLiveSS:
    def __init__(self):
        self._baseSeaUrl=''
        self._baseUrl=''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SetBaseSeaUrl(self,url):
        self._baseSeaUrl = url

    def SearchPlace(self):
        all_addr_list = []
        my_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'www.66zhibo.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
        }

        req = requests.get(url=self._baseSeaUrl,headers=my_headers)
        req.encoding='gbk'
        match_str = re.findall('<dl class="filter-dl filter-area">(.*?)</dl>',req.text,re.I|re.S)
        match_str = re.findall('<ul class="filter-list">(.*?)</ul>', match_str[0], re.I | re.S)
        for match_item in match_str:
            temp_list_1 = re.findall('<li date-id.*?</li>',match_item,re.I|re.S)
            for item in temp_list_1:
                addr_link = re.findall('href="(.*?)"',item,re.I|re.S)
                addr_name = re.findall('<a.*?>(.*?)</a>',item,re.I|re.S)
                date_id = re.findall('date-id="(.*?)"',item,re.I|re.S)
                dict_addr={
                    'AddrName':addr_name[0],
                    'AddrLink':addr_link[0],
                    'DateId':date_id[0]
                }
                all_addr_list.append(dict_addr)
        return all_addr_list

    def SearchTvProgram(self,dict_addr):
        all_live_list = []
        url = self._baseUrl+'/e/extend/list.php'
        ticks = time.time()
        param_t = math.ceil(ticks*1000 / 3600000)
        my_headers = {
            'Host':'www.66zhibo.net',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept':'text/plain, */*; q=0.01',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding':'gzip, deflate',
            'X-Requested-With':'XMLHttpRequest',
            'Connection':'keep-alive',
            'Referer':'http://www.66zhibo.net/'
        }
        data={
            'enews':'homezhibo',
            'classid':dict_addr['DateId'],
            't':str(param_t)
        }

        req = requests.get(url=url,params=data,headers=my_headers)
        req.encoding='gbk'
        match_str = re.findall('<li class="p-item">(.*?)</li>',req.text,re.I|re.S)
        for match_item in match_str:
            link = re.findall('<a href="(.*?)"',match_item,re.I|re.S)
            title = re.findall('class="thumb-outer" title="(.*?)"',match_item,re.I|re.S)
            img = re.findall('src="(.*?)"', match_item, re.I | re.S)
            dict_tv_list = {
                'LiveTitle':title[0],
                'LiveLink':link[0],
                'LiveIcon':img[0]
            }
            all_live_list.append(dict_tv_list)
        return all_live_list

    def SearchTvLink(self,dict_live):
        list_link = []
        list_sign = []
        url = self._baseUrl+dict_live['LiveLink']
        headers = {
            'Host': 'www.66zhibo.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='gbk'

        #获取输入参数
        match_param = re.findall('<script>var sourid.*?</script> ',req.text,re.I|re.S)
        param_gid= re.findall('gid=\'(.*?)\'',match_param[0],re.I|re.S)[0]
        param_v = re.findall('v=\'(.*?)\'', match_param[0], re.I | re.S)[0]

        # 获取线路ID
        match_str = re.findall('<ul class="tab-list-syb">(.*?)</ul>',req.text,re.I|re.S)
        match_list = re.findall('<li data-player.*?</li>',match_str[0],re.I|re.S)
        for match_item in match_list:
            signal_name = re.findall('<span class="s">(.*?)</span>',match_item,re.I|re.S)
            signal_id = re.findall('<li data-player="(.*?)"',match_item,re.I|re.S)
            dict_signal = {
                'SigName':signal_name[0],
                'SourId':signal_id[0]
            }
            list_sign.append(dict_signal)

        for item in list_sign:
            dict_link = self._SearchM3ULink(url,item['SourId'],param_gid,param_v)
            list_link.append(dict_link)
            time.sleep(0.1)

        return list_link


    #获取M3U路径根网址
    def _SearchM3ULink(self,root_url,sour_id,gid,v):
        url = self._baseUrl+'/e/extend/tv.php'
        headers={
            'Host': 'www.66zhibo.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': root_url,
            'Upgrade-Insecure-Requests': '1'
        }

        data={
            'id':sour_id,
            'gid':gid,
            'v':v
        }

        req = requests.get(url=url,headers=headers,params=data)
        req.encoding='gbk'
        match_str = re.findall('signal = \'(.*?)\';',req.text,re.I|re.S)
        data = match_str[0].split('$')
        if 'html?id=' in data[1]:
            temp_link = data[1].split('html?id=')
            data[1] = temp_link[1]
        dict_data = {
            'LiveTitle':data[0],
            'LiveLink':data[1]
        }
        return dict_data


    # 下载图片
    def DownPicture(self, link):
        #link = 'http://supcache.haobobbs.cn/data/www.loldytt.org' + link
        img = urlopen(link).read()
        return img