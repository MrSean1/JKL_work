from datetime import datetime
from urllib import parse

import json
from send_email.write_email import WriteEmail
from base_api.api_all import api_base


class third_four_functions(api_base):
    def __init__(self, key_dic):
        super().__init__(key_dic)

    # 验证码接口
    def sendTo(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/api/v1/dm/sendTo'
        params = {
            'countryCode': "string",
            'phone': "1",
            'templateCode': "REGISTER_VERIFY",
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 发送验证码接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 发送验证码接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    # def verify(self):
    #     if not self.token:
    #         self.get_token()
    #     method = '/api/v1/dm/verify'
    #     params = {
    #         "code": "string",
    #         "countryCode": "string",
    #         "email": "string",
    #         "phone": "string",
    #         "templateCode": "string"
    #     }
    #     params = json.dumps(params)
    #     url = self.market_root + method
    #     headers = ["Content-Type: application/json", "Authorization: " + self.token]
    #     ret = self.api_call(url, headers, 'POST', params)
    #     if ret[0] == 200:
    #         print(self.ex_name + '交易所' + url + ': verify接口验证通过')
    #         return self.ex_name + '交易所' + url + ': verify接口验证通过'
    #     else:
    #         message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
    #         title = '{}接口请求问题总和'.format(self.ex_name)
    #         WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
    #     return ret

    # def sendTo_sms(self):
    #     method = '/sms/sendTo'
    #     params = {
    #         "countryCode": "string",
    #         "email": "string",
    #         "mobile": "string",
    #         "templateCode": 100001,
    #         "templateParam": {}
    #     }
    #     params = json.dumps(params)
    #     url = self.market_root + method
    #     headers = ["Content-Type: application/json"]
    #     ret = self.api_call(url, headers, 'POST', params)
    #     if ret[0] == 200:
    #         print(self.ex_name + '交易所' + url + ': 发送短信接口验证通过')
    #         return self.ex_name + '交易所' + url + ': 发送短信接口验证通过'
    #     else:
    #         message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
    #         title = '{}接口请求问题总和'.format(self.ex_name)
    #         WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
    #     return ret

    def trade_market(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/trade/market'
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': tradeMarketList接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': tradeMarketList接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def home_market(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        params = {
            "areaId": 'area',
        }
        method = '/trade/market/{}'.format(params['areaId'])
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 首页市场信息接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 首页市场信息接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def market_depth(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        params = {
            "mergeType": 'string',
            "symbo": 'string',
        }
        method = '/trade/market/depth/{}/{}'.format(params['symbo'], params['mergeType'])
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 币币交易市场深度接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 币币交易市场深度接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def favorite(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/trade/market/favorite'
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 个人收藏交易市场信息接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 个人收藏交易市场信息接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def getBySymbol(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        params = {
            "symbo": 'string',
        }
        method = '/trade/market/getBySymbol/{}'.format(params['symbo'])
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 币币交易市场深度接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 币币交易市场深度接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def kline(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        params = {
            "symbo": 'string',
            'lintType': ''
        }
        time_list = ['5sec', '1min', '5min', '15min', '30min', '1hour', '2hour', '4hour', '6hour', '12hour', '1day',
                     '1week', '1mon', '1year']
        for time in time_list:
            params['lintType'] = time
            method = '/trade/market/kline/{}/{}'.format(params['symbo'], params['lintType'])
            url = self.market_root + method
            headers = ["Content-Type: application/json"]
            ret = self.api_call(url, headers, 'GET')
            if ret[0] == 200:
                # print(self.ex_name + '交易所' + url + ': 币币交易K线数据接口验证通过')
                return now_time + self.ex_name + '交易所' + url + ': 币币交易市场深度接口验证通过'
            else:
                message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
                title = now_time + '{}接口请求问题总和'.format(self.ex_name)
                WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
                return ret

    def realtime_ticker(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        params = {
            "symbo": 'string',
        }
        method = '/trade/market/ticker/{}'.format(params['symbo'])
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 币币交易实时行情接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 币币交易实时行情接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def new_trades(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        params = {
            "symbo": 'string',
        }
        method = '/trade/market/ticker/{}'.format(params['symbo'])
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 币币交易最新成交列表接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 币币交易最新成交列表接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def orderid_to_entrust(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "orderId": '1',
        }
        method = '/trade/order/entrusts/{}'.format(params['orderId'])
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 根据订单号查询委托订单接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 根据订单号查询委托订单接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def unfinish_orderid_to_entrust(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "current": '1',
            "size": '1',
            "symbol": 'string',
        }
        method = '/trade/order/entrusts/{}/{}/{}'.format(params['symbol'], params['current'], params['size'])
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': ORDER-003 币币交易未完成委托订单接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': ORDER-003 币币交易未完成委托订单接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def history_orderid_to_entrust(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "current": '1',
            "size": '1',
            "symbol": 'string',
        }
        method = '/trade/order/history/{}/{}/{}'.format(params['symbol'], params['current'], params['size'])
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': ORDER-004 币币交易历史委托订单接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': ORDER-004 币币交易历史委托订单接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret
