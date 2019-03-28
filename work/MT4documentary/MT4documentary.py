#!/usr/bin/env python # -*- coding: utf-8 -*-
# *_*coding:utf-8 *_*
import os
import time

from Account.mt4_account import MT4Account
from config import *
from send_email.send_email import Email
from Mythread import MyThread
import pandas as pd

'''
    跟单系统  
        1. 区分主次账户   次账户跟随主账户下单      主账户不断被扫描查找是否存在成交单
            1）有成交单  次账户跟随下单（承担不同的风险下不同的订单， 不同的风险下不同的量的订单）
            2）下单失败处理方式：
                重新下单 继续失败  标注不进行此轮操作
                重新下单成功  继续此次交易
            3）无成交单则继续扫描主账户
'''

# order_signal = 0  # 0 没有成交单 1存在成交单
# trade_order_signal_old = list()  # 存储旧的已成交订单号列表
# trade_order_signal_new = list()  # 存储新的已成交订单号列表
# # 两个记录的存在差别即出现订单被平仓
# close_out_signal = 0  # 0 没有平仓 1 出现平仓
# close_out_order = list()  # 平仓订单信息


Email = Email(em_user=em_user, pwd=pwd, address=address, smtp_server=smtp_server)


class MainAccount(MT4Account):
    def __init__(self, account):
        MT4Account.__init__(self, account)

    def check_update(self):
        order_list = self.get_trade_order()
        ret = dict()
        if order_list:
            for order in order_list:
                order_id = order['ticket']  # 订单号
                volume = order['lots']  # 订单量
                # price = order['openPrice']  # 订单价格
                symbol = order['symbol']  # 指数名称
                if order['type']['val'] == 0:
                    order_type = 'buy'
                elif order['type']['val'] == 1:
                    order_type = 'sell'
                else:
                    # 警告订单出问题了  附带账户主副信息
                    pass
                print ('主账户订单信息：', volume, symbol, order_type, order_id)
                ret[order_id] = {'volume': volume, 'symbol': symbol, 'order_type': order_type}
            return ret
        else:
            return {}


class FallowAccount(MT4Account):
    def __init__(self, account):
        MT4Account.__init__(self, account)
        self.old_pos = dict()
        self.count_signal = False  # 此信号可以判断第几次进入交易  第一次进入交易时将主账户的订单情况存储在self.ole_pos中， 用于判断仓位的变化
        # 第一次进入时为False 之后转为True
        self.m_acc_change_signal = False  # 主账户仓位改变信号
        self.m_acc_add_order_info = list()  # 加仓信息
        self.m_acc_del_order_info = list()  # 平仓信息

    # def check_account_info(self):
    #     self.get_account()
    #     balance = self.balance
    #     print('账户：{} 余额：{}'.format(self.account, balance))
    #     if self.get_trade_order():
    #         # 提醒账户存在已成交的订单  且为平掉
    #         pass

    def fallow_add_order(self, ret, slippage=5, stop_loss=0, take_profit=0, magic=0,
                         last_data=None):
        """
        :param ret: 主账户订单信息
        :param slippage: 滑点
        :param stop_loss: 止损
        :param take_profit: 止盈
        :param magic: 默认0
        :param last_data: 截止日期
        :return:
        """
        volume = ret['volume']
        symbol = ret['symbol']
        order_type = ret['order_type']
        if order_type == 'buy':
            order_type = 'OP_BUY'
        elif order_type == 'sell':
            order_type = 'OP_SELL'
        order_id = self.add_order(symbol=symbol, volume=volume, operation=order_type)
        return order_id

    def fallow_delete_order(self, order_id, volume):
        """
        平仓信号
        :return:
        """
        count = 0
        while True:
            ret = self.close_position(order_id, volume)
            if ret:
                break
            else:
                count += 1
            if count % 100 == 0:
                print ('撤单失败， account:{}, order_id:{}, volume:{}'.format(self.account, order_id, volume))
                Email.send_email(
                    message='撤单失败超过100次，account:{}, order_id:{}, volume:{}'.format(self.account, order_id, volume),
                    title='mt4 撤单失败')
        return [order_id, True]

    def get_f_account_orderinfo(self):
        """
        获取副账户的订单信息
        :return: 订单信息 字典形式
        """
        order_list = self.get_trade_order()
        ret = dict()
        if order_list:
            for order in order_list:
                order_id = order['ticket']  # 订单号
                volume = order['lots']  # 订单量
                price = order['openPrice']  # 订单价格
                symbol = order['symbol']  # 指数名称
                if order['type']['val'] == 0:
                    order_type = 'buy'
                elif order['type']['val'] == 1:
                    order_type = 'sell'
                ret[order_id] = {'volume': volume, 'symbol': symbol, 'order_type': order_type}
            return ret
        return {}

    def check_and_update(self, m_account_order_info):
        if self.count_signal:
            # 第二次循环后判断
            # 先判断主账户仓位变化情况
            if m_account_order_info == self.old_pos:
                print ('主账户仓位没有变化，不进行操作, old_pos: %s' % self.old_pos)
                # pass
            else:
                # 判断是增加订单还是减少订单
                if len(self.old_pos.keys()) > len(m_account_order_info.keys()):
                    # 主账户做了平仓操作
                    print ('主账户做了平仓操作')
                    delete_order_id_list = list()
                    for order_id in self.old_pos.keys():
                        if order_id not in m_account_order_info:
                            delete_order_id_list.append(order_id)
                    # 判断副账户需要平掉哪些订单
                    self.m_acc_del_order_info = [v for k, v in self.old_pos.items() if k in delete_order_id_list]
                    self.m_acc_change_signal = True
                    # f_order_info = self.get_f_account_orderinfo()
                    # delete_order_info = [v for k, v in self.old_pos.items() if k in delete_order_id_list]
                    # for k, v in f_order_info.items():
                    #     if v in delete_order_info:
                    #         delete_order_id = k
                    #         volume = v['volume']
                    #         ret = self.fallow_delete_order(delete_order_id, volume)
                    #         if ret is not True:
                    #             """
                    #                 报警没有平掉此订单
                    #             """
                    #             print (
                    #                 '副账户订单为平掉，账户：{}， 订单号：{} error_msg: {}'.format(self.account, delete_order_id, ret))
                    #             msg = '副账户订单为平掉，账户：{}， 订单号：{} error_msg: {}'.format(self.account, delete_order_id, ret)
                    #             title = 'MT4 跟单系统，副账户平仓失败'
                    #             Email.send_email(
                    #                 message=msg, title=title)
                    #         else:
                    #             print ('副账户订单被平掉，f_account:{}, order_id:{}'.format(self.account, delete_order_id))
                elif len(self.old_pos.keys()) < len(m_account_order_info.keys()):
                    # 主账户做了下单操作 新增订单
                    print ('主账户做了下单操作')
                    self.m_acc_change_signal = True
                    self.m_acc_add_order_info = [v for k, v in m_account_order_info.items() if
                                                 k not in self.old_pos.keys()]
                    # add_order_info_list = [v for k, v in m_account_order_info.items() if k not in self.old_pos.keys()]
                    # for order_info in add_order_info_list:
                    #     ret = self.fallow_add_order(order_info)
                    #     if type(ret) is int:
                    #         print ('副账户跟单成功, 订单编号：%s' % ret)
                    #     else:
                    #         print ('副账户跟单失败')
                    #         msg = "副账户跟单失败，账户：{}， 订单信息：{}， error_msg:{}".format(self.account, order_info, ret)
                    #         title = "MT4 跟单系统，副账户跟单失败"
                    #         Email.send_email(message=msg, title=title)
            self.old_pos = m_account_order_info
        else:
            """
            第一次循环 只需判断主副账户基本仓位情况
            """
            f_account_order_info = self.get_f_account_orderinfo()
            if f_account_order_info == m_account_order_info:
                print ('主副账户仓位一致，f_account:{}, f_order_info:{}, m_order_info: {}'.format(self.account,
                                                                                         f_account_order_info,
                                                                                         m_account_order_info))
            elif f_account_order_info and m_account_order_info:
                m_pos = [v for k, v in m_account_order_info.items()]
                f_pos = [v for k, v in f_account_order_info.items()]
                if len(m_pos) == len(f_pos):
                    if m_pos == f_pos:
                        print ('主副账户仓位一致，f_account:{}, f_order_info:{}, m_order_info: {}'.format(self.account,
                                                                                                 f_account_order_info,
                                                                                                 m_account_order_info))
                    else:
                        print ('两账户出事持仓量不一致f_account:{} m_account_order:{}, f_account_order:{}'.format(self.account,
                                                                                                       m_account_order_info,
                                                                                                       f_account_order_info))
                else:
                    print ('主副帐户出事持仓量不一致f_account:{} m_account_order:{}, f_account_order:{}'.format(self.account,
                                                                                                    m_account_order_info,
                                                                                                    f_account_order_info))
            elif not f_account_order_info or not m_account_order_info:
                print ('主副账户订单不一致 f_account: {} f_order_info: {} m_order_info: {},'.format(self.account,
                                                                                           f_account_order_info,
                                                                                           m_account_order_info))
            else:
                print ('主副账户持仓量一致, f_account: %s' % self.account)
            self.count_signal = True
            self.old_pos = m_account_order_info

    def fallow_obj(self):
        if self.m_acc_change_signal:
            # 需要做下单或者平仓操作
            if self.m_acc_del_order_info:
                # 做平仓操作
                print ('副账户开始做平仓操作')
                f_order_info = self.get_f_account_orderinfo()
                delete_order_info = list()
                for k, v in f_order_info.items():
                    if v in self.m_acc_del_order_info:
                        delete_order_info.append([k, v['volume']])
                if delete_order_info:
                    # print ('平仓订单信息。 order_id:%s' % delete_order_info[0])
                    # th_mt4 = [MyThread(self.fallow_delete_order, args=(order_id[0], order_id[1])) for order_id
                    #           in delete_order_info]
                    # [th.start() for th in th_mt4]
                    # [th.join() for th in th_mt4]
                    #
                    # for ret in [th.get_result() for th in th_mt4]:
                    #     if not ret[1]:
                    #         print ('副账户订单为平掉，账户：{ }， 订单号：{} error_msg: {}'.format(self.account, ret[0], ret))
                    #         msg = '副账户订单为平掉，账户：{}， 订单号：{} error_msg: {}'.format(self.account, ret[0], ret)
                    #         title = 'MT4 跟单系统，副账户平仓失败'
                    #         Email.send_email(message=msg, title=title)
                    #     else:
                    #         print (
                    #             '副账户订单被平掉，f_account:{}, order_id:{}, msg:{}'.format(self.account, ret[0], ret))
                    for order_info in delete_order_info:
                        ret = self.fallow_delete_order(order_id=order_info[0], volume=order_info[1])
                        if ret[1] is not True:
                            """
                                报警没有平掉此订单 
                            """
                            print (
                                '副账户订单未平掉，账户：{}， 订单号：{} error_msg: {}'.format(self.account, order_info[0], ret))
                            msg = '副账户订单未平掉，账户：{}， 订单号：{} error_msg: {}'.format(self.account, order_info[0], ret)
                            title = 'MT4 跟单系统，副账户平仓失败'
                            Email.send_email(message=msg, title=title)
                        else:
                            pwd = os.getcwd() + os.sep + 'orders_info'
                            if os.path.exists(pwd) is False:
                                os.mkdir(pwd)
                            df = pd.DataFrame(data=[[self.account, order_info[0], order_info[1], 'close_order']])
                            file_name = self.account + '.csv'
                            df.to_csv(pwd + os.sep + file_name, header=False, index=False, encoding='utf-8', mode='a+')
                            print (
                                '副账户订单被平掉，f_account:{}, order_id:{}, msg:{}'.format(self.account, order_info[0], ret))
                else:
                    print ('副账户没有可以跟随主账户撤销的订单， f_order_info:{}, m_delete_order_info：{}'.format(f_order_info,
                                                                                               self.m_acc_del_order_info))
                self.m_acc_del_order_info = list()
                self.m_acc_change_signal = False
            elif self.m_acc_add_order_info:
                print ('副账户开始做下单操作')
                for order_info in self.m_acc_add_order_info:
                    ret = self.fallow_add_order(order_info)
                    if type(ret) is int:
                        pwd = os.getcwd() + os.sep + 'orders_info'
                        if os.path.exists(pwd) is False:
                            os.mkdir(pwd)
                        df = pd.DataFrame(data=[[self.account, ret, order_info['volume'], 'add_order']])
                        file_name = self.account + '.csv'
                        df.to_csv(pwd + os.sep + file_name, header=False, index=False, encoding='utf-8', mode='a+')
                        print ('副账户跟单成功, 订单编号：%s' % ret)
                    else:
                        print ('副账户跟单失败')
                        msg = "副账户跟单失败，账户：{}， 订单信息：{}， error_msg:{}".format(self.account, order_info, ret)
                        title = "MT4 跟单系统，副账户跟单失败"
                        Email.send_email(message=msg, title=title)
                self.m_acc_add_order_info = list()
                self.m_acc_change_signal = False
            else:
                self.m_acc_change_signal = False
                print ('程序出错 信号发出 却没有可以下单和撤单的信息')
        else:
            print ('没有收到主账户订单变化信号')


# main_acc = MainAccount('30295272')
# fallow_acc = FallowAccount('30266262')
#
#
# def refresh():
#     while True:
#         ret = main_acc.check_update()
#         # if ret:
#         #     print ('副账户判断一次')
#         fallow_acc.check_and_update(ret)
#         time.sleep(0.1)
#
#
# def fallow_order():
#     while True:
#         fallow_acc.fallow_obj()
#         # time.sleep(0.01)
#
#
# main_th = MyThread(refresh, args=())
# fallow_th = MyThread(fallow_order, args=())
# main_th.start()
# fallow_th.start()
# main_th.join()
# fallow_th.join()
