import time
import requests
import re
import json

#港剧网爬取
class GetLinkGj:
    def __init__(self):
        self._baseUrl=''
        self._searchUrl=''

    def SetBaseUrl(self,url):
        self._baseUrl =url

    def SetSearchUrl(self,url):
        self._searchUrl = url

    def SearchMasterKey(self,key):
        all_list = []
        url = self._searchUrl.format(key)
        req = requests.get(url=url)
        req.encoding='utf-8'
        match_str = re.findall('<article class="u-movie">.*?</article>',req.text,re.I|re.S)
        for item in match_str:
            title = re.findall('<a title="(.*?)"',item,re.I|re.S)[0]
            link = re.findall('<a.*?href="(.*?)">',item,re.I|re.S)[0]
            img =  re.findall('<img src="(.*?)"',item,re.I|re.S)[0]
            dict_temp = {
                'MovName': title,
                'MovLink': self._baseUrl + link,
                'MovImg': img
            }
            all_list.append(dict_temp)
        return all_list

    def SearchLink(self,dict_temp):
        all_list = []
        url = dict_temp['MovLink']
        req = requests.get(url=url)
        req.encoding='utf-8'
        match_str = re.findall('<div id="video_list_li".*?</div>',req.text,re.I|re.S)

        list_t = []
        for item in match_str:
            match_list_t = re.findall('<li>(.*?)</li>',item,re.I|re.S)
            list_dict_t = []
            for item_t in match_list_t:
                title = re.findall('<a title=\'(.*?)\'',item_t,re.I|re.S)[0]
                link = re.findall('href=\'(.*?)\'',item_t,re.I|re.S)[0]
                str_t = link.replace('/p/','').replace('.html','').split('-')
                if len(str_t)==3:
                    vid = str_t[0]
                    vfrom = str_t[1]
                    vpart = str_t[2]
                    dict_item_t = {
                        'MovTitle':title,
                        'Vid':vid,
                        'Vfrom':vfrom,
                        'Vpart':vpart
                    }
                    list_dict_t.append(dict_item_t)
            list_t.append(list_dict_t)
        for item in list_t:
            #取首个地址
            self._GetM3U8Link(item[0],all_list)
        return all_list


    def _GetM3U8Link(self,dict_temp,all_link):
        url = self._baseUrl+'/ass.php'
        data = {
            'url':'dp',
            'vid':dict_temp['Vid'],
            'vfrom':dict_temp['Vfrom'],
            'vpart':dict_temp['Vpart'],
            'cb':'jQuery111309312653578388785_'+str(self._GetUtcTime()),
            '_':str(self._GetUtcTime())
        }
        req = requests.get(url=url,params=data)
        js_ele = re.findall('\((.*?)\)',req.text,re.I|re.S)[0]
        json_t = json.loads(js_ele)

        js_count = json_t['s']['num']
        for item in range(0,js_count):
            mov_title = str(item+1)
            link = json_t['s']['video'][item]
            if link != None:
                dict_play = {
                    'Title': mov_title,
                    'PlayLink': link
                }
                all_link.append(dict_play)



    # 获取13位时间戳
    def _GetUtcTime(self):
        time_stamp = int(time.time() * 1000)
        return time_stamp

    # 获取图片
    def DownMovPicture(self, link):
        img = requests.get(url=link).content
        return img