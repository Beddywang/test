# -*- coding: utf-8 -*-
import json

class casejson(object):
    def __init__(self,casename,casepath):
        self.casename = casename
        self.casepath = casepath
    def getcasejson(self):
        str = {"casename":self.casename,"casenumber":"","investigator":"","investigatorpart":"","sendername":"","senderpart":"",\
               "remark":"","casepath":self.casepath,"type":"case"}
        return json.dumps(str)

class MyJson(object):
    '''
    获取param的两个参数，name和report
    '''
    def __init__(self,name,report):
        # self.appname = appname
        self.name = name
        self.report = report

    def get_json(self):
        if self.report == 'False' or self.report == 'false':
            self.report = False
        else:
            self.report = True
        str = {"name":self.name,"report":self.report}
        # return str
        return json.dumps(str)

class nameJson(object):
    '''
    获取name中的两个参数appname,param
    '''
    def __init__(self,appname,param):
        self.appname = appname
        self.param = param

    def get_Param(self):
        param = []
        if isinstance(self.appname,list):
            for i in self.appname:
                json = {"appname":i,"param":self.param}
                param.append(json)
        else:
            json = {"appname": self.appname, "param": self.param}
            param.append(json)
        return param

class Param():
    '''
    param有两个参数range和param
    '''
    def __init__(self,range,paramson):
        self.paramson = paramson
        self.range = range

    def get_param_json(self):
        str1 = {"param":self.paramson,"range":self.range}
        return json.dumps(str1)
        # return str1
class Range():
    '''
    range 有两个参数，range和type
    '''
    def __init__(self,appname,range,type=[]):
        self.appname = appname
        self.range = range
        self.type = type

    def get_range_json(self):
        if self.appname == 'groot':
            str2 = {"range":"","type":self.type}
        else:
            str2 = {"range":self.range,"type":self.type}
        # return json.dumps(str2)
        return str2
class ParamSon():
    '''
    paramson是name中的param参数的值，含有多个参数
    '''
    def __init__(self,appname,devices,loadmode,multi,type,other="",timezone="UTC+08:00"):
        self.appname = appname
        self.devices = devices
        self.loadmode = loadmode
        self.multi = multi
        self.type = type
        self.other = other
        self.timezone = timezone

    def get_param_json(self):
        if self.multi == 'False' or self.multi == 'false':
            self.multi = False
        else:
            self.multi = True
        if self.appname == 'groot':
            str3 = {"devices":[self.devices],"timezone":self.timezone,"loadmode":self.loadmode,"multi":self.multi,"type":self.type,"other":self.other}
        else:
            str3 = {"param":""}
        # print json.dumps(str3)
        return json.dumps(str3)
        # return str3
class Devices_json():
    '''
    device需要一个参数path,主要是为了groot
    '''
    def __init__(self,path):
        self.path = path

    def get_devices_json(self):
        str4 = {"path":self.path}
        # return json.dumps(str4)
        return str4
def get_my_json(appname,path,loadmode,multi,type,range,report):
    #devices_json
    devices_json = Devices_json(path).get_devices_json()
    # print "devices_json:",devices_json
    #paramson
    paramson = ParamSon(appname,devices_json,loadmode,multi,type).get_param_json()
    # print type(paramson)
    # print "paramson:",paramson
    #rangejson
    rangejson = Range(appname,range).get_range_json()
    # print "rangejson:",rangejson
    #paramjson
    paramjson = Param(rangejson,paramson).get_param_json()
    # print "paramjson:",paramjson
    namejson = nameJson(appname,paramjson).get_Param()
    # print "namejson:",namejson
    #myjson
    myjson = MyJson(namejson,report).get_json()
    return myjson

if __name__ == '__main__':
    d = param.get_param(r'E:\python_file\Exercise\blade-test\blade-test\conf\config.ini')
    print d
    appname_groot = d['appname_groot']
    path = d["imagepath"]
    loadmode = d["loadmode"]
    multi = d["multi"]
    type = d["type"]
    range = d["range"]
    report = d["report"]
    # filesystemparam = get_my_json("groot","D:\FAT32.E01","deleterecovery",False,"image","RelevantFile",False)
    filesystemparam = get_my_json(appname_groot,path,loadmode,multi,type,range,report)
    print filesystemparam
    print get_my_json(["reg","usb"],"D:\FAT32.E01","deleterecovery",False,"image","RelevantFile",False)

