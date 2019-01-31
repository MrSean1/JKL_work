from datetime import datetime
from urllib import parse

import json
from send_email.write_email import WriteEmail
from base_api.api_all import api_base


class user_controller(api_base):
    def __init__(self, key_dic):
        super().__init__(key_dic)

    def apikey(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/apikey'
        url = self.account_root + method
        params = {"validateCode": "string"}
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        params = json.dumps(params)
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '/user/apikey接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name, )
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def getApikey(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/apikey/get'
        url = self.account_root + method
        params = {"validateCode": "string"}
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        params = json.dumps(params)
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '/user/apikey/get接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def user_account(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/authAccount'
        url = self.account_root + method
        params = {
            "geetest_challenge": "string",
            "geetest_seccode": "string",
            "geetest_validate": "string",
            "idCard": "44030419920919207x",
            "idCardType": 1,
            "imageUrl": "string",
            "realName": "Doug Lea"
        }
        params = json.dumps(params)
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '实名认证接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def authUser(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/authUser'
        url = self.account_root + method
        params = [
            "string"
        ]
        params = json.dumps(params)
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return self.ex_name + '交易所' + url + '高级认证接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def checkEmail(self, email='wht190421@163.com'):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/user/checkEmail' + '?email=' + str(email)
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: "]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '邮箱注册验证接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def checkTel(self, countryCode='+86', mobile='13120362121'):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/user/checkTel?'
        headers = ["Content-Type: application/json", "Authorization: "]
        params = {
            'countryCode': countryCode,
            'mobile': mobile,
        }
        params_dict = parse.urlencode(params)
        url = self.account_root + method + params_dict
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '手机号注册验证接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def checkUname(self, username='MrSean'):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/user/checkUname?'
        params = {
            'username': username,
        }
        params_dict = parse.urlencode(params)
        url = self.account_root + method + params_dict
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '用户名注册验证接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

        # 关闭GA验证

    def cancel(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/ga/cancel?'
        params = {
            'code': 0,
        }
        params_dict = parse.urlencode(params)
        url = self.account_root + method + params_dict
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '关闭GA验证接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def generate(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/ga/generate?'
        params = {
            "data_NK_HS-YM": {},
            "errcode": 0,
            "errmsg": "string"
        }
        params_dict = parse.urlencode(params)
        url = self.account_root + method + params_dict
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + ': GA秘钥生成接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def verify(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/ga/verify?'
        params = {
            "code": 0,
            "secret": "string"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + ': GA验证并绑定接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def userinfo(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/info'
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '用户信息接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name )
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def invitation(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/invitation'
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + 'ACCOUNT-005 邀请列表接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def language(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/user/lang/'
        params = {
            "lang": '语言-zh en',
        }
        params_dict = parse.urlencode(params)
        url = self.account_root + method + params_dict
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'GET')
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '切换语言接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def register(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        method = '/user/register?'
        params = {
            "countryCode": "string",
            "email": "wht190421@163.com",
            "geetest_challenge": "string",
            "geetest_seccode": "string",
            "geetest_validate": "string",
            "invitionCode": "string",
            "mobile": "13120362121",
            "password": "string",
            "userName": "string",
            "validateCode": "string"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json"]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' +  url + '首页注册信息接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def setPassword(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/setPassword?'
        params = {
            "countryCode": "string",
            "email": "string",
            "mobile": "string",
            "password": "string",
            "validateCode": "string"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '忘记密码接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def setPayPassword(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/setPayPassword?'
        params = {
            "payPassword": "string",
            "validateCode": "string"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '设置资金密码接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def updateEmail(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/updateEmail'
        params = {
            "newEmail": "string",
            "oldValidateCode": "string",
            "validateCode": "string"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '： ACCOUNT-004 修改邮箱接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def updateLoginPassword(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/updateLoginPassword'
        params = {
            "newpassword": "string",
            "oldpassword": "string",
            "validateCode": "string"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '： ACCOUNT-004 修改登录密码接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    def updatePayPassword(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/updatePayPassword'
        params = {
            "newpassword": "string",
            "oldpassword": "string",
            "validateCode": "string"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '： ACCOUNT-006 修改资金密码接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret

    # 修改手机号接口有问题
    # def updatePhone(self):
    #     if not self.token:
    #         self.get_token()
    #     method = '/user/updatePhone'
    #     params = {
    #         "countryCode": "string",
    #         "newMobilePhone": "string",
    #         "oldValidateCode": "string",
    #         "validateCode": "string"
    #     }
    #     params = json.dumps(params)
    #     url = self.account_root + method
    #     print(self.token)
    #     headers = ["Content-Type: application/json", "Authorization: " + self.token]
    #     ret = self.api_call(url, headers, 'POST', params)
    #     if ret[0] == 200:
    #         print(url + '： ACCOUNT-003 修改手机号接口验证通过')
    #         return url + '： ACCOUNT-003 修改手机号接口验证通过'
    #     else:
    #         message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
    #         title = '{}接口请求问题总和'.format(self.ex_name)
    #         WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
    #     return ret

    def userBase(self):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
        if not self.token:
            self.get_token()
        method = '/user/userBase'
        params = {
            "email": "qiang.ins@gmail.com",
            "payPassword": "qiang",
            "username": "qiang"
        }
        params = json.dumps(params)
        url = self.account_root + method
        headers = ["Content-Type: application/json", "Authorization: " + self.token]
        ret = self.api_call(url, headers, 'POST', params)
        if ret[0] == 200:
            return now_time + self.ex_name + '交易所' + url + '： ACCOUNT-006 修改资金密码接口验证通过'
        else:
            message = '{}交易所，接口：{}, 出现错误码：'.format(self.ex_name, url) + ret[1]
            title = now_time + '{}接口请求问题总和'.format(self.ex_name)
            WriteEmail(message, title, filename='./email_msg/warn_api.txt').write()
            return ret
