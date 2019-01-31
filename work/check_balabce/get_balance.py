# -*- coding:utf-8 -*-
from datetime import datetime
import time
from ex_api.exchange import Exchange, MyThread, isPause, get_USDT_CNY, isExPause
from accounts_bxx import account_info
from send_email.send_email import Email

##################################

from ex_api.exchange import Exchange, MyThread
start_time = time.time()
account_info = dict()
account_info['TTEX'] = {
    'BTC': {
        'POWR': [],
    },
}
for i in range(5000, 7000):
    account_info['TTEX']['BTC']['POWR'].append(['TTEX', str(12012340001 + i), '1234Rty77899x']),
##############################

with open('a.txt', 'r') as f:
    msg = f.read()
bxx_token = eval(msg)





em_user = '295861809@qq.com'
pwd = 'agagwzladccqbhce'
address = ['295861809@qq.com', '568327240@qq.com']
smtp_server = 'smtp.qq.com'
phone_java = ['8613120362121', '8615311460485', '8613910860759']
phone_python = ['8613120362121', '15201479252']

parames = [
            ['TTEX', ['POWR', 'BTC']]
           # ["BXX", ["LPAY", "NBXX"]],
           # ["BXX", ["NBPAY", "NBXX"]],
           # ["BXX", ["EPAY11", "NBXX"]],
           # ["COINFLY", ["DUH", "BTC"]],
           # ["COINFLY", ["TTGS", "BTC"]],
           # ["COINFLY", ["PTIT", "BTC"]],
           # ["COINFLY", ["FGBL", "BTC"]],
           # ["COINFLY", ["LCOC", "BTC"]],
           # ["COINFLY", ["ICWF", "BTC"]],
           # ["COINFLY", ["ZVX", "BTC"]],
           # ["COINFLY", ["TUOD", "BTC"]],
           # ["COINFLY", ["JLO", "BTC"]],
           # ["COINFLY", ["NCBS", "BTC"]],
           ]


def get_all_balance():
    while True:
        try:
            th_b = []
            for ex in ex_bxx:
                th_b.append(MyThread(ex.api.get_account, args=()))
            for th in th_b:
                th.start()
                time.sleep(0.5)
            # [th.start() for th in th_b]
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


count = 0
balance = dict()
balance_new_list = list()
# while True:
for i in parames:
    ex_name = i[0]
    sym = i[1][0]
    sym_base = i[1][1]
    if ex_name not in balance.keys():
        balance[ex_name] = dict()
    if sym_base not in balance[ex_name].keys():
        balance[ex_name][sym_base] = dict()
    symbol = [sym, sym_base]
    bxx_key = account_info[ex_name][symbol[1]][symbol[0]]
    # ex_bxx = [Exchange('bxx', key) for key in bxx_key]
    ex_bxx = [Exchange('bxx', key) for key in bxx_token]
    sum_balance = get_all_balance()
    balance[ex_name][sym_base][sym] = sum_balance[0]
    # balance[sym_base] = sum_balance[1]
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(str(now_time) + sym + "，" + sym_base + ' 结果获取结束')
    time.sleep(10)
balance_new_list.append(balance)
if count == 0:
    balance_old_list = balance_new_list
    balance = {}
    balance_new_list = []
print(balance_old_list)
print(balance_new_list)
    # else:
    #     now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     if balance_new_list == balance_old_list:
    #         print(str(now_time) + '机器人账户总余额没有变动')
    #         print(balance_new_list)
    #         title = '机器人账户总余额没有变动'
    #         message = str(now_time) + '目前机器人账户总余额为：' + str(balance_new_list).replace(',', '\n')
    #         Email(em_user=em_user, pwd=pwd, address=address, smtp_server=smtp_server).send_email(message=message,
    #                                                                                              title=title)
    #         balance_new_list = []
    #     else:
    #         print(str(now_time) + '机器人账户总余额已经发生变动')
    #         print('balance_new_list = ' + str(balance_new_list))
    #         print('balance_old_list = ' + str(balance_old_list))
    #         title = '机器人账户总余额已经发生变动'
    #         dif_balance = [i for i in balance_new_list if i not in balance_old_list]
    #         message = str(now_time) + '机器人账户总余额发生变动的地方为：' + str(dif_balance).replace(',',
    #                                                                                  '\n') + '\n\n' + "最新的账户余额情况：\n" + str(
    #             balance_new_list).replace(',', '\n') + '\n\n' + '之前的账户余额情况为：\n' + str(balance_old_list).replace(',',
    #                                                                                                             '\n')
    #         balance_old_list = balance_new_list
    #         Email(em_user=em_user, pwd=pwd, address=address, smtp_server=smtp_server).send_email(message=message,
    #                                                                                              title=title)
    #         balance = {}
    #         balance_new_list = []
    # count += 1
    # if count >= 2:
    #     time.sleep(7200)
    # else:
    #     time.sleep(60)
