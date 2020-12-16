import re
import requests

class GetLinkBtMov:
    def __init__(self):
        self._baseUrl=''
        self._rootUrl =''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SetRootUrl(self,url):
        self._rootUrl = url

    #根据关键字搜索
    def SearchMasterKey(self,key):
        all_list = []
        url = self._baseUrl+key+'.html'
        headers={
            'Host': 'www.btmovi.space',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://www.btmovi.space',
            'Connection': 'keep-alive'
        }
        req = requests.get(url,headers=headers)

        #获取总页数
        count_str = re.findall('<ul class="pagination">.*?<li class="last_p"><a href="(.*?)">.*?<ul>',req.text,re.I|re.S)[0]
        count = int(re.findall('_rel_(.*?).html',count_str,re.I|re.S)[0])
        self._SearchData(req.text,all_list)
        for i in range(2,count+1):
            temp_url = self._baseUrl+key+'_rel_{0}.html'.format(str(i))
            temp_req = requests.get(temp_url,headers=headers)
            self._SearchData(temp_req.text,all_list)
        return all_list

    #单页爬取需要的数据
    def _SearchData(self,text,list):
        match_str = re.findall('<div class="search-list(.*?)</ul>',text,re.I|re.S)[0]
        match_list = re.findall('<div class="search-item">(.*?)</h3>',match_str,re.I|re.S)
        for item in match_list:
            title = re.findall('target="_blank">(.*?)</a>',item,re.I|re.S)[0].replace('<em>','').replace('</em>','')
            link = re.findall('href="(.*?)"',item,re.I|re.S)[0]
            dict_link = {
                'BtName':title,
                'BtLink':self._rootUrl+link
            }
            list.append(dict_link)

    #获取BT连接诶
    def SearchLink(self,dict_data):
        url = dict_data['BtLink']
        req = requests.get(url=url)
        req.encoding = 'utf-8'

        title = re.findall('<h1.*?>(.*?)</h1>',req.text,re.I|re.S)[0]
        link = temp_link = ''
        try:
            link = re.findall('<input.*?id=".*?link" value="(.*?)"',req.text,re.I|re.S)[0]
            temp_link = re.findall(' 资源下载：<a href="(.*?)" class="download" id="down-url">', req.text, re.I | re.S)[0]
        except Exception as msg:
            print(msg)
        return title+'\n\n'+link+'\n\n'+temp_link