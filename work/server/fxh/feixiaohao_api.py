# 非小号接口检测
import io
import json
import pycurl
import time
from datetime import datetime
from threading import Thread
import certifi

from send_email.write_email import WriteEmail

#  'shadow_zhulin@163.com'
em_user = '295861809@qq.com'
pwd = 'agagwzladccqbhce'
address = ['295861809@qq.com', ]
smtp_server = 'smtp.qq.com'
phone = ['8613120362121', '8618501251795']


class MyThread(Thread):
    def __init__(self, func, args=(), lag=0):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.lag = lag

    def run(self):
        time.sleep(self.lag)
        count = 0
        while count < 1:
            try:
                self.result = self.func(*self.args)
                if self.result is not False:
                    break
                else:
                    raise ValueError
            except Exception:
                time.sleep(1)
                count += 1
                continue

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class fexiaohao_api:
    def __init__(self, key_dic):
        self.ex_name = key_dic
        if self.ex_name == 'BXX':
            pass
        elif self.ex_name == 'TEST':
            pass
        elif self.ex_name == 'HBANK':
            pass
        elif self.ex_name == 'TTEX':
            self.market_root = 'https://www.ttex.pro/v2/o/openapi/allticker'
        elif self.ex_name == 'DAPP':
            pass
        elif self.ex_name == 'COINFLY':
            pass
        elif self.ex_name == 'COINX':
            self.market_root = 'https://coinx.im/v2/o/openapi/allticker'

    def __api_call(self, url, headers, type, params=json.dumps({})):
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        curl.setopt(pycurl.CAINFO, certifi.where())
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
        count_error = 0
        while count_error < 10:
            curl.setopt(pycurl.URL, url)
            try:
                curl.perform()
                ret = iofunc.getvalue().decode('utf-8')
            except Exception as e:
                count_error += 1
                if count_error % 10 == 0:
                    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(e)
                    code = curl.getinfo(pycurl.HTTP_CODE)
                    message = now_time + ': ' + self.ex_name + '交易所 ' + '飞小号接口：' + url + '错误状态码：' + str(
                        code) + '错误信息：' + e + '\n\n'
                    title = '飞小号接口问题总和'
                    print(title, message)
                    WriteEmail(message, title, filename='./email_msg/fxh_api.txt').write()
                time.sleep(1)
                continue
            print(ret)
            try:
                ret = json.loads(ret)
                now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = now_time + ': ' + self.ex_name + "交易所 " + '飞小号接口没有问题'
                print(message)
            except Exception as e:
                print(e)
            return ret

    def call(self):
        headers = ["Content-Type: application/json"]
        ret = self.__api_call(self.market_root, headers, 'GET')
        return ret


class Monitor:
    def __init__(self, monitor_list):
        self.monitor_list = monitor_list

    # 检查市场深度
    def check_market_depth(self):
        t = []
        for i in self.monitor_list:
            api = fexiaohao_api(i)
            t.append(MyThread(api.call, args=()))
        [th.start() for th in t]
        [th.join() for th in t]

    def send_email(self, count):
        email = WriteEmail('', '', filename='./email_msg/fxh_api.txt')
        email.send(count, em_user, pwd, address, smtp_server, '飞小号接口')
        email.send_fxh_sm(phone=phone)
        email.del_email()


fxh_list = [
            'TTEX',
            'COINX',
            ]

m = Monitor(fxh_list)
flag_30m = 0
count = 0
while True:
    m.check_market_depth()
    if flag_30m % 1 == 0:
        m.send_email(count)
    count = (count + 1) % 2
    time.sleep(1800)
    flag_30m += 1
