import sys
from threading import Thread
import time
from rest_kline import rest_kline
# from bitmex.websocket_bitmex import BitMEXWebsocket
from bitmex_websocket import BitMEXWebsocket
from count_kline import count_kline

# symbol = 'XBTUSD'
# key = ['6jOxgwVwabghW2RzkFJ5XoWI', 'X2Gfkbd3RFiXzDtQ5ei8B9zJF8RwjW8Ey1tyzMZ22XwBLlkz']


class kline_realtime:
    def __init__(self, symbol, key, kl1m_length=120, kl5m_length=60, kl1h_length=24):
        self.symbol = symbol
        self.api_key = key[0]
        self.secret_key = key[1]
        # 按交易所websocket使用方法初始化ws
        self.__ws = BitMEXWebsocket(endpoint="wss://www.bitmex.com/realtime", symbol=self.symbol, api_key=key[0],
                                    api_secret=key[1])
        self.kl1m = []
        self.__kl1m_length = kl1m_length
        self.kl5m = []
        self.__kl5m_length = kl5m_length
        self.kl1h = []
        self.__kl1h_length = kl1h_length
        # 按当前时间使用rest api初始化各k线
        self.__init_kline()
        # 使用websocket实时更新各k线
        th_refresh = Thread(target=self.__refresh_kline, args=())
        th_refresh.start()

    def __rest_kline(self, period, kline_length):
        """
        根据period: 1m, 5m, 1h等，通过rest api获取k线
        返回k线列表，由旧到新，[[时间，开，高，低，收，量],...]
        函数中需要考虑到当前时间和k线列表长度限制
        """
        data_kline = rest_kline(period, self.symbol, kline_length).get_kline()
        return data_kline

    def __init_kline(self):
        """使用rest_kline初始化各k线"""
        self.kl1m = self.__rest_kline("1m", self.__kl1m_length)
        # print(self.kl1m)
        # print('###################################################################################')
        self.kl5m = self.__rest_kline("5m", self.__kl5m_length)
        # print(self.kl5m)
        # print('###################################################################################')
        self.kl1h = self.__rest_kline("1h", self.__kl1h_length)
        # print(self.kl1h)
        # print('###################################################################################')

    def __ws_kline(self, period, last_complete_time, last_price):
        """
        使用websocket，计算某个时间点之后的实时k线
        返回k线列表，由旧到新，[[时间，开，高，低，收，量],...]
        """
        # Thread.is_alive(th_refresh)
        data = self.__ws.data['trade']
        if period == '5m':
            data = self.kl1m
        elif period == '1h':
            data = self.kl5m
        sum_kline = count_kline(period, last_complete_time, data, last_price)
        new_kline = sum_kline.count()
        # if period == '1m':
        #     print(new_kline)
        return new_kline

    def __refresh_kline(self):
        """
        通过ws_kline获取最新的若干根k线，更新原k线列表
        更新方法，去掉原列表中最新的一根和最老的若干根
        """
        while True:
            # 1m
            start_1m = self.kl1m[-2][0]  # 原列表中除了最新的一根（可能不完整）外，最后一根完整k线的更新时间
            start_1m_price = self.kl1m[-2][-2]
            temp_kl1m = self.__ws_kline("1m", start_1m, start_1m_price)
            self.kl1m = self.kl1m[len(temp_kl1m) - 1:-1]  # 去掉最后一根，再去掉前面的若干根
            self.kl1m = self.kl1m + temp_kl1m
            # 5m
            start_5m = self.kl5m[-2][0]
            start_5m_price = self.kl5m[-2][-2]
            temp_kl5m = self.__ws_kline("5m", start_5m, start_5m_price)
            self.kl5m = self.kl5m[len(temp_kl5m) - 1:-1]
            self.kl5m = self.kl5m + temp_kl5m
            # 1h
            start_1h = self.kl1h[-2][0]
            start_1h_price = self.kl1h[-2][-2]
            temp_kl1h = self.__ws_kline("1h", start_1h, start_1h_price)
            self.kl1h = self.kl1h[len(temp_kl1h) - 1:-1]
            self.kl1h = self.kl1h + temp_kl1h
            time.sleep(1)