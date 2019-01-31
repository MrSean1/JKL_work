# *_*coding:utf-8 *_*
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
        self.base_url = 'https://api.miaodiyun.com/20150822/affMarkSMS/sendSMS'

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

    def send_message(self, phone_list):
        ACCOUNTSID = '390796517a6e4a1689398e076aefd5b3'
        TOKEN = '676a445638f9486588a81325b6f01685'
        timestamp = str(datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S"))
        message = ACCOUNTSID + TOKEN + timestamp
        params = {
            'accountSid': '390796517a6e4a1689398e076aefd5b3',
            'smsContent': '您好，我司是全球领先的区块链技术提供商与MT4白标提供商，可以帮助行业从业者（1）开办数字货币交易所与（2）外汇期货交易平台，以及(3)两者相融合的产业解决方案，有想详细了解的欢迎添加微信详细咨询。（微信号：Abby24154）',
            'to': phone_list,
            'timestamp': str(datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d%H%M%S")),
            'sig': hashlib.md5(message.encode()).hexdigest(),
            'respDataType': 'JSON',
        }
        headers = ['Content-type:application/x-www-form-urlencoded']
        # params = json.dumps(params)
        params_dict = parse.urlencode(params)
        ret = self.__api_call(self.base_url, headers, 'POST', params_dict)
        return ret


def get_phton(filename):
    bk = xlrd.open_workbook(filename)
    table = bk.sheet_by_name('Sheetname')
    phone_list = table.col_values(1)[1:]
    phone_list = [int(phone) for phone in phone_list[:len(phone_list) - 1]]
    return phone_list
