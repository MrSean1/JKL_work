from ex_api.api_all import api
from threading import Thread
import time
import pycurl
import io
import certifi
import json


class MyThread(Thread):
    def __init__(self, func, args=(), lag=0):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.lag = lag

    def run(self):
        time.sleep(self.lag)
        while True:
            try:
                self.result = self.func(*self.args)
                if self.result is not False:
                    break
                else:
                    raise ValueError
            except Exception:
                time.sleep(1)
                continue

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def api_must_success(func, args=()):
    while True:
        try:
            ret = func(*args)
            if ret is not False:
                return ret
            else:
                raise ValueError
        except Exception as e:
            print(e)


def get_USDT_CNY():
    while True:
        try:
            with open('./USDT_rate.txt', 'r') as f:
                rate = f.read()
            break
        except Exception:
            continue
    return float(rate)


def isPause():
    while True:
        try:
            with open('./pause.txt', 'r') as f:
                isP = f.read()
            if int(isP) in [0, 1]:
                break
            else:
                raise ValueError
        except Exception:
            continue
    return int(isP)


def isExPause(ex_name):
    while True:
        try:
            with open('./pause_ex.txt', 'r') as f:
                res = f.read().split('\n')
            isPd = {item.split()[0]: item.split()[1] for item in res if item != ''}
            isP = int(isPd[ex_name])
            if int(isP) in [0, 1]:
                break
            else:
                raise ValueError
        except Exception:
            continue
    return isP


def tempcurl(url, headers, type, params=""):
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
    curl.setopt(pycurl.TIMEOUT, 15)
    print(url)
    curl.setopt(pycurl.URL, url)
    curl.perform()
    ret = iofunc.getvalue().decode('utf-8')
    # print(ret)
    ret = json.loads(ret)
    print(ret)
    return ret


class Exchange:
    def __init__(self, exchange, key, fee=0.001):
        self.api = api(exchange, key)
        self.trade_fee = fee
        self.trade_symbol = []
        self.trade_pair = []
        self.trade_pair_indirect = []
        self.account_info = {}
        self.depth = {pair[0] + '_' + pair[1]: {} for pair in self.trade_pair}
        self.depth_indirect = {pair[0] + '_' + pair[1] + '-' + pair[2]: {} for pair in self.trade_pair_indirect}

    def set_trade_symbol_and_pair(self, trade_symbol=[], trade_pair=[],
                                  trade_pair_indirect=[]):
        self.trade_symbol = trade_symbol
        self.trade_pair = trade_pair
        self.trade_pair_indirect = trade_pair_indirect

    def refresh_account(self):
        self.account_info = self.api.get_account()

    def refresh_depth(self):
        try:
            if self.trade_pair:
                t = []
                depth = {}
                for pair in self.trade_pair:
                    t.append(MyThread(self.api.get_depth, args=(pair,)))
                [th.start() for th in t]
                [th.join() for th in t]
                for i in range(len(t)):
                    pair = self.trade_pair[i]
                    if t[i].get_result():
                        depth[pair[0] + '_' + pair[1]] = t[i].get_result()
                    else:
                        raise ValueError
                self.depth = depth
        except Exception as e:
            print(e)
            print('unable to refresh depth at', time.asctime())

        try:
            if self.trade_pair_indirect:
                t = {}
                depth_indirect = {}
                for pair in self.trade_pair_indirect:
                    t[pair[0] + '_' + pair[2]] = MyThread(self.api.get_depth, args=([pair[0]] + [pair[2]],))
                    t[pair[1] + '_' + pair[2]] = MyThread(self.api.get_depth, args=([pair[1]] + [pair[2]],))
                for th in t.keys():
                    t[th].start()
                for th in t.keys():
                    t[th].join()
                for pair in self.trade_pair_indirect:
                    if t[pair[0] + '_' + pair[2]].get_result() and t[pair[1] + '_' + pair[2]].get_result():
                        depth_indirect[pair[0] + '_' + pair[1] + '-' + pair[2]] = [
                            t[pair[0] + '_' + pair[2]].get_result(), t[pair[1] + '_' + pair[2]].get_result()]
                    else:
                        raise ValueError
                self.depth_indirect = depth_indirect
        except Exception as e:
            print(e)
            print('unable to refresh depth at', time.asctime())

    def cancel_all(self, symbol=''):
        if symbol:
            coin = symbol[0]
            order_id_list = []
            my_depth = self.api.get_my_depth(symbol)
            if coin:
                for order_dict in my_depth:
                    if order_dict['product_code'] == coin:
                        order_id_list.append(order_dict['order_id'])
            else:
                order_id_list = [order_dict['order_id'] for order_dict in my_depth]
            t = []
            for order_id in order_id_list:
                t.append(MyThread(self.api.cancel, args=(order_id, symbol)))
            [th.start() for th in t]
            [th.join() for th in t]
        else:
            order_id_list1 = [order_dict['order_id'] for order_dict in self.api.get_my_depth(['', 'BTC'])]
            order_id_list2 = [order_dict['order_id'] for order_dict in self.api.get_my_depth(['', 'USD'])]
            t = []
            for order_id in order_id_list1:
                t.append(MyThread(self.api.cancel, args=(order_id, ['', 'BTC'])))
            for order_id in order_id_list2:
                t.append(MyThread(self.api.cancel, args=(order_id, ['', 'USD'])))
            [th.start() for th in t]
            [th.join() for th in t]

    def cancel_all_bxx(self, symbol):
        if symbol:
            coin = symbol[0]
            order_id_list = []
            my_depth = self.api.get_my_depth(symbol)
            if coin:
                for order_dict in my_depth:
                    order_id_list.append(order_dict['orderId'])
            else:
                order_id_list = [order_dict['order_id'] for order_dict in my_depth]
            t = []
            for order_id in order_id_list:
                t.append(MyThread(self.api.cancel, args=(order_id,)))
            [th.start() for th in t]
            [th.join() for th in t]
