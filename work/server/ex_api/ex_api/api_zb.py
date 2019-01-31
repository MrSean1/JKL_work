import time
from urllib import parse
import pycurl
import hashlib
import hmac
import json
import io
import certifi


class api_zb():
    def __init__(self, key):
        self.api_key = key[0]
        self.bsecret = key[1].encode('utf-8')
        self.market_root = 'http://api.zb.cn/'
        self.account_root = 'https://trade.zb.cn/'
        self.reptime = int(round(time.time() * 1000))

    def __sym(self, symbol):
        return symbol[0].lower() + '_' + symbol[1].lower()

    def sort_params(self, params):
        p = dict(sorted(params.items(), key=lambda item: item[0]))
        return p

    # def __sign(self, message):
    #     return hmac.new(self.bsecret, message.encode('ascii'), digestmod=hashlib.md5).hexdigest()

    def __sign(self, message):
        sha_secretkey = hashlib.sha1(self.bsecret).hexdigest()
        signature = hmac.new(sha_secretkey.encode('utf-8'), message.encode('utf-8'),
                             digestmod='MD5').hexdigest()  # 32位md5算法进行加密签名
        return signature

    def __api_call(self, url, type, params=json.dumps({})):
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        curl.setopt(pycurl.CAINFO, certifi.where())
        if type == 'POST':
            curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
            curl.setopt(pycurl.POSTFIELDS, params)
            print(params)
        elif type == 'GET':
            curl.setopt(pycurl.CUSTOMREQUEST, 'GET')
        elif type == 'DELETE':
            curl.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        curl.setopt(pycurl.TIMEOUT, 30)
        curl.setopt(pycurl.USERAGENT,
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
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

    def get_depth(self, symbol, size=10):
        symbol = self.__sym(symbol)
        method = 'data_NK_HS-YM/v1/depth?market=' + symbol + '&size=' + str(size)
        url = self.market_root + method
        ret = self.__api_call(url, 'GET')
        print(ret)
        return ret

    def get_account(self):
        method = 'api/getAccountInfo?'
        params = {
            'accesskey': self.api_key,
            'method': 'getAccountInfo',
        }
        params = self.sort_params(params)
        # params['secret_key'] = self.bsecret
        params = parse.urlencode(params)
        params_dict = {
            'accesskey': self.api_key,
            'method': 'getAccountInfo',
            'sign': self.__sign(params),
            'reqTime': self.reptime,
        }
        params_dict = parse.urlencode(params_dict)
        url = self.account_root + method + params_dict
        ret = self.__api_call(url, 'GET')
        return ret['result']['coins']

    # 委托下单
    def order(self, symbol, type, amount, price=''):
        method = 'api/order?'
        if type == 'buy':
            type = 1
        elif type == 'sell':
            type = 0
        params = {
            'accesskey': self.api_key,
            'currency': self.__sym(symbol),
            'tradeType': type,
            'method': 'order',
            'amount': amount,
            'price': price
        }

        params = self.sort_params(params)
        params = parse.urlencode(params)
        params_dict = {
            'accesskey': self.api_key,
            'amount': amount,
            'currency': self.__sym(symbol),
            'method': 'order',
            'price': price,
            'tradeType': type,
            'sign': self.__sign(params),
            'reqTime': self.reptime,
        }
        params_dict = parse.urlencode(params_dict)
        url = self.account_root + method + params_dict
        ret = self.__api_call(url, 'GET')
        return ret

    # 撤销订单
    def cancel(self, orderId, symbol):
        method = 'api/cancelOrder?'
        params = {
            'accesskey': self.api_key,
            'currency': self.__sym(symbol),
            'id': orderId,
            'method': 'cancelOrder'
        }

        params = self.sort_params(params)
        params = parse.urlencode(params)
        params_dict = {
            'accesskey': self.api_key,
            'currency': self.__sym(symbol),
            'id': orderId,
            'method': 'cancelOrder',
            'sign': self.__sign(params),
            'reqTime': self.reptime,
        }
        params_dict = parse.urlencode(params_dict)
        url = self.account_root + method + params_dict
        ret = self.__api_call(url, 'GET')
        return ret

    # 获取委托买单或卖单
    # 返回值1/buy   0/sell
    def get_query(self, order_id, symbol):
        method = 'api/getOrder?'
        params = {
            'accesskey': self.api_key,
            'currency': self.__sym(symbol),
            'id': order_id,
            'method': 'getOrder',
        }
        params = self.sort_params(params)
        params = parse.urlencode(params)
        params_dict = {
            'accesskey': self.api_key,
            'currency': self.__sym(symbol),
            'id': order_id,
            'method': 'getOrder',
            'sign': self.__sign(params),
            'reqTime': self.reptime,
        }
        params_dict = parse.urlencode(params_dict)
        url = self.account_root + method + params_dict
        ret = self.__api_call(url, 'GET')
        return ret

    # 获得所有订单
    # tradeType 交易类型 1/buy  0/sell   默认0
    def get_my_depth(self, symbol, current_page=1):
        method = 'api/getUnfinishedOrdersIgnoreTradeType?'
        params = {
            'accesskey': self.api_key,
            'currency': self.__sym(symbol),
            'method': 'order',
            'pageIndex': current_page,
            'pageSize': 10,
        }
        params = self.sort_params(params)
        params = parse.urlencode(params)
        params_dict = {
            'accesskey': self.api_key,
            'currency': self.__sym(symbol),
            'method': 'order',
            'pageIndex': current_page,
            'pageSize': 10,
            'sign': self.__sign(params),
            'reqTime': self.reptime,
        }
        params_dict = parse.urlencode(params_dict)
        url = self.account_root + method + params_dict
        ret = self.__api_call(url, 'GET')
        return ret
