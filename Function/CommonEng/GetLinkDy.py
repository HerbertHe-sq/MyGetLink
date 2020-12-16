import re
import requests
import urllib
import urllib.request
import urllib.error
import base64

from urllib.request import urlopen

#993dy电影
class GetLinkDy:
    def __init__(self):
        self._baseUrl=""

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchMasterKey(self, key):
        all_list = []

        asc_str = urllib.parse.quote(key)
        #url = "https://www.993dy.com/index.php?m=vod-search&wd={0}&submit=%E6%90%9C%E7%B4%A2%E5%BD%B1%E7%89%87".format(asc_str)
        url = self._baseUrl.format(asc_str)
        html = requests.get(url)

        match_str = re.findall('<div class="pagelist">.*?<ul class="img-list clearfix">.*?</div>', html.text, re.S | re.I)
        match_str = re.findall('<ul class="img-list clearfix">.*?</ul>', str(match_str), re.S | re.I)
        match_str = re.findall('<li>.*?</li>', str(match_str), re.S | re.I)

        for item in match_str:
            dic_mov={
                'MovName': re.findall('title="(.*?)" target="_blank">', str(item), re.S | re.I)[0],
                'Link': re.findall('<a class="play-img" href="(.*?)" title', str(item), re.S | re.I)[0],
                'Img': re.findall('<img src="(.*?)"', str(item), re.S | re.I)[0],
                'Notice': re.findall('<em>(.*?)</em>', str(item), re.S | re.I)[0]
            }
            all_list.append(dic_mov)

        return all_list

    def SearchLinkBt(self, url):
        all_link = []
        myurl='https://www.993dy.com'+url
        html = requests.get(myurl)
        html.encoding='utf-8'       #解析编码
        match_str = re.findall('<ul class="downurl"(.*?)</ul>', str(html.text), re.S | re.I)[0]
        match_str = re.findall('<script>(.*?)</script>', str(match_str), re.S | re.I)[0]
        match_str = re.findall('var downurls="(.*?)"', str(match_str), re.S | re.I)[0]
        match_source = re.findall('(.*?)#', str(match_str), re.S | re.I)
        for item in match_source:
            temp_str=''
            link_temp = item.split('$')
            if not (link_temp[1].find('thunder')>=0):
                temp_str='AA'+link_temp[1]+'ZZ'
                temp_str = base64.b64encode(temp_str.encode('utf-8'))
                temp_str = "thunder://" + str(temp_str, 'utf-8')
            else:
                temp_str = link_temp[1]
            dic_link = {
                'Name':link_temp[0],
                'SLink':link_temp[1],
                'ThunderLink':temp_str
            }
            all_link.append(dic_link)
        return all_link

    # 获取图片
    def DownMovPicture(self, link):
        img = urlopen(link).read()
        return img

