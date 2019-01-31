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


class get_phone():
    def __init__(self, username, password):
        self.account_root = 'http://api.fxhyd.cn/UserInterface.aspx?'
        self.account = username
        self.password = password
        self.token = ''

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
        return ret

    def get_token(self):
        headers = ["Content-Type: application/json"]
        params = {
            'action': 'login',
            "username": self.account,
            "password": self.password,
        }
        params = urllib.parse.urlencode(params)
        ret = self.__api_call(self.account_root + params, headers, 'GET', )
        self.token = ret.split('|')[1]
        return self.token

    def get_phone_num(self):
        if self.token == '':
            self.get_token()
        headers = ["Content-Type: application/json"]
        params = {
            'action': 'getmobile',
            "token": self.token,
            # 项目编号
            "itemid": 15583,
        }
        params = urllib.parse.urlencode(params)
        while True:
            ret = self.__api_call(self.account_root + params, headers, 'GET', )
            if 'success' in ret:
                break
            else:
                time.sleep(5)
        phone_num = ret.split('|')[1]
        print('获取到的手机号是：%s' % phone_num)
        return phone_num

    def get_sm(self, phone_num):
        if self.token == '':
            self.get_token()
        headers = ["Content-Type: application/json"]
        params = {
            'action': 'getsms',
            "token": self.token,
            # 项目编号
            "itemid": 15583,
            'mobile': phone_num,
        }
        params = urllib.parse.urlencode(params)
        while True:
            ret = self.__api_call(self.account_root + params, headers, 'GET', )
            if 'success' in ret:
                break
            else:
                time.sleep(5)
        sms = ret.split('|')[1]
        pattern = r"\d+"
        verifi = re.compile(pattern).findall(sms)
        print('获取得验证码是%s' % verifi[0])
        return verifi[0]

    def get_account(self):
        if self.token == '':
            self.get_token()
        headers = ["Content-Type: application/json"]
        params = {
            'action': 'getaccountinfo',
            "token": self.token,
            'format': 1,
        }
        params = urllib.parse.urlencode(params)
        ret = self.__api_call(self.account_root + params, headers, 'GET', )
        try:
            ret = ret.split('|')[1]
            ret = json.loads(ret)['Balance']
        except Exception as e:
            print('出错了')
        return ret

    def release_phone(self, phone_num):
        headers = ["Content-Type: application/json"]
        params = {
            'action': 'release',
            "token": self.token,
            'itemid': 15583,
            'mobile': phone_num
        }
        params = urllib.parse.urlencode(params)
        ret = self.__api_call(self.account_root + params, headers, 'GET', )
        if ret == 'success':
            return ret
        else:
            return '撤销失败'

# 009128217a15ca37d350b0087e07cc7b584c3239
# 009128217a15ca37d350b0087e07cc7b584c3239
