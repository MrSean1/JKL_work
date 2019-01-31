import time
import sys
from datetime import datetime
from threading import Thread

from check_api.bxx_kline_1 import bxx_kline_1
from check_api.bxx_kline_30 import bxx_kline_30
from check_api.bxx_kline_1h import bxx_kline_1h

# '568327240@qq.com'
from send_email.write_email import WriteEmail

em_user = '295861809@qq.com'
pwd = 'agagwzladccqbhce'
address = ['295861809@qq.com', '568327240@qq.com']
smtp_server = 'smtp.qq.com'
phone_java = ['8613120362121']
phone_python = ['8613120362121', '15201479252']


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
            message = '{}交易所{}'.format(self.keydict[0], self.args[0])
            title = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ': ' + self.keydict[
                0] + ': 交易所' + '网络请求问题'
            print(title, message)
            WriteEmail(message, title).write()

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


class Monitor:
    def __init__(self, monitor_list):
        self.monitor_list = monitor_list

    def __sym(self, symbol):
        return symbol[0].upper() + symbol[1].upper()

    # 检查一分钟请求数据
    def check_kline_1min(self):
        t = []
        for i in self.monitor_list:
            if self.__sym(i[1]) != 'TRXBTC':
                key_dict = [i[0], '', '']
                symbol = self.__sym(i[1])
                api = bxx_kline_1(key_dict)
                t.append(MyThread(api.check_kline, args=(symbol, key_dict,)))
        [th.start() for th in t]
        [th.join() for th in t]
        # result = [th.get_result() for th in t]
        # 5
        # monitor_list[5][0]

    # 检查30分钟请求数据
    def check_kline_30min(self):
        l = []
        for i in self.monitor_list:
            key_dict = [i[0], '', '']
            symbol = self.__sym(i[1])
            api = bxx_kline_30(key_dict)
            l.append(MyThread(api.check_kline, args=(symbol, key_dict,)))
        [th.start() for th in l]
        [th.join() for th in l]

    # 检查1小时得请求数据
    def check_kline_1h(self):
        l = []
        for i in self.monitor_list:
            key_dict = [i[0], '', '']
            symbol = self.__sym(i[1])
            api = bxx_kline_1h(key_dict)
            l.append(MyThread(api.check_kline, args=(symbol, key_dict,)))
        [th.start() for th in l]
        [th.join() for th in l]

    def send_all_email(self, count):
        email = WriteEmail('', '')
        email.send(count, em_user, pwd, address, smtp_server, 'k线')
        email.send_sm(phone_java)
        email.del_email()

    def send_all_sm(self, count):
        email = WriteEmail('', '', filename='./email_msg/price_iss.txt')
        email.send(count, em_user, pwd, address, smtp_server, '价格涨幅问题')
        email.send_sm_price(phone_python)
        email.del_email()


# monitor_list = [['BXX', ['BTC', 'USDT']], ['BXX', ['ETH', 'USDT']], ['BXX', ['TRX', 'USDT']],
#                 ['BXX', ['OMG', 'USDT']], ['BXX', ['ZRX', 'USDT']], ['BXX', ['ZIL', 'USDT']],
#                 ['BXX', ['AE', 'USDT']], ['BXX', ['ICX', 'USDT']], ['BXX', ['REP', 'USDT']],
#                 ['BXX', ['ETH', 'BTC']], ['BXX', ['AE', 'BTC']], ['BXX', ['ICX', 'BTC']], ['BXX', ['REP', 'BTC']],
#                 ['BXX', ['EMBC', 'ETH']], ['BXX', ['OMG', 'ETH']], ['BXX', ['AE', 'ETH']], ['BXX', ['ICX', 'ETH']],
#                 ['BXX', ['REP', 'ETH']], ]
# 撤销 暂时不监控的交易对
# ['TTEX', ['TRX', 'BTC']],  ['DAPP', ['MKR', 'USDT']], ['DAPP', ['MKR', 'ETH']],
# ['BXX', ['AE', 'USDT']], ['BXX', ['ICX', 'USDT']],  ['BXX', ['NBXX', 'ETH']], ['BXX', ['NBXX', 'BTC']],
# 下掉机器人的交易对
# ['BXX', ['EMBC', 'ETH']],['COINX', ['GATC', 'USDT']],
# ['HBANK', ['BTC', 'USDT']], ['HBANK', ['ETH', 'USDT']], ['HBANK', ['BTM', 'USDT']],
#                 ['HBANK', ['ETH', 'BTC']], ['HBANK', ['BTM', 'BTC']],
#                 ['HBANK', ['BTM', 'ETH']],
#  ['COINX', ['DVC', 'USDT']],
# ['COINFLY', ['BTC', 'USDT']], ['COINFLY', ['ETH', 'USDT']],
# ['COINFLY', ['ETH', 'BTC']], ['COINFLY', ['AE', 'BTC']],
# ['COINFLY', ['OMG', 'BTC']], ['COINFLY', ['ZRX', 'BTC']], ['COINFLY', ['ICX', 'BTC']],
# ['COINFLY', ['BTM', 'BTC']], ['COINFLY', ['BAT', 'BTC']],
# ['COINFLY', ['OMG', 'ETH']], ['COINFLY', ['AE', 'ETH']],
# ['COINFLY', ['ZRX', 'ETH']], ['COINFLY', ['ICX', 'ETH']], ['COINFLY', ['BTM', 'ETH']],
# ['COINFLY', ['BAT', 'ETH']],
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
    m.check_kline_1min()
    if flag_30m % 1 == 0:
        m.check_kline_30min()
    if flag_30m % 2 == 0:
        m.check_kline_1h()
    if flag_30m % 1 == 0:
        m.send_all_email(count)
        m.send_all_sm(count)
        pass
    count = (count + 1) % 2
    time.sleep(1800)
    flag_30m += 1
