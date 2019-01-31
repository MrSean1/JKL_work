from datetime import datetime
from urllib import parse

import json
from send_email.write_email import WriteEmail
from base_api.api_all import api_base


class fourth_four_functions(api_base):
    def __init__(self, key_dic):
        super().__init__(key_dic)

    def trading_area(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/trading_area'
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': tradingArea接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': tradingArea接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def trading_area_list(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/trading_area/list'
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': trading_area_list接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': trading_area_list接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def preupload(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/preupload'
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': preupload接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': preupload接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def upload_callback(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/upload/callback'
        params = {
            "payload": "string",
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': callback接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': callback接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def user_account(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "symbol": "btcusdt",
        }
        method = '/user/account/asset/{}'.format(params["symbol"])
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': ACCOUNT-001 币币交易用户交易对账户资产接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': ACCOUNT-001 币币交易用户交易对账户资产接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def wallet_address(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/wallet/address'
        params = {
            "address": "1CK6KHY6MHgYvmRQ4PAafKYDrg1ejbH1cE",
            "coinId": 11111,
            "name": "比特币冷钱包",
            "payPassword": "******"
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': WITHDRAW-ADDRESS-001 添加提币地址接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': WITHDRAW-ADDRESS-001 添加提币地址接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def deleteAddress(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/wallet/deleteAddress'
        params = {
            "addressId": 1,
            "payPassword": 1
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 删除钱包地址接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 删除钱包地址接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def getCoinAddress(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "coinId": 1,
        }
        method = '/user/wallet/getCoinAddress/{}'.format(params["coinId"])
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 用户的提币地址接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 用户的提币地址接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret
