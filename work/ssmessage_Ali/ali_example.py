import datetime
import hashlib
from urllib import parse

import xlrd
import time
import random
import pycurl
import hmac
import io
import certifi
import json


class miaodi_message:
    def __init__(self):
        self.base_url = 'http://dingxinyx.market.alicloudapi.com/dx/marketSendSms'

    def __api_call(self, url, headers, type, params=json.dumps({})):
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.HTTPHEADER, headers)
        if type == 'POST':
            curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
            curl.setopt(pycurl.POSTFIELDS, params)
        elif type == 'GET':
            curl.setopt(pycurl.CUSTOMREQUEST, 'GET')
        elif type == 'DELETE':
            curl.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        curl.setopt(pycurl.TIMEOUT, 30)
        print(url)
        curl.setopt(pycurl.URL, url)
        try:
            curl.perform()
            ret = iofunc.getvalue().decode('utf-8')
        except Exception as e:
            print(e)
            return False
        print(ret)
        try:
            ret = json.loads(ret)
        except Exception as e:
            print(e)
            return False
        return ret

    def send_sms(self):
        params = {
            'mobile': 13120362121,
            'param': '您好，我司是全球领先的区块链技术提供商与MT4白标提供商，可以帮助行业从业者（1）开办数字货币交易所与（2）外汇期货交易平台（微信号：Abby24154）',
            'tpl_id': 'TP18041310'
        }
        params_dict = parse.urlencode(params)
        headers = ['Accept: application/json']
        ret = self.__api_call(self.base_url, headers, 'POST', params_dict)
        return ret