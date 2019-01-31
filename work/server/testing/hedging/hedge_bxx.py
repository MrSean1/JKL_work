from datetime import datetime
from email.mime.text import MIMEText
import os
import smtplib
import time
from ex_api.exchange import Exchange, MyThread
# 要改动得
# from config_bxx import get_config
from hedging.config_bxx import get_config
# from accounts_bxx import account_info
from hedging.account_info import account_info
import json

# delete unnecessary symbol's accounts
del_symbol = [['BXX', ['EMBC', 'ETH']], ['BXX', ['APV', 'ETH']], ['DAPP', ['CC', 'USDT']], ['HBANK', ['HB', 'USDT']],
              ['HBANK', ['HB', 'BTC']], ['HBANK', ['HB', 'ETH']]]
for l in del_symbol:
    try:
        del (account_info[l[0]][l[1][1]][l[1][0]])
    except Exception as e:
        pass

# delete done

ex_name_all = ['BXX', 'TTEX']

balance_diff_all = dict()
balance_diff = dict()
balance_bxx = dict()
ex_bxx = dict()
balance_base = dict()

# init
# ex_name 将交易所得名字变为key
for ex_name in ex_name_all:
    balance_bxx[ex_name] = dict()
    ex_bxx[ex_name] = dict()
    balance_base[ex_name] = dict()
    balance_diff[ex_name] = dict()
    # 将 交易区得名字变为key
    for sym_base in account_info[ex_name].keys():
        print('交易区')
        print(sym_base)
        balance_bxx[ex_name][sym_base] = dict()
        ex_bxx[ex_name][sym_base] = dict()
        balance_base[ex_name][sym_base] = dict()
        balance_diff[ex_name][sym_base] = dict()
        # balance_diff_all[sym_base] = dict()
        if sym_base not in balance_diff_all.keys():
            balance_diff_all[sym_base] = dict()
        for sym in account_info[ex_name][sym_base].keys():
            print(sym)
            balance_bxx[ex_name][sym_base][sym] = [0, 0]
            balance_base[ex_name][sym_base][sym] = 0
            balance_diff[ex_name][sym_base][sym] = 0
            ex_bxx[ex_name][sym_base][sym] = [Exchange('bxx', key) for key in account_info[ex_name][sym_base][sym]]
            # if sym not in balance_diff_all.keys():
            #     balance_diff_all[sym] = 0
            balance_diff_all[sym_base][sym] = 0


# 获取某个交易所中某个交易对的操盘账户的总余额
def get_all_balance(ex_name, symbol):
    th_b = []
    for ex in ex_bxx[ex_name][symbol[1]][symbol[0]]:
        th_b.append(MyThread(ex.api.get_account, args=()))
    [th.start() for th in th_b]
    [th.join() for th in th_b]
    ac_list = [th.get_result() for th in th_b]
    sum_sym = 0
    sum_sym_base = 0
    for acl in ac_list:
        for dic in acl:
            if dic['coinName'] == symbol[0]:
                sum_sym += dic['carryingAmount']
            elif dic['coinName'] == symbol[1]:
                sum_sym_base += dic['carryingAmount']
    balance_bxx[ex_name][symbol[1]][symbol[0]] = [sum_sym, sum_sym_base]


# 刷新历史表  即往字典中存入账户历史信息
def refresh_base():
    for ex_name in balance_bxx.keys():
        for sym_base in balance_bxx[ex_name].keys():
            for sym in balance_bxx[ex_name][sym_base].keys():
                balance_base[ex_name][sym_base][sym] = balance_bxx[ex_name][sym_base][sym][0]


# 存放差异的表 记录账户变动币种数量
def refresh_diff():
    # for sym in balance_diff_all.keys():
    #     balance_diff_all[sym] = 0
    for ex_name in balance_bxx.keys():
        for sym_base in balance_bxx[ex_name].keys():
            for sym in balance_bxx[ex_name][sym_base].keys():
                balance_diff[ex_name][sym_base][sym] = balance_bxx[ex_name][sym_base][sym][0] - \
                                                       balance_base[ex_name][sym_base][sym]
                balance_diff_all[sym_base][sym] += balance_diff[ex_name][sym_base][sym]


def refresh_all_balance():
    for ex_name in ex_name_all:
        for sym_base in account_info[ex_name].keys():
            for sym in account_info[ex_name][sym_base].keys():
                symbol = [sym, sym_base]
                get_all_balance(ex_name, symbol)


# 更新balance_bxx
refresh_all_balance()
# 更新balance_base
refresh_base()
# 更新balance_diff和balance_diff_all
refresh_diff()




while True:
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # 判断时间
    # 更新balance_bxx
    refresh_all_balance()
    print(now_time + ': ' + '当前账户总资产余额： ' + eval(balance_bxx))
    # 输出余额日志
    # 更新balance_diff和balance_diff_all
    refresh_diff()
    # 根据balance_diff_all在其它交易所进行对冲

    # 判断对冲账户余额
    # 进行买卖然后撤销然后查询然后更新火币的对冲结果表

    # 根据对冲结果刷新balance_diff_all
    # 输出对冲需求和结果日志

    # 刷新历史状态
    refresh_base()
    time.sleep(60)



binance_key = ['YDEaP2pwwNnTgxnVvTykElck9tTL3ODt5pYZGZWANPPCqIoRAK02Ma003susa9nZ',
               'LFhd1YzD9Hby4SVlXFqL0sxhXg3I30tjJsjCH8u90KGkIClp9PMLs1Ockr4dGQDd']

# huobi_key = ['23d16220-7b1883cc-dc468afc-6865d',
#              'fe31646f-78407147-ec119bc8-cbdab']
huobi_key = ['5c857632-23a0a848-5948e573-c39a8',
             '20f02610-1623ff8f-98731f9b-2ca99']

coinw_key = ['a048a77f-b61e-49c5-b459-3ad171242959', 'ZTMF18573EILZLUIBB4RARLDOM3YCFOAYPXZ']

ex_bin = Exchange('binance', binance_key)

ex_huobi = Exchange('huobi', huobi_key)

ex_cw = Exchange('coinw', coinw_key)

symbol_bin = ['BTC', 'ETH', 'LTC', 'QTUM', 'USDT']
symbol_huobi = ['DASH', 'EOS', 'HSR', 'USDT']
symbol_cw = ['Doge', 'hpy']

user = 'pkusimon@qq.com'
pwd = 'zvgtfnzjvlkmbdig'
to_xl = '568327240@qq.com'
# to_yl = '124397321@qq.com'
smtp_server = 'smtp.qq.com'


# ex_bin.refresh_account()
# balance_bin = {sym: float(ex_bin.account_info[sym]['avaid_balance']) for sym in symbol_bin}

# ex_huobi.refresh_account()
# balance_huobi = {}
# for sym in symbol_huobi:
#     for dic in ex_huobi.account_info:
#         if dic['currency'] == sym.lower() and dic['type'] == 'trade':
#             balance_huobi[sym] = float(dic['balance'])
#             break
#
# ex_cw.refresh_account()
# balance_cw = {sym: float(ex_cw.account_info[sym]['avaid_balance']) for sym in symbol_cw}


# step 1: check balance of bxx Exchange


# step 2:

def check_balance_binance():
    balance_bin_new = dict(balance_bin)
    try:
        ex_bin.refresh_account()
        if ex_bin.account_info is False:
            raise ValueError
    except Exception:
        print('binance account api error')
    else:
        balance_bin_new = {sym: float(ex_bin.account_info[sym]['avaid_balance']) for sym in symbol_bin}
        if balance_bin_new['BTC'] < 0.1 and balance_bin_new['BTC'] != balance_bin['BTC']:
            msg = MIMEText('BTC当前余额为' + str(balance_bin_new['BTC']))
            msg['Subject'] = '币安余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
        elif balance_bin_new['LTC'] < 4 and balance_bin_new['LTC'] != balance_bin['LTC']:
            msg = MIMEText('LTC当前余额为' + str(balance_bin_new['LTC']))
            msg['Subject'] = '币安余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
        elif balance_bin_new['ETH'] < 2 and balance_bin_new['ETH'] != balance_bin['ETH']:
            msg = MIMEText('ETH当前余额为' + str(balance_bin_new['ETH']))
            msg['Subject'] = '币安余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
        elif balance_bin_new['QTUM'] < 10 and balance_bin_new['QTUM'] != balance_bin['QTUM']:
            msg = MIMEText('QTUM当前余额为' + str(balance_bin_new['QTUM']))
            msg['Subject'] = '币安余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
        elif balance_bin_new['USDT'] < 1000 and balance_bin_new['USDT'] != balance_bin['USDT']:
            msg = MIMEText('USDT当前余额为' + str(balance_bin_new['USDT']))
            msg['Subject'] = '币安余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
    return balance_bin_new


def check_balance_huobi():
    balance_huobi_new = dict(balance_huobi)
    try:
        ex_huobi.refresh_account()
        if ex_huobi.account_info is False:
            raise ValueError
    except Exception:
        print('huobi account api error')
    else:
        balance_huobi_new = {}
        for sym in symbol_huobi:
            for dic in ex_huobi.account_info:
                if dic['currency'] == sym.lower() and dic['type'] == 'trade':
                    balance_huobi_new[sym] = float(dic['balance'])
                    break
        if balance_huobi_new['EOS'] < 20 and balance_huobi_new['EOS'] != balance_huobi['EOS']:
            msg = MIMEText('EOS当前余额为' + str(balance_huobi_new['EOS']))
            msg['Subject'] = '火币余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
        elif balance_huobi_new['DASH'] < 2 and balance_huobi_new['DASH'] != balance_huobi['DASH']:
            msg = MIMEText('DASH当前余额为' + str(balance_huobi_new['DASH']))
            msg['Subject'] = '火币余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
        elif balance_huobi_new['USDT'] < 500 and balance_huobi_new['USDT'] != balance_huobi['USDT']:
            msg = MIMEText('USDT当前余额为' + str(balance_huobi_new['USDT']))
            msg['Subject'] = '火币余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
    return balance_huobi_new


def check_balance_coinw():
    balance_cw_new = dict(balance_cw)
    try:
        ex_cw.refresh_account()
        if ex_cw.account_info is False:
            raise ValueError
    except Exception:
        print('coinw account api error')
    else:
        balance_cw_new = {sym: float(ex_cw.account_info[sym]['avaid_balance']) for sym in symbol_cw}
        if balance_cw_new['Doge'] < 20000 and balance_cw_new['Doge'] != balance_cw['Doge']:
            msg = MIMEText('DOGE当前余额为' + str(balance_cw_new['Doge']))
            msg['Subject'] = 'coinw余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
        elif balance_cw_new['hpy'] < 10000 and balance_cw_new['hpy'] != balance_cw['hpy']:
            msg = MIMEText('hpy当前余额为' + str(balance_cw_new['hpy']))
            msg['Subject'] = 'coinw余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
        elif balance_cw_new['CNYT'] < 2000 and balance_cw_new['CNYT'] != balance_cw['CNYT']:
            msg = MIMEText('CNYT当前余额为' + str(balance_cw_new['CNYT']))
            msg['Subject'] = 'coinw余额警告'
            send_email_xl(msg)
            send_email_yl(msg)
    return balance_cw_new


while True:
    if int(time.strftime('%M')) in [0]:
        check_balance_coinx()
    a = os.popen('ps -f -C python').read().split('\n')[1:-1]
    b = [pr.split(' -u ')[1] for pr in a]
    print(time.asctime())
    print(len(b))
    if len(set(process_short).difference(set(b))) != 0:
        msg = MIMEText('有' + str(number_process - len(b)) + '个进程被意外关闭，当前为' + str(len(b)) + '个\n被关闭的进程为'
                       + str(set(process_short).difference(set(b))) + '\n')
        msg['Subject'] = '进程数量警告'
        send_email_xl(msg)
    number_process = len(b)
    process_short = list(b)
    # balance_bin = check_balance_binance()
    # balance_cw = check_balance_coinw()
    # balance_huobi = check_balance_huobi()
    time.sleep(55)
