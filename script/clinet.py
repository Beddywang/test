# -*- coding: utf-8 -*-
import socket
import encoding, define
import threading

class Client:
    def __init__(self, name):

        self.name = name
        self.ctx = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.mutex = threading.Lock()

    def connect(self):
        try:
            self.ctx.connect((define.Server_Addr, define.Server_Port))
        except Exception as e:
            print e

    def close(self):
        self.ctx.close()

    def writeMessage(self, method, param):
        msg = encoding.encode(self.name, method, param)
        # print "send msg:", msg
        return self.ctx.send(msg)

    def readMessage(self):
        lb = self.ctx.recv(define.PKG_CONTENT_LEN)
        n = encoding.bytesToInt(lb)
        lb = self.ctx.recv(define.PKG_CONTENT_LEN)
        hh = encoding.bytesToInt(lb)  # header length
        h = self.ctx.recv(hh)  # header
        r = self.ctx.recv(n - hh)  # reply message
        return h, r

    ###
    # return : 1. request operation
    #			2. returned messages
    ###
    def call(self, method, param):
        self.mutex.acquire()
        self.writeMessage(method, param)
        h, r = self.readMessage()
        self.mutex.release()
        return h, r
