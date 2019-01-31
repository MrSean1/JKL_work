import time
import random
import pycurl
import hmac
import hashlib
import io
from datetime import datetime
from urllib import parse

import certifi
import json
from send_email.write_email import WriteEmail


class api_base():
    def __init__(self, key_dic):
        if len(key_dic) == 3:
            self.ex_name = str(key_dic[0])
            self.user_name = str(key_dic[1])
            self.password = str(key_dic[2])
            self.token = ''
        elif len(key_dic) == 2:
            self.ex_name = str(key_dic[0])
            self.token = key_dic[1]
        if self.ex_name == 'BXX':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPa'
            # self.account_root = 'http://47.91.163.110/v2/u'
            # self.market_root = 'http://47.91.163.110/v2/s'
            self.account_root = 'http://service-robot.bxx.com/v2/u'
            self.market_root = 'http://service-robot.bxx.com/v2/s'
        elif self.ex_name == 'TEST':
            self.api_key = '3SHn27c0jLfLtvKaMNZnbWv&AF%HjGONBgtIu9uax@yZG2#wpGRx#lIOCd!4VQlY'
            self.account_root = 'http://47.106.158.72/v2/u'
            self.market_root = 'http://47.106.158.72/v2/s'
        elif self.ex_name == 'HBANK':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPb'
            self.account_root = 'http://47.89.60.31/v2/u'
            self.market_root = 'http://47.89.60.31/v2/s'
        elif self.ex_name == 'TTEX':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPa'
            # self.account_root = 'http://47.91.161.88/v2/u'
            # self.market_root = 'http://47.91.161.88/v2/s'
            self.account_root = 'http://service-robot.ttex.pro/v2/u'
            self.market_root = 'http://service-robot.ttex.pro/v2/s'
        elif self.ex_name == 'DAPP':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPc'
            # self.account_root = 'http://47.52.84.252/v2/u'
            # self.market_root = 'http://47.52.84.252/v2/s'
            self.account_root = 'http://service-robot.dappex.net/v2/u'
            self.market_root = 'http://service-robot.dappex.net/v2/s'
        elif self.ex_name == 'COINFLY':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPd'
            # self.account_root = 'http://47.91.170.40/v2/u'
            # self.market_root = 'http://47.91.170.40/v2/s'
            self.account_root = 'http://service-robot.coinfly.com/v2/u'
            self.market_root = 'http://service-robot.coinfly.com/v2/s'
        elif self.ex_name == 'COINX':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPa'
            # self.account_root = 'http://47.75.149.78/v2/u'
            # self.market_root = 'http://47.75.149.78/v2/s'
            self.account_root = 'http://service-robot.coinx.im/v2/u'
            self.market_root = 'http://service-robot.coinx.im/v2/s'
        elif self.ex_name == 'GT210':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPa'
            self.account_root = 'http://service-robot.gt210.net/v2/u'
            self.market_root = 'http://service-robot.gt210.net/v2/s'

    def __sym(self, symbol):
        return symbol[0].upper() + symbol[1].upper()

    def api_call(self, url, headers, type, params=json.dumps({})):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        global a
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
        count = 0
        while count < 10:
            try:
                curl.setopt(pycurl.URL, url)
                curl.perform()
                break
            except Exception as e:
                print(str(self.ex_name) + url + str(e))
                a = e
                count += 1
        print(now_time + ': ' + '状态码：' + str(curl.getinfo(pycurl.HTTP_CODE)) + ' ' + '接口：' + url)
        ret = iofunc.getvalue().decode('utf-8')
        if count == 10:
            message = '{}交易所，接口：{}, 请求错误超过十次, 错误是信息：'.format(self.ex_name, url, a)
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            print(title, message)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
        return curl.getinfo(pycurl.HTTP_CODE), ret

        # except Exception as e:
        #     print(e)
        #     return False
        # print(ret)
        # try:
        #     ret = json.loads(ret)
        #     if 'errcode' in ret.keys() and str(ret['errcode']) == '40001':
        #         print('token expired')
        #         self.get_token()
        #         headers[1] = "Authorization: " + self.token
        #         ret = self.__api_call(url, headers, type, params)
        # except Exception as e:
        #     print(e)
        #     return False
        # return ret

    def get_token(self):
        method = '/login'
        headers = ["Content-Type: application/json"]
        params = {
            "countryCode": "+86",
            "ga_code": 0,
            "geetest_challenge": "string",
            "geetest_seccode": "string",
            "geetest_validate": "string",
            "password": hashlib.md5(self.password.encode()).hexdigest(),
            "type": 1,
            "username": self.user_name
        }
        params = json.dumps(params)
        ret = self.api_call(self.account_root + method, headers, 'POST', params)
        try:
            ret = json.loads(ret[1])
            self.token = ret['data_NK_HS-YM']['access_token']
        except Exception:
            self.token = ''
        return ret

    def get_register(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/gt/register'
        url = self.account_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return url + '验证预处理接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return message
