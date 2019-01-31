import io
import json
import pycurl
import time
from datetime import datetime

import certifi
from ex_api.api_bxx import api_bxx

from send_email.write_email import WriteEmail


class bxx_kline_1(api_bxx):
    def __sym(self, symbol):
        return symbol[0].upper() + symbol[1].upper()

    def __api_call(self, url, headers, type, params=json.dumps({})):
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        # curl.setopt(pycurl.CAINFO, certifi.where())
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
            if 'errcode' in ret.keys() and str(ret['errcode']) == '40001':
                print('token expired')
                self.get_token()
                headers[1] = "Authorization: " + self.token
                ret = self.__api_call(url, headers, type, params)
        except Exception as e:
            print(e)
            return False
        return ret

    def check_kline(self, symbol, lineType='1min', num=30):
        # symbol = self.__sym(symbol)
        method = '/trade/market/kline/' + symbol + '/' + lineType
        headers = ["Content-Type: application/json"]
        ret = self.__api_call(self.market_root + method, headers, 'GET')
        kline = eval(ret['data_NK_HS-YM'])[-num - 1:-1]
        ret = self.check_k(kline, symbol, num)
        print(ret)
        return ret

    def check_k(self, kline, symbol, num):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        a = int(time.time())
        if a - (int(kline[-1][0]) / 1000) < 1800:
            for i in range(len(kline)):
                if i + 1 == len(kline):
                    break
                elif kline[i][1] == kline[i][2] == kline[i][3] == kline[i][4] and kline[i+1][1] == kline[i+1][2] == kline[i+1][3] == kline[i+1][4]:
                    message_1 = '{}交易所{}{}分钟之内存在出现两根相邻得K线开高低收都相等得情况，请查看k线确认是否出现问题'.format(self.ex_name, symbol, num)
                    title_1 = now_time + ' ' + self.ex_name + '交易所' + symbol + ' k线问题'
                    WriteEmail(message_1, title_1).write()
                    break
                elif kline[i][1] == kline[i][2] == kline[i][3] == kline[i][4] and kline[i][-1] == 0:
                    message = '{}交易所{}{}分钟之内存在开高低收都相等且交易量为0的k线，请查看k线确认是否出现问题'.format(self.ex_name, symbol, num)
                    title = now_time + self.ex_name + '交易所' + symbol + ' k线问题'
                    WriteEmail(message, title).write()
                    return message, title
            if kline[-1][1] == kline[-1][2] == kline[-1][3] == kline[-1][4] and kline[-1][-1] == 0:
                message = '{}交易所{}{}分钟之内存在开高低收都相等且交易量为0的k线，请查看k线确认是否出现问题'.format(self.ex_name, symbol, num)
                title = now_time + self.ex_name + '交易所' + symbol + ' k线问题'
                WriteEmail(message, title).write()
                return message, title
            return now_time + ' {}交易所{}{}分钟之内一切正常'.format(self.ex_name, symbol, num)
        else:
            # 将时间戳转化为 能读懂的时间
            timeStamp = kline[-1][0] / 1000
            timeArray = time.localtime(timeStamp)
            styletime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            message = '{}交易所{}交易对，以无法获取当前K线，请确认是网站问题，还是交易对被撤下，获取1分钟k线的最早时间节点为{}'.format(self.ex_name, symbol, styletime)
            title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，交易对被撤或服务器问题'
            WriteEmail(message, title).write()
            return message, title

# symbol = ['BTC', 'USDT']
# a = ['COINX', '', '']
