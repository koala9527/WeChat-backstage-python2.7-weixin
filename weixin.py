# -*- coding:utf-8 -*-  
import sys
sys.setdefaultencoding('utf-8')
import web
import os
import hashlib
import time
import lxml
import urllib2,json
from pacong import mian
from lxml import etree
from talk import talk

class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        token = "wxpy"

        l = [token, timestamp, nonce]
        l.sort()
        sha1 = hashlib.sha1()
        map(sha1.update,l)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            return echostr
    def POST(self):
        str_xml = web.data()
        xml = etree.fromstring(str_xml)
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        userid = fromUser[0:15]
        toUser = xml.find("ToUserName").text
        if msgType == "text":
            content = xml.find("Content").text
            #火车票 2018-06-21 广州 哈尔滨
            l=(content.encode()).split(" ")
            if l[0] == '火车票':
                mu =mian(l[1],l[2],l[3])
                return self.render.reply_text(fromUser,toUser,int(time.time()),mu)
            
            else:
                text = talk(content,userid)
                return self.render.reply_text(fromUser,toUser,int(time.time()),text)

                