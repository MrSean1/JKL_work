# *_*coding:utf-8 *_*
import datetime
import sys
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

symbol = sys.argv[1]
type_time = sys.argv[2]
filename = sys.argv[3]


class JP255_data():
    def __init__(self, symbol, type, filename):
        if symbol == 'JP255':
            self.symbol = '8859'
            self.baseurl = 'https://tvc4.forexpros.com/410ca7504fc4957fc290ed92c61d31a7/1541594797/6/6/28/history?'
        if symbol == 'DOWjONES':
            self.symbol = '8873'
            self.baseurl = 'https://tvc4.forexpros.com/6162fbf74f8bca464820c19b9dea9b6b/1541767911/6/6/28/history?'
        if symbol == 'HS':
            self.symbol = '179'
            self.baseurl = 'https://tvc4.forexpros.com/f7ee1096f48897b66f2cd5d0823f0f51/1541768725/6/6/28/history?'
        if symbol == 'SZ':
            self.symbol = '40820'
            self.baseurl = 'https://tvc4.forexpros.com/455a70a7989a8e9dbc6f800dab9e0512/1541768992/6/6/28/history?'
        # self.base_time = start_date
        # self.start_date = int(time.mktime(self.strtime_to_timedatetime(self.base_time).timetuple()))
        self.last_date = int(time.time())
        self.start_data = self.last_date - 2400
        self.filename = filename
        self.type = type

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
        except Exception as e:
            print(e)
            return False
        return ret

    def strtime_to_timedatetime(self, time_str):
        '''
        :param time_str: bitmex的K线时间
        :return: datetime类型时间
        '''
        timestamp = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        return timestamp

    def get_data(self):
        number = 1
        while True:
            # last_time = int(
            #     time.mktime(
            #         (self.strtime_to_timedatetime(self.base_time) + datetime.timedelta(seconds=400 * number)).timetuple()))
            params = {
                'symbol': self.symbol,
                'resolution': self.type,
                'from': self.start_data,
                'to': self.last_date,
            }
            params = urllib.parse.urlencode(params)
            headers = ["Content-Type: application/json", "Authorization: "]
            ret = self.__api_call(self.baseurl + params, headers, 'GET')
            if ret['s'] == 'ok':
                self.write_data(ret, self.filename, number)
                self.last_date = self.start_data
                self.start_data = self.last_date - 40*int(self.type)*60
            elif 'nextTime' in ret:
                self.last_date = ret['nextTime']
                self.start_data = self.last_date - 40*int(self.type)*60
            else:
                print('提示信息是：' + ret['s'] + str(self.last_date))
                break
            number += 1

        print('全都写完了')

    def write_data(self, ret, fileName, number):
        print('开始写')
        # dataf = []
        # for i in range(len(ret['t'])):
        #     data_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ret['t'][i])).split(' ')
        #     data_NK_HS-YM = data_time[0]
        #     d_time = data_time[1]
        #     open = ret['o'][i]
        #     high = ret['h'][i]
        #     low = ret['l'][i]
        #     close = ret['c'][i]
        #     book = [data_NK_HS-YM, d_time, open, high, low, close]
        #     dataf.append(book)
        dataf = [
            [self.times_to_strtime(ret['t'][i])[0], self.times_to_strtime(ret['t'][i])[1], ret['o'][i], ret['h'][i],
             ret['l'][i], ret['c'][i]]
            for i in range(len(ret['t']) - 1, -1, -1)]
        data = pd.DataFrame(dataf)
        # 写入csv文件,'a+'是追加模式
        try:
            if number == 1:
                csv_headers = ['data_NK_HS-YM', 'time', 'open', 'high', 'low', 'close']
                data.to_csv(fileName, header=csv_headers, index=False, mode='a+', encoding='utf-8')
            else:
                data.to_csv(fileName, header=False, index=False, mode='a', encoding='utf-8')
            print('写完一个')
        except UnicodeEncodeError:
            print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

    def times_to_strtime(self, times):
        strtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(times)).split(' ')
        return strtime


a = JP255_data(symbol, type_time, filename)
a.get_data()
