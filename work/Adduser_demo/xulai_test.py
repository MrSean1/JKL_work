# import requests
import datetime
# import numpy as np
import pandas as pd
# import pickle
import time
from threading import Thread
from sp_account import Account
from mt4_account import MT4Account
import logging
from send_email.send_email import Email


class MyThread(Thread):
    def __init__(self, func, args=(), lag=0):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.lag = lag
        self.result = False

    def run(self):
        time.sleep(self.lag)
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


log = setup_logger()
log.setLevel(logging.INFO)

sp_account_list = ["1001524403"]
sp_acc = Account(sp_account_list[0])
sp_pos = 1
sym_s = "YMM9"

account_info = pd.read_csv("./mt4_account_config.csv")
account_info = account_info[account_info["inactive"] != 1]

mt4_account_list = list(account_info["account"])
mt4_account_list = [str(i) for i in mt4_account_list]
mt4_acc = [MT4Account(str(row_acc['account']), str(row_acc['ip'])) for index, row_acc in account_info.iterrows()]
sym_m = list(account_info["sym"])
mt4_max_retracement_per = list(account_info["max_retracement_per"])
balance = [mt4_acc[i].balance for i in range(len(mt4_account_list))]
for i in range(len(mt4_max_retracement_per)):
    if list(account_info["fix_balance"])[i] != 0:
        balance[i] = list(account_info["fix_balance"])[i]
    if sym_m[i] == 'DJI30':
        balance[i] = balance[i] / 166
# mt4_pos = [int(balance[i] * mt4_max_retracement_per[i] / 1000) for i in range(len(mt4_account_list))]
mt4_pos = list()
for i in range(len(mt4_account_list)):
    if sym_m[i] == 'DJI' or sym_m[i] == 'DJ30':
        mt4_pos.append(int(balance[i] * mt4_max_retracement_per[i] / 1000) / 10)
    elif sym_m[i] == 'USA30':
        mt4_pos.append(int(balance[i] * mt4_max_retracement_per[i] / 1000) / 100)
    else:
        mt4_pos.append(int(balance[i] * mt4_max_retracement_per[i] / 1000))

log.info("account: " + " ".join(mt4_account_list))
log.info("position: " + " ".join([str(i) for i in mt4_pos]))

# em = Email('295861809@qq.com', 'qxkrwbmoxosdbhfi', "pkusimon@qq.com", "smtp.qq.com")
em = Email('295861809@qq.com', 'qxkrwbmoxosdbhfi', '295861809@qq.com', "smtp.qq.com")

error_count = 0

# step 1: 检查昨天收盘时间和状况，输入收盘价，计算各账户仓位

last_close = 25574

# step 2: 等待2：30，确定总体做单方向

cut_time = datetime.time(14, 30, 0)
while True:
    try:
        dep = sp_acc_1.get_depth(sym_s)
        if dep is False:
            log.info('两点半之前， 开始转到第二个sp账户获取深度')
            dep = sp_acc_2.get_depth(sym_s)
        ts = datetime.datetime.strptime(dep["timestamp"][2:], "%y-%m-%d %H:%M:%S").time()
        ts_1 = datetime.datetime.strptime(dep["timestamp"], "%Y-%m-%d %H:%M:%S")
        t_now = datetime.datetime.now()
        if (t_now - ts_1) > datetime.timedelta(minutes=5):
            # 报警数据不动了
            msg = 'sp 账户的获取深度接口时间不动了，请查看脚本，返回数据是{}， 当前时间为：{}'.format(dep, t_now)
            title = 'sp 深度数据不动了'
            em.send_email(message=msg, title=title)
        if ts < cut_time:
            continue
        else:
            break
    except Exception as e:
        # 邮件提醒
        error_count += 1
        em.send_email(str(e), "Error Step 2")
        log.error(e)
        if error_count >= 100:
            raise ValueError(e)
mark_price = dep["last"][0]
if mark_price < last_close:
    open_side = "buy"
else:
    open_side = "sell"
log.info(str(mark_price) + " " + open_side)
m = str(datetime.datetime.now()) + "\n"
m += "last close price: " + str(last_close) + "\n"
m += "mark price: " + str(mark_price) + "\n"
m += "open side: " + str(open_side)
em.send_email(m, "Step 2 Report")


# step 3: 等待机会下单

def open_together():
    if open_side == "buy":
        # sp_side = "buy"
        mt4_side = "OP_BUY"
    elif open_side == "sell":
        # sp_side = "sell"
        mt4_side = "OP_SELL"
    else:
        raise ValueError(open_side)
    # th_sp = MyThread(sp_acc.add_order, args=(6, sym_s, sp_side, sp_pos,))
    th_mt4 = [MyThread(mt4_acc[i].add_order, args=(sym_m[i], mt4_pos[i], mt4_side,)) for i in range(len(mt4_acc))]
    # th_sp.start()
    [th.start() for th in th_mt4]
    # th_sp.join()
    [th.join() for th in th_mt4]
    # return [th_sp.get_result(), [th.get_result() for th in th_mt4]]
    # check slippage
    th_mt4_depth = [MyThread(mt4_acc[i].get_depth, args=(str(sym_m[i]),)) for i in range(len(mt4_acc))]
    [th.start() for th in th_mt4_depth]
    [th.join() for th in th_mt4_depth]
    result = [[th.get_result() for th in th_mt4_depth]]
    log.info('account check slippage: ' + str(mt4_account_list))
    log.info('market open price : ' + str(result))
    return [[th.get_result() for th in th_mt4]], result


ret = open_together()
res_open = ret[0]
open_b1_s1 = ret[1]

m = str(datetime.datetime.now()) + "\n"
m += str(res_open)
em.send_email(m, "Step 3 Report")


def check_open_price():
    th_mt4 = [MyThread(mt4_acc[i].get_trade_order, args=()) for i in range(len(mt4_acc))]
    [th.start() for th in th_mt4]
    [th.join() for th in th_mt4]
    order_info = [[th.get_result() for th in th_mt4]]
    order_price = list()
    try:
        for i in order_info[0]:
            if i:
                order_price.append(i[0]['openPrice'])
            else:
                order_price.append(i)
        return order_price
    except Exception as e:
        print(e)
        return False


open_price = check_open_price()

# step 4: 等待第一个信号，进止盈轨道或止损平仓
close_b1_s1 = list()


def close_together():
    th_mt4 = [MyThread(mt4_acc[i].close_position, args=(str(res_open[0][i]), mt4_pos[i],)) for i in range(len(mt4_acc))]
    [th.start() for th in th_mt4]
    [th.join() for th in th_mt4]
    th_mt4_depth = [MyThread(mt4_acc[i].get_depth, args=(str(sym_m[i]),)) for i in range(len(mt4_acc))]
    [th.start() for th in th_mt4_depth]
    [th.join() for th in th_mt4_depth]
    close_result = [[th.get_result() for th in th_mt4_depth]]
    log.info('account check slippage: ' + str(mt4_account_list))
    log.info('market close price : ' + str(close_result))
    close_b1_s1 = close_result
    return [[th.get_result() for th in th_mt4]], close_result


while True:
    try:
        dep = sp_acc_1.get_depth(sym_s)
        if dep is False:
            log.info('两点半之后， 开始转到第二个sp账户获取深度')
            dep = sp_acc_2.get_depth(sym_s)
        # ts = datetime.datetime.strptime(dep["timestamp"][2:], "%y-%m-%d %H:%M:%S").time()
        ts = datetime.datetime.strptime(dep["timestamp"], "%Y-%m-%d %H:%M:%S")
        t_now = datetime.datetime.now()
        if (t_now - ts) > datetime.timedelta(minutes=5):
            # 报警数据不动了
            msg = 'sp 账户的获取深度接口时间不动了，请查看脚本，返回数据是{}， 当前时间为：{}'.format(dep, t_now)
            title = 'sp 深度数据不动了'
            em.send_email(message=msg, title=title)
        last_p = dep["last"][0]
        log.debug(last_p)
        if last_p == 0:
            raise ValueError("sp price is 0")
        if open_side == "buy":
            if last_p <= mark_price - 200:
                status = "closed"
                break
            elif last_p < mark_price + 50:
                continue
            else:
                status = "orbit"
                orbit_time = datetime.datetime.now()
                orbit_price = mark_price + 48
                break
        if open_side == "sell":
            if last_p >= mark_price + 200:
                status = "closed"
                break
            if last_p > mark_price - 50:
                continue
            else:
                status = "orbit"
                orbit_time = datetime.datetime.now()
                orbit_price = mark_price - 48
                break
    except Exception as e:
        # 邮件提醒
        error_count += 1
        em.send_email(str(e), "Error Step 4")
        log.error(e)
        if error_count >= 100:
            raise ValueError(e)

m = str(datetime.datetime.now()) + "\n"
m += "status: " + str(status) + "\n"
m += "current price: " + str(last_p)
em.send_email(m, "Step 4 Report")
# close_together()

# step 5: 破轨道平仓
if status == "closed":
    print('轨道平仓')
    while True:
        res_close = close_together()
        break_flag = True
        for i in range(len(mt4_acc)):
            if len(mt4_acc[i].order_id_list) != 0:
                break_flag = False
        if break_flag is True:
            break
    m = str(datetime.datetime.now()) + "\n"
    m += str(res_close[0])
    em.send_email(m, "Close Report")
    close_b1_s1 = res_close[1]

if status == "orbit":
    while True:
        try:
            dep = sp_acc_1.get_depth(sym_s)
            if dep is False:
                log.info('进轨道之后， 开始转到第二个sp账户获取深度')
                dep = sp_acc_2.get_depth(sym_s)
            ts = datetime.datetime.strptime(dep["timestamp"], "%Y-%m-%d %H:%M:%S")
            t_now = datetime.datetime.now()
            if (t_now - ts) > datetime.timedelta(minutes=5):
                # 报警数据不动了
                msg = 'sp 账户的获取深度接口时间不动了，请查看脚本，返回数据是{}， 当前时间为：{}'.format(dep, t_now)
                title = 'sp 深度数据不动了'
                em.send_email(message=msg, title=title)
            last_p = dep["last"][0]
            if last_p == 0:
                raise ValueError("sp price is 0")
            if open_side == "buy":
                break_price = orbit_price + int((datetime.datetime.now() - orbit_time).seconds / 900) * 10
                if last_p <= break_price:
                    res_close = close_together()
                    # while True:
                    #     res_close = close_together()
                    #     # for i in range(len(mt4_acc)):
                    #     #     if res_open[0][i] != "false":
                    #     #         if type(res_close[0][i]) == type({}) \
                    #     #                 and str(res_open[0][i]) in res_close[0][i].keys() \
                    #     #                 and res_close[0][i][str(res_open[0][i])] is True:
                    #     #             res_open[0][i] = "false"
                    #     break_flag = True
                    #     for i in range(len(mt4_acc)):
                    #         if len(mt4_acc[i].order_id_list) != 0:
                    #             break_flag = False
                    #     if break_flag is True:
                    #         break
                    m = str(datetime.datetime.now()) + "\n"
                    m += str(res_close[0]) + "\n"
                    m += "break price: " + str(break_price) + "\n"
                    m += "last price: " + str(last_p) + "\n"
                    em.send_email(m, "Orbit Report")
                    close_b1_s1 = res_close[1]
                    break
                else:
                    continue
            if open_side == "sell":
                break_price = orbit_price - int((datetime.datetime.now() - orbit_time).seconds / 900) * 10
                if last_p >= break_price:
                    res_close = close_together()
                    # while True:
                    #     res_close = close_together()
                    #     # for i in range(len(mt4_acc)):
                    #     #     if res_open[0][i] != "false":
                    #     #         if type(res_close[0][i]) == type({}) \
                    #     #                 and str(res_open[0][i]) in res_close[0][i].keys() \
                    #     #                 and res_close[0][i][str(res_open[0][i])] is True:
                    #     #             res_open[0][i] = "false"
                    #     break_flag = True
                    #     for i in range(len(mt4_acc)):
                    #         if len(mt4_acc[i].order_id_list) != 0:
                    #             break_flag = False
                    #     if break_flag is True:
                    #         break
                    m = str(datetime.datetime.now()) + "\n"
                    m += str(res_close[0]) + "\n"
                    m += "break price: " + str(break_price) + "\n"
                    m += "last price: " + str(last_p) + "\n"
                    em.send_email(m, "Orbit Report")
                    close_b1_s1 = res_close[1]
                    break
                else:
                    continue
        except Exception as e:
            # 邮件提醒
            error_count += 1
            em.send_email(str(e), "Error Step 5")
            log.error(e)
            if error_count >= 100:
                raise ValueError(e)

# step 6: 统计当日收益
