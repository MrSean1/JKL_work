# *_*coding:utf-8 *_*
import logging
import time
from Mythread import MyThread
from mt4_config import *
# from MT4documentary.MT4Account import MainAccount
# from MT4documentary.MT4Account import MainAccount
from MT4documentary import MainAccount
from MT4documentary import FallowAccount

main_account = MainAccount(all_account['main_account'])
fallow_account_list = [FallowAccount(f_acc) for f_acc in all_account['fallow_account']]


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
        if count == 1:
            old_pos = ret
            signal = True
            count += 1
        else:
            if ret == old_pos:
                logging.info('没有变化')
                signal = False
                count += 1
            else:
                logging.info("主账户订单信息发生变化")
                old_pos = ret
                signal = True
                count = 2
        # print('主账户返回的结果' + str(ret))
        if signal:
            # if ret:
            #     print ('副账户判断一次')
            f_th = [MyThread(f_account.check_and_update, args=(ret,)) for f_account in fallow_account_list]
            [th.start() for th in f_th]
            [th.join() for th in f_th]
            # fallow_acc.check_and_update(ret)
        time.sleep(0.1)


def fallow_order(f_account):
    while True:
        f_account.fallow_obj()
        # fallow_acc.fallow_obj()
        # time.sleep(0.01)


main_th = MyThread(refresh, args=())
fallow_th = [MyThread(fallow_order, args=(f_account,)) for f_account in fallow_account_list]
main_th.start()
[f_th.start() for f_th in fallow_th]
[f_th.join() for f_th in fallow_th]
main_th.join()
