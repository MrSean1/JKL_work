#!/usr/bin/python
# *_*coding:utf-8 *_*
import logging
from config import *
import requests


# account = ["30266262", "30266263", "30275963", "30275964", "30275965"]


class MT4Account:
    def __init__(self, account):
        self.logger = logging.getLogger(__name__)
        self.order_id_list = list()
        self.account = account
        self.balance = 0  # 总余额
        self.margin = 0  # 已使用保证金
        self.buy_power = 0  # 购买力 约等于余额减去保证金
        self.equity = 0  # 账户资产净值
        self.pos = {}  # 当前仓位
        self.order_status = 0  # 无挂单/有挂单
        self.pos_status = 0  # 有仓位/无仓位
        # self.__rest_root = 'http://47.52.254.64:8989'
        # self.__rest_root = 'http://47.244.37.23:8989'
        # self.__rest_root = 'http://47.75.194.25:8989'
        self.__rest_root = "http://localhost:8989"
        self.get_account()
        self.check_all_position()
        self.get_orders()
        self.get_trade_order()

    def get_account(self):
        """
        :return: 账户信息
        """
        try:
            ret = requests.get(self.__rest_root + mt4_account + self.account, timeout=5).json()
            msg = self.__dispose_info(ret)
            if msg:
                self.balance = msg['balance']  # 账户余额
                self.margin = msg['margin']  # 已用预付款
                self.buy_power = msg['freeMargin']  # 账户可用预付款
                self.equity = msg['equity']  # 账户资产净值
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))

    def __dispose_info(self, ret):
        """
        处理返回信息
        :param ret: 返回信息
        :return:
        """
        try:
            if ret['code'] == 1:
                return ret['data']
            else:
                self.logger.error('账号：' + str(self.account) + str(ret))
                return False
        except:
            self.logger.error('账号：' + str(self.account) + str(ret))
            return False

    def get_orders(self):
        """
        查询未成交的订单
        :return: 未成交订单列表
        """
        try:
            ret = requests.get(self.__rest_root + mt4_order + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
            if order_list:
                un_bargain_order_list = [order for order in order_list if
                                         order['type']['val'] != 1 and order['type']['val'] != 0]
                if un_bargain_order_list:
                    self.order_status = 1
                else:
                    self.order_status = 0
                return un_bargain_order_list
            else:
                return False
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            return False

    def get_trade_order(self):
        """
        查询已成交订单
        0 为buy  1为sell
        :return: 已成交订单列表
        """
        try:
            ret = requests.get(self.__rest_root + mt4_order + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
            if order_list:
                traded_order = [order for order in order_list if order['type']['val'] == 1 or order['type']['val'] == 0]
                self.order_id_list = [order_info['ticket'] for order_info in traded_order]
                return traded_order
            else:
                self.order_id_list = []
                return []
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            return False

    def get_order(self, order_id):
        """
        查询单个订单
        :param order_id: 订单id
        :return: 订单信息
        """
        try:
            ret = requests.get(self.__rest_root + mt4_order + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
            if order_list:
                for order in order_list:
                    if order['ticket'] == int(order_id):
                        return order
                return '没有此订单信息'
            else:
                return '没有此订单信息'
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            return False

    def check_all_position(self):
        try:
            ret = requests.get(self.__rest_root + mt4_order + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
            if order_list:
                self.pos = {}
                for order in order_list:
                    if order['type']['val'] in [0, 1]:
                        if order['symbol'] not in self.pos.keys():
                            self.pos[order['symbol']] = dict()
                            if order['type']['val'] == 0:
                                self.pos[order['symbol']]['buy'] = order['lots']
                            elif order['type']['val'] == 1:
                                self.pos[order['symbol']]['sell'] = order['lots']
                        else:
                            if order['type']['val'] == 1 and 'sell' not in self.pos[order['symbol']].keys():
                                self.pos[order['symbol']]['sell'] = order['lots']
                            elif order['type']['val'] == 1 and 'sell' in self.pos[order['symbol']].keys():
                                self.pos[order['symbol']]['sell'] += order['lots']
                            elif order['type']['val'] == 0 and 'buy' not in self.pos[order['symbol']].keys():
                                self.pos[order['symbol']]['buy'] = order['lots']
                            elif order['type']['val'] == 0 and 'buy' in self.pos[order['symbol']].keys():
                                self.pos[order['symbol']]['buy'] += order['lots']
                if self.pos:
                    self.pos_status = 1  # 判断有无仓位
                return self.pos
            else:
                self.pos = {}
                self.pos_status = 0  # 表示当前无仓位
                return self.pos
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            return False

    def add_order(self, symbol, volume, operation=None, price=None, slippage=5, stop_loss=0, take_profit=0, magic=0,
                  last_data=None):
        """
        :param symbol: 产品类型
        :param volume: 量
        :param operation: OP_BUY:0 OP_SELL:1 OP_BUYLIMIT:2 OP_SELLLIMIT:3 OP_BUYSTOP:4 OP_SELLSTOP:5 OP_DEPOSIT OP_CREDIT
        :param price: 价格
        :param slippage: 滑点
        :param stop_loss: 止损
        :param take_profit: 止盈
        :param magic: 默认0
        :param last_data: 截止日期
        :return: 订单编号
        """
        parmes = dict()
        if operation == 'OP_BUY' or operation == 'OP_SELL':
            if price:
                return '市价买卖不应该传递价格参数'
            else:
                parmes['operation'] = operation
                parmes['price'] = 0
        elif operation in ['OP_BUYLIMIT', 'OP_SELLLIMIT', 'OP_BUYSTOP', 'OP_SELLSTOP', 'OP_DEPOSIT', 'OP_CREDIT']:
            if not price:
                return '挂单交易应该传递价格,但是没有传递'
            else:
                parmes['operation'] = operation
                parmes['price'] = price
        else:
            return '参数传递错误'
        if last_data:
            parmes['date'] = last_data

        parmes['symbol'] = symbol
        parmes['volume'] = volume
        parmes['slippage'] = slippage
        parmes['stoploss'] = stop_loss
        parmes['takeprofit'] = take_profit
        parmes['magic'] = magic
        try:
            ret = requests.post(self.__rest_root + mt4_add_order + self.account, json=parmes, timeout=5).json()
            # print(ret)
            ret = self.__dispose_info(ret)
            if ret:
                self.order_id_list.append(ret)
                return ret
            else:
                # 返回值出错 就重新查一次已成交订单
                order_old_list = self.order_id_list
                order_new_list = self.get_trade_order()
                if order_new_list is not False:
                    if set(self.order_id_list) - set(order_old_list):
                        # 此时存在新的订单
                        return list(set(self.order_id_list) - set(order_old_list))[0]
                    else:
                        # 此时没有新的订单 添加信息失败
                        self.logger.warning('账号：' + str(self.account) + ' 此时没有新的订单加入，订单添加失败')
                        return False
                else:
                    # 查询成交单出错
                    self.logger.error('账号：' + str(self.account) + ' 查询已成交订单接口失败')
                    return False
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            # 下单接口报错  查询下已成交订单接口 确认是否已经下单成功
            order_old_list = self.order_id_list
            order_new_list = self.get_trade_order()
            if order_new_list is not False:
                if set(self.order_id_list) - set(order_old_list):
                    # 此时存在新的订单
                    return list(set(self.order_id_list) - set(order_old_list))[0]
                else:
                    # 此时没有新的订单 添加信息失败
                    self.logger.warning('账号：' + str(self.account) + ' 下单接口失败的情况下，此时仍没有新的订单加入，订单添加失败')
                    return False
            else:
                self.logger.error('账号：' + str(self.account) + ' 查询已成交订单接口失败')
                return False

    def close_position(self, order_id, volume, price=0, slippage=5, arrow_color=0):
        """
        :param order_id: 按指定价格平仓
        :param volume: 平仓数量
        :param price: 平仓价格 可以不指定
        :param slippage: 固定参数
        :param arrow_color: 固定参数
        :return: true
        """
        try:
            parmes = {
                'ticket': str(order_id),
                'lots': float(volume),
                'price': float(price),
                'slippage': slippage,
                'arrowColor': arrow_color,
            }
            ret = requests.post(self.__rest_root + mt4_close_a_order + self.account, json=parmes, timeout=5).json()
            msg = self.__dispose_info(ret)
            # 确认订单 是否被撤掉
            if msg:
                self.order_id_list.remove(int(order_id))
                return msg
            else:
                order_old_list = self.order_id_list
                order_new_list = self.get_trade_order()
                if order_new_list is not False:
                    if set(order_old_list) - set(self.order_id_list) and \
                            list(set(order_old_list) - set(self.order_id_list))[0] == int(order_id):
                        # 订单变少并且 订单号与被撤销订单号一致则撤单成功
                        return True
                    else:
                        # 该订单未被撤销
                        self.logger.error('账号：' + str(self.account) + ' 订单撤销失败')
                        return False
                else:
                    self.logger.error('账号：' + str(self.account) + ' 撤单失败后，查询已成交订单接口失败')
                    return False
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            order_old_list = self.order_id_list
            order_new_list = self.get_trade_order()
            if order_new_list is not False:
                if set(order_old_list) - set(self.order_id_list) and \
                        list(set(order_old_list) - set(self.order_id_list))[0] == int(order_id):
                    # 订单变少并且 订单号与被撤销订单号一致则撤单成功
                    return True
                else:
                    # 该订单未被撤销
                    self.logger.error('账号：' + str(self.account) + ' 撤单接口失败情况下，查询已成交订单，订单撤销失败')
                    return False
            else:
                self.logger.error('账号：' + str(self.account) + ' 撤单接口失败情况下，查询已成交订单接口失败')
                return False

    def close_all_position(self):
        """
        一次平掉所有已成叫订单
        :return: {订单号：true}
        """
        try:
            ret = requests.get(self.__rest_root + mt4_close_all_order + self.account, timeout=5).json()
            msg = self.__dispose_info(ret)
            # print(msg)
            # print(type(msg))
            # 重新进行修改
            self.order_id_list = [order_id for order_id, status in msg.items() if status is not True]
            return msg
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            order_old_list = self.order_id_list
            order_new_list = self.get_trade_order()
            if order_new_list is not False:
                if order_new_list:
                    result = [True for i in range(len(self.order_id_list))]
                    return dict(zip(self.order_id_list, result))
                else:
                    True_order = list(set(order_old_list) - set(self.order_id_list))
                    False_order = self.order_id_list
                    result_false = [False for i in range(len(False_order))]
                    result_true = [True for i in range(len(True_order))]
                    return dict(zip(True_order+False_order, result_true+result_false))
            else:
                return False

    def delete_order(self, order_id):
        """
        根据订单id 删除未成交订单
        :param order_id: 订单id
        :return: true
        """
        try:
            ret = requests.get(self.__rest_root + mt4_delete_unset_order + self.account + '/' + str(order_id),
                               timeout=5).json()
            # print(ret)
            return self.__dispose_info(ret)
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            return False

    def delete_all_orders(self):
        """
        删除所有挂单
        :return:  {订单号：true}
        """
        try:
            ret = requests.get(self.__rest_root + mt4_order + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            order_list = False
        if order_list:
            order_num_list = []
            for order in order_list:
                if order['type']['val'] not in [0, 1]:
                    order_num_list.append(order['ticket'])
            result_dict = dict()
            if order_num_list:
                for order_id in order_num_list:
                    result = self.delete_order(order_id)
                    result_dict[str(order_id)] = result
                return result_dict
            else:
                self.logger.info('账号：' + str(self.account) + ' not any order')
                return False
        return False

    def get_depth(self, symbol):
        """
        获取交易对深度
        :param symbol: 交易对
        :return: {买一, 卖一, 时间}
        """
        try:
            ret = requests.get(self.__rest_root + mt4_market_msg + self.account + '/' + symbol, timeout=5).json()
            msg = self.__dispose_info(ret)
            if msg:
                data = {
                    'bid': msg['BID'],
                    'ask': msg['ASK'],
                    'time': msg['TIME']
                }
                return data
            else:
                return False
        except Exception as e:
            self.logger.error('账号：' + str(self.account) + str(e))
            return False
