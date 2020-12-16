import re
import urllib
import requests
import base64

class GetLinkTvEye:
    def __init__(self):
        self._baseUrl=''

    def SetBaseUrl(self,url):
        self._baseUrl = url

    def SearchPlace(self):
        all_list = []
        url = self._baseUrl
        headers={
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
            'Host':'luotuo.oss-cn-beijing.aliyuncs.com',
            'Accept-Encoding':'gzip, deflate, br'
        }

        req = requests.get(url=url,headers=headers,verify=False)
        req.encoding='utf-8'
        temp_data = str(base64.b64decode(req.text), 'utf-8')
        all_line = temp_data.split('\n')
        cnt = 0
        for item in all_line:
            try:
                if item!='':
                    if '#genre#' in item:
                        if '关于'in item:break
                        place_title = item.split(',')[0]
                        dict_live = {
                            'PlaceName':place_title,
                            'LiveList':[]
                        }
                        all_list.append(dict_live)
                        cnt+=1
                    else:
                        item = item.replace('，',',')
                        live_title = item.split(',')[0]
                        live_link = item.split(',')[1]
                        if '%' in live_link:
                            live_link = urllib.parse.unquote(live_link)
                        dict_live_item = {
                            'LiveTitle':live_title,
                            'LiveLink':live_link
                        }
                        all_list[cnt-1]['LiveList'].append(dict_live_item)
            except Exception as msg:
                print(msg)
        return all_list