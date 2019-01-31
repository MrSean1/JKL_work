from ex_api.exchange import Exchange, MyThread, isPause, get_USDT_CNY, isExPause
import time
import random
import sys
from config_bxx import get_config
from accounts_bxx import account_info

# !!!initiate parameter

ex_non_mine = []

ex_name = sys.argv[1]
sym = sys.argv[2]
sym_base = sys.argv[3]
# sym = 'BTC'
# sym_base = 'USDT'
symbol = [sym, sym_base]
if sym == 'HB' and sym_base == 'USDT':
    symbol = ['BTC', 'USDT']
USD_CNY = 6.3
USDT_CNY = 6.6

symbol_config = get_config(ex_name, symbol)

sym0 = symbol_config['sym0']
sym_base0 = symbol_config['sym_base0']
exchange_base = symbol_config['exchange_base']
base_order_quantity_scale = symbol_config['base_order_quantity_scale']
base_order_range_scale = symbol_config['base_order_range_scale']
account_fee = symbol_config['account_fee']
avg_sym_btc = symbol_config['avg_sym_btc']
symbol_price_decimal = symbol_config['symbol_price_decimal']
symbol_quant_decimal = symbol_config['symbol_quant_decimal']
symbol_quant_int_decimal = symbol_config['symbol_quant_int_decimal']
min_quant = symbol_config['min_quant']
msym = symbol_config['msym']
order_gap = symbol_config['order_gap']
quantity_scale_buy = symbol_config['quantity_scale_buy']
quantity_scale_sell = symbol_config['quantity_scale_sell']
total_quant_per_day_btc = symbol_config['total_quant_per_day_btc']
bxx_key = account_info[ex_name][symbol[1]][symbol[0]]

symbol0 = [sym0, sym_base0]

sdecimal = [symbol_price_decimal, symbol_quant_decimal]

binance_key = ['YDEaP2pwwNnTgxnVvTykElck9tTL3ODt5pYZGZWANPPCqIoRAK02Ma003susa9nZ',
               'LFhd1YzD9Hby4SVlXFqL0sxhXg3I30tjJsjCH8u90KGkIClp9PMLs1Ockr4dGQDd']

# zb_key = ['a', 'b']

fcoin_key = ['948f765b4bd7427c9c02d09fc42e6c8d', '3bfa3d0fd9534a8fb0f55884d0460021']

huobi_key = ['23d16220-7b1883cc-dc468afc-6865d',
             'fe31646f-78407147-ec119bc8-cbdab']

coinw_key = ['a048a77f-b61e-49c5-b459-3ad171242959', 'ZTMF18573EILZLUIBB4RARLDOM3YCFOAYPXZ']

# !!!initiate

ex_bin = Exchange('binance', binance_key)

# ex_zb = Exchange('zb', zb_key)

ex_huobi = Exchange('huobi', huobi_key)

ex_hadax = Exchange('hadax', huobi_key)

ex_bxx = [Exchange('bxx', key) for key in bxx_key]
ex_bxx1 = ex_bxx[-2]
ex_bxx2 = ex_bxx[-1]
if sym == 'HB':
    symbol = ['HB', 'USDT']
    ex_bxx1 = ex_bxx[-1]
    sdecimal = [6, 4]
if sym == 'DVC':
    ex_bxx1 = ex_bxx[20]

ex_cw = Exchange('coinw', coinw_key)


# USD_CNY = 6.33


def get_standard_depth(depth_dict):
    return float(depth_dict['bids'][0][0]), float(depth_dict['asks'][0][0])


def get_standard_price(depth_dict):
    return (float(depth_dict['bids'][0][0]) + float(depth_dict['asks'][0][0])) / 2


def plog():
    print('no thread')


class fake_quantity:
    def __init__(self, api, api_volume, symbol, volume_symbol, base_quantity, decimal):
        self.__count = 0
        # self.order_id_list = []
        # self.active_order_id_buy = []
        # self.active_order_id_sell = []
        # self.__thread_cancel_buy = []
        # self.__thread_cancel_sell = []
        # self.__thread_order_buy = MyThread(plog)
        # self.__thread_order_sell = MyThread(plog)
        self.__api = api
        self.__api_volume = api_volume
        self.__symbol = symbol
        self.__volume_symbol = volume_symbol
        # self.__wave = wave * range_scale
        self.__fake_price = 0
        self.__fake_quantity = 0
        # base quantity comes from two arguments
        self.__base_quantity = base_quantity
        # self.refresh_flag = False
        # self.__refresh_rate = refresh_rate
        self.__price_decimal = decimal[0]
        self.__quant_decimal = decimal[1]
        self.otime = time.time()
        self.__rtime = time.time()
        self.__volume_1m = 1
        self.__volume_1d = 1440
        self.__lower_bound = 0
        self.__higher_bound = 0

    def refresh_volume(self):
        if self.__count % 100 == 0:
            try:
                temp_1m = self.__api_volume.get_volume(self.__volume_symbol, '1m', 2)
                if temp_1m:
                    v1m = float(temp_1m[0])
                else:
                    raise ValueError
            except Exception:
                print('refresh volume failed')
            else:
                self.__volume_1m = v1m
        if self.__count % 1000 == 0:
            try:
                temp_1d = self.__api_volume.get_volume(self.__volume_symbol, '1d', 2)
                if temp_1d:
                    v1d = float(temp_1d[0])
                else:
                    raise ValueError
            except Exception:
                print('refresh volume failed')
            else:
                self.__volume_1d = v1d
        self.__count += 1

    def trade(self, standard_bid, standard_ask, bid_quantity, ask_quantity):
        # calculate fake price and quantity when there is space
        if round(standard_ask - standard_bid, self.__price_decimal) >= 2 * 10 ** -self.__price_decimal:
            # refresh bound
            rb_flag = False
            if time.time() - self.__rtime > 360:
                rb_flag = True
            elif standard_ask < self.__higher_bound or standard_bid > self.__lower_bound:
                rb_flag = True
            if rb_flag:
                self.__rtime = time.time()
                decimal_number = int(round((standard_ask - standard_bid) / 10 ** -self.__price_decimal, 0))
                mid = round((standard_bid + standard_ask) / 2, self.__price_decimal)
                while True:
                    if decimal_number < 10:
                        lower = random.randint(0, decimal_number - 2)
                        higher = random.randint(lower + 2, decimal_number)
                        if 2 <= higher - lower <= max(2, int(round(decimal_number / 2.0, 0))):
                            break
                    else:
                        if standard_ask - standard_bid < 0.06 * standard_bid:
                            lower = random.randint(0, int(decimal_number / 3.0 * 2))
                            higher = random.randint(lower + 2, decimal_number)
                            if max(2, int(round(decimal_number / 4.0, 0))) <= higher - lower <= int(
                                    round(decimal_number / 2.0, 0)):
                                break
                        else:
                            lower = random.randint(int(decimal_number / 5 * 2), int(decimal_number / 2) - 1)
                            higher = random.randint(int(decimal_number / 2) + 1, int(decimal_number / 5 * 3))
                            break
                self.__lower_bound = round(standard_bid + lower * 10 ** -self.__price_decimal, self.__price_decimal)
                self.__higher_bound = round(standard_bid + higher * 10 ** -self.__price_decimal, self.__price_decimal)
                print('refresh bound for 6 minutes', self.__lower_bound, 'to', self.__higher_bound)
            tp = random.randint(0, 1)
            self.__fake_price = round(
                random.uniform(self.__lower_bound + 10 ** -self.__price_decimal,
                               self.__higher_bound - 10 ** -self.__price_decimal),
                self.__price_decimal)
            last_time = time.time() - self.otime
            last_time = min(last_time, 20)
            # self.__fake_quantity = round(
            #     last_time * self.__base_quantity * (60.0 * 24 * min(self.__volume_1m / self.__volume_1d, 1 / 144)),
            #     self.__quant_decimal)
            self.otime = time.time()
            if tp == 0:
                # self.__fake_price = round(standard_bid + random.randint(1, 5) * 10 ** -self.__price_decimal,
                #                           self.__price_decimal)
                # self.__fake_price = standard_bid
                self.__fake_quantity = \
                    round(random.uniform(1.0 / 4 * bid_quantity,
                                         bid_quantity * max(min(1.5, 1 * 1440 * self.__volume_1m / self.__volume_1d),
                                                            0.8)),
                          self.__quant_decimal)
                fside = 'buy'
            else:
                # self.__fake_price = round(standard_ask - random.randint(1, 2) * 10 ** -self.__price_decimal,
                #                           self.__price_decimal)
                # self.__fake_price = standard_ask
                self.__fake_quantity = \
                    round(random.uniform(1.0 / 4 * ask_quantity,
                                         ask_quantity * max(min(1.5, 1 * 1440 * self.__volume_1m / self.__volume_1d),
                                                            0.8)),
                          self.__quant_decimal)
                fside = 'sell'
            # self.__fake_price = round((standard_ask + standard_bid) / 2, self.__price_decimal)
            # if sym == 'EMBC':
            #     self.__fake_quantity = round(self.__fake_quantity * 4, symbol_quant_decimal)
            #     self.__fake_quantity = random.randint(10, 1000)
            #     if random.randint(1, 10) == 1:
            #         self.__fake_quantity = round(self.__fake_quantity * 10, symbol_quant_decimal)
            # if sym == 'APV':
            #     self.__fake_quantity = round(self.__fake_quantity * 4, symbol_quant_decimal)
            #     self.__fake_quantity = random.randint(10, 200)
            #     # if random.randint(1, 10) == 1:
            #     #     self.__fake_quantity = round(self.__fake_quantity * 10, symbol_quant_decimal)
            if random.randint(0, 1) == 1:
                self.__fake_quantity = round(self.__fake_quantity, symbol_quant_int_decimal)
            self.__fake_quantity = min(self.__fake_quantity,
                                       round(0.01 * base_order_quantity_scale * 10, self.__quant_decimal))
            self.__fake_quantity = max(self.__fake_quantity, min_quant)
            self.__fake_price = round(self.__fake_price, self.__price_decimal)
            # if ex_name == 'BXX' and sym != 'EMBC':
            #     self.__fake_quantity = round(self.__fake_quantity * 15, self.__quant_decimal)
            if ex_name == 'TTEX':
                time.sleep(5 + random.uniform(0, 10))
                self.__fake_quantity = round(self.__fake_quantity * 15, self.__quant_decimal)
            if ex_name == 'COINFLY':
                time.sleep(10 + random.uniform(0, 20))
                self.__fake_quantity = round(self.__fake_quantity * 4, self.__quant_decimal)
            if ex_name == 'BXX':
                time.sleep(10 + random.uniform(0, 20))
                self.__fake_quantity = round(self.__fake_quantity / 3, self.__quant_decimal)
            # if ex_name == 'HBANK':
            #     time.sleep(40 + random.uniform(0, 20))
            #     self.__fake_quantity = round(self.__fake_quantity / 10, self.__quant_decimal)
            if ex_name == 'COINX':
                time.sleep(10 + random.uniform(0, 20))
                self.__fake_quantity = round(self.__fake_quantity * 10, self.__quant_decimal)
            if ex_name == 'DAPP':
                time.sleep(10 + random.uniform(0, 20))
                self.__fake_quantity = round(self.__fake_quantity * 4, self.__quant_decimal)
            if ex_name == 'GT210':
                time.sleep(10 + random.uniform(0, 20))
                self.__fake_quantity = round(self.__fake_quantity * 4, self.__quant_decimal)
            if sym == 'DVC':
                time.sleep(60 + random.uniform(0, 30))
                self.__fake_quantity = round(self.__fake_quantity / 30, symbol_quant_decimal)
                if self.__fake_quantity < 100:
                    self.__fake_quantity = round(random.randint(100, 300))
            if sym == 'HB':
                a = random.randint(1, 5)
                if a <= 4:
                    self.__fake_quantity = round(random.randint(100, 1000))
                else:
                    self.__fake_quantity = round(random.randint(1000, 5000))
                if random.randint(1, 3) == 3:
                    self.__fake_quantity = round(self.__fake_quantity, -1)
            if sym == 'COTO':
                a = random.randint(1, 5)
                if a <= 4:
                    self.__fake_quantity = round(random.randint(10, 100))
                else:
                    self.__fake_quantity = round(random.randint(100, 5000))
                if random.randint(1, 3) == 3:
                    self.__fake_quantity = round(self.__fake_quantity, -1)
            print(self.__fake_price, self.__fake_quantity)
            if fside == 'buy':
                if ex_name not in ex_non_mine:
                    ex_buy.api.self_order(self.__symbol, 'buy', self.__fake_quantity, self.__fake_price)
                else:
                    ex_buy.api.order(self.__symbol, 'buy', self.__fake_quantity, self.__fake_price)
                    ex_sell.api.order(self.__symbol, 'sell', self.__fake_quantity, self.__fake_price)
            else:
                if ex_name not in ex_non_mine:
                    ex_buy.api.self_order(self.__symbol, 'sell', self.__fake_quantity, self.__fake_price)
                else:
                    ex_sell.api.order(self.__symbol, 'sell', self.__fake_quantity, self.__fake_price)
                    ex_buy.api.order(self.__symbol, 'buy', self.__fake_quantity, self.__fake_price)
            # while True:
            #     try:
            #         ret = ex_bxx1.api.order(self.__symbol, fside, self.__fake_quantity, self.__fake_price)
            #         if ret is not False:
            #             break
            #         else:
            #             raise ValueError
            #     except Exception:
            #         continue
            # time.sleep(0.3)
            # while True:
            #     try:
            #         ret = ex_bxx2.api.order(self.__symbol, gside, self.__fake_quantity, self.__fake_price)
            #         if ret is not False:
            #             break
            #         else:
            #             raise ValueError
            #     except Exception:
            #         continue
            # oid = ret
            # while True:
            #     try:
            #         ret = ex_cx1.api.cancel(str(oid), self.__symbol)
            #         if ret is not False:
            #             break
            #         else:
            #             raise ValueError
            #     except Exception:
            #         continue
            # while True:
            #     try:
            #         ret = self.__api.self_order(self.__symbol, self.__fake_quantity, self.__fake_price)
            #         if ret is not False:
            #             break
            #         else:
            #             raise ValueError
            #     except Exception:
            #         continue
            self.__count += 1
            # print(self.__count)


test_quantity = fake_quantity(ex_bxx1.api, ex_bin.api, symbol, [msym, 'USDT'],
                              total_quant_per_day_btc / avg_sym_btc / 86400.0, sdecimal)

# ex_cx1.cancel_all()
# ex_cx2.cancel_all()

st = time.time()

id_buy = ''
id_sell = ''

num = 0
ex_buy = ex_bxx1
ex_sell = ex_bxx1

while True:
    isP = isExPause(ex_name)
    if isP == 1:
        time.sleep(20)
        continue
    else:
        time.sleep(0 + random.uniform(0, 3))
    # if num % 50 == 0:
    #     balance1 = [dic['balanceAmount'] for dic in ex_bxx1.api.get_account() if dic['coinName'] == sym][0]
    #     balance2 = [dic['balanceAmount'] for dic in ex_bxx2.api.get_account() if dic['coinName'] == sym][0]
    #     if balance1 > balance2:
    #         ex_buy = ex_bxx2
    #         ex_sell = ex_bxx1
    #     else:
    #         ex_buy = ex_bxx1
    #         ex_sell = ex_bxx2
    num += 1
    print('No', num, 'time:', round(time.time() - test_quantity.otime, 3))
    print(time.asctime())
    try:
        test_quantity.refresh_volume()
    except Exception as e:
        print('refresh volume failed')
    if num % 10 == 0:
        thp_cancel = list()
        thp_cancel.append(MyThread(ex_bxx1.cancel_all_bxx, args=(symbol,)))
        # thp_cancel.append(MyThread(ex_bxx2.cancel_all_bxx, args=(symbol,)))
        [th.start() for th in thp_cancel]
    # ex_bxx1.cancel_all_bxx(symbol)
    # ex_bxx2.cancel_all_bxx(symbol)
    try:
        dep = ex_bxx1.api.get_depth(symbol)
        bid_1 = 0
        bid_1_q = 0
        if len(dep['bids']) > 0:
            bid_1 = dep['bids'][0][0]
            bid_1_q = dep['bids'][0][1]
        ask_1 = dep['asks'][0][0]
        ask_1_q = dep['asks'][0][1]
        bid_1 = max(ask_1 * 0.7, bid_1)
        # depth = tempcurl(url_symbol)
        # bid_1 = depth['bids'][0][0]
        # bid_1_q = depth['bids'][0][1]
        # ask_1 = depth['asks'][0][0]
        # ask_1_q = depth['asks'][0][1]
        test_quantity.trade(float(bid_1), float(ask_1), float(bid_1_q), float(ask_1_q))
    except Exception as e:
        print(e)
