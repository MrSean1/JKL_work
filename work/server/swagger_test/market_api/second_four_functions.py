from datetime import datetime
from urllib import parse

import json
from send_email.write_email import WriteEmail
from base_api.api_all import api_base


class second_four_functions(api_base):
    def __init__(self, key_dic):
        super().__init__(key_dic)

    def banner(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/home/other/banner'
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': HOME-002 首页banner信息接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': HOME-002 首页banner信息接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def documents(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/home/other/documents'
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': HOME-003 首页底部文案信息接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': HOME-003 首页底部文案信息接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def notice1(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        params = {
            "current": 1,
            "size": 1
        }
        method = '/notice/{}/{}'.format(params['current'], params['size'])
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': notice1接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': notice1接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def notice2(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        params = {
            "noticeId": 1,
        }
        method = '/notice/{}'.format(params['noticeId'])
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': notice2接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': notice2接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def dealOrder(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/orderManager/dealOrder'
        params = {
            "current": 1,
            "size": 10,
            "symbol": 1,
            "type": 1
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': ORDER-002 成交记录接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': ORDER-002 成交记录接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def entrustOrder(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/orderManager/entrustOrder'
        params = {
            "current": 1,
            "size": 10,
            "symbol": 1,
            "type": 1
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': ORDER-001 委托记录接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': ORDER-001 委托记录接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def otc_account(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "coinName": "string",
        }
        method = '/otc/account/{}'.format(params['coinName'])
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': OUTSIDE-001 C2C账户资产验证通过')
            return now_time + self.ex_name + '交易所' + url + ': OUTSIDE-001 C2C账户资产验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def buy(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/otc/c2c/buy'
        params = {
            "coinId": 1,
            "mum": 1,
            "num": 1
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': OUTSIDE-003 c2c买入接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': OUTSIDE-003 c2c买入接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def buy_record(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/otc/c2c/buy/record'
        params = {
            "current": 1,
            "size": 10,
            "status": 1
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': OUTSIDE-005 c2c买入记录接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': OUTSIDE-005 c2c买入记录接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def sell(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/otc/c2c/sell'
        params = {
            "coinId": 1,
            "mum": 1,
            "num": 1,
            "payPassword": "e10adc3949ba59abbe56e057f20f883e",
            "validateCode": 1111
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': OUTSIDE-004 c2c卖出接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': OUTSIDE-004 c2c卖出接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def sell_record(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/otc/c2c/sell/record'
        params = {
            "current": 1,
            "size": 10,
            "status": 1
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': OUTSIDE-004 c2c卖出记录接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': OUTSIDE-004 c2c卖出记录接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret
