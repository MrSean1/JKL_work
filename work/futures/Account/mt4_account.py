#!/usr/bin/python
# *_*coding:utf-8 *_*
import logging

import requests

# account = ["30266262", "30266263", "30275963", "30275964", "30275965"]


class MT4Account:
    def __init__(self, account):
        self.account = account
        self.balance = 0  # 总余额
        self.margin = 0  # 已使用保证金
        self.buy_power = 0  # 购买力 约等于余额减去保证金
        self.equity = 0  # 账户资产净值
        self.pos = {}  # 当前仓位
        self.order_status = 0  # 无挂单/有挂单
        self.pos_status = 0  # 有仓位/无仓位
        # self.__rest_root = 'http://192.168.0.161:8989'
        self.__rest_root = 'http://47.75.194.25:8989'
        self.get_account()
        self.check_all_position()
        self.get_orders()
        self.logger = logging.getLogger(__name__)

    def get_account(self):
        """
        :return: 账户信息
        """
        try:
            ret = requests.get(self.__rest_root + '/accInfo/' + self.account, timeout=5).json()
            msg = self.__dispose_info(ret)
            if msg is not 'error':
                self.balance = msg['balance']  # 账户余额
                self.margin = msg['margin']  # 已用预付款
                self.buy_power = msg['freeMargin']  # 账户可用预付款
                self.equity = msg['equity']  # 账户资产净值
        except Exception as e:
            print(e)

    @staticmethod
    def __dispose_info(ret):
        """
        处理返回信息
        :param ret: 返回信息
        :return:
        """
        if ret['code'] == 1:
            return ret['data_NK_HS-YM']
        else:
            print(ret)
            return 'error'

    def get_orders(self):
        """
        查询未成交的订单
        :return: 未成交订单列表
        """
        try:
            ret = requests.get(self.__rest_root + '/orders/' + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
            if order_list is not 'error':
                un_bargain_order_list = [order for order in order_list if
                                         order['type']['val'] != 1 and order['type']['val'] != 0]
                if un_bargain_order_list:
                    self.order_status = 1
                else:
                    self.order_status = 0
                return un_bargain_order_list
            else:
                return 'false'
        except Exception as e:
            print(e)
            return 'false'

    def get_trade_order(self):
        """
        查询已成交订单
        0 为buy  1为sell
        :return: 已成交订单列表
        """
        try:

            ret = requests.get(self.__rest_root + '/orders/' + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
            if order_list is not 'error':
                traded_order = [order for order in order_list if order['type']['val'] == 1 or order['type']['val'] == 0]
                return traded_order
            else:
                return 'false'
        except Exception as e:
            print(e)
            return 'false'

    def get_order(self, order_id):
        """
        查询单个订单
        :param order_id: 订单id
        :return: 订单信息
        """
        try:
            ret = requests.get(self.__rest_root + '/orders/' + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
            if order_list is not 'error':
                for order in order_list:
                    if order['ticket'] == int(order_id):
                        return order
                return '没有此订单信息'
            else:
                return '没有此订单信息'
        except Exception as e:
            print(e)
            return 'false'

    def check_all_position(self):
        try:
            ret = requests.get(self.__rest_root + '/orders/' + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
            if order_list is not 'error':
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
            print(e)
            return 'false'

    def add_order(self, symbol, volume, operation=None, price=None, slippage=5, stop_loss=0, take_profit=0, magic=0,
                  last_data=None):
        '''
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
        '''
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
            ret = requests.post(self.__rest_root + '/sendOrder/' + self.account, json=parmes, timeout=5).json()
            return self.__dispose_info(ret)
        except Exception as e:
            print(e)
            return 'false'

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
            ret = requests.post(self.__rest_root + '/closeOrder/' + self.account, json=parmes, timeout=5).json()
            msg = self.__dispose_info(ret)
            return msg
        except Exception as e:
            print(e)
            return 'false'

    def close_all_position(self):
        """
        一次平掉所有已成叫订单
        :return: {订单号：true}
        """
        try:
            ret = requests.get(self.__rest_root + '/closeAll/' + self.account, timeout=5).json()
            msg = self.__dispose_info(ret)
            return msg
        except Exception as e:
            print(e)
            return "false"
        pass

    def delete_order(self, order_id):
        """
        根据订单id 删除未成交订单
        :param order_id: 订单id
        :return: true
        """
        try:
            ret = requests.get(self.__rest_root + '/delete/' + self.account + '/' + str(order_id), timeout=5).json()
            print(ret)
            return self.__dispose_info(ret)
        except Exception as e:
            print(e)
            return 'false'

    def delete_all_orders(self):
        """
        删除所有挂单
        :return:  {订单号：true}
        """
        try:
            ret = requests.get(self.__rest_root + '/orders/' + self.account, timeout=5).json()
            order_list = self.__dispose_info(ret)
        except Exception as e:
            print(e)
            order_list = 'error'
        if order_list is not 'error':
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
                return '没有挂单'
        return 'false'

    def get_depth(self, symbol):
        """
        获取交易对深度
        :param symbol: 交易对
        :return: {买一, 卖一, 时间}
        """
        try:
            ret = requests.get(self.__rest_root + '/market/' + self.account + '/' + symbol, timeout=5).json()
            msg = self.__dispose_info(ret)
            data = {
                'bid': msg['BID'],
                'ask': msg['ASK'],
                'time': msg['TIME']
            }
            return data
        except Exception as e:
            print(e)
            return 'false'
