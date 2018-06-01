# -*- coding: utf-8 -*-

from win32com import client
import os
# import win32api

def check_exsit(path,process_name):
    WMI = client.GetObject('winmgmts:')
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where Name="%s"' % process_name)
    if len(processCodeCov) > 0:
        print '%s is exists' % process_name
    else:
        print '%s is not exists' % process_name
        os.chdir(path)
        # win32api.ShellExecute(0, 'open', process_name, '', '', 0)  # 后台执行
        print os.path.join(path,"services",process_name)
        os.system(os.path.join(path,"services",process_name))



if __name__ == '__main__':
    check_exsit(r"E:\blade",'service.exe')