import json
from datetime import datetime

from send_email.write_email import WriteEmail
from base_api.api_all import api_base


class user_bank_controller(api_base):
    def __init__(self, key_dic):
        super().__init__(key_dic)

    # /v3/cards 绑卡列表    接口通了  返回状态码 {"errcode":-1,"errmsg":"系统异常"}
    def cards(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/v3/cards'
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + ': 绑卡列表接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def bank(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/v3/cards/bank'
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + ': OUTSIDE-002 C2C个人银行卡接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def bind(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/v3/cards/bind'
        params = {
            "bank": "string",
            "bankCard": "string",
            "id": 0,
            "payPassword": "string",
            "realName": "string",
            "remark": "string"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '： 添加银行卡接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret