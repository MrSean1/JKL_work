from datetime import datetime
from urllib import parse

import json
from send_email.write_email import WriteEmail
from base_api.api_all import api_base


class login_controller(api_base):
    def __init__(self, key_dic):
        super().__init__(key_dic)

    def access_token(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/cgi-bin/token?'
        params = {
            "access_key": 'string',
            "secret": 'string',
        }
        params_dict = parse.urlencode(params)
        url = self.account_root + method + params_dict
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '获取access_token（机器人专用）接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def login(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/login'
        params = {
            "countryCode": "+86",
            "ga_code": 0,
            "geetest_challenge": "string",
            "geetest_seccode": "string",
            "geetest_validate": "string",
            "password": "e10adc3949ba59abbe56e057f20f883e",
            "type": 1,
            "username": "qiang"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '： 用户登录接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def refreshToken(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/refreshToken?'
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + ': 刷新密钥接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def history(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/login/history'
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + ': 登录历史接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret