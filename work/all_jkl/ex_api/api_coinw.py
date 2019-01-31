import json
import pycurl
import io
import certifi
import urllib
from urllib import parse
import time
import hmac
import hashlib


class api_coinw:
    def __init__(self, key):
        self.api__key = key[0]
        self.secret_key = key[1].encode('utf-8')
        self.dict_symbol = {'HPY': 17, 'DOGE': 25, 'ETH': 14, 'HSR': 5}

    def __sym(self, symbol):
        return self.dict_symbol[symbol[0]]

    def __sign(self, message):
        hl = hashlib.md5()
        hl.update(message.encode('utf-8'))
        signature = hl.hexdigest().upper()
        return signature

    def sort_params(self, params):
        p = dict(sorted(params.items(), key=lambda item: item[0]))
        return urllib.parse.urlencode(p)

    def __api_call(self, method, params=''):
        base_endpoint = 'https://www.coinw.me'
        # header = ['Accept: application/json']
        # header = ['Accept:*/*',
        #  'Content-Type:application/xml',
        #  'render:json',
        #  'clientType:json',
        #  'Accept-Charset:GBK,utf-8;q=0.7,*;q=0.3',
        #  'Accept-Encoding:gzip,deflate,sdch',
        #  'Accept-Language:zh-CN,zh;q=0.8',
        #  'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0']
        if params == '':
            url = base_endpoint + method
        else:
            params_sign = dict(params)
            m_sign = self.sort_params(params_sign) + '&secret_key=' + self.secret_key.decode()
            sign = self.__sign(m_sign)
            m = self.sort_params(params)
            url = base_endpoint + method + '&' + m + '&sign=' + sign
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.SSL_VERIFYPEER, False)
        # curl.setopt(pycurl.HTTPHEADER,header)
        curl.setopt(pycurl.TIMEOUT, 15)
        # curl.setopt(pycurl.COOKIE,
        #             'acw_sc_=0233E112A73D3C6C2B072990ACB6E9E03BAA5D95; path=/; expires=Tue Jan 19 2038 03:14:07 GMT+0800; max_age=600')
        curl.setopt(pycurl.USERAGENT,
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
        # curl.setopt(pycurl.ENCODING, 'gzip')
        curl.setopt(pycurl.CUSTOMREQUEST, 'GET')
        curl.setopt(pycurl.URL, url)
        # print(url)
        try:
            curl.perform()
        except Exception as e:
            print(e)
            print('Error: curl.perform')
            return False
        # print(iofunc.getvalue())
        ret_message = iofunc.getvalue().decode()
        # print(ret_message)
        curl.close()
        iofunc.close()
        try:
            ret = json.loads(ret_message)
        except Exception as e:
            print(e)
            print('Error: json.loads')
            return False
        else:
            return ret

    # 深度
    def get_depth(self, symbol):
        symbol = self.__sym(symbol)
        method = "/appApi.html?action=depth&symbol=" + str(symbol)
        ret = self.__api_call(method)
        bids = ret["data_NK_HS-YM"]["bids"]
        list_bids = []
        list_asks = []
        asks = ret["data_NK_HS-YM"]["asks"]
        dict = {}
        for i in bids:
            b = [i["price"], i["amount"]]
            list_bids.append(b)
        for i in asks:
            a = [i["price"], i["amount"]]
            list_asks.append(a)
        dict['asks'] = list_asks
        dict['bids'] = list_bids
        return dict

    # K线
    # step值为60,60*1,60*5
    def get_volume(self, symbol, step):
        method = '/appApi.html?action=kline'
        params = {
            'symbol': self.__sym(symbol),
            'step': str(step),
        }
        ret = self.__api_call(method, params)
        # list_vo=[]
        # for vo in ret:
        #     print(vo)
        #     list_vo.append(vo[4])
        # print(list_vo)
        # return list_vo
        return ret

    # 获取用户资产
    def get_account(self):
        method = '/appApi.html?action=userinfo'
        params = {
            'api_key': self.api__key,
        }
        ret = self.__api_call(method, params=params)
        ret1 = ret['data_NK_HS-YM']['free'].keys()
        new = {}
        for fr in ret1:
            new[fr] = {
                'avaid_balance': ret['data_NK_HS-YM']['free'][fr],
                'freeze_balance': ret['data_NK_HS-YM']['frozen'][fr]
            }
        return new

    # 下单
    def order(self, symbol, side, quantity, price):
        if side == 'buy':
            side = 0
        elif side == 'sell':
            side = 1
        method = '/appApi.html?action=trade'
        params = {
            'symbol': self.__sym(symbol),
            'type': str(side),
            'amount': str(quantity),
            'price': str(price),
            'api_key': self.api__key,
        }
        ret = self.__api_call(method, params=params)
        return ret

    # 撤销订单
    def cancel(self, orderId):
        method = '/appApi.html?action=cancel_entrust'
        params = {
            'api_key': self.api__key,
            'id': str(orderId)
        }
        ret = self.__api_call(method, params=params)
        return ret

    # 委托记录
    def get_my_depth(self, symbol):
        method = '/appApi.html?action=entrust'
        params = {
            'symbol': self.__sym(symbol),
            'api_key': self.api__key,
        }
        ret = self.__api_call(method, params=params)
        ret = ret['data_NK_HS-YM']
        new_ret = []
        for dic in ret:
            dict_data = {}
            dict_data['price'] = dic['prize']
            dict_data['quantity'] = dic['count']
            dict_data['order_id'] = dic['id']
            dict_data['side'] = dic['type']
            dict_data['success_count'] = dic['success_count']
            dict_data['amount'] = dic['amount']
            dict_data['success_amount'] = dic['success_amount']
            dict_data['type_s'] = dic['type_s']
            dict_data['status'] = dic['status']
            dict_data['status_s'] = dic['status_s']
            new_ret.append(dict_data)
        return new_ret
