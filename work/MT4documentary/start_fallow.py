# *_*coding:utf-8 *_*
import logging
import os
import time

from send_email.send_email import Email

from Mythread import MyThread
from mt4_config import *
# from MT4documentary.MT4Account import MainAccount
# from MT4documentary.MT4Account import MainAccount
from MT4documentary import MainAccount
from MT4documentary import FallowAccount
from mt4_config import *

main_account = MainAccount(all_account['main_account'])
fallow_account_list = [FallowAccount(f_acc) for f_acc in all_account['fallow_account']]

# for foll_account in fallow_account_list:
#     pos[foll_account.account] = foll_account.balance/main_account.balance
# pwd = os.getcwd() + os.sep + 'log' + os.sep
# filename = pwd + "mt4_logs.log"


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


log = setup_logger()
log.setLevel(logging.INFO)


def refresh():
    count = 1
    while True:
        ret = main_account.check_update()
        if ret is not False:
            if count == 1:
                old_pos = ret
                signal = True
                count += 1
            else:
                if ret == old_pos:
                    # logging.info('没有变化')
                    signal = False
                    count += 1
                else:
                    logging.info("主账户订单信息发生变化")
                    old_pos = ret
                    signal = True
                    count = 2
            if signal:
                f_th = [MyThread(f_account.check_and_update, args=(ret,)) for f_account in fallow_account_list]
                [th.start() for th in f_th]
                [th.join() for th in f_th]
            time.sleep(0.5)
        elif ret is False:
            break
    msg = "主账户停掉了， 快检查程序"
    title = "MT4 跟单软件，主账户停掉了"
    Email(em_user, pwd, address, smtp_server).send_email(msg, title)
    logging.error('主账户停掉了， 赶紧检查主账户接口问题')


def fallow_order(f_account):
    while True:
        f_account.fallow_obj()
        f_account.judge_close()
        # fallow_acc.fallow_obj()
        # time.sleep(0.01)


main_th = MyThread(refresh, args=())
fallow_th = [MyThread(fallow_order, args=(f_account,)) for f_account in fallow_account_list]
main_th.start()
[f_th.start() for f_th in fallow_th]
[f_th.join() for f_th in fallow_th]
main_th.join()
