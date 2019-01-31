import time
import random
import pycurl
import hmac
import hashlib
import io
import certifi
import json


class api_bxx():
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
            self.account_root = 'http://47.91.163.110/v2/u'
            self.market_root = 'http://47.91.163.110/v2/s'
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
            self.account_root = 'http://47.91.161.88/v2/u'
            self.market_root = 'http://47.91.161.88/v2/s'
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

    def __sym(self, symbol):
        return symbol[0].upper() + symbol[1].upper()

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
            if 'errcode' in ret.keys() and str(ret['errcode']) == '40001':
                print('token expired')
                self.get_token()
                headers[1] = "Authorization: " + self.token
                ret = self.__api_call(url, headers, type, params)
        except Exception as e:
            print(e)
            return False
        return ret

    def get_token(self):
        # method = '/cgi-bin/token'
        # headers = ["Content-Type: application/json"]
        # params = {}
        # params = json.dumps(params)
        # url = self.account_root + method + '?access_key=' + self.user_name + '&secret=' + self.password
        # ret = self.__tempcurl(url, headers, params, 'GET')
        # return ret['data_NK_HS-YM']['access_token']
        # if self.ex_name=='TTEX':
        #     headers = []
        #     ret = self.__api_call('https://service.ttex.pro/v2/u/cgi-bin/token?access_key='+str(self.user_name)+'&secret=$2a$10$GA4/C55MaGm06AMr/urkBe9',headers,'GET')
        #     return ret
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
        ret = self.__api_call(self.account_root + method, headers, 'POST', params)
        self.token = ret['data_NK_HS-YM']['access_token']
        return ret

    def get_my_depth(self, symbol, page=1, size=100):
        symbol = self.__sym(symbol)
        if not self.token:
            self.get_token()
        method = '/trade/order/entrusts/' + symbol + '/' + str(page) + '/' + str(size)
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.__api_call(self.market_root + method, headers, 'GET')
        return ret['data_NK_HS-YM']['records']

    def get_account(self):
        if not self.token:
            self.get_token()
        method = '/account/accounts'
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.__api_call(self.market_root + method, headers, 'GET')
        return ret['data_NK_HS-YM']['assertList']

    def order(self, symbol, side, quantity, price):
        symbol = self.__sym(symbol)
        if not self.token:
            self.get_token()
        method = '/trade/order/entrusts'
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        params = {
            'price': price,
            'symbol': symbol,
            'volume': quantity,
            'type': 1
        }
        if side == 'sell':
            params['type'] = 2
        params = json.dumps(params)
        ret = self.__api_call(self.market_root + method, headers, 'POST', params)
        if 'status' in ret.keys():
            return ret['status']
        return ret['data_NK_HS-YM']

    def cancel(self, order_id):
        if not self.token:
            self.get_token()
        method = '/trade/order/entrusts/' + str(order_id)
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.__api_call(self.market_root + method, headers, 'POST')
        return ret

    def get_depth(self, symbol):
        symbol = self.__sym(symbol)
        # if not self.token:
        #     self.get_token()
        method = '/trade/market/depth/' + symbol + '/step0'
        # headers = ["Content-Type: application/json", "Authorization: " + self.token]
        headers = ["Content-Type: application/json"]
        ret = self.__api_call(self.market_root + method, headers, 'GET')
        depth = ret['data_NK_HS-YM']
        depth['bids'] = [[dic['price'], dic['volume']] for dic in depth['bids']]
        depth['asks'] = [[dic['price'], dic['volume']] for dic in depth['asks']]
        return depth

    def get_tick(self, symbol):
        symbol = self.__sym(symbol)
        # if not self.token:
        #     self.get_token()
        method = '/trade/market/ticker/' + symbol
        # headers = ["Content-Type: application/json", "Authorization: " + self.token]
        headers = ["Content-Type: application/json"]
        ret = self.__api_call(self.market_root + method, headers, 'GET')
        return ret['data_NK_HS-YM']

    def get_query(self, order_id):
        if not self.token:
            self.get_token()
        method = '/trade/order/entrusts/' + str(order_id)
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.__api_call(self.market_root + method, headers, 'GET')
        return ret['data_NK_HS-YM']

    def self_order(self, symbol, side, quantity, price):
        symbol = self.__sym(symbol)
        if not self.token:
            self.get_token()
        method = '/trade/order/deal'
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        params = {
            'price': price,
            'symbol': symbol,
            'volume': quantity,
            'type': 1,
            'api_key': self.api_key
        }
        if side == 'sell':
            params['type'] = 2
        params = json.dumps(params)
        ret = self.__api_call(self.market_root + method, headers, 'POST', params)
        return ret

    def get_history_depth(self, symbol, page=1, size=100):
        symbol = self.__sym(symbol)
        if not self.token:
            self.get_token()
        method = '/trade/order/history/' + symbol + '/' + str(page) + '/' + str(size)
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.__api_call(self.market_root + method, headers, 'GET')
        return ret['data_NK_HS-YM']['records']
