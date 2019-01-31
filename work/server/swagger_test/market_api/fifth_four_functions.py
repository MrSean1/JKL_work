from datetime import datetime
from urllib import parse

import json
from send_email.write_email import WriteEmail
from base_api.api_all import api_base


class fifth_four_functions(api_base):
    def __init__(self, key_dic):
        super().__init__(key_dic)

    # def addWorkIssue(self):
    #     if not self.token:
    #         self.get_token()
    #     method = '/workIssue/addWorkIssue'
    #     params = {
    #         "question": 1
    #     }
    #     params = json.dumps(params)
    #     url = self.market_root + method
    #     headers = ["Content-Type: application/json", "Authorization: " + self.token]
    #     ret = self.api_call(url, headers, 'POST', params)
    #     if ret[0] == 200:
    #         # print(self.ex_name + '交易所' + url + ': 添加工单接口验证通过')
    #         return self.ex_name + '交易所' + url + ': 添加工单接口验证通过'
    #     else:
    #         message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
    #         title = '{}接口请求问题总和'.format(self.ex_name)
    #         WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
    #         return ret

    def getWorkIssue(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        params = {
            "current": 1,
            'size': 1
        }
        method = '/workIssue/issueList/{}/{}'.format(params["current"], params['size'])
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 获取工单列表验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 获取工单列表接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def getpool(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/mine/pool'
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 查看矿池接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 查看矿池接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def setpool(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/mine/pool'
        params = {
            "description": "string",
            "name": "string"
        }
        params = json.dumps(params)
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 创建矿池接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 创建矿池接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def pool_data(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/mine/data_NK_HS-YM'
        url = self.market_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': mine--002 查询挖矿信息接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': mine--002 查询挖矿信息接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def reward_info(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/reward/info'
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 可解冻邀请奖励接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 可解冻邀请奖励接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    # def reward_invite(self):
    #     params = {
    #         "userId": 1,
    #     }
    #     method = '/reward/invite/{}'.format(params['userId'])
    #     params = json.dumps(params)
    #     url = self.market_root + method
    #     headers = ["Content-Type: application/json"]
    #     ret = self.api_call(url, headers, 'POST', params)
    #     if ret[0] == 200:
    #         print(url + ': inviteReward接口验证通过')
    #         return url + ': inviteReward接口验证通过'
    #     else:
    #         message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
    #         title = '{}接口请求问题总和'.format(self.ex_name)
    #         WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
    #     return ret
    #
    # def reward_register(self):
    #     if not self.token:
    #         self.get_token()
    #     params = {
    #         "userId": 1,
    #     }
    #     method = '/reward/register/'
    #     params = json.dumps(params)
    #     url = self.market_root + method
    #     headers = ["Content-Type: application/json", "Authorization: " + self.token]
    #     ret = self.api_call(url, headers, 'POST', params)
    #     if ret[0] == 200:
    #         print(url + ': registerReward接口验证通过')
    #         return url + ': registerReward接口验证通过'
    #     else:
    #         message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
    #         title = '{}接口请求问题总和'.format(self.ex_name)
    #         WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
    #     return ret

    def reward_unfreeze(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/reward/unfreeze'
        url = self.market_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST')
        if ret[0] == 200:
            # print(self.ex_name + '交易所' + url + ': 解冻邀请奖励接口验证通过')
            return now_time + self.ex_name + '交易所' + url + ': 解冻邀请奖励接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret
