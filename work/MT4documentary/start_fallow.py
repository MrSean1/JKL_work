# *_*coding:utf-8 *_*
import time
from Mythread import MyThread
from config import *
from MT4documentary import main_acc
from MT4documentary import fallow_acc

main_account = main_acc(all_account['main_account'])
fallow_account_list = [fallow_acc(f_acc) for f_acc in all_account['fallow_account']]


def refresh():
    while True:
        ret = main_account.check_update()
        # if ret:
        #     print ('副账户判断一次')
        f_th = [MyThread(f_account.check_and_update, args=(ret, )) for f_account in fallow_account_list]
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
main_th.join()
fallow_th.join()


