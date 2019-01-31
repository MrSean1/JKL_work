import io
import json
import pycurl
import time
from datetime import datetime

import certifi

from ex_api.api_bxx import api_bxx

from send_email.write_email import WriteEmail


class bxx_kline_30(api_bxx):
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

    def check_kline(self, symbol, lineType='30min'):
        # symbol = self.__sym(symbol)
        method = '/trade/market/kline/' + symbol + '/' + lineType
        headers = ["Content-Type: application/json"]
        ret = self.__api_call(self.market_root + method, headers, 'GET')
        kline = eval(ret['data_NK_HS-YM'])[-3:-1]
        result = self.check_k(kline, symbol)
        print(result)
        return result

    def check_k(self, kline, symbol):
        k_first = kline[0]
        k_second = kline[1]
        # 第二根
        # 跌
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        a = int(time.time())
        if a - (k_second[0] / 1000) < 4500:
            if k_first[1] > k_first[-2]:
                fall = k_first[1] / k_first[-2] - 1
                if 0.1 <= fall < 0.3:
                    message = '{}交易所{}币种跌幅过大，已超过10%，请查看k线确认是否出现问题'.format(self.ex_name, symbol)
                    title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，k线问题'
                    WriteEmail(message, title).write()
                    return message, title
                elif fall >= 0.3:
                    message = '{}交易所{}币种跌幅过大，已超过30%，请查看k线确认是否出现问题'.format(self.ex_name, symbol)
                    title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，k线问题'
                    WriteEmail(message, title, filename='./email_msg/price_iss.txt').write()
                    return message, title
                else:
                    message = now_time + ' {}交易所{}30分钟跌幅正常'.format(self.ex_name, symbol)
                    return message
            # 涨
            if k_first[1] <= k_first[-2]:
                rise = k_first[-2] / k_first[1] - 1
                if 0.1 <= rise < 0.3:
                    message = '{}交易所{}币种涨幅过大，已超过10%，请查看k线确认是否出现问题'.format(self.ex_name, symbol)
                    title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，k线问题'
                    WriteEmail(message, title).write()
                    return message, title
                elif rise >= 0.3:
                    message = '{}交易所{}币种涨幅过大，已超过30%，请查看k线确认是否出现问题'.format(self.ex_name, symbol)
                    title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，k线问题'
                    WriteEmail(message, title, filename='./email_msg/price_iss.txt').write()
                    return message, title
                else:
                    message = now_time + ' {}交易所{}30分钟涨幅正常'.format(self.ex_name, symbol)
                    return message
            if k_first[-1] == 0:
                message = '{}交易所{}币种k线在30分钟内没有成交量，请查看机器人是否出现问题'.format(self.ex_name, symbol)
                title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，k线问题'
                WriteEmail(message, title).write()
                return message, title
            if k_first[1] == k_first[2] == k_first[3] == k_first[4]:
                message = '{}交易所{}币种k线在30分钟内开高低收都相等没有波动，请查看机器人是否出现问题'.format(self.ex_name, symbol)
                title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，k线问题'
                WriteEmail(message, title).write()
                return message, title
            # 最新得一根
            # 跌
            if k_second[1] >= k_second[-2]:
                fall = k_second[1] / k_second[-2] - 1
                if fall >= 0.3:
                    message = '{}交易所{}币种跌幅过大，已超过30%，请查看k线确认是否出现问题'.format(self.ex_name, symbol)
                    title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，k线问题'
                    WriteEmail(message, title, filename='./email_msg/price_iss.txt').write()
                    return message, title
                else:
                    message = now_time + ' {}交易所{}30分钟跌幅正常'.format(self.ex_name, symbol)
                    return message
            # 涨
            if k_second[1] < k_second[-2]:
                rise = k_second[-2] / k_second[1] - 1
                if rise >= 0.3:
                    message = '{}交易所{}币种涨幅过大，已超过30%，请查看k线确认是否出现问题'.format(self.ex_name, symbol)
                    title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，k线问题'
                    WriteEmail(message, title, filename='./email_msg/price_iss.txt').write()
                    return message, title
                else:
                    message = now_time + ' {}交易所{}30分钟涨幅正常'.format(self.ex_name, symbol)
                    return message
        else:
            timeStamp = k_first[1] / 1000
            timeArray = time.localtime(timeStamp)
            styletime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            message = '{}交易所{}交易对，以无法获取当前K线，请确认是网站问题，还是交易对被撤下，获取30分钟k线的最早时间节点为{}'.format(self.ex_name, symbol, styletime)
            title = now_time + ' ' + self.ex_name + '交易所' + symbol + '，交易对被撤或服务器问题'
            WriteEmail(message, title).write()
            return message, title
# symbol = ['BTC', 'USDT']
# bxx = ['BXX', '', '']
