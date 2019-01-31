import pycurl
import hmac
import hashlib
import json
import base64
import io
import certifi
import urllib
from urllib import parse
from threading import Thread
import time
from pandas import DataFrame


class MyThread(Thread):
    def __init__(self, func, args=()):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class api_vbtc():
    def __init__(self, key, test=False):
        self.memberCode = key[0]
        self.customer_id = key[1]
        self.mastKey = key[2]
        self.bsecret = key[3]
        self.nonce = str(int(time.time() * 1000))
        self.__test = test

    def __sym(self, symbol):
        return symbol[0]

    def __sign(self, message_c):
        # 加密方式
        signature = hmac.new(self.bsecret.encode('ascii'), message_c.encode('ascii'), digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(signature)
        signature = urllib.parse.quote_plus(signature)
        return signature

    def __api_call(self, method, params=''):
        # 请求头，告诉浏览器传过去的是json
        headers = ["Content-Type: application/json"]
        # 最头的URL
        if self.__test:
            base_endpoint = "https://t.coinx.im/gateway"
            # base_endpoint = 'https://test-openapi.coinx.im/gateway'
            # base_endpoint = 'http://test-db.coinx.im/gateway'
        else:
            base_endpoint = 'http://openapi.ttex.pro/gateway'
            # base_endpoint = 'https://www.coinx.im/gateway'
        # 拼接成功的URL
        url = base_endpoint + method
        # 处理方式
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        # curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
        curl.setopt(pycurl.HTTPHEADER, headers)
        curl.setopt(pycurl.PORT, 80)
        # curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        # curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        # curl.setopt(pycurl.TIMEOUT, 15)
        print(url)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.POSTFIELDS, json.dumps(params))
        print(params)
        try:
            curl.perform()
        except Exception as e:
            print(e)
            print('Error: curl.perform')
            return False
        ret_message = iofunc.getvalue().decode('utf-8')
        print(ret_message)
        curl.close()
        iofunc.close()
        try:
            ret = json.loads(ret_message)
        except Exception as e:
            print(e)
            print(ret_message)
            print('Error: json.loads')
            return False
        else:
            return ret

    def get_account(self):
        # 需要拼接的URL
        method = "/apiMyAssets.jhtml"
        # 需要传递的参数
        params = {
            "mastKey": self.mastKey,
            "memberCode": self.memberCode,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['memberCode'] + params_c['customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # print(params)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        ret = ret["my_assets"]
        dict1 = {}
        for i in ret:
            dict1[i['ac_type']] = i
        ret = dict1
        # print(ret)
        return ret

    def get_depth(self, symbol, size='useless'):
        symbol = self.__sym(symbol)
        # 需要拼接的URL
        method = "/apiDepth.jhtml"
        # 需要传递的参数
        params = {
            "mastKey": self.mastKey,
            "coin": symbol,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['coin'] + params_c['customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        dict0 = {}
        dict0['asks'] = ret['asks']
        dict0['bids'] = ret['bids']
        return dict0

    def __order_buy(self, price, qty, symbol):
        # 需要拼接的URL
        method = "/apiBuy.jhtml"
        # 需要传递的参数
        # print(price, qty, symbol)
        params = {
            "mastKey": self.mastKey,
            "price": str(price),
            "qty": str(qty),
            "coin": symbol,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['price'] + params_c['qty'] + params_c['coin'] + params_c[
            'customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        ret = ret['orderid']
        return ret

    def __order_sell(self, price, qty, symbol):
        # 需要拼接的URL
        method = "/apiSell.jhtml"
        # 需要传递的参数
        params = {
            "mastKey": self.mastKey,
            "price": str(price),
            "qty": str(qty),
            "coin": symbol,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['price'] + params_c['qty'] + params_c['coin'] + params_c[
            'customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        ret = ret['orderid']
        return ret

    def order(self, symbol, side, quantity, price):
        symbol = self.__sym(symbol)
        if side == 'buy':
            return str(self.__order_buy(price, quantity, symbol))
        elif side == 'sell':
            return str(self.__order_sell(price, quantity, symbol))

    def self_order(self, symbol, quantity, price):
        symbol = self.__sym(symbol)
        method = '/apiAutoTrade.jhtml'
        params = {
            "mastKey": self.mastKey,
            "price": str(price),
            "qty": str(quantity),
            "coin": symbol,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['price'] + params_c['qty'] + params_c['coin'] + params_c[
            'customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        # ret = ret['orderid']
        return ret

    def cancel(self, orderId):
        # 需要拼接的URL
        method = "/apiCancel.jhtml"
        # 需要传递的参数
        params = {
            "mastKey": self.mastKey,
            "orderId": str(orderId),
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['orderId'] + params_c['customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        return ret

    def get_query(self, orderId):
        # 需要拼接的URL
        method = "/apiQuery.jhtml"
        # 需要传递的参数
        params = {
            "mastKey": self.mastKey,
            "orderId": orderId,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['orderId'] + params_c['customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        return ret

    def get_query_info(self, orderId):
        # 需要拼接的URL
        method = "/apiQueryInfo.jhtml"
        # 需要传递的参数
        params = {
            "mastKey": self.mastKey,
            "orderId": orderId,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['orderId'] + params_c['customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        return ret

    def get_my_depth(self):
        # 需要拼接的URL
        method = "/apiMyDepth.jhtml"
        # 需要传递的参数
        params = {
            "mastKey": self.mastKey,
            "memberCode": self.memberCode,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['memberCode'] + params_c['customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        ret = ret['apply_records']
        return ret

    def get_decimal(self, symbol):
        symbol = self.__sym(symbol)
        method = "/apiDecimalPoint.jhtml"
        params = {
            "mastKey": self.mastKey,
            "coin": symbol,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['coin'] + params_c['customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        ret = ret['coin_info']
        return ret

    # def query_info(self):
    #     f = open('id_list.txt', 'r', encoding='utf-8').read()
    #     list = f.split(' ')
    #     list.pop(-1)
    #     # print(list)
    #     l = []
    #     for i in range(int(len(list) / 100) + 1):
    #         l.append([])
    #     for i in range(len(list)):
    #         data_NK_HS-YM = list[i]
    #         count = int(i / 100)
    #         l[count].append(data_NK_HS-YM)
    #     t = []
    #     for i in range(15):
    #         t.append([])
    #         for order_id in l[i]:
    #             t[i].append(MyThread(self.get_query_info, args=(str(order_id),)))
    #         [th.start() for th in t[i]]
    #         [th.join() for th in t[i]]
    #
    #     ll = []
    #     for i in range(15):
    #         for j in range(len(t[i])):
    #             dictt = t[i][j].get_result()
    #             d = [dictt['o_order_id'], dictt['o_apply_flag'], dictt['o_success_qty'], dictt['o_apply_price']]
    #             ll.append(d)
    #             frem = DataFrame(ll, columns=('orderId', 'side', 'quantity', 'price'))
    #             # print(frem)
    #     return ll

    def get_usd_rate(self):
        method = "/apiRate.jhtml"
        params = {
            "mastKey": self.mastKey,
            "nonce": self.nonce,
        }
        params_c = dict(params)
        # 需要加密的参数（在原有的基础上加入一个新的KEY）
        params_c['customer_id'] = self.customer_id
        # 需要进行加密的字符串的拼接
        message_c = params_c['nonce'] + params_c['customer_id'] + params_c['mastKey']
        # 给params加上一个签名KEY
        params['signature'] = self.__sign(message_c=message_c)
        # 返回主体函数处理数据
        ret = self.__api_call(method, params=params)
        ret = ret['err_msg']
        return ret
