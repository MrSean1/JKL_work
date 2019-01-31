#!/home/haitao/anaconda3/bin/python
# from datetime import datetime
# from email.mime.text import MIMEText
# import os
# import smtplib
# import time
from ex_api.exchange import Exchange, MyThread
# 要改动得
# from config_bxx import get_config
# from hedging.config_bxx import get_config
# from accounts_bxx import account_info
# from hedging.account_info import account_info
# import json
# from hedge_bxx import balance_diff_all

# 获取火币交易所中某个交易对的操盘账户的总余额
huobi_account = [['5c857632-23a0a848-5948e573-c39a8', '20f02610-1623ff8f-98731f9b-2ca99']]
ex_name = 'huobi'
market_list = ['BTC', 'USDT', 'ETH']


# 获取火币账户信息
def get_huobi_balance():
    th_h = []
    ex_huobi = [Exchange('huobi', key) for key in huobi_account]
    for ex in ex_huobi:
        th_h.append(MyThread(ex.api.get_account, args=()))
    # for ex in ex_bxx[ex_name][symbol[1]][symbol[0]]:
    #     th_b.append(MyThread(ex.api.get_account, args=()))
    [th.start() for th in th_h]
    [th.join() for th in th_h]
    ac_list = [th.get_result() for th in th_h]
    blance_huobi = dict()
    for acl in ac_list[0]:
        if acl['type'] != 'frozen':
            blance_huobi[acl['currency']] = acl['balance']
    print(blance_huobi)
    return blance_huobi


# 对冲判断
def is_hedge(balance_diff_all, blance_huobi):
    for sym_base in market_list:
        for sym, v in balance_diff_all[sym_base]:
            if v > 0 and blance_huobi[sym] == 0:
                print('对冲账户对%s币，账户余额为0')
            if v > 0 and blance_huobi[sym] > 0:
                print('在火币进行抛售对冲')
            if v < 0 and blance_huobi[sym_base] > 0:
                print('对冲账户进行买入对冲')


# 通过市场深度获得对冲价格
def get_price(sym_base, sym, type):
    print('开始获取市场深度')
    symbol = [sym, sym_base]
    th_h = []
    ex_huobi = [Exchange('huobi', key) for key in huobi_account]
    for ex in ex_huobi:
        th_h.append(MyThread(ex.api.get_depth, args=(symbol,)))
    # for ex in ex_bxx[ex_name][symbol[1]][symbol[0]]:
    #     th_b.append(MyThread(ex.api.get_account, args=()))
    [th.start() for th in th_h]
    [th.join() for th in th_h]
    price_dict = [th.get_result() for th in th_h]
    # 卖
    if type == 'asks':
        print(price_dict)
        price = price_dict[0][type][4][0]
        print(price)
        return price
    # 买
    elif type == 'bids':
        print(price_dict)
        price = price_dict[0][type][4][0]
        print(price)
        return price

# 撤销订单并获取已成交数量
def cancle(orderid):
    print('开始撤销订单')
    ex_huobi = [Exchange('huobi', key) for key in huobi_account]
    th_h = []
    for ex in ex_huobi:
        th_h.append(MyThread(ex.api.cancel, args=(orderid,)))
    # for ex in ex_bxx[ex_name][symbol[1]][symbol[0]]:
    #     th_b.append(MyThread(ex.api.get_account, args=()))
    [th.start() for th in th_h]
    [th.join() for th in th_h]
    order_result = [th.get_result() for th in th_h]
    print('订单撤销完毕')
    print(order_result)
    return order_result


get_huobi_balance()
# get_price('USDT', 'BTC', 'bids')
# cancle(9186361398)
