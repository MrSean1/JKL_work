# coding:utf-8
import logging

import pandas as pd

from Mythread import MyThread
from mt4account_add_order import MT4AccountAddOrder


class SendOrderSignal():
    def __init__(self):
        self.logger = logging.getLogger('SendOrderSignal')
        acc_info = pd.read_csv('accInfo.csv')
        ate_acc_info = acc_info[acc_info['inactive'] != 1]
        self.f_list = [MT4AccountAddOrder(row['account'], row['ip']) for index, row in ate_acc_info.iterrows()]

    def send_add_order_signal(self, order_type, symbol, position):
        mt4_th = [MyThread(f.add_adss_order, args=(order_type, symbol, position)) for f in self.f_list]
        [th.start() for th in mt4_th]
        [th.join() for th in mt4_th]

    def send_close_pos(self, cancel):
        if cancel == 'cancel':
            mt4_th = [MyThread(f.close_pos, args=()) for f in self.f_list]
            [th.start() for th in mt4_th]
            [th.join() for th in mt4_th]
        else:
            self.logger.error('参数传递不对， 传递的参数为：{}'.format(cancel))