# coding=utf-8
import re
import time
import random
import pycurl
import hmac
import hashlib
import io
import certifi
import json
import urllib.parse

class get_ip():
    def __init__(self, num, agreement):
        self.account_root = 'https://h.wandouip.com/get/ip-list?'
        self.ip_root = 'https://h.wandouip.com/get/add-white-list?'
        self.num = num
        self.agreement = agreement
        self.token = '0091282191b62a39d51f1509b5a9c293471f1e77bf01'
        self.app_key = '3a9b30eabf8bc64241a972096e72f0f5'
        self.app_secret = '5b8a9d302ddc542d3f37be0909b8fb6f'

    def __api_call(self, url, type, params=json.dumps({})):
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        curl.setopt(pycurl.CAINFO, certifi.where())
        # curl.setopt(pycurl.HTTPHEADER, headers)
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
        return ret

    # def add_ip(self):
    #     params =
    #     'https://h.wandouip.com/get/add-white-list?iplist=47.75.200.191 '

    def get_ip_address(self):
        params = {
            'app_key': self.app_key,
            'num': self.num,
            'xy': self.agreement,
            'type': 'json',
        }
        params = urllib.parse.urlencode(params)
        # headers = ["Content-Type: application/json"]
        ret = self.__api_call(self.account_root + params, 'GET', )
        ret = json.loads(ret)
        proxy_list = []
        for i in ret['data_NK_HS-YM']:
            ip = i['ip']
            port = i['port']
            proxy = str(ip) + ':' + str(port)
            proxy_list.append(proxy)
        print(proxy_list)
        return proxy_list