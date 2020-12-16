import re
import requests

#奇哈电视直播网站http://www.dszbdq.cn/
class GetLinkLiveQhtv:
    def __init__(self):
        self._baseUrl = ''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchPlace(self):
        all_list = []
        url = self._baseUrl
        headers={
            'Host': 'www.dszbdq.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<h2>地方导航</h2></div>.*?<ul class="nav-type">(.*?)</ul>',req.text,re.I|re.S)[0]
        match_list = re.findall('<li class="channel">(.*?)</li>',match_str,re.I|re.S)
        for item in match_list:
            temp_link = re.findall('<a class="channel-link" href="(.*?)"',item,re.I|re.S)[0]
            title = re.findall('<a class="channel-link" href=.*?>(.*?)</a></div>',item,re.I|re.S)[0]
            if not 'http' in temp_link:
                temp_link = self._baseUrl+temp_link

            dict_place = {
                'PlaceName':title,
                'PlaceLink':temp_link
            }
            all_list.append(dict_place)
        return all_list

    def SearchTvProgram(self,dict_prog):
        all_list = []
        url = dict_prog['PlaceLink']
        headers = {
            'Host': 'www.dszbdq.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'http://www.dszbdq.cn/'
        }
        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<div class="big_title">.*?<ul class="nav-type">(.*?)</ul>',req.text,re.I|re.S)
        for item in match_str:
            temp_list = re.findall('<li class="channel">(.*?)</li>',item,re.I|re.S)
            for item_s in temp_list:
                link = re.findall('<a class="channel-link" href="(.*?)"', item_s, re.I | re.S)[0]
                title = re.findall('<a class="channel-link" href=".*?>(.*?)</a>', item_s, re.I | re.S)[0]
                if not 'http' in link:
                    link = self._baseUrl + link
                if not '个' in title:
                    if not '更多' in title:
                        pattern = ''
                        if ('</strong>' in title) and (not '</font>' in title):
                            pattern = '<strong>(.*?)</strong>'
                            title = re.findall(pattern, title, re.I | re.S)[0]
                        elif '</font></strong>' in title:
                            pattern = '<font.*?>(.*?)</font></strong>'
                            title = re.findall(pattern, title, re.I | re.S)[0]
                        else:
                            pass
                        dict_prog = {
                            'LiveTitle':title,
                            'LiveLink':link
                        }
                        all_list.append(dict_prog)
                    else:
                        self._GetTvProg_S(link,all_list)
        result_list = self._remove_duplicate(all_list)
        return result_list

    def _GetTvProg_S(self,url,list):
        headers = {
            'Host': 'www.dszbdq.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'http://www.dszbdq.cn/'
        }

        req = requests.get(url=url,headers=headers)
        req.encoding='utf-8'
        match_str = re.findall('<div class="big_title">.*?<ul class="nav-type">(.*?)</ul>', req.text, re.I | re.S)
        for item in match_str:
            temp_list = re.findall('<li class="channel">(.*?)</li>', item, re.I | re.S)
            for item_s in temp_list:
                try:
                    link = re.findall('<a class="channel-link" href="(.*?)"', item_s, re.I | re.S)[0]
                    title = re.findall('<a class="channel-link" href=".*?>(.*?)</a>', item_s, re.I | re.S)[0]
                    if not 'http' in link:
                        link = self._baseUrl + link
                    if not '个' in title:
                        if not '更多' in title:
                            pattern=''
                            if ('</strong>' in title) and (not '</font>' in title):
                                pattern = '<strong>(.*?)</strong>'
                                title = re.findall(pattern, title, re.I | re.S)[0]
                            elif '</font></strong>' in title:
                                pattern = '<font.*?>(.*?)</font></strong>'
                                title = re.findall(pattern, title, re.I | re.S)[0]
                            else:
                                pass
                            dict_prog = {
                                'LiveTitle': title,
                                'LiveLink': link
                            }
                            list.append(dict_prog)
                except Exception as msg:
                    print(msg)

    def GetM3U8Link(self,dict_prog):
        all_link = []
        url = dict_prog['LiveLink']
        req = requests.get(url=url)
        req.encoding = 'utf-8'
        html = req.text
        if '<video' in html:
            link = re.findall('<video.*?src="(.*?)"', html, re.I | re.S)[0]
            all_link.append({'Title':'Unkonw Source','Link':link})
        elif '<a class="play-link"' in html:
            match_list = re.findall('<div class="play-link-wrap">(.*?)</div>', html, re.I | re.S)
            for item in match_list:
                title = re.findall('>(.*?)</a>',item,re.I|re.S)[0]
                link = re.findall('href="(.*?)"',item,re.I|re.S)[0]
                if 'http' in link:
                    dict_live = {
                        'Title':title,
                        'Link':link
                    }
                    all_link.append(dict_live)
        return all_link

    #解析M3U8文件
    def ExplainM3U8File(self,url):
        all_list = []
        req = requests.get(url=url)
        req.encoding = 'utf-8'
        if '\r\n' in req.text:
            dat_arr = req.text.split('\r\n')
        else:
            dat_arr = req.text.split('\n')
        for item in dat_arr:
            if 'http' in item:
                all_list.append(item)
        return all_list

    def _remove_duplicate(self, dict_list):
        seen = set()
        new_dict_list = []
        for dict in dict_list:
            t_dict = {'LiveTitle': dict['LiveTitle'], 'LiveLink': dict['LiveLink']}
            t_tup = tuple(t_dict.items())
            if t_tup not in seen:
                seen.add(t_tup)
                new_dict_list.append(dict)
        return new_dict_list
