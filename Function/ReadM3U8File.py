import os
import requests
import re

class ReadM3U8File:
    def __init__(self,path):
        self._tagPath = path

    #读取文件
    def ReadFile(self):
        flag = False
        all_line = []
        if os.path.exists(self._tagPath):
            with open(self._tagPath,"r",encoding='utf-8') as f_read:
                all_line.clear()
                for line in f_read:
                    all_line.append(line)
                flag = True
        return flag,all_line

    #获取M3U8地址
    def GetUrlFile(self,url):
        key_url = ''
        mov_url = ''
        list = []
        req = requests.get(url=url)
        req.encoding='utf-8'

        if '/hls/index.m3u8' in req.text:
            temp_str_arr = req.text.split('\n')
            return self.GetUrlFile(os.path.dirname(url)+'/'+temp_str_arr[2])
        else:
            mov_url = url
            sum_url = ''
            #检查是否带加密
            if '#EXT-X-KEY' in req.text:
                key_url = re.findall('#EXT-X-KEY.*?,URI="(.*?)"',req.text,re.I|re.S)[0]
            elif '#EXT-MGTV-X-MAP:URI="data:video/mp4;base64' in req.text:
                #;base64,
                key_url = 'base64,'+re.findall('#EXT-MGTV-X-MAP:URI="data:video/mp4;base64,(.*?)"',req.text,re.I|re.S)[0]
                sum_url = re.findall('#EXT-X-MAP:URI="(.*?)"',req.text,re.I|re.S)[0]

            if 'http' in req.text:  #兼容特殊网站
                if 'ts?' in req.text:
                    match_str = re.findall('(http.*?.ts.*?)#EXTINF', req.text, re.I | re.S)
                elif 'ts' in req.text:
                    match_str = re.findall('http.*?.ts', req.text, re.I | re.S)
                elif 'jpg' in req.text:
                    match_str = re.findall('http.*?.jpg', req.text, re.I | re.S)
                elif 'pgc-image' in req.text:
                    match_str = re.findall('(http.*?.)#EXTINF', req.text, re.I | re.S)
                else:
                    match_str = ''
            else:
                if 'ts?' in req.text:
                    match_str = re.findall('EXTINF:.*?,(.*?.ts.*?)#', req.text, re.I | re.S)
                elif 'm4s?' in req.text:
                    match_str = re.findall('EXTINF:.*?,(.*?.m4s.*?)#', req.text, re.I | re.S)
                else:
                    match_str = re.findall('#EXTINF.*?,(.*?.ts)',req.text,re.I|re.S)
            for item in match_str:
               temp = item.replace(',\n','')
               temp = temp.replace('\n', '')
               temp_key = temp[0:temp.rfind('/')]

               if temp_key in url:
                    root_url = url.split(temp_key)
                    list.append(root_url[0].replace(',\n','')+temp)
               else:
                list.append(temp)
        return list,key_url,mov_url


    #筛选链接
    def GetM3U8FromList(self,list):
        all_list = []
        temp_i = 0
        for item in list:
            if '.ts?' in item:
                file_name = re.findall('(.*?.ts)', os.path.basename(item), re.I | re.S)[0]
                dict_file = {
                    'MovName': file_name.replace('\n', ''),
                    'MovPath': item.replace('\r', '')
                }
                all_list.append(dict_file)
            elif ('.ts' in item) or ('.jpg' in item) or ('.png' in item):
                file_name = os.path.basename(item)
                dict_file = {
                    'MovName': str(temp_i)+file_name.replace('\n', ''),
                    'MovPath': item.replace('\n', '')
                }
                all_list.append(dict_file)
                temp_i+=1
            elif 'pgc-image' in item:
                file_name = os.path.basename(item).replace('\r','')+'.ts'
                dict_file = {
                    'MovName': file_name.replace('\n', ''),
                    'MovPath': item.replace('\r', '')
                }
                all_list.append(dict_file)
            elif '.m4s' in item:
                file_name = re.findall('(.*?.m4s)', os.path.basename(item), re.I | re.S)[0]
                dict_file = {
                    'MovName': file_name.replace('\n', '').replace('.m4s','.mp4'),
                    'MovPath': item.replace('\r', '')
                }
                all_list.append(dict_file)
        return all_list


    #获取AES秘钥
    def GetAesKey(self,url):
        req = requests.get(url)
        return req.text