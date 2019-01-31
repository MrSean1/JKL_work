from ex_api.api import base_api
import pycurl
import hmac
import hashlib
import json
import base64
import io
import certifi
import urllib
from urllib import parse
import time


class api_tt(base_api):
    def __init__(self, user_info):
        self.user_info = user_info

    def __code(self, symbol):
        return symbol

    def __api_call(self, user_id, method, xtype, params=''):
        headers = [
            # 'x-requestted-with: XMLHttpRequest', 'Accept-Language: en-US,en;q=0.5',
            'ContentType: application/x-www-form-urlencoded; chartset=UTF-8',
            # 'Cache-Control: max-age=0',
            'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        ]
        base_endpoint = 'https://www.lhex.pro'
        curl, iofunc = self.initcurl(xtype)
        curl.setopt(pycurl.HTTPHEADER, headers)
        if user_id != -1:
            curl.setopt(pycurl.COOKIEFILE, "cookie_ttex/cookie" + str(user_id))
            curl.setopt(pycurl.COOKIEJAR, "cookie_ttex/cookie" + str(user_id))
        curl.setopt(pycurl.USERAGENT,
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0')
        url = base_endpoint + method
        if params:
            url = url + '?' + self.sort_params(params)
        curl.setopt(pycurl.URL, url)
        print(url)
        # print(params)
        try:
            curl.perform()
        except Exception as e:
            print(e)
            print('Error: curl.perform')
            return False
        ret_message = iofunc.getvalue().decode()
        print('return:', ret_message)
        curl.close()
        iofunc.close()
        if ret_message == '' and user_id != -1:
            self.login(user_id)
            return self.__api_call(user_id, method, xtype, params)
        try:
            ret = json.loads(ret_message)
        except Exception as e:
            print(e)
            print('Error: json.loads')
            print(ret_message)
            return False
        else:
            return ret

    def login(self, user_id):
        method = '/public/user/login'
        params = {
            'name': self.user_info[str(user_id)]['name'],
            'password': self.user_info[str(user_id)]['password'],
            'loginType': str(1)
        }
        ret = self.__api_call(user_id, method, 0, params)
        return ret

    def get_account(self, user_id):
        method = '/member/getAccount'
        ret = self.__api_call(user_id, method, 0)
        return ret

    def get_depth(self, symbol):
        method = '/public/stock/market'
        params = {
            'code': self.__code(symbol)
        }
        ret = self.__api_call(-1, method, 0, params)
        return ret

    def __order_buy(self, user_id, symbol, quantity, price):
        method = '/currency/trade/buy'
        code = self.__code(symbol)
        params = {
            'code': code,
            'num': str(quantity),
            'price': str(price)
        }
        ret = self.__api_call(user_id, method, 0, params)
        return ret

    def __order_sell(self, user_id, symbol, quantity, price):
        method = '/currency/trade/sell'
        code = self.__code(symbol)
        params = {
            'code': code,
            'num': str(quantity),
            'price': str(price)
        }
        ret = self.__api_call(user_id, method, 0, params)
        return ret

    def order(self, user_id, symbol, side, quantity, price):
        if side == 'buy':
            return self.__order_buy(user_id, symbol, quantity, price)
        elif side == 'sell':
            return self.__order_sell(user_id, symbol, quantity, price)
        else:
            print('wrong side')
            return False

    def cancel(self, user_id, txNo):
        method = '/currency/trade/cancel'
        params = {
            'txNo': str(txNo)
        }
        ret = self.__api_call(user_id, method, 0, params)
        return ret

    def cancelByPrice(self, user_id, symbol, start, end):
        method = '/currency/trade/cancelByPrice'
        params = {
            'code': self.__code(symbol),
            'start': str(start),
            'end': str(end)
        }
        ret = self.__api_call(user_id, method, 0, params)
        return ret

    def get_my_depth(self, user_id, symbol, page=0, limit=1000):
        method = '/currency/trade/findEntrust'
        params = {
            'code': self.__code(symbol),
            'page': str(page),
            'limit': str(limit)
        }
        ret = self.__api_call(user_id, method, 0, params)
        return ret
