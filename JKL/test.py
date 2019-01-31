from ex_api.exchange import Exchange, MyThread, isPause, get_USDT_CNY, isExPause
import time
import random
import sys

# from config_bxx import get_config
# from accounts_bxx import account_info
# from price import *

# !!!initiate parameter
account_info = dict()
account_info['TTEX'] = {
    'BTC': {
        'POWR': [],
    },
}
for i in range(5000, 7000):
    account_info['TTEX']['BTC']['POWR'].append(['TTEX', str(12012340001 + i), '1234Rty77899x']),

fake_coin = ['LPAY', 'EPAY11', 'NBPAY', 'DUH', 'TTGS', 'PTIT', 'FGBL', 'LCOC', 'ICWF', 'ZVX', 'TUOD', 'JLO', 'NCBS']

# key = ['BXX', '13224453501', 'aa800820']
# key = ['BXX','12012340036','1234Rty77899x']
# key = ['COINX', '15141021502', '1234Rty77899x']
# key = ['COINX', '15543707268', 'aa800820']
ex_name = sys.argv[1]
sym = sys.argv[2]
sym_base = sys.argv[3]
symbol = [sym, sym_base]
USD_CNY = 6.3
USDT_CNY = 6.6

# symbol_config = get_config(ex_name, symbol)

# sym0 = symbol_config['sym0']
# sym_base0 = symbol_config['sym_base0']
# exchange_base = symbol_config['exchange_base']
# base_order_quantity_scale = symbol_config['base_order_quantity_scale']
# base_order_range_scale = symbol_config['base_order_range_scale']
# account_fee = symbol_config['account_fee']
# avg_sym_btc = symbol_config['avg_sym_btc']
# symbol_price_decimal = symbol_config['symbol_price_decimal']
# symbol_quant_decimal = symbol_config['symbol_quant_decimal']
# symbol_quant_int_decimal = symbol_config['symbol_quant_int_decimal']
# min_quant = symbol_config['min_quant']
# msym = symbol_config['msym']
# order_gap = symbol_config['order_gap']
# quantity_scale_buy = symbol_config['quantity_scale_buy']
# quantity_scale_sell = symbol_config['quantity_scale_sell']
# total_quant_per_day_btc = symbol_config['total_quant_per_day_btc']
# auto_price = symbol_config['auto_price']
bxx_key = account_info[ex_name][symbol[1]][symbol[0]]

# symbol0 = [sym0, sym_base0]

# sdecimal = [symbol_price_decimal, symbol_quant_decimal]

binance_key = ['YDEaP2pwwNnTgxnVvTykElck9tTL3ODt5pYZGZWANPPCqIoRAK02Ma003susa9nZ',
               'LFhd1YzD9Hby4SVlXFqL0sxhXg3I30tjJsjCH8u90KGkIClp9PMLs1Ockr4dGQDd']

# zb_key = ['a', 'b']

fcoin_key = ['948f765b4bd7427c9c02d09fc42e6c8d', '3bfa3d0fd9534a8fb0f55884d0460021']

huobi_key = ['23d16220-7b1883cc-dc468afc-6865d',
             'fe31646f-78407147-ec119bc8-cbdab']

okex_key = ['', '']

coinw_key = ['a048a77f-b61e-49c5-b459-3ad171242959', 'ZTMF18573EILZLUIBB4RARLDOM3YCFOAYPXZ']

# !!!initiate

ex_bin = Exchange('binance', binance_key)

# ex_zb = Exchange('zb', zb_key)

ex_huobi = Exchange('huobi', huobi_key)

ex_hadax = Exchange('hadax', huobi_key)

ex_okex = Exchange('okex', okex_key)

ex_bxx = [Exchange('bxx', key) for key in bxx_key]

ex_cw = Exchange('coinw', coinw_key)


# USD_CNY = 6.33

def get_all_balance():
    while True:
        try:
            th_b = []
            for ex in ex_bxx:
                th_b.append(MyThread(ex.api.get_account, args=()))
            [th.start() for th in th_b]
            [th.join() for th in th_b]
            ac_list = [th.get_result() for th in th_b]
            sum_sym = 0
            sum_sym_base = 0
            for acl in ac_list:
                for dic in acl:
                    if dic['coinName'] == sym:
                        sum_sym += dic['carryingAmount']
                    elif dic['coinName'] == sym_base:
                        sum_sym_base += dic['carryingAmount']
        except Exception as e:
            print(e)
        else:
            break
    return sum_sym, sum_sym_base


def plog():
    print('no thread')


class test_pressure():
    def __init__(self, api, stand_price, side, symbol, quantity='', price=''):
        self.stand_price = float(stand_price)
        self.side = side
        self.symbol = symbol
        self.api = api.api
        self.quantity = quantity
        self.price = price

    def refresh_price_qt(self, count):
        # probability = random.randint(0, 5)
        # if probability == 0:
        #     price = round(self.stand_price , 8)
        #     quantity = 10
        # elif probability == 1:
        #     price = round(self.stand_price * 1.1, 8)
        #     quantity = 10 * 1.1
        # elif probability == 2:
        #     price = round(self.stand_price * 1.2, 8)
        #     quantity = 10 * 1.2
        # elif probability == 3:
        #     price = round(self.stand_price * 1.3, 8)
        #     quantity = 10 * 1.3
        # elif probability == 4:
        #     price = round(self.stand_price * 1.4, 8)
        #     quantity = 10 * 1.4
        # elif probability == 5:
        #     price = round(self.stand_price * 1.4, 8)
        #     quantity = 10 * 1.25
        price = self.stand_price + (count % 100) * 0.00000001
        quantity = count % 5 + 1
        order_msg = [quantity, price]
        return order_msg

    def refresh_order(self):
        self.__thread_order = MyThread(self.api.order,
                                       args=(self.symbol, self.side, self.quantity, self.price,))

        return self.__thread_order


# 获取两千个账户的所有token
# bxx_token = []
# for i in ex_bxx:
#     while True:
#         try:
#             ret = i.api.get_token()
#             bxx_token.append(['TTEX', ret['data']['access_token']])
#         except Exception:
#             ret = 'error'
#         if ret != 'error':
#             break
with open('a.txt', 'r') as f:
    msg = f.read()
bxx_token = eval(msg)

ex_bxx = [Exchange('bxx', key) for key in bxx_token]


stand_price = '0.00002135'
buy_order_msg = []
sell_order_msg = []
for api_id in range(len(ex_bxx)):
    if api_id % 2 == 0:
        buy_order_msg.append(ex_bxx[api_id])
    else:
        sell_order_msg.append(ex_bxx[api_id])

count = 0
while True:
    # start_time = time.time()
    for i in range(1):
        th_order = []
        for api_id in range(i * 1000, (i + 1) * 1000):
            api = buy_order_msg[api_id]
            # msg = test_pressure(api, stand_price, 'buy', symbol).refresh_price_qt(count)
            quantity_buy = round(random.random() + 1, 8)
            th_order.append(test_pressure(api, stand_price, 'buy', symbol, quantity_buy, '0.00002074').refresh_order())
            # api = sell_order_msg[api_id]
            quantity_sell = round(random.random() + 1, 8)
            th_order.append(test_pressure(api, stand_price, 'sell', symbol, quantity_sell, '0.00002074').refresh_order())
        [th.start() for th in th_order]
        # result = [th.get_result() for th in th_order]
        # print('############################################## ' + str(time.time()))
        # print('%s个账户在同时交易' % (i + 1) * 10)
        # print(str(result))
        time.sleep(1)
    count += 1
    print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
    print('程序跑完了')
    # end_time = time.time()
    # print('共需要%s时间' % (end_time - start_time))
    if count == 3600:
        start_time = time.time()
        symbol = ['POWR', "BTC"]
        bxx_key = account_info["TTEX"]["BTC"]['POWR']
        ex_bxx = [Exchange('bxx', key) for key in bxx_key]
        th_cancel_all = []
        for i in range(len(ex_bxx), 0, -1):
            th_cancel_all.append(MyThread(ex_bxx[i - 1].cancel_all_bxx, args=(symbol,)))
            # ex_bxx[i - 1].cancel_all_bxx(symbol)
        [th.start() for th in th_cancel_all]
        [th.join() for th in th_cancel_all]
        end_time = time.time()
        print('&&&&&&&&&&&&&&&&&&&&&&')
        print('共用%s' % (end_time - start_time))
        break
