import pycurl
import io
import time
import datetime
import certifi
import json
import urllib.parse
from bitmex_websocket import BitMEXWebsocket


class rest_kline():
    def __init__(self, type, symbol, number, start_time='', partial=True, ):
        self.account_root = "https://www.bitmex.com/api/v1"
        self.symbol = symbol
        self.number = number
        self.finall_num = self.number
        self.type = type
        if start_time:
            self.start_time = start_time
        elif self.type == '1m':
            self.start_time = datetime.datetime.strftime(
                datetime.datetime.utcnow() - datetime.timedelta(0, (self.number + 60) * 60), '%Y-%m-%d %H:%M:%S')
            self.number = self.number + 80
        elif self.type == '5m':
            self.start_time = datetime.datetime.strftime(
                datetime.datetime.utcnow() - datetime.timedelta(0, (self.number + 20) * 60 * 5), '%Y-%m-%d %H:%M:%S')
            self.number = self.number + 30
        elif self.type == '1h':
            self.start_time = datetime.datetime.strftime(
                datetime.datetime.utcnow() - datetime.timedelta(0, (self.number + 12) * 60 * 60), '%Y-%m-%d %H:%M:%S')
            self.number = self.number + 25
        self.partial = partial

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
        # print(ret)
        try:
            ret = json.loads(ret)
        except Exception as e:
            print(e)
            return False
        return ret

    def get_kline(self):
        params = {
            "binSize": self.type,
            "symbol": self.symbol,
            'startTime': self.start_time,
            "count": self.number,
            'partial': self.partial
        }
        params = urllib.parse.urlencode(params)
        method = '/trade/bucketed?' + params
        headers = ["Content-Type: application/json"]
        ret = self.__api_call(self.account_root + method, headers, 'GET')
        ret = ret[-self.finall_num:]
        kline_list = [[dic['timestamp'], dic['open'], dic['high'], dic['low'], dic['close'], dic['volume']] for dic in ret]
        return kline_list
    #
    # def make_kline(self, dic):
    #     kline_dic = dict()
    #     kline_dic['timestamp'] = dic['timestamp']
    #     kline_dic['open'] = dic['open']
    #     kline_dic['high'] = dic['high']
    #     kline_dic['low'] = dic['low']
    #     kline_dic['close'] = dic['close']
    #     return

    #
    # def init_kline(self):
    #     self.kl1m = self.get_kline('1m', self.symbol, self.kline_num_1m+60, self.start_time_1m, self.kline_num_1m)
    #     self.kl5m = self.get_kline('5m', self.symbol, self.kline_num_5m+20, self.start_time_5m, self.kline_num_5m)
    #     self.kl1h = self.get_kline('1h', self.symbol, self.kline_num_1h+12, self.start_time_1h, self.kline_num_1h)
    #
    #
    # def refresh_kline(self):
    #     pass
