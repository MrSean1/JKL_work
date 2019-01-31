import time
import random
import pycurl
import hmac
import hashlib
import io
import certifi
import json
import urllib.parse
import pandas as pd


class kline():
    def __init__(self, symbol, fileName):
        self.account_root = "https://www.bitmex.com/api/v1"
        self.symbol = symbol
        self.fileName = fileName

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

    # 'XBTUSD'
    def get_kline(self, binSize='5m', startTime='2018-1-28'):
        if self.symbol == 'XBTZ18':
            startTime = '2018-7-2'
        elif self.symbol == 'XBTU18':
            startTime = '2018-3-31'
        number = 1
        while True:
            params = {
                "binSize": binSize,
                "partial": True,
                "symbol": self.symbol,
                'startTime': startTime,
                "count": 750
            }
            params = urllib.parse.urlencode(params)
            method = '/trade/bucketed?' + params
            headers = ["Content-Type: application/json"]
            ret = self.__api_call(self.account_root + method, headers, 'GET')

            if not ret:
                break
            print(type(ret))
            self.write_data(ret, self.fileName, number)
            startTime = self.get_starttime(ret)
            number += 1

    def get_starttime(self, ret):
        str_time = ret[-1]['timestamp']
        time_list = str_time.split(':')
        if int(time_list[1]) < 55:
            startTime = time_list[0] + ':' + str(int(time_list[1]) + 5) + ':' + time_list[2]
        elif int(time_list[0][-2:]) < 9:
            startTime =time_list[0][:-2] + '0' + str(int(time_list[0][-2:])+1) + ':' + str('00') + ':' + time_list[2]
        elif 9 <= int(time_list[0][-2:]) < 23:
            startTime =time_list[0][:-2] + str(int(time_list[0][-2:])+1) + ':' + str('00') + ':' + time_list[2]
        else:
            startTime = time_list[0][:-2] + '00' + ':' + str('00') + ':' + time_list[2]
        return startTime

    def write_data(self, ret, fileName, number):
        print('开始写')
        dataf = []
        for i in ret:
            time_list = i['timestamp'].split('.')
            time_list2 = time_list[0].split('T')
            book = [time_list2[0], time_list2[1], i['open'], i['high'], i['low'], i['close'], ]
            dataf.append(book)
        data = pd.DataFrame(dataf)
        # 写入csv文件,'a+'是追加模式
        try:
            if number == 1:
                csv_headers = ['data_NK_HS-YM', 'time', 'open', 'high', 'low', 'close']
                data.to_csv(fileName, header=csv_headers, index=False, mode='a+', encoding='utf-8')
            else:
                data.to_csv(fileName, header=False, index=False, mode='a', encoding='utf-8')

        except UnicodeEncodeError:
            print("编码错误, 该数据无法写到文件中, 直接忽略该数据")
        print('写完一个')


a = [['XBTUSD', '永续.csv'], ['XBTZ18', '12月期货.csv'], ['XBTU18', '9月期货.csv'], ['XBTM18', '6月期货.csv'], ['XBTH18', '3月期货.csv']]
for i in a:
    kline(i[0], i[1]).get_kline()