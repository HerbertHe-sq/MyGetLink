import configparser

class OperateIniFile:
    def __init__(self):
        self._iniPath=""
        self._iniFile = configparser.ConfigParser()

    #获取地址
    def SetResPath(self,path):
        self._iniPath = path
        self._iniFile.read(path,encoding='utf-8')

    def GetIniValue(self,selection,key):
        return self._iniFile[selection][key]

    def SetIniValue(self,selection,key,val):
        self._iniFile[selection][key] = val
        self._SaveIniFile(self._iniPath)

    def _SaveIniFile(self,path):
        with open(path,"w",encoding='utf-8') as f_write:
            if self._iniFile:
                self._iniFile.write(f_write)
