from ex_api.exchange import Exchange, MyThread, isPause, get_USDT_CNY, isExPause
import time
import random
import sys
from config_bxx import get_config
from accounts_bxx import account_info
from price import *

# !!!initiate parameter

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
auto_price = symbol_config['auto_price']
bxx_key = account_info[ex_name][symbol[1]][symbol[0]]

symbol0 = [sym0, sym_base0]

sdecimal = [symbol_price_decimal, symbol_quant_decimal]

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


class fake_order:
    def __init__(self, order_type, api_id, symbol, side, low, high, base_quantity, refresh_rate, decimal, range_scale):
        self.order_type = order_type
        # self.order_id_list = []
        self.active_order_id = []
        self.__thread_cancel = []
        self.__thread_order = MyThread(plog)
        self.__thread_query = []
        self.api_id = api_id
        self.__api = ex_bxx[api_id].api
        self.__symbol = symbol
        self.sym = symbol[0]
        self.sym_base = symbol[1]
        self.side = side
        self.__low = low * range_scale
        self.__high = high * range_scale
        self.fake_price = 0
        self.__base_quantity = base_quantity
        self.refresh_flag = False
        self.__refresh_rate = refresh_rate
        self.__price_decimal = decimal[0]
        self.__quant_decimal = decimal[1]
        self.__latest_refresh_time = time.time()
        self.delay = 0

    def print_info(self):
        print('symbol:', self.__symbol)
        print('side:', self.side)

    def set_quantity(self, new_quantity):
        self.__base_quantity = new_quantity

    def set_api_id(self, new_api_id):
        self.api_id = new_api_id
        self.__api = ex_bxx[new_api_id].api

    def reset_params_midnight(self):
        self.__low += 0.05
        self.__high += 0.05
        self.__base_quantity /= 5

    def reset_params_normal(self):
        self.__low -= 0.05
        self.__high -= 0.05
        self.__base_quantity *= 5

    def start_confirm(self):
        for idt in self.active_order_id:
            self.__thread_query.append(MyThread(self.__api.get_query, args=(idt,)))
        [thr.start() for thr in self.__thread_query]

    def end_confirm(self):
        cond = 0
        num_id = 0
        for thr in self.__thread_query:
            thr.join()
            ret = thr.get_result()
            try:
                if ret and float(ret['deal']) > 0:
                    cond += 1
                    # with open('./' + self.__symbol[0] + '_' + self.__symbol[1] + '_hedge/id_list.txt', 'a') as f:
                    #     f.writelines(self.active_order_id[num_id] + ' ')
            except Exception:
                print(ret)
            num_id += 1
        if cond > 0:
            self.__latest_refresh_time = time.time()
            if self.order_type == 'thin':
                self.delay = 30
        self.__thread_query = []
        return cond

    def refresh(self, standard_price, my_bid, my_ask):
        if self.side == 'buy':
            low_price = standard_price * (1 - self.__low)
            high_price = standard_price * (1 - self.__high)
            dtag = (low_price < self.fake_price)
        else:
            low_price = standard_price * (1 + self.__low)
            high_price = standard_price * (1 + self.__high)
            dtag = (low_price > self.fake_price)
        if not self.active_order_id:
            dtag = True
        if random.uniform(0, 1) < self.__refresh_rate and time.time() - self.__latest_refresh_time > self.delay:
            dtag = True
        if self.side == 'buy' and low_price >= my_ask:
            dtag = False
        if self.side == 'sell' and low_price <= my_bid:
            dtag = False
        if dtag:
            self.refresh_flag = True
            self.__latest_refresh_time = time.time()
            self.delay = 0
            for idt in self.active_order_id:
                self.__thread_cancel.append(MyThread(self.__api.cancel, args=(idt,)))
            self.fake_price = round(random.uniform(low_price, high_price), self.__price_decimal)
            fake_qty = round(random.uniform(0.5 * self.__base_quantity, 1.5 * self.__base_quantity),
                             self.__quant_decimal)
            if random.randint(0, 1) == 1:
                fake_qty = round(fake_qty, symbol_quant_int_decimal)
            # print(self.__symbol, self.side, self.fake_price, fake_qty)
            fake_qty = max(fake_qty, min_quant)
            self.__thread_order = MyThread(self.__api.order,
                                           args=(self.__symbol, self.side, fake_qty, self.fake_price,))
            # may add a thread of order info
            for thr in self.__thread_cancel:
                thr.start()
            self.__thread_order.start()

    def result(self):
        if self.refresh_flag:
            # may add a thread of order info
            for thr in self.__thread_cancel:
                thr.join()
            self.__thread_order.join()
            # confirm success of 'cancel'
            tempc = 0
            temp_order_id = []
            all_order_id = list(self.active_order_id)
            for idt in self.active_order_id:
                err_flag = False
                res = self.__thread_cancel[tempc].get_result()
                if 'errcode' in res.keys():
                    err_flag = True
                if not err_flag:
                    temp_order_id.append(idt)
                tempc += 1
            self.active_order_id = []
            # add active order id to list
            res = self.__thread_order.get_result()
            if res and str(res) not in ['0', 'None', '500', '405']:
                self.active_order_id.append(self.__thread_order.get_result())
                # self.order_id_list.append(self.__thread_order.get_result())
            # reset thread
            self.__thread_cancel = []
            self.__thread_order = MyThread(plog)
            self.refresh_flag = False
            return temp_order_id, all_order_id
        else:
            return [], []


far_order = []
for i in range(1):
    far_order.append(
        fake_order('far', 5, symbol, 'buy', order_gap + 0.01, order_gap + 0.015,
                   0.15 * base_order_quantity_scale * quantity_scale_buy, 0.1,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'sell', order_gap + 0.01, order_gap + 0.015,
                   0.15 * base_order_quantity_scale * quantity_scale_sell, 0.1,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'buy', order_gap + 0.013, order_gap + 0.02,
                   0.15 * base_order_quantity_scale * quantity_scale_buy, 0.05,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'sell', order_gap + 0.013, order_gap + 0.02,
                   0.15 * base_order_quantity_scale * quantity_scale_sell,
                   0.05, sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'buy', order_gap + 0.017, order_gap + 0.025,
                   0.2 * base_order_quantity_scale * quantity_scale_buy, 0.05,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'sell', order_gap + 0.017, order_gap + 0.025,
                   0.2 * base_order_quantity_scale * quantity_scale_sell, 0.05,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'buy', order_gap + 0.02, order_gap + 0.03,
                   0.2 * base_order_quantity_scale * quantity_scale_buy, 0.05,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'sell', order_gap + 0.02, order_gap + 0.03,
                   0.2 * base_order_quantity_scale * quantity_scale_sell, 0.05,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'buy', order_gap + 0.025, order_gap + 0.035,
                   0.3 * base_order_quantity_scale * quantity_scale_buy, 0.03,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'sell', order_gap + 0.025, order_gap + 0.035,
                   0.3 * base_order_quantity_scale * quantity_scale_sell, 0.03,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'buy', order_gap + 0.03, order_gap + 0.05,
                   0.3 * base_order_quantity_scale * quantity_scale_buy, 0.03,
                   sdecimal, base_order_range_scale))
    far_order.append(
        fake_order('far', 5, symbol, 'sell', order_gap + 0.03, order_gap + 0.05,
                   0.3 * base_order_quantity_scale * quantity_scale_sell, 0.03,
                   sdecimal, base_order_range_scale))

thin_order_buy = []
thin_order_sell = []
for i in range(3):
    thin_order_buy.append(
        fake_order('thin', 0, symbol, 'buy', order_gap, order_gap + 0.002,
                   0.01 * base_order_quantity_scale * quantity_scale_buy, 1, sdecimal, base_order_range_scale))
    thin_order_sell.append(
        fake_order('thin', 1, symbol, 'sell', order_gap, order_gap + 0.002,
                   0.01 * base_order_quantity_scale * quantity_scale_sell, 1, sdecimal, base_order_range_scale))
for i in range(3):
    thin_order_buy.append(
        fake_order('thin', 2, symbol, 'buy', order_gap + 0.002, order_gap + 0.008,
                   0.02 * base_order_quantity_scale * quantity_scale_buy, 0.6, sdecimal, base_order_range_scale))
    thin_order_sell.append(
        fake_order('thin', 2, symbol, 'sell', order_gap + 0.002, order_gap + 0.008,
                   0.02 * base_order_quantity_scale * quantity_scale_sell, 0.6, sdecimal, base_order_range_scale))
for i in range(3):
    thin_order_buy.append(
        fake_order('thin', 3, symbol, 'buy', order_gap + 0.003, order_gap + 0.009,
                   0.05 * base_order_quantity_scale * quantity_scale_buy, 0.3, sdecimal, base_order_range_scale))
    thin_order_sell.append(
        fake_order('thin', 3, symbol, 'sell', order_gap + 0.003, order_gap + 0.009,
                   0.05 * base_order_quantity_scale * quantity_scale_sell, 0.3, sdecimal, base_order_range_scale))
for i in range(3):
    thin_order_buy.append(
        fake_order('thin', 4, symbol, 'buy', order_gap + 0.004, order_gap + 0.015,
                   0.1 * base_order_quantity_scale * quantity_scale_buy, 0.2, sdecimal, base_order_range_scale))
    thin_order_sell.append(
        fake_order('thin', 4, symbol, 'sell', order_gap + 0.004, order_gap + 0.015,
                   0.1 * base_order_quantity_scale * quantity_scale_sell, 0.2, sdecimal, base_order_range_scale))

for i in range(12):
    thin_order_sell[i].set_api_id(2 * (11 - i))

for i in range(12):
    thin_order_buy[i].set_api_id((11 - i) * 2 + 1)

for i in range(12):
    far_order[i].set_api_id(i + 24)

th_cancel_all = []
for i in range(len(ex_bxx), 0, -1):
    th_cancel_all.append(MyThread(ex_bxx[i - 1].cancel_all_bxx, args=(symbol,)))
    # ex_bxx[i - 1].cancel_all_bxx(symbol)
[th.start() for th in th_cancel_all]
[th.join() for th in th_cancel_all]

cur_time = time.time()

id_buy = ''
id_sell = ''

num = 0
my_bid_1 = 0
my_ask_1 = 1000000
flag_midnight = False

if sym in fake_coin:
    start_balance = get_all_balance()[0]
    customer_balance = 0
    auto_price.refresh_price({'customer_balance': customer_balance})
    sd_price = auto_price.price
else:
    auto_price.refresh_price()
    sd_price = auto_price.price

while True:
    print(time.asctime())
    # 检查是否暂停
    isP = isExPause(ex_name)
    if isP == 1:
        time.sleep(20)
        continue
    # 更新汇率
    if num % 1000 == 0:
        USDT_CNY = get_USDT_CNY()
        while True:
            try:
                ret = 6.33
                if ret is False:
                    raise ValueError
                else:
                    break
            except Exception:
                continue
        USD_CNY = ret
        # USDT_CNY = USD_CNY
        print('USD rate', USD_CNY)
        print('USDT rate', USDT_CNY)
    # if int(time.strftime('%H%M')) > 2330 and flag_midnight is False:
    #     flag_midnight = True
    #     for fo in far_order + thin_order_buy + thin_order_sell:
    #         fo.reset_params_midnight()
    #     print('midnight is coming')
    # elif int(time.strftime('%H%M')) <= 40 or int(time.strftime('%H%M')) >= 2340:
    #     time.sleep(60)
    #     continue
    # elif 40 < int(time.strftime('%H%M')) <= 130 and flag_midnight is True:
    #     flag_midnight = False
    #     for fo in far_order + thin_order_buy + thin_order_sell:
    #         fo.reset_params_normal()
    #     print('midnight has gone')
    # 暂停一段时间
    if num > 0 and time.time() - cur_time < 3:
        time.sleep(2.5)
    time.sleep(15 + random.uniform(0, 5))
    cur_time = time.time()
    # 检查买一卖一
    try:
        dep = ex_bxx[0].api.get_depth(symbol)
        if dep['asks'][0][0] < dep['bids'][0][0]:
            print('match error')
            time.sleep(30)
            continue
    except Exception as e:
        print(e)
    num += 1

    # 刷新价格
    if sym in fake_coin:
        robot_balance = get_all_balance()[0]
        start_balance = 38000000
        if ex_name == 'COINFLY':
            start_balance = 19000000
            if sym == 'LCOC':
                start_balance = 13500000
        customer_balance = start_balance - robot_balance
        auto_price.refresh_price({'customer_balance': customer_balance})
    else:
        auto_price.refresh_price()
    print(auto_price.price)
    if abs(auto_price.price / sd_price - 1) < 0.5:
        sd_price = auto_price.price
    else:
        print('error sd price')

    print('symbol:', symbol, '  standard price:', sd_price)
    # ex_cx1.api.self_order(symbol, 1, sd_price)

    # 检查所有订单的状态
    cond_buy = 0
    cond_sell = 0
    delay_flag = False
    count_delay = 0

    # confirm order status
    for fo in far_order:
        fo.start_confirm()
    for fo in thin_order_buy:
        if fo.delay == 0:
            fo.start_confirm()
        else:
            count_delay += 1
            delay_flag = True
    for fo in thin_order_sell:
        if fo.delay == 0:
            fo.start_confirm()
        else:
            count_delay += 1
            delay_flag = True

    for fo in far_order:
        fo.end_confirm()
    for fo in thin_order_buy:
        if fo.delay == 0:
            cond_buy += fo.end_confirm()
    for fo in thin_order_sell:
        if fo.delay == 0:
            cond_sell += fo.end_confirm()
    if cond_buy > 0 or cond_sell > 0:
        delay_flag = True

    print(count_delay, 'orders were delayed')
    print(cond_buy, 'thin bid orders were eaten')
    print(cond_sell, 'thin ask orders were eaten')

    # adjust delay of thin order
    if cond_buy > 0:
        for i in range(3):
            thin_order_buy[i].delay += 30
    if cond_buy > 3:
        for i in range(6):
            thin_order_buy[i].delay += 30
    if cond_buy > 6:
        for i in range(9):
            thin_order_buy[i].delay += 30
    if cond_buy > 9:
        for i in range(12):
            thin_order_buy[i].delay += 30
    if cond_sell > 0:
        for i in range(3):
            thin_order_sell[i].delay += 30
    if cond_sell > 3:
        for i in range(6):
            thin_order_sell[i].delay += 30
    if cond_sell > 6:
        for i in range(9):
            thin_order_sell[i].delay += 30
    if cond_sell > 9:
        for i in range(12):
            thin_order_sell[i].delay += 30

    # 刷新订单
    for fo in far_order + thin_order_buy + thin_order_sell:
        time.sleep(1)
        if sym != 'COTO' or fo.side != 'buy':
            fo.refresh(sd_price, my_bid_1, my_ask_1)

    count = 0
    for fo in far_order + thin_order_buy + thin_order_sell:
        if fo.refresh_flag:
            count += 1
    print('refreshed order:', count)

    # get global order status
    order_list_cancel = []
    order_list_cancel_all = []
    order_list_active = []
    for i in range(36):
        order_list_cancel.append([])
        order_list_cancel_all.append([])
        order_list_active.append([])
    for fo in far_order + thin_order_buy + thin_order_sell:
        r1, r2 = fo.result()
        order_list_cancel[fo.api_id] += r1
        order_list_cancel_all[fo.api_id] += r2
        order_list_active[fo.api_id] += fo.active_order_id

    # calculate my_bid and my_ask
    time.sleep(1)
    t_my_depth = []
    for ex in ex_bxx:
        t_my_depth.append(MyThread(ex.api.get_my_depth, args=(symbol,)))
    [th.start() for th in t_my_depth]
    [th.join() for th in t_my_depth]
    sym_dep = []
    for i in range(36):
        sym_dep.append([])
    for i in range(36):
        my_depth = t_my_depth[i].get_result()
        for dic in my_depth:
            sym_dep[i].append(dic)
    order_list_dep = []
    for i in range(36):
        order_list_dep.append([dic['orderId'] for dic in sym_dep[i]])
    my_bid_1 = 0
    my_ask_1 = 1000000
    for dic in sym_dep:
        if not dic:
            continue
        dic = dic[0]
        if str(dic['type']) == '1':
            if float(dic['price']) > my_bid_1:
                my_bid_1 = float(dic['price'])
        elif str(dic['type']) == '2':
            if float(dic['price']) < my_ask_1:
                my_ask_1 = float(dic['price'])
    if sym == 'HPS':
        while True:
            try:
                dep = ex_bxx[0].api.get_depth(symbol)
                if dep:
                    break
                else:
                    raise ValueError
            except Exception:
                continue
        try:
            # my_ask_1 = dep['asks'][0][0]
            my_bid_1 = dep['bids'][0][0]
        except Exception:
            pass
    print('my_bid_1:', my_bid_1, 'my_ask_1:', my_ask_1)
    my_bid_1 = 0
    my_ask_1 = 1000000
    time.sleep(1)

    # maker sure every active order is in 'active_order'
    for i in range(36):
        order_list_cancel[i] = order_list_cancel[i] + list(
            set(order_list_dep[i]).difference(set(order_list_active[i])).difference(set(order_list_cancel[i])))
        # print('order_list_active:', order_list_active)
        # print('order_list_cancel:', order_list_cancel)
        print(len(order_list_dep[i]), 'orders in my depth')
        print(len(order_list_active[i]), 'orders are active')
        print(len(order_list_cancel[i]), 'orders waiting to be canceled')
        while len(order_list_cancel[i]) > 0:
            t_c = dict()
            for order_id in order_list_cancel[i]:
                t_c[order_id] = MyThread(ex_bxx[i].api.cancel, args=(order_id,))
            for order_id in order_list_cancel[i]:
                t_c[order_id].start()
            for order_id in order_list_cancel[i]:
                t_c[order_id].join()
            temp_list = []
            for order_id in order_list_cancel[i]:
                if t_c[order_id].get_result() is not False:
                    temp_list.append(order_id)
            order_list_cancel[i] = list(set(order_list_cancel[i]).difference(set(temp_list)))
            # time.sleep(60)
