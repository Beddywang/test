# -*- coding: utf-8 -*-

import param
import time
import getjson
import clinet
import count
import write
import os
import checkprocess

checkprocess.check_exsit(r"D:\Blade_V0.5.132.287","service.exe")

def main():
    c = clinet.Client("test")
    c.connect()
    d = param.get_param(r'D:\Python_file\blade-test\conf\config.ini')
    casename = d["casename"]
    casepath = d["casepath"]
    appname_groot = d['appname_groot']
    path = d["imagepath"].decode('gbk')
    loadmode = d["loadmode"]
    multi = d["multi"]
    type = d["type"]
    range = d["range"]
    report = d["report"]
    appname = d["appname"].split(",")
    if os.path.isdir(path):
        for root,dirs,files in os.walk(path):
            for file in files:
                imagepath = os.path.join(root,file)
                if os.path.isfile(imagepath) and os.path.splitext(imagepath)[1] in [".dd",'.E01',".DD",".e01",".ISO",".iso",".dmg",".aff",".img"]:
                    print imagepath
                    print u"客户端已连接"
                    case_json = getjson.casejson(casename,casepath).getcasejson()
                    case_respone = c.call("control.AddCase",case_json)
                    print "addcase response:",case_respone  #addcase
                    filesystem_param = getjson.get_my_json(appname_groot, imagepath, loadmode, multi, type,range,report)#获取groot所需的param
                    filesystem_result = c.call("app.CreateAction",filesystem_param)  #添加证据
                    print "analysize filesysterm:", filesystem_result
                    time.sleep(3)
                    status= count.check_status(c,'app.History','{}')
                    file_count = count.get_file_count(c,status)
                    print u"文件系统分析结果为：",file_count
                    app_json = getjson.get_my_json(appname,imagepath, loadmode, multi, type,range,report) #获取取证分析的param
                    print "app_json:",app_json
                    app_analysis = c.call("app.CreateAction", app_json)  # 取证分析
                    print "app_analysis:",app_analysis
                    query_param = count.query_param(appname).get_query_param()
                    # print "query_param:",query_param
                    app_count = count.check_status(c,'app.QueryProgress',query_param)
                    print u"APP分析结果：",app_count
                    write.write_json(r"D:\Python_file\blade-test\source\source.xlsx",'1.0',imagepath,file_count,app_count)
                    c.call("control.CloseCase", {})
        c.close()


if __name__ == '__main__':
    main()