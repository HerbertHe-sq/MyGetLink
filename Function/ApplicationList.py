import os
import winreg

class AppList:
    #初始化
    def __init__(self):
        self._subKey = [r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall', r'SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall']
        self._softwareName = []
        self._softwareName.clear()
        for i in self._subKey:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, i, 0, winreg.KEY_ALL_ACCESS)
            for j in range(0, winreg.QueryInfoKey(key)[0] - 1):
                try:
                    key_name = winreg.EnumKey(key, j)
                    key_path = i + '\\' + key_name
                    each_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path, 0, winreg.KEY_ALL_ACCESS)
                    DisplayName, REG_SZ = winreg.QueryValueEx(each_key, 'DisplayName')
                    DisplayName = DisplayName.encode('utf-8')
                    self._softwareName.append(DisplayName)
                except WindowsError:
                    pass


    def GetAppList(self):
        return self._softwareName