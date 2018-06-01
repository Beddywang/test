# coding = utf-8
import array
import json


class Header:
    def __init__(self, Type, Name, Method):
        self.Type = Type
        self.Client = Name
        self.Method = Method


class Message:
    def __init__(self, header, body):
        self.Header = header
        self.Body = body

class Packet :
    def __init__(self, message):
        hs = json.dumps(message.Header, default=lambda obj: obj.__dict__)
        content = bytes(intToBytes(len(hs)))+bytes(hs)+bytes(message.Body)
        self.length = len(content)
        self.content = content

def intToBytes(n):  ## LittleEndian
    b = bytearray([0, 0, 0, 0])
    b[0] = n & 0xFF
    n >>= 8
    b[1] = n & 0xFF
    n >>= 8
    b[2] = n & 0xFF
    n >>= 8
    b[3] = n & 0xFF
    return b

def bytesToInt(bs):
    return int(array.array("I", bs)[0])


def encode(name, menthod, param):
    h = Header(0, name, menthod)
    m = Message(h, param)
    p = Packet(m)
    return intToBytes(p.length) +  p.content

def decode():
    print ""