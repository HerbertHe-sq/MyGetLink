import re
import requests
import time
import datetime
from urllib.request import urlopen



#下载荔枝网的外来媳妇本地郎
class GetLinkWlxf:
    def __init__(self):
        self._baseUrl = ''
        self._MIN_DATE_DICT={
            'Year': 2016,
            'Mon': 1,
            'Day': 1,
            'Hour': 0,
            'Min': 0,
            'Sec': 0
        }

        self._TV_COLUMN_PK = 788
        self._PAGE_SIZE = 40




    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self):
        all_list = []
        url = self._baseUrl
        dict_date_now_t =  self._GetDate()
        headers={
            'Host': 'v.gdtv.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

        for i_year in range(self._MIN_DATE_DICT['Year'],dict_date_now_t['Year']+1):
            if i_year==dict_date_now_t['Year']:
                max_mon = dict_date_now_t['Mon']+1
            else:
                max_mon = 13
            for i_mon in range(1,max_mon):
                #构造时间戳
                dict_date_time_t = {
                    'Year': i_year,
                    'Mon': i_mon,
                    'Day': 1,
                    'Hour': 0,
                    'Min': 0,
                    'Sec': 0
                }
                utc_time = self._GetUtcTime(dict_date_time_t)
                self._LoginOptions(url,utc_time)
                self._GetReqData(url,all_list,utc_time)
        #self.GetReqData(url, headers, all_list)  # 使用递归-直到访问完成
        return all_list

    def _LoginOptions(self,url,date_t):
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'gdtv-api.gdtv.cn:7443',
            'Origin': 'https://www.gdtv.cn',
            'Referer': 'https://www.gdtv.cn/tvColumn/788',
            'TE': 'Trailers',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
        }

        data = {
            'pageSize': self._PAGE_SIZE,
            'tvColumnPk': self._TV_COLUMN_PK,
            'currentPage': '1',
            'searchByTime': 'true',
            'beginScore': str(date_t)
        }

        req = requests.options(url=url, headers=headers, params=data)
        print(req.status_code)

    def _GetReqData(self,url,list,date_t):
        headers={
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Host': 'gdtv-api.gdtv.cn:7443',
            'Origin': 'https://www.gdtv.cn',
            'Referer': 'https://www.gdtv.cn/tvColumn/788',
            'X-ITOUCHTV-Ca-Key': '89541443007807288657755311869534',
            'X-ITOUCHTV-Ca-Signature': '+8U4bNqXR3rZ8Eqfof2zSxGuZpX+dQpqY7cAzudsXOw=',
            'X-ITOUCHTV-Ca-Timestamp': str(self._GetUtcNowTime()),
            'X-ITOUCHTV-CLIENT': 'WEB_PC',
            'X-ITOUCHTV-DEVICE-ID': 'WEB_cb0d72c0-4828-11eb-b87a-332435e7092b',
            'Content-Type':'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
        }

        data={
            'pageSize': self._PAGE_SIZE,
            'tvColumnPk': self._TV_COLUMN_PK,
            'currentPage': 1,
            'searchByTime': 'false'
            #'beginScore': str(date_t)
        }

        req = requests.get(url=url,headers=headers,params=data)
        print(req.text)



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

    #获取时间
    def _GetDate(self):
        date_time_t = datetime.datetime.now()
        dict_date = {
            'Year':date_time_t.year,
            'Mon':date_time_t.month,
            'Day':date_time_t.day,
            'Hour':date_time_t.hour,
            'Min':date_time_t.minute,
            'Sec':date_time_t.second
        }
        return dict_date

    # 获取13位时间戳
    def _GetUtcTime(self,dict_date):
        date_t = datetime.datetime(dict_date['Year'],dict_date['Mon'],dict_date['Day'],dict_date['Hour'],dict_date['Min'],dict_date['Sec'])
        time_t = int(time.mktime(date_t.timetuple()))
        time_stamp = int(time_t * 1000)
        return time_stamp

    def _GetUtcNowTime(self):
        time_stamp = int(time.time() * 1000)
        return time_stamp

    # 获取图片
    def DownMovPicture(self, link):
        img = urlopen(link).read()
        return img