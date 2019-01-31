import io
import json
import pycurl
import time
from datetime import datetime
from threading import Thread
import certifi

from send_email.write_email import WriteEmail

#  'shadow_zhulin@163.com'
from ex_api.api_bxx import api_bxx

em_user = '295861809@qq.com'
pwd = 'agagwzladccqbhce'
address = ['295861809@qq.com']
smtp_server = 'smtp.qq.com'
phone = ['8613120362121', '8615201479252', '8613910860759']


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
        while count < 10:
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
        if count == 10:
            message = '{}交易所{}交易对'.format(self.keydict[0], self.args[0])
            title = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + self.keydict[
                0] + ': 交易所' + '网络请求问题'
            print(title, message)
            WriteEmail(message, title, filename='./email_msg/market_all_depth.txt').write()

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class bxx_all_depth():
    def __init__(self, key_dic):
        if len(key_dic) == 3:
            self.ex_name = str(key_dic[0])
            self.user_name = str(key_dic[1])
            self.password = str(key_dic[2])
            self.token = ''
        elif len(key_dic) == 2:
            self.ex_name = str(key_dic[0])
            self.token = key_dic[1]
        if self.ex_name == 'BXX':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPa'
            # self.account_root = 'http://47.91.163.110/v2/u'
            # self.market_root = 'http://47.91.163.110/v2/s'
            self.account_root = 'http://service-robot.bxx.com/v2/u'
            self.market_root = 'http://service-robot.bxx.com/v2/s'
        elif self.ex_name == 'TEST':
            self.api_key = '3SHn27c0jLfLtvKaMNZnbWv&AF%HjGONBgtIu9uax@yZG2#wpGRx#lIOCd!4VQlY'
            self.account_root = 'http://47.106.158.72/v2/u'
            self.market_root = 'http://47.106.158.72/v2/s'
        elif self.ex_name == 'HBANK':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPb'
            self.account_root = 'http://47.89.60.31/v2/u'
            self.market_root = 'http://47.89.60.31/v2/s'
        elif self.ex_name == 'TTEX':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPa'
            # self.account_root = 'http://47.91.161.88/v2/u'
            # self.market_root = 'http://47.91.161.88/v2/s'
            self.account_root = 'http://service-robot.ttex.pro/v2/u'
            self.market_root = 'http://service-robot.ttex.pro/v2/s'
        elif self.ex_name == 'DAPP':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPc'
            # self.account_root = 'http://47.52.84.252/v2/u'
            # self.market_root = 'http://47.52.84.252/v2/s'
            self.account_root = 'http://service-robot.dappex.net/v2/u'
            self.market_root = 'http://service-robot.dappex.net/v2/s'
        elif self.ex_name == 'COINFLY':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPd'
            # self.account_root = 'http://47.91.170.40/v2/u'
            # self.market_root = 'http://47.91.170.40/v2/s'
            self.account_root = 'http://service-robot.coinfly.com/v2/u'
            self.market_root = 'http://service-robot.coinfly.com/v2/s'
        elif self.ex_name == 'COINX':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPa'
            # self.account_root = 'http://47.75.149.78/v2/u'
            # self.market_root = 'http://47.75.149.78/v2/s'
            self.account_root = 'http://service-robot.coinx.im/v2/u'
            self.market_root = 'http://service-robot.coinx.im/v2/s'
        elif self.ex_name == 'GT210':
            self.api_key = 'bPf87fUctgHzXxkVDS*42e#rWjq33fNKCaAI@oECRWNzqbITfOLU%UWHNEXu4KPa'
            self.account_root = 'http://service-robot.gt210.net/v2/u'
            self.market_root = 'http://service-robot.gt210.net/v2/s'

    def __sym(self, symbol):
        return symbol[0].upper() + symbol[1].upper()

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
        curl.setopt(pycurl.URL, url)
        try:
            curl.perform()
            ret = iofunc.getvalue().decode('utf-8')
        except Exception as e:
            print(e)
            return False
        # print(ret)
        ret = json.loads(ret)

        return ret, url

    def get_depth(self, symbol):
        # symbol = self.__sym(symbol)
        # if not self.token:
        #     self.get_token()
        method = '/trade/market/depth/' + symbol + '/step0'
        # headers = ["Content-Type: application/json", "Authorization: " + self.token]
        headers = ["Content-Type: application/json"]
        ret = self.__api_call(self.market_root + method, headers, 'GET')
        depth = ret[0]['data_NK_HS-YM']
        depth['bids'] = [[dic['price'], dic['volume']] for dic in depth['bids']]
        depth['asks'] = [[dic['price'], dic['volume']] for dic in depth['asks']]
        # print(depth)
        depth_msg = self.check_price(depth, ret[1], symbol)
        return depth_msg,

    def check_price(self, depth, url, symbol):
        now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print('最低买价' + str(depth['bids'][0][0]))
        # print('最高卖价' + str(depth['asks'][0][0]))
        # 买的最高价 小于 卖的最低价
        if depth['bids'][0][0] < depth['asks'][0][0]:
            print(now_time + ' ' + '交易所：' + self.ex_name + ': 交易对:' + symbol + '最高买价和最低卖价正常')
            return '价格正常'
        elif depth['bids'][0][0] == depth['asks'][0][0]:
            message = now_time + ' ' + '交易所：' + self.ex_name + ': 交易对:' + symbol + '最高买价和最低卖价相等，请查看市场价格是否存在问题'
            title = '全站市场深度价格问题总和'
            WriteEmail(message, title, filename='./email_msg/market_all_depth.txt').write()
            print(message)
            return message
        else:
            message = now_time + ' ' + '交易所：' + self.ex_name + ': 交易对:' + symbol + '最高买价大于最低卖价，请查看市场价格是否存在问题'
            title = '全站市场深度价格问题总和'
            WriteEmail(message, title, filename='./email_msg/market_all_depth.txt').write()
            print(message)
            return message


class Monitor:
    def __init__(self, monitor_list):
        self.monitor_list = monitor_list

    def __sym(self, symbol):
        return symbol[0].upper() + symbol[1].upper()

    # 检查市场深度
    def check_market_depth(self):
        t = []
        for i in self.monitor_list:
            key_dict = [i[0], '', '']
            symbol = self.__sym(i[1])
            api = bxx_all_depth(key_dict)
            t.append(MyThread(api.get_depth, args=(symbol, key_dict,)))
        [th.start() for th in t]
        [th.join() for th in t]

    def send_email(self, count, phone):
        email = WriteEmail('', '', filename='./email_msg/market_all_depth.txt')
        email.send(count, em_user, pwd, address, smtp_server, '全站市场深度价格')
        email.send_depth_all_sm(phone=phone)
        email.del_email()


# ['HBANK', ['BTC', 'USDT']], ['HBANK', ['ETH', 'USDT']], ['HBANK', ['BTM', 'USDT']],
#                 ['HBANK', ['ETH', 'BTC']], ['HBANK', ['BTM', 'BTC']],
#                 ['HBANK', ['BTM', 'ETH']],
# ['COINX', ['DVC', 'USDT']],

monitor_list = [
                ['BXX', ['BTC', 'USDT']],
                ['BXX', ['ETH', 'USDT']],
                ['BXX', ['OMG', 'USDT']],
                ['BXX', ['ZIL', 'USDT']],
                ['BXX', ['NBXX', 'USDT']],
                ['BXX', ['ETH', 'BTC']],
                ['BXX', ['REP', 'BTC']],
                ['BXX', ['AE', 'BTC']],
                ['BXX', ['ICX', 'BTC']],
                ['BXX', ['OMG', 'ETH']],
                ['BXX', ['REP', 'ETH']],
                ['BXX', ['ICX', 'ETH']],
                ['BXX', ['AE', 'ETH']],
                ['BXX', ['LPAY', 'NBXX']],
                ['BXX', ['NBPAY', 'NBXX']],
                ['BXX', ['EPAY11', 'NBXX']],

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

                # ['DAPP', ['BTC', 'USDT']],
                # ['DAPP', ['ETH', 'USDT']],
                # ['DAPP', ['AE', 'USDT']],
                # ['DAPP', ['OMG', 'USDT']],
                # ['DAPP', ['ZRX', 'USDT']],
                # ['DAPP', ['ICX', 'USDT']],
                # ['DAPP', ['BTM', 'USDT']],
                # ['DAPP', ['BAT', 'USDT']],
                # ['DAPP', ['DGD', 'USDT']],
                # ['DAPP', ['ETH', 'BTC']],
                # ['DAPP', ['REP', 'BTC']],
                # ['DAPP', ['DGD', 'ETH']],
                # ['DAPP', ['ICX', 'ETH']],
                # ['DAPP', ['ZRX', 'ETH']],
                # ['DAPP', ['REP', 'ETH']],

                ['COINX', ['BTC', 'USDT']],
                ['COINX', ['ETH', 'USDT']],
                ['COINX', ['EOS', 'USDT']],
                ['COINX', ['LTC', 'USDT']],
                ['COINX', ['DASH', 'USDT']],
                ['COINX', ['QTUM', 'USDT']],
                ['COINX', ['DOGE', 'USDT']],
                ['COINX', ['XMX', 'USDT']],
                ['COINX', ['HPS', 'USDT']],
                ['COINX', ['HPY', 'USDT']],
                ['COINX', ['HC', 'USDT']],
                ['COINX', ['ETH', 'BTC']],
                ['COINX', ['EOS', 'BTC']],
                ['COINX', ['LTC', 'BTC']],
                ['COINX', ['DASH', 'BTC']],
                ['COINX', ['QTUM', 'BTC']],
                ['COINX', ['ZIL', 'BTC']],
                ['COINX', ['AE', 'BTC']],
                ['COINX', ['CTXC', 'BTC']],
                ['COINX', ['NAS', 'BTC']],
                ['COINX', ['HPS', 'BTC']],
                # ['COINX', ['COTO', 'USDT']],
                ['COINX', ['BTM', 'USDT']],
                ['COINX', ['GNT', 'USDT']],
                ['COINX', ['SNT', 'USDT']],
                ['COINX', ['IOST', 'USDT']],

                # ['GT210', ['BTC', 'USDT']],
                # ['GT210', ['ETH', 'USDT']],
                # ['GT210', ['EOS', 'USDT']],
                # ['GT210', ['XRP', 'USDT']],
                # ['GT210', ['LTC', 'USDT']],
                # ['GT210', ['TRX', 'USDT']],
                # ['GT210', ['ADA', 'USDT']],
                # ['GT210', ['BTM', 'USDT']],
                # ['GT210', ['ONT', 'USDT']],
                # ['GT210', ['NEO', 'USDT']],
                ]

m = Monitor(monitor_list)
flag_30m = 0
count = 0
while True:
    m.check_market_depth()
    if flag_30m % 1 == 0:
        m.send_email(count, phone)
    count = (count + 1) % 6
    time.sleep(600)
    flag_30m += 1
