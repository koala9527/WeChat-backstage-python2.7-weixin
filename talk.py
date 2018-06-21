# -*- coding: utf-8 -*-
import requests
import json




def talk(content,userid):
    
    url = "http://www.tuling123.com/openapi/api"
    s = requests.session()
    d={"key":"c69585cd12a65331ad35b90bda88bc56","info":content,"userid":userid}
    data = json.dumps(d)
    r = s.post(url,data = data)
    text = json.loads(r.text)
    code = text['code']
    if code == 100000:
        result = text["text"]
    elif code == 200000:
    	result = text['text']+"\n"+text["url"]
    elif code == 302000:
    	result = text['text']+'\n'+text["list"][0]["article"]+text["list"][0]["detailurl"]
    elif code == 308000:
        result = text['text']+'\n'+text["list"][0]["info"]+text["list"][0]["detailurl"]

    return result

