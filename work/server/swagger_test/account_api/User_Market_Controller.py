import json
from datetime import datetime

from send_email.write_email import WriteEmail
from base_api.api_all import api_base


class user_market_controller(api_base):
    def __init__(self, key_dic):
        super().__init__(key_dic)

    def addFavorite(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/favorite/addFavorite'
        url = self.account_root + method
        params = {
            "symbol": "BTCUSDT",
            "type": 1
        }
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        params = json.dumps(params)
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + ': 添加用户交易市场验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name, )
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def deleteFavorite(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "symbol": "BTCUSDT",
            "type": 1
        }
        method = '/favorite/deleteFavorite/{}/{}'.format(params['symbol'], params['type'])
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        url = self.account_root + method
        ret = self.api_call(url, headers, 'DELETE')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + ': 添加用户交易市场验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name, )
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

