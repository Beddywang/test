# -*- coding: utf-8 -*-

def get_param(path):
    d = {}
    with open(path,'r') as f:
        for readline in f.readlines():
            data = readline.strip().replace(" ","").split('=')
            d[data[0]] = data[1]
        return d




if __name__ == '__main__':
    path = r'D:\Python_file\blade-test\conf\config.ini'
    print get_param(path)