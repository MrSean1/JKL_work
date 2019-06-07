# *_*coding:utf-8 *_*
import datetime
import logging
import time

from send_email.send_email import Email

from Mythread import MyThread
from mt4documentary import MainAccount, FallowAccount
from mt4_config import *
import pandas as pd

acc_info = pd.read_csv('accInfo.csv')
ate_acc_info = acc_info[acc_info['inactive'] != 1]
main_account_info = ate_acc_info[ate_acc_info['account'] == all_account['main_account']]
f_account_info = ate_acc_info[ate_acc_info['account'] != all_account['main_account']]

main_account = MainAccount(str(main_account_info['account'].item()), str(main_account_info['ip'].item()))

# fallow_account_list = [FallowAccount(str(row['account']), str(row['ip'])) for index, row in f_account_info.iterrows()]
ip_list = ['47.75.195.6', '47.75.151.240', '47.75.194.25', '47.244.37.23', '47.75.169.118', '47.52.244.28']
# ip_list = ['47.75.169.118']
fallow_account_list = [FallowAccount(ip) for ip in ip_list]


def setup_logger():
    # Prints logger info to terminal
    logging.basicConfig(
        level=logging.INFO,
        filename="./log/mt4_{}.log".format(datetime.datetime.now().date()),
        format='%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        filemode='a',
    )
    # logging.FileHandler(filename="./log/mt4_logs.log", encoding='utf-8')
    logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    sh = logging.StreamHandler()  # 往屏幕上输出
    # 屏幕输出格式
    sh.setFormatter("%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    logger.addHandler(ch)
    return logger


log = setup_logger()


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
                # fallow_account.check_and_update(ret)
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


def fallow_order(fallow_account):
    while True:
        fallow_account.fallow_obj()
        # fallow_acc.fallow_obj()
        # time.sleep(0.01)


th_r = MyThread(refresh, args=())
th_s = [MyThread(fallow_order, args=(fallow_account,)) for fallow_account in fallow_account_list]
th_r.start()
[th.start() for th in th_s]