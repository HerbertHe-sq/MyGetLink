import re
import urllib
import urllib.request
import urllib.error
import win32api,win32con
import base64

from MyPinYin import Pinyin
from urllib.request import urlopen

#LOL电影天堂
class GetLink:
    def __init__(self):
        self._pinEx = Pinyin()
        self._pinName=''

    def _SearchConLink(self,link):
        try:
            html = urlopen(link).read().decode('gb2312')
        except:
            html = urlopen(link).read().decode('gbk')
        return html

    def SearchLink(self,link):
        all_last_link = []
        movie_img = ""
        try:
            html = self._SearchConLink(link)
            match_pic = re.findall('<div class="haibao">.*?</div>', html, re.S | re.I)
            match_pic=str(match_pic)
            match_pic = re.findall('src=".*?"', match_pic, re.S | re.I)
            if len(match_pic)==1:
                match_pic = match_pic[0].replace('src=','')
                match_pic = match_pic.replace('"','')
                match_pic = match_pic
                movie_img = self._DownPicture(match_pic)

            matchObj = re.findall('<ul class="downurl">.*?</ul>', html, re.S | re.I)  # 获取下载链接
            matchObj = str(matchObj)
            if len(matchObj)>2:
                #进一步筛选链接
                matchAllLink = re.findall('<script>.*?</script>', matchObj, re.S | re.I)  # 获取下载链接部分

                # matchAllLink = str(matchAllLink)
                cnt = len(matchAllLink)
                allLink = []
                for i in range(0, cnt):
                    dat = str(matchAllLink[i]).replace('<script>', '')
                    dat = str(dat).replace('</script>', '')
                    dat = dat.split('= ', 1)
                    allLink.append(dat[1])

                for i in range(0, len(allLink)):
                    link_temp = allLink[i].split('$###')
                    last_list = []
                    for j in range(0, len(link_temp)-1):
                        last_list.append(link_temp[j])
                    all_last_link.append(last_list)
            else:
                win32api.MessageBox(0, "Can not find the link!!!", "Warning", win32con.MB_OK)
        except Exception as msg:
            print("Exception%s"%msg)
            win32api.MessageBox(0, str(msg), "Error", win32con.MB_OK)

        return all_last_link,movie_img

    #根据关键字搜索
    def SearchKey(self,link,type,name):
        all_last_link = []
        self._pinName = self._pinEx.get_pinyin(name, "")
        temp = link + "/" + type + "/" + self._pinName #拼接链接
        all_last_link,img = self.SearchLink(temp)
        return all_last_link,img

    #解码
    def _ConnectLink(self,url):
        try:
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req)
            html = res.read().decode('gb2312')
        except:
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req)
            html = res.read().decode('gbk')
        return html

    #模糊搜索
    def SearchMasterKey(self,key,link):
        all_link = []
        all_link_title = []
        mystr = str(key).encode("gb2312")
        mystr = urllib.parse.quote(mystr)

        try:
            url = link+'?searchword={0}&s='.format(mystr)
            html = self._ConnectLink(url)

            #筛选标题
            title = re.findall('<em>.*?</em>', html, re.S | re.I)
            for i in range(0,len(title)):
                title[i] = str(title[i]).replace('<em>', '')
                title[i] = str(title[i]).replace('</em>', '')
            all_link_title = title

            #筛选链接
            matchObj = re.findall('<span class="c-showurl">.*?</span>', html, re.S | re.I)  # 获取下载链接
            matchObj = str(matchObj)
            matchObj = re.findall('www.*?/ ', matchObj, re.S | re.I)
            all_link = matchObj


        except Exception as msg:
            print("Exception%s"%msg)
            win32api.MessageBox(0, str(msg), "Error", win32con.MB_OK)

        return all_link,all_link_title

    #下载图片
    def _DownPicture(self,link):
        link = 'http://supcache.haobobbs.cn/data/www.loldytt.org'+link
        img = urlopen(link).read()
        return img