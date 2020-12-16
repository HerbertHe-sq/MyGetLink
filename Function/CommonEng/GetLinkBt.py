import re
import urllib
import urllib.request
import urllib.error

from urllib.request import urlopen

#SOBT
class GetLinkBt:
    def __init__(self):
        self._baseUrl = ""

    # 设置基础网址
    def SetBaseUrl(self,url):
        self._baseUrl = url

    # 连接服务端
    def _ConLink(self, link):
        try:
            html = urlopen(link).read().decode('utf-8')
        except:
            html = urlopen(link).read().decode()
        return html

    #主键搜索
    def SearchMasterKey(self,key):
        all_list = []
        all_list_title = []

        asc_str = urllib.parse.quote(key)
        url = self._baseUrl+r'/q/{0}.html'.format(asc_str)  # 拼接网址
        html = self._ConLink(url)  # GET消息
        page_count = self._SearchAllPage(html)
        #轮询所有网址
        if page_count>1:
            for i in range(1,page_count):
                url_temp = url+'?sort=rel&page={0}'.format(str(i))
                html_temp = self._ConLink(url_temp)
                list_link_temp, list_title_temp = self._RegexMatch(html_temp, self._baseUrl)
                if len(list_link_temp)>0:
                    for j in range(0,len(list_link_temp)):
                        all_list.append(list_link_temp[j])
                        all_list_title.append(list_title_temp[j])
        else:
            all_list, all_list_title = self._RegexMatch(html,self._baseUrl)

        return all_list, all_list_title

    #匹配所有选项
    def _RegexMatch(self,html,base_url):
       match_str = re.findall('<div class="search-item">.*?</div>',html,re.S | re.I)
       match_str_link = re.findall('href=.*?html', str(match_str), re.S | re.I)
       match_str_title = re.findall('target.*?</a>', str(match_str), re.S | re.I)

       if len(match_str_link)>0:
           for i in range(0,len(match_str_link)):
               match_str_link[i] = match_str_link[i].replace(r'href="','')
               match_str_link[i] = base_url+match_str_link[i]

       if len(match_str_title)>0:
           for i in range(0,len(match_str_title)):
               match_str_title[i] = match_str_title[i].replace('target="_blank">','')
               match_str_title[i] = match_str_title[i].replace('</a>', '')
               match_str_title[i] = match_str_title[i].replace('<em>', '')
               match_str_title[i] = match_str_title[i].replace('</em>', '')

       return match_str_link,match_str_title

    #根据网址搜索需要的东西
    def SearchLinkBt(self,url):
       html = self._ConLink(url)

       match_str = re.findall('<input  id="m_link".*?>',html,re.S | re.I)
       match_link = re.findall('value=".*?"', str(match_str), re.S | re.I)

       match_str2 = re.findall('<div class="fileDetail">.*?</div>', html, re.S | re.I)
       match_str2 = re.findall('<input.*?</a>',str(match_str2),re.S | re.I)
       match_str2 = re.findall('<a.*?</a>', str(match_str2), re.S | re.I)
       match_link2 = re.findall('href=".*?"', str(match_str2), re.S | re.I)
       if len(match_link)>0:
           match_link = match_link[0].replace(r'value="','')
           match_link = match_link.replace(r'"', '')

       if len(match_link2)>0:
           match_link2 = match_link2[0].replace(r'href="', '')
           match_link2 = match_link2.replace(r'"', '')

       return match_link,match_link2

    #搜索页面总数
    def _SearchAllPage(self,html):
        page = 0
        match_str = re.findall('<li class="last_p">.*?>', html, re.S | re.I)
        match_str = re.findall('page.*?"', str(match_str), re.S | re.I)
        if len(match_str)>0:
            match_str = match_str[0].replace('page=','')
            match_str = match_str.replace('"', '')
            page = int(match_str)
        return page