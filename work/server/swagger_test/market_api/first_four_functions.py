from datetime import datetime
from urllib import parse

import json
from send_email.write_email import WriteEmail
from base_api.api_all import api_base


class first_four_functions(api_base):
    def __init__(self, key_dic):
        super().__init__(key_dic)

    def accounts(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/account/accounts'
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 资金账户列表接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 资金账户列表接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def allCoin(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/coin/allCoin'
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 获取数字货币基础币列表接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 获取数字货币基础币列表接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def baseCoin(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/coin/baseCoin'
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 获取数字货币基础币列表接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 获取数字货币基础币列表接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def wallet(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/coin/trade/wallet'
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': COIN-001 获取钱包币信息接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': COIN-001 获取钱包币信息接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def recharge(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "coinId": "1010101010101010102",
        }
        method = '/recharge/address/{}'.format(params['coinId'])
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': COIN-RECHARGE-001 获取充值地址(过时,请使用币种名称)接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': COIN-RECHARGE-001 获取充值地址(过时,请使用币种名称)接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def recharge_record(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "coinId": "1010101010101010102",
            "current": 1,
            "size": 1
        }
        method = '/recharge/record?'
        params_dict = parse.urlencode(params)
        url = self.market_root + method + params_dict
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': COIN-RECHARGE-002 获取充值记录接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': COIN-RECHARGE-002 获取充值记录接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def withdraw(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/withdraw'
        params = {
            "address": "13hQVEstgo4iPQZv9C7VELnLWF7UWtF4Q3",
            "addressId": 123,
            "amount": 100,
            "coinId": 1,
            "payPassword": "******",
            "verifyCode": 123456
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': COIN-WITHDRAW-001 申请提币接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': COIN-WITHDRAW-001 申请提币接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def user_record(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "coinId": "1010101010101010102",
            "current": 1,
            "size": 1
        }
        method = '/withdraw/record?'
        params_dict = parse.urlencode(params)
        url = self.market_root + method + params_dict
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 用户提现接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 用户提现接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

