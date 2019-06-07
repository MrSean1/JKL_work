#!/usr/bin/env python # -*- coding: utf-8 -*-
# *_*coding:utf-8 *_*
import datetime
import io
import json
import os
import logging
import random
import time

import certifi
import pycurl
import requests
from mt4_account import MT4Account

from cal_order_quantity import CalOrderQty
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
    def __init__(self, account, ip):
        MT4Account.__init__(self, account, ip)
        self.logger = logging.getLogger('MainAccount ' + str(account))
        self.count = 0

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
                        # 说明存在挂单  非市价交易订单
                        pass
                    ret[order_id] = {'volume': volume, 'symbol': symbol, 'order_type': order_type}
                    if self.count % 3 == 0:
                        self.logger.info('主账户: {} 订单信息：{}'.format(self.account, ret))
                        self.count = 1
                    else:
                        self.count += 1
                return ret
            else:
                return {}
        else:
            msg = '主账户: {}被打崩了， 赶紧手动操作，减少损失, 返回值是{}'.format(self.account, order_list)
            title = 'MT4 主账户被打崩了'
            mt4_send_email(msg=msg, title=title)
            return False


class FallowAccount:
    def __init__(self, ip):
        # MT4Account.__init__(self, account, ip)
        self.old_pos = dict()  # 主账户老的订单信息
        self.ip = ip
        self.t_start = datetime.datetime.now()
        # 第一次进入时为False 之后转为True
        self.count_signal = False  # 此信号可以判断第几次进入交易  第一次进入交易时将主账户的订单情况存储在self.ole_pos中， 用于判断仓位的变化
        self.judge_close_signal = False
        self.m_acc_add_order_info = list()  # 加仓信息
        self.total_add_order_info = list()  # 副账户总的添加订单信息
        self.m_acc_del_order_info = list()  # 平仓信息
        self.m_correspond_f_order_id = list()  # 主副账户订单对应信息
        self.logger = logging.getLogger("FallowAccount ")
        self.m_pos = 0
        self.logger_count = 0
        self.req = requests.session()
        # self.cal_order_quantity = CalOrderQty(account)

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
                else:
                    # 判断是增加订单还是减少订单
                    unusual_order_id = list(set(list(self.old_pos.keys()) + list(m_account_order_info.keys())))
                    for order_id in unusual_order_id:
                        if order_id not in self.old_pos.keys() and order_id in m_account_order_info.keys():
                            # 新增的订单
                            # 根据平台名称  及对应股票列表 判断该副账户是否需要跟单
                            # m_acc_server = m_account_order_info[order_id]['server']
                            # m_acc_symbol = m_account_order_info[order_id]['symbol']
                            self.m_acc_add_order_info.append((order_id, m_account_order_info[order_id]))
                            self.logger.info("主账户做了下单操作，品种名称为：{}，更新下单信息成功, 添加信息为：{}".format(
                                m_account_order_info[order_id]['symbol'], self.m_acc_add_order_info))
                        elif order_id in self.old_pos.keys() and order_id not in m_account_order_info.keys():
                            # 订单被撤掉
                            self.logger.info("主账户做了平仓操作")
                            self.m_acc_del_order_info.append((order_id, self.old_pos[order_id]))
                            print('ip： {}  需要删除的订单列表：{}'.format(self.ip, self.m_acc_del_order_info))
                self.old_pos = m_account_order_info
            else:
                # 第一次循环只做记录
                self.logger.info('主账户初始状态：%s' % str(m_account_order_info))
            self.count_signal = True
            self.old_pos = m_account_order_info
        except Exception as e:
            self.count_signal = True
            msg = '副账户，检查更新的方法出错，赶紧停掉程序，查看程序的问题，错误信息是：{}'.format(e)
            title = 'MT4 副账户检查更新的方法出错'
            mt4_send_email(msg=msg, title=title)
            self.logger.error(msg)

    def fallow_obj(self):
        # , '47.75.151.240'
        # ip_list = ['47.75.195.6', '47.75.151.240']
        if self.m_acc_del_order_info:
            self.logger.info('ip:{}, 开始写平仓信号'.format(self.ip))
            while self.m_acc_del_order_info:
                ret = self.m_acc_del_order_info.pop(0)
                if ret:
                    # cancle_th = [MyThread(self.send_calcle_signal, args=(ip,)) for ip in ip_list]
                    # [th.start() for th in cancle_th]
                    # [th.join() for th in cancle_th]
                    # close_result = [[th.get_result() for th in cancle_th]]
                    close_result = self.send_calcle_signal()
                    self.logger.info('发送平仓信号, 结果：{}, ip:{}'.format(str(close_result), self.ip))
                # 检查信号是否被执行完成
        elif self.m_acc_add_order_info:
            while self.m_acc_add_order_info:
                order_info = self.m_acc_add_order_info.pop(0)
                # 根据IP 进行计算获取副账户需要下什么量的订单
                self.logger.info("ip:{} 开始发送下单信号，".format(self.ip))
                # add_order_th = [MyThread(self.send_add_order_signal, args=(order_info[1], ip)) for ip in ip_list]
                # [th.start() for th in add_order_th]
                # [th.join() for th in add_order_th]
                # add_result = [[th.get_result() for th in add_order_th]]
                add_result = self.send_add_order_signal(order_info[1])
                self.logger.info('下单信号，发送结果：{}, ip:{}'.format(str(add_result), self.ip))
                delay_time = random.randint(1, 6)
                time.sleep(delay_time)
                self.logger.info('随机添加延迟时间：{}， ip:{}'.format(delay_time, self.ip))
                # 检查信号是否被执行完成
        else:
            t3 = datetime.datetime.now()
            if (t3 - self.t_start).total_seconds() % 60 < 0.02:
                self.logger.info('ip：{} ，没有收到主账户订单变化信号 时间：{}'.format(self.ip, t3))

    def send_calcle_signal(self):
        calcle = {
            'direction': 'cancle'
        }
        try:
            ret = self.req.post('http://{}:8009/share/buy_shares/'.format(self.ip), data=calcle).json()
            self.req.close()
            print(str(ret) + " ip:{}".format(self.ip))
            if ret['status'] == 0 and '写入文件成功' in ret['msg']:
                self.logger.info('信号发送成功：' + str(ret))
                try:
                    self.logger.info('等待平仓文件被删除， IP：{}'.format(self.ip))
                    ret1 = self.req.post('http://{}:8009/share/check_info/'.format(self.ip), data=calcle).json()
                    self.req.close()
                    if ret1['msg'] == '文件不存在' or ret1['msg'] == '信息不存在':
                        self.logger.info('程序执行完毕, ip:{}'.format(self.ip))
                    else:
                        self.logger.error('查询文件出错了, ip:{}'.format(self.ip))
                    return ret1
                except Exception as e:
                    self.logger.error(str(e) + " ip:{}".format(self.ip))
                    return False
            else:
                self.logger.error('发送失败，返回值是：{}, ip:{}'.format(ret, self.ip))
                msg = str(ret)
                title = '狼哥跟单，接口问题, ip:{}'.format(self.ip)
                mt4_send_email(msg=msg, title=title)
                return ret
        except Exception as e:
            self.logger.error(str(e) + " ip:{}".format(self.ip))
            msg = str(e) + " ip:{}".format(self.ip)
            title = '狼哥跟单，接口问题, ip:{}'.format(self.ip)
            mt4_send_email(msg=msg, title=title)
            return False

    def send_add_order_signal(self, add_order_info):
        add_order = dict()
        add_order['direction'] = add_order_info['order_type']
        add_order['share'] = add_order_info['symbol']
        volume = add_order_info['volume']
        # add_order['number'] = add_order_info['volume']
        add_order['number'] = self.count_pos(volume)
        try:
            ret = self.req.post('http://{}:8009/share/buy_shares/'.format(self.ip), data=add_order).json()
            self.req.close()
            print(str(ret) + " ip:{}".format(self.ip))
            if ret['status'] == 0 and '写入文件成功' in ret['msg']:
                self.logger.info('信号发送成功：{}, ip:{}'.format(ret, self.ip))
                try:
                    self.logger.info('等待文件被删除， IP：{}'.format(self.ip))
                    ret1 = self.req.post('http://{}:8009/share/check_info/'.format(self.ip), data=add_order).json()
                    self.req.close()
                    if ret1['msg'] == '文件不存在' or ret1['msg'] == '信息不存在':
                        self.logger.info('程序执行完毕, ip:{}'.format(self.ip))
                    else:
                        self.logger.error('查询文件出错了, ip:{}'.format(self.ip))
                    return ret1
                except Exception as e:
                    self.logger.error(str(e) + " ip:{}".format(self.ip))
                    return False
            else:
                self.logger.error('发送失败，返回值是{}, ip:{}'.format(ret, self.ip))
                msg = str(ret)
                title = '狼哥跟单，接口问题, ip:{}'.format(self.ip)
                mt4_send_email(msg=msg, title=title)
                return ret
        except Exception as e:
            self.logger.error(str(e) + " ip:{}".format(self.ip))
            msg = str(e) + " ip:{}".format(self.ip)
            title = '狼哥跟单，接口问题, ip:{}'.format(self.ip)
            mt4_send_email(msg=msg, title=title)
            return False

    def count_pos(self, volume):
        pos = {
            '47.75.195.6': 1,
            '47.75.151.240': 2,
            '47.75.194.25': 3,
            '47.244.37.23': 4,
            '47.75.169.118': 1,
            '47.52.244.28': 2
        }
        if self.ip in list(pos.keys()):
            ret_v = volume * pos[self.ip]
            return ret_v
        else:
            self.logger.error('账号所在IP不在列表里， IP：{}'.format(self.ip))
            return 0
    # def check(self, ret):
