#!/usr/bin/env python # -*- coding: utf-8 -*-
# *_*coding:utf-8 *_*
import datetime
import os
import time
import logging

from mt4_account import MT4Account
from mt4_config import *
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


mt4_Email = Email(em_user=em_user, pwd=pwd, address=address, smtp_server=smtp_server)


def mt4_send_email(msg, title):
    th = MyThread(mt4_Email.send_email, args=(msg, title))
    th.start()


class MainAccount(MT4Account):
    def __init__(self, account):
        MT4Account.__init__(self, account)
        self.logger = logging.getLogger(__name__)

    def check_update(self):
        order_list = self.get_trade_order()
        ret = dict()
        if order_list is not False:
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
                    ret[order_id] = {'volume': volume, 'symbol': symbol, 'order_type': order_type}
                    self.logger.info('主账户订单信息：' + str(ret))
                return ret
            else:
                return {}
        else:
            msg = '主账户被打崩了， 赶紧手动操作，减少损失, 返回值是%s' % order_list
            title = 'MT4 主账户被打崩了'
            mt4_send_email(msg=msg, title=title)
            return False


class FallowAccount(MT4Account):
    def __init__(self, account):
        MT4Account.__init__(self, account)
        self.old_pos = dict()
        self.t_start = datetime.datetime.now()
        self.count_signal = False  # 此信号可以判断第几次进入交易  第一次进入交易时将主账户的订单情况存储在self.ole_pos中， 用于判断仓位的变化
        # 第一次进入时为False 之后转为True
        self.m_acc_change_signal = False  # 主账户仓位改变信号
        self.judge_close_signal = False
        self.m_acc_add_order_info = list()  # 加仓信息
        self.m_acc_del_order_info = list()  # 平仓信息
        self.m_correspond_f_order_id = list()  # 主副账户订单对应信息
        self.logger = logging.getLogger(__name__)
        self.m_pos = 0
        self.logger_count = 0

    def fallow_add_order(self, ret, slippage=5, stop_loss=0, take_profit=0, magic=0,
                         last_data=None):
        """
        副账户下单
        :param ret: 主账户订单信息
        :param slippage: 滑点
        :param stop_loss: 止损
        :param take_profit: 止盈
        :param magic: 默认0
        :param last_data: 截止日期
        :return:
        """
        volume = round(pos[self.account] * ret['volume'])
        symbol = ret['symbol']
        order_type = ret['order_type']
        if order_type == 'buy':
            order_type = 'OP_BUY'
        elif order_type == 'sell':
            order_type = 'OP_SELL'
        order_id = self.add_order(symbol=symbol, volume=volume, operation=order_type)
        self.logger.info('下了一个订单，symblo={}, volume={}, order_type={}'.format(symbol, volume, order_type))
        return order_id

    # 需要改
    def fallow_delete_order(self, order_id, volume):
        """
        平仓操作
        :return: 订单号及平仓成功信号
        """
        count = 0
        while True:
            volume = round(pos[self.account] * volume)
            ret = self.close_position(order_id, volume)
            print('账号：{}平仓订单号：{}， 结果：{}'.format(self.account, order_id, ret))
            if ret:
                break
            else:
                count += 1
            if count % 100 == 0:
                msg = '撤单失败超过100次，account:{}, order_id:{}, volume:{}, 接口返回值：{}'.format(self.account, order_id, volume, ret)
                title = 'mt4 撤单失败'
                self.logger.error(msg)
                mt4_send_email(msg, title)
        return [order_id, True]

    # def fallow_delete_all_order(self):
    #     ret = self.close_all_position()

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

    # 判断主账户信息是否发生变动  并作出相应的操作
    def check_and_update(self, m_account_order_info):
        try:
            if self.count_signal:
                # 第二次循环后判断
                # 先判断主账户仓位变化情况
                if m_account_order_info == self.old_pos:
                    if self.logger_count % 500 == 0:
                        self.logger.info('主账户仓位没有变化，不进行操作, old_pos: %s' % self.old_pos)
                        self.logger_count = 1
                    else:
                        self.logger_count += 1
                        # pass
                else:
                    # 判断是增加订单还是减少订单
                    unusual_order_id = list(set(list(self.old_pos.keys()) + list(m_account_order_info.keys())))
                    for order_id in unusual_order_id:
                        if order_id not in self.old_pos.keys() and order_id in m_account_order_info.keys():
                            # 新增的订单
                            self.logger.info("主账户做了下单操作")
                            self.m_acc_change_signal = True
                            self.m_acc_add_order_info.append((order_id, m_account_order_info[order_id]))
                        elif order_id in self.old_pos.keys() and order_id not in m_account_order_info.keys():
                            # 订单被撤掉
                            self.logger.info("主账户做了平仓操作")
                            self.m_acc_change_signal = True
                            self.m_acc_del_order_info.append((order_id, self.old_pos[order_id]))
                self.old_pos = m_account_order_info
            else:
                """
                第一次循环 只需判断主副账户基本仓位情况
                """
                f_account_order_info = self.get_f_account_orderinfo()
                if f_account_order_info == m_account_order_info:
                    self.logger.info('主副账户仓位一致，f_account:{}, 且主副账户都没有订单'.format(self.account))
                elif f_account_order_info and m_account_order_info:
                    m_pos = [v for k, v in m_account_order_info.items()]
                    f_pos = [v for k, v in f_account_order_info.items()]
                    if len(m_pos) == len(f_pos):
                        if m_pos == f_pos:
                            self.logger.info(
                                '主副账户仓位一致，f_account:{}, f_order_info:{}, m_order_info: {}'.format(self.account,
                                                                                                  f_account_order_info,
                                                                                                  m_account_order_info))
                        else:
                            self.logger.warning(
                                '两账户出事持仓量不一致f_account:{} m_account_order:{}, f_account_order:{}'.format(self.account,
                                                                                                        m_account_order_info,
                                                                                                        f_account_order_info))
                    else:
                        self.logger.warning(
                            '主副帐户出事持仓量不一致f_account:{} m_account_order:{}, f_account_order:{}'.format(self.account,
                                                                                                     m_account_order_info,
                                                                                                     f_account_order_info))
                elif not f_account_order_info or not m_account_order_info:
                    self.logger.warning(
                        '主副账户订单不一致 f_account: {} f_order_info: {} m_order_info: {},'.format(self.account,
                                                                                            f_account_order_info,
                                                                                            m_account_order_info))
                else:
                    self.logger.info('主副账户持仓量一致, f_account: %s' % self.account)
                self.count_signal = True
                self.old_pos = m_account_order_info
        except Exception as e:
            self.count_signal = True
            msg = '副账户检查更新的方法出错，赶紧停掉程序，查看程序的问题，错误信息是：%s' % e
            title = 'MT4 副账户检查更新的方法出错'
            mt4_send_email(msg=msg, title=title)
            self.logger.error(e)

    def fallow_obj(self):
        try:
            if self.m_acc_change_signal:
                # 需要做下单或者平仓操作
                if self.m_acc_del_order_info:
                    # 做平仓操作
                    self.logger.info('副账户开始做平仓操作')
                    delete_order_info = list()
                    for f_order_del_info in self.m_acc_del_order_info:
                        f_order_id = f_order_del_info[0]
                        for m_order_id in self.m_correspond_f_order_id:
                            if f_order_id in list(m_order_id.keys()):
                                delete_order_info.append([m_order_id[f_order_id], f_order_del_info[1]['volume']])
                    if delete_order_info:
                        while delete_order_info:
                            order_info = delete_order_info.pop(0)
                            # for order_info in delete_order_info:
                            ret = self.fallow_delete_order(order_id=order_info[0], volume=order_info[1])
                            msg = "账户：{}， 平仓操作结果：{}， ".format(self.account, ret)
                            title = "MT4 跟单软件 平仓"
                            # Email.send_email(message=msg, title=title)
                            mt4_send_email(msg, title)
                            if ret[1] is not True:
                                """
                                    报警没有平掉此订单 
                                """
                                self.logger.error(
                                    '副账户订单未平掉，账户：{}， 订单号：{} error_msg: {}'.format(self.account, order_info[0], ret))
                                msg = '副账户订单未平掉，账户：{}， 订单号：{} error_msg: {}'.format(self.account, order_info[0], ret)
                                title = 'MT4 跟单系统，副账户平仓失败'
                                # Email.send_email(message=msg, title=title)
                                mt4_send_email(msg, title)
                            else:
                                # 删除掉订单对应表中记录的订单
                                print("平仓订单：{}平仓前后：{}".format(ret, str(self.m_correspond_f_order_id)))
                                for correspond_order in self.m_correspond_f_order_id:
                                    for order_m_id, order_f_id in correspond_order.items():
                                        if order_f_id == order_info[0]:
                                            self.m_correspond_f_order_id.remove(correspond_order)
                                pwd = os.getcwd() + os.sep + 'orders_info'
                                if os.path.exists(pwd) is False:
                                    os.mkdir(pwd)
                                df = pd.DataFrame(data=[[self.account, order_info[0], order_info[1], 'close_order',
                                                         datetime.datetime.now()]])
                                file_name = self.account + '.csv'
                                df.to_csv(pwd + os.sep + file_name, header=False, index=False, encoding='utf-8',
                                          mode='a+')
                                self.logger.info(
                                    '副账户订单被平掉，f_account:{}, order_id:{}, msg:{}'.format(self.account, order_info[0],
                                                                                        ret))
                    else:
                        f_order_info = self.get_f_account_orderinfo()
                        self.logger.warning(
                            '副账户没有可以跟随主账户撤销的订单， 副账户订单信息：f_order_info:{}, 主账户删除订单信息：m_delete_order_info：{}, \
                            对应订单记录表m_correspond_f_order_id：{}'.format(f_order_info, self.m_acc_del_order_info,
                                                                      self.m_correspond_f_order_id))
                    self.m_acc_del_order_info = list()
                    self.m_acc_change_signal = False
                elif self.m_acc_add_order_info:
                    self.logger.info('副账户开始做下单操作')
                    while self.m_acc_add_order_info:
                        order_info = self.m_acc_add_order_info.pop(0)
                        f_order_id = self.fallow_add_order(order_info[1])
                        # for order_info in self.m_acc_add_order_info:
                        #     f_order_id = self.fallow_add_order(order_info[1])
                        msg = '账户：{}， 跟单账户所下订单：{},'.format(self.account, f_order_id)
                        title = "MT4 跟单系统跟单情况"
                        # Email.send_email(message=msg, title=title)
                        mt4_send_email(msg, title)
                        if type(f_order_id) is int:
                            print('下单ID:' + str(f_order_id))
                            self.m_correspond_f_order_id.append({order_info[0]: f_order_id})
                            print("下单后" + str(self.m_correspond_f_order_id))
                            pwd = os.getcwd() + os.sep + 'orders_info'
                            if os.path.exists(pwd) is False:
                                os.mkdir(pwd)
                            df = pd.DataFrame(data=[[self.account, f_order_id, order_info[1]['volume'], 'add_order',
                                                     datetime.datetime.now()]])
                            file_name = self.account + '.csv'
                            df.to_csv(pwd + os.sep + file_name, header=False, index=False, encoding='utf-8', mode='a+')
                            self.logger.info('副账户跟单成功, 订单编号：%s' % f_order_id)
                            self.judge_close_signal = True
                        else:
                            self.logger.error('副账户跟单失败')
                            msg = "副账户跟单失败，账户：{}， 订单信息：{}， error_msg:{}".format(self.account, order_info, f_order_id)
                            title = "MT4 跟单系统，副账户跟单失败"
                            # Email.send_email(message=msg, title=title)
                            mt4_send_email(msg, title)
                    # self.m_acc_add_order_info = list()
                    self.m_acc_change_signal = False
                else:
                    self.m_acc_change_signal = False
                    self.logger.critical('程序出错 信号发出 却没有可以下单和撤单的信息')
                    msg = '程序出错 信号发出 却没有可以下单和撤单的信息，主账户信号：m_acc_change_signal={}， \
                          主账户下单信息：m_acc_add_order_info={}， 主账户平常信息表：m_acc_del_order_info={}'.format(
                        self.m_acc_change_signal, self.m_acc_add_order_info, self.m_acc_del_order_info)
                    title = "mt4, 跟单软件程序出错"
                    # Email.send_email(message=msg, title="mt4, 跟单软件程序出错")
                    mt4_send_email(msg, title)
            else:
                t3 = datetime.datetime.now()
                if (t3 - self.t_start).total_seconds() % 60 < 0.02:
                    self.logger.info(
                        '没有收到主账户订单变化信号' + str(t3) + " " + str(self.t_start) + " " + str((t3 - self.t_start).seconds))
        except Exception as e:
            self.m_acc_add_order_info = list()
            self.m_acc_del_order_info = list()
            self.m_acc_change_signal = False
            msg = '跟单方法出错，赶紧停掉程序改为手动， 方法名：fallow_obj， 错误信息是%s' % e
            title = "MT4 跟单方法出错"
            mt4_send_email(msg=msg, title=title)
            self.logger.error(e)

    # 风控
    def judge_close(self):
        if self.judge_close_signal:
            trader_order_info = self.get_trade_order()
            if trader_order_info is not False:
                if trader_order_info and self.m_correspond_f_order_id:
                    f_order_id = list()
                    for m_f_order_id_dict in self.m_correspond_f_order_id:
                        f_order_id.append(list(m_f_order_id_dict.values())[0])
                    while trader_order_info:
                        order_info = trader_order_info.pop(0)
                        if order_info['ticket'] in f_order_id:
                            # if order_info['type']['val'] == 0:
                            #     order_type = 'buy'
                            # elif order_info['type']['val'] == 1:
                            #     order_type = 'sell'
                            lost_limit = (order_info['closePrice'] - order_info['openPrice']) / order_info['openPrice']
                            if order_info['type']['val'] == 1 and lost_limit > 0.02:
                                self.logger.info('开始平仓')
                                # 买跌 涨幅超过1% 启动平仓机制
                                lost_ret = self.fallow_delete_order(order_id=order_info['ticket'],
                                                                    volume=order_info['lots'])
                                if lost_ret[1]:
                                    msg = 'Mt4 美股跟单账户，到达止损点，强行平仓。平仓账户：{}，跟单账户订单号：{}， 开仓价格：{}，\
                                          强行平仓时的价格：{}'.format(self.account, order_info['ticket'],
                                                              order_info['openPrice'], order_info['closePrice'])
                                    title = "mt4, 跟单软件强制平仓"
                                    self.logger.warning(msg)
                                    pwd = os.getcwd() + os.sep + 'orders_info'
                                    if os.path.exists(pwd) is False:
                                        os.mkdir(pwd)
                                    df = pd.DataFrame(data=[[self.account, order_info['ticket'], order_info['lots'],
                                                             'constraint_close_order', datetime.datetime.now()]])
                                    file_name = self.account + '.csv'
                                    df.to_csv(pwd + os.sep + file_name, header=False, index=False, encoding='utf-8',
                                              mode='a+')
                                    for i in self.m_correspond_f_order_id:
                                        if list(i.values())[0] == order_info['ticket']:
                                            self.m_correspond_f_order_id.remove(i)
                                    self.judge_close_signal = False
                                    mt4_send_email(msg=msg, title=title)
                            elif order_info['type']['val'] == 0 and lost_limit < -0.02:
                                # 买涨 跌幅超过1% 启动平仓
                                lost_ret = self.fallow_delete_order(order_id=order_info['ticket'],
                                                                    volume=order_info['lots'])
                                if lost_ret[1]:
                                    msg = 'Mt4 美股跟单账户，到达止损点，强行平仓。平仓账户：{}，跟单账户订单号：{}， 开仓价格：{}，\
                                          强行平仓时的价格：{}'.format(self.account, order_info['ticket'],
                                                              order_info['openPrice'], order_info['closePrice'])
                                    title = "mt4, 跟单软件强制平仓"
                                    self.logger.warning(msg)
                                    mt4_send_email(msg=msg, title=title)
                                    pwd = os.getcwd() + os.sep + 'orders_info'
                                    if os.path.exists(pwd) is False:
                                        os.mkdir(pwd)
                                    df = pd.DataFrame(
                                        data=[[self.account, order_info['ticket'], order_info['lots'],
                                               'constraint_close_order', datetime.datetime.now()]])
                                    file_name = self.account + '.csv'
                                    df.to_csv(pwd + os.sep + file_name, header=False, index=False, encoding='utf-8',
                                              mode='a+')
                                    # 删除主副订单编号关联 变量
                                    for i in self.m_correspond_f_order_id:
                                        if list(i.values())[0] == order_info['ticket']:
                                            self.m_correspond_f_order_id.remove(i)
                                self.judge_close_signal = False
                            else:
                                self.logger.info('没有达到强制平仓要求')
                        else:
                            self.logger.info(
                                '账户：{}， 订单号：{}， 此订单不在跟单列表中不做强制平仓处理'.format(self.account, order_info['ticket']))
                else:
                    msg = '收到副账户已下单信号但是没有查到副账户成交单信息, 副账户查询返回值：{}，主副账户关联订单号{}'.format(trader_order_info,
                                                                                     self.m_correspond_f_order_id)
                    title = 'MT4 跟单 风控问题'
                    mt4_send_email(msg=msg, title=title)
                    self.logger.info(msg)
            else:
                # 接口爆掉了
                msg = '副账户，查询成交订单接口被打爆，将停止该账户：{}订单的风控 接口返回信息是：{}'.format(self.account, trader_order_info)
                title = "MT4 跟单 副账户接口被刷爆"
                mt4_send_email(msg=msg, title=title)
                self.logger.error(msg)
                self.judge_close_signal = False
        else:
            t2 = datetime.datetime.now()
            if (t2 - self.t_start).total_seconds() % 60 < 0.02:
                self.logger.info('副账户现在没有开始跟单, 时间差是' + str(t2) + " " + str(self.t_start) + " " + str(
                    (t2 - self.t_start).seconds))
                # except Exception as e:
                #     self.judge_close_signal = False  # 这一步出错就将更空单信号修改为False 不进行判断平仓
                #     msg = '风控方法出现问题，赶紧进行修改，错误信息是：%s' % e
                #     title = 'MT4 风控方法出现问题'
                #     mt4_send_email(msg=msg, title=title)
                #     self.logger.error('风控方法出现错误，赶紧修改，错误信息是：%e' % e)
