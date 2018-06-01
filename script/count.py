# -*- coding: utf-8 -*-
import encoding
import clinet
import json
import time,re
import threading
import getjson
import write


class getParam(object):
    '''
    将不同method需要的参数保存到json中，return str
    '''
    def __init__(self,path):
        self.path = path

    def get_json_str(self):
        with open(self.path,'r') as f:
            res = json.load(f)
        return json.dumps(res)


class GetHistoryStatus(object):
    '''
    分析文件系统和APP分析，结果都是查询status，call返回的结果获取status
    '''
    def __init__(self,connect,method,key):
        self.connect = connect
        self.method = method
        self.key = key

    def get_status(self):
        query_result = self.connect.call(self.method,"{}")
        result = json.loads(query_result[1])
        # print type(result), result
        if result.has_key("error"):
            print u"查询进度出错"
        elif result.values == [False]:
            print u"error"
        else:
            if isinstance(result.values(),list):
                # print "result_valuse():",result.values()[0][-1][self.key]
                try:
                    status = result.values()[0][-1][self.key]
                    return status
                except Exception as e:
                    # print query_result
                    print e


class GetQueryStuts(object):
    '''
    存在多个APP同时进行分析，得到的是一个list，是所有的APP的status值,并且返回服务的response
    '''
    def __init__(self,connect,method,param,key):
        self.connect = connect
        self.method = method
        self.param = param
        self.key = key

    def get_status(self):
        list = []
        query_result = self.connect.call(self.method,self.param)
        result = json.loads(query_result[1])
        # print result.values()
        if result.has_key("error"):
            print u"查询进度出错",result
        else:
            for v in result.values():
                list.append(v[self.key])
            return list,result


class query_param():
    '''
    QueryProgress需要的参数
    '''
    def __init__(self,appname):
        self.appname = appname

    def get_query_param(self):
        param = {"name":self.appname}
        return json.dumps(param)

def get_file_count(connect,status):
    '''
    获取文件系统的统计结果，需要使用到createview
    '''
    count = 0
    if status == 5:
        result = connect.call("view.CreateView",'{"type":"FsRoot","id":1537,"enum":true,"filter":{}}')
        try:
            for i in json.loads(result[1])['views']:
                count += i['total']
            return count
        except:
            print "createView error!"

def get_app_count(status,result):
    '''
    获取每个APP的分析结果，返回一个list，每个list中的元素是元祖
    '''
    count_list = []
    if status.count('5') == len(status):
        for i in result:
            count_list.append((i,result[i]["number"]))
        return count_list

def check_status(connect,method,param):
    '''
    循环查status的值为5时，app.history返回status，app.queryprogress返回list，list中为元祖[(u'reg', u'0'), (u'usb', u'0')]
    '''
    while True:
        if method == "app.History":
            status = GetHistoryStatus(connect,'app.History', 'status').get_status()
            time.sleep(10)
            if status == 5 or status == 4:
                return status
        else:
            status,result = GetQueryStuts(connect,'app.QueryProgress',param, 'status').get_status()
            time.sleep(10)
            # print status
            if status.count('5') == len(status) or (status.count('5') + status.count('4') == len(status)):
                app_count = get_app_count(status,result)
                # print app_count
                return app_count


if __name__ == '__main__':
    c = clinet.Client("test")
    c.connect()
    print u"客户端已连接"
    result = c.call("control.AddCase", getParam('addcase.json').get_json_str())  #新建案件
    print "addcase response:",result  #addcase
    # filesystem_param = addcaseJson.get_my_json("groot",u"D:\\FAT32.E01","deleterecovery",False,"image","RelevantFile",False)
    filesystem_param = getjson.get_my_json("groot", u"E:\\测试.dmg", "deleterecovery", False, "image","RelevantFile",False)#获取groot所需的param
    filesystem_result = c.call("app.CreateAction",filesystem_param)  #添加证据
    print "analysize filesysterm:", filesystem_result
    time.sleep(3)
    # print type(check_status()),check_status()
    status= check_status(c,'app.History','{}')
    # print status, number
    print u"文件系统分析结果为：",get_file_count(c,status)
    app_json = getjson.get_my_json(["reg","usb","thunderbird","foxmail","outlookexpress","reg","reg_recover","usb","usb_recover","chrome","firefox","IE4-9","edge","opera","qqbrowser"],"D:\FAT32.E01","deleterecovery",False,"image","RelevantFile",False) #获取取证分析的param
    print "app_json:",app_json
    app_analysis = c.call("app.CreateAction", app_json)  # 取证分析
    print "app_analysis:",app_analysis
    query_param = query_param(["reg","usb","thunderbird","foxmail","outlookexpress","reg","reg_recover","usb","usb_recover","chrome","firefox","IE4-9","edge","opera","qqbrowser"]).get_query_param()
    app_count = check_status(c,'app.QueryProgress',query_param)
    print u"APP分析结果：",app_count

    # write_json()
    c.call("control.CloseCase",{})
    c.close()



