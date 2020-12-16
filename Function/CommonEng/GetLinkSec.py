import re
import urllib
import urllib.request
import urllib.error
import win32api,win32con

from urllib.request import urlopen

#bubulai
class GetLinkSec:
    def __init__(self):
        self._baseUrl = ""

    #设置基础网址
    def SetBaseUrl(self,url):
        self._baseUrl = url

    #根据关键字搜索
    def SearchKey(self,key):
        #转换为ASCII
        asc_str = urllib.parse.quote(key)
        url = self._baseUrl+'/go.html?wd={0}'.format(asc_str)  #拼接网址
        html = self._ConnectLink(url)                               #GET消息
        return self._ReageGetLink(html)   #正则匹配爬取结果


    #连接服务器
    def _ConnectLink(self,url):
        try:
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req)
            html = res.read().decode('utf-8')
        except:
            req = urllib.request.Request(url)
            res = urllib.request.urlopen(req)
            html = res.read().decode()
        return html

    #利用正则表达式获取
    def _ReageGetLink(self,html):
        all_link_title = []  #放置所有标题
        all_link = []        #放置所有连接

        # 筛选标题
        title = re.findall('<a href="#".*?>', html, re.S | re.I)#筛选a标签
        title = re.findall('Add_Favourite.*?;', str(title), re.S | re.I)#二次筛选

        all_link = re.findall('http.*?html', str(title), re.S | re.I)
        reg_str = r'\''
        for i in range(0,len(title)):
            str_arr = title[i].split(',')
            all_link_title.append((str_arr[1].replace(reg_str,'')).replace(');',''))

        return all_link,all_link_title

    #连接服务端
    def SearchConLink(self,link):
        try:
            html = urlopen(link).read().decode('utf-8')
        except:
            html = urlopen(link).read().decode()
        return html

    #抓取下载连接
    def SearchDownLink(self,url):
        movie_img=""

        html = self.SearchConLink(url)
        #提取图片连接
        match_pic = re.findall('<div class="soft">.*?<ul>', html, re.S | re.I)
        match_pic = str(match_pic)
        match_pic = re.findall('src=".*?"', match_pic, re.S | re.I)
        if len(match_pic) == 1:
            match_pic = match_pic[0].replace('src=', '')
            match_pic = match_pic.replace('"', '')
            movie_img = self._DownMovPicture(match_pic)
        #print(match_pic)

        #提取连接
        html = re.findall('<div class="down">.*?</div>', html, re.S | re.I)
        #print(html)
        html = str(html)
        match_str = re.findall('<script>var GvodUrls = .*?</script>',html, re.S | re.I)
        match_str = str(match_str).replace('<script>var GvodUrls = ','')
        match_str = match_str.replace('</script>', '')
        match_str = re.findall('^.*?;echoDown', match_str, re.S | re.I)
        first_str = str(match_str).split('###')

        all_Link1 = []
        all_Link2 = []

        for i in range(0,len(first_str)-1):
            link_arr = first_str[i].split('#')
            if len(link_arr) >0:
                all_Link1.append(re.findall('[a-zA-Z].*', link_arr[0], re.S | re.I)[0])
                all_Link2.append(link_arr[1])
        return all_Link1,all_Link2,movie_img

    # 获取百度云保存连接
    def SearchPanLink(self,url):
        pan_title = []
        pan_link = []
        html_obj = self.SearchConLink(url)
        html = re.findall('<a name="wangpan"></a>', html_obj, re.S | re.I)
        cnt = len(html)
        if cnt >0:
            match_str = re.findall('<a name="wangpan"></a>.*?<div class="tab">.*?</div>', html_obj, re.S | re.I)#寻找是否存在网盘连接
            match_str2 = re.findall('<a href.*?target="_blank">.*?</a>', str(match_str), re.S | re.I)           #寻找跳转网址
            match_str_link = re.findall('href=.*?html', str(match_str2), re.S | re.I)                           #正则匹配出跳转网址
            match_str_title = re.findall('>.*?<', str(match_str2), re.S | re.I)
            for i in range(0,len(match_str_title)):
                if i%2==0:
                    temp_str = (match_str_title[i].replace('<','')).replace('>','')
                    pan_title.append(temp_str)

            for i in range(0,len(match_str_link)):
                match_str_link[i] = match_str_link[i].replace('href="',self._baseUrl)
            #print(match_str_link)
            #print(pan_title)

            # 逐个网址抓取数据
            for item in match_str_link:
                pan_link.append(self._SearchPanSaveLink(item))
        return pan_title,pan_link

    #获取百度云保存连接
    def _SearchPanSaveLink(self,url):
        html = self.SearchConLink(url)
        match_str = re.findall('>http.*?://pan.baidu.com.*?</a>.*?</li>',html, re.S | re.I)
        match_str = str(match_str[0])
        match_str = match_str.replace('</a>',' ')
        match_str = match_str.replace('</li>', '')
        match_str = match_str.replace('>', '')
        return match_str

    #获取图片
    def _DownMovPicture(self,link):
        img = urlopen(link).read()
        return img