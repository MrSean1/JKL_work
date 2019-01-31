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
address = ['295861809@qq.com', '568327240@qq.com']
smtp_server = 'smtp.qq.com'
phone = ['8613120362121', ]


class MyThread(Thread):
    def __init__(self, func, args=(), lag=0):
        super(MyThread, self).__init__()
        self.func = func
        self.args = (args[0],)
        self.lag = lag
        self.keydict = args[1]

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


class bxx_depth:
    def __init__(self, key_dic):
        self.ex_name = key_dic
        if self.ex_name == 'BXX':
            self.market_root = 'http://service-robot.bxx.com/v2/s'
        elif self.ex_name == 'TEST':
            self.market_root = 'http://47.106.158.72/v2/s'
        elif self.ex_name == 'HBANK':
            self.market_root = 'https://service.hbank.pro/v2/s'
        elif self.ex_name == 'TTEX':
            self.market_root = 'https://www.ttex.pro/v2/o'
        elif self.ex_name == 'DAPP':
            self.market_root = 'https://service.dappex.net/v2/s'
        elif self.ex_name == 'COINFLY':
            self.market_root = 'http://service-robot.coinfly.com/v2/s'

    def __sym(self, symbol):
        return symbol[0].lower() + "_" + symbol[1].lower()

    def __api_call(self, url, headers, type, symbol, params=json.dumps({})):
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
                    message = now_time + ': ' + self.ex_name + '交易所 ' + '市场深度接口：' + url + '错误状态码：' + str(
                        code) + '错误信息：' + e + '\n\n'
                    title = '市场深度接口问题总和'
                    print(title, message)
                    WriteEmail(message, title, filename='./email_msg/market_depth.txt').write()
                time.sleep(1)
                continue
            # print(ret)
            try:
                ret = json.loads(ret)
                now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                message = now_time + ': ' + self.ex_name + "交易所 " + symbol + '交易对，' + '市场深度接口没有问题'
                print(message)
            except Exception as e:
                print(e)
            return ret

    def get_depth(self, symbol):
        method = '/aicoin/depth?symbol=' + symbol + '&size=10'
        headers = ["Content-Type: application/json"]
        ret = self.__api_call(self.market_root + method, headers, 'GET', symbol)
        return ret


class Monitor:
    def __init__(self, monitor_list):
        self.monitor_list = monitor_list

    def __sym(self, symbol):
        return symbol[0].lower() + '_' + symbol[1].lower()

    # 检查市场深度
    def check_market_depth(self):
        t = []
        for i in self.monitor_list:
            key_dict = i[0]
            symbol = self.__sym(i[1])
            api = bxx_depth(key_dict)
            t.append(MyThread(api.get_depth, args=(symbol, key_dict,)))
        [th.start() for th in t]
        [th.join() for th in t]

    def send_email(self, count):
        email = WriteEmail('', '', filename='./email_msg/market_depth.txt')
        email.send(count, em_user, pwd, address, smtp_server, '市场深度接口')
        email.send_fxh_sm(phone=phone)
        email.del_email()


monitor_list = [
                ['TTEX', ['BTC', 'USDT']],
                ['TTEX', ['ETH', 'USDT']],
                ['TTEX', ['BTM', 'USDT']],
                ['TTEX', ['REP', 'USDT']],
                ['TTEX', ['ETH', 'BTC']],
                ['TTEX', ['OMG', 'BTC']],
                ['TTEX', ['AE', 'BTC']],
                ['TTEX', ['BTM', 'BTC']],
                ['TTEX', ['ZRX', 'BTC']],
                ['TTEX', ['ZIL', 'BTC']],
                ['TTEX', ['BAT', 'BTC']],
                ['TTEX', ['ICX', 'BTC']],
                ['TTEX', ['REP', 'BTC']],
                ['TTEX', ['WTC', 'BTC']],
                ['TTEX', ['GNT', 'BTC']],
                ['TTEX', ['IOST', 'BTC']],
                ['TTEX', ['SNT', 'BTC']],
                ['TTEX', ['LINK', 'BTC']],
                ['TTEX', ['ELF', 'BTC']],
                ['TTEX', ['QASH', 'BTC']],
                ['TTEX', ['CMT', 'BTC']],
                ['TTEX', ['POLY', 'BTC']],
                ['TTEX', ['MANA', 'BTC']],
                ['TTEX', ['PAY', 'BTC']],
                ['TTEX', ['POWR', 'BTC']],
                ['TTEX', ['GVT', 'BTC']],
                ]

m = Monitor(monitor_list)
flag_30m = 0
count = 0
while True:
    m.check_market_depth()
    if flag_30m % 1 == 0:
        m.send_email(count)
    count = (count + 1) % 2
    time.sleep(1800)
    flag_30m += 1
