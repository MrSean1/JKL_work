# *_*coding:utf-8 *_*
import csv
import datetime
import json
import os
import threading
import time
from Log import Logger
# import pandas as pd
import requests

# account = 'DEMO201812037'
# a = Account('73883669')

product_list = ["YMH9", "HSI8", "HSIF9", "SSIH9"]


class Account:
    def __init__(self, account):
        self.log = Logger('all.log', level='debug')
        self.account = account
        self.balance = 0  # 总余额
        self.margin = 0  # 已使用保证金
        self.maintain_margin = 0  # 维持保证金
        self.buy_power = 0  # 购买力 约等于余额减去保证金
        self.pos = {}  # 当前仓位
        self.order_status = 0  # 无挂单/有挂单
        self.pos_status = 0  # 有仓位/无仓位
        self.__rest_root = 'http://47.75.194.25:8081'
        # self.__rest_root = "http://localhost:8081"
        self.login()
        self.check_all_position()
        self.get_account()
        self.get_orders()
        # self.logger = logging.getLogger(__name__)
        # for prod in product_list:
        #     self.get_depth(prod)

    # 用requests实现各种api方法
    # @staticmethod
    def __dispose_info(self, ret):
        """
        处理返回信息
        :param ret: 返回信息
        :return:
        """
        if ret['code'] == 1 and ret['data'] == '':
            return ret['msg']
        elif ret['code'] == 1 and ret['data'] != 'null':
            return ret['data']
        else:
            # print(ret)
            self.log.logger.error(ret)
            return 'error'

    def login(self):
        try:
            self.log.logger.debug(self.__rest_root + "/login/{}".format(self.account))
            ret = requests.get(self.__rest_root + "/login/{}".format(self.account), timeout=5).json()
            # print(self.__dispose_info(ret))
            self.log.logger.info(str(self.__dispose_info(ret)))
            return self.__dispose_info(ret)
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def logout(self):
        try:
            ret = requests.get(self.__rest_root + '/logout/{}'.format(self.account), timeout=5).json()
            # print(self.__dispose_info(ret))
            self.log.logger.info(self.__dispose_info(ret))
        except Exception as e:
            # print(e)
            self.log.logger.error(e)

    def get_account(self):
        """
        获取账户信息
        :return:
        """
        try:
            self.check_all_position()
            if self.pos.keys():
                for proCode in self.pos.keys():
                    self.subscription(proCode)
            ret = requests.get(self.__rest_root + "/accInfo/{}".format(self.account), timeout=5).json()
            msg = self.__dispose_info(ret)
            # print(msg)
            self.log.logger.info(msg=msg)
            if msg is not 'error':
                self.balance = msg['nav']
                self.margin = msg['iMargin']
                self.buy_power = msg['buyingPower']
                self.maintain_margin = msg['mmargin']  # 维持保证金
        except Exception as e:
            # print(e)
            self.log.logger.error(e)

    def get_orders(self):
        """
        查询未成交订单
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + '/getOrders/{}'.format(self.account), timeout=5).json()
            msg = self.__dispose_info(ret)
            if msg is not 'error' and type(msg) is list:
                order_list = [i for i in msg if i['status'] == 1]
                if order_list:
                    self.order_status = 1
                return order_list
            else:
                if msg == '没有订单':
                    self.order_status = 0
                # print(ret)
                self.log.logger.info(str(ret))
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def get_trade_order(self):
        """
        查询已成交订单
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + '/getTradeOrders/{}'.format(self.account), timeout=5).json()
            if ret == "系统没有成交单":
                ret = []
            return self.__dispose_info(ret)
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def get_order(self, order_id):
        """
        根据订单id查询
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + "/getOrder/{}/{}".format(self.account, order_id), timeout=5).json()
            return self.__dispose_info(ret)
        except Exception as e:
            self.log.logger.error(e)
            return False

    def add_order(self, order_type, prod_code, side, quantity, price=0, order_options=0, valid_type=0,
                  status=1):
        """
        下单
        :param order_type:0 限价 6市价
        :param prod_code: 商品编码
        :param side: 买卖类型
        :param quantity: 量
        :param price: 价格
        :param order_options: 默认0  有时1
        :param valid_type: 0当天有效 3直到有效期
        :param status: 1为有效单 2为无效单
        :return:
        """
        dec_dic = {'HO': 4, 'HSI': 0, 'SSI': 0, 'YM': 0}
        if prod_code[0:-2] in dec_dic.keys():
            dec_in_price = dec_dic[prod_code[0:-2]]
        else:
            # print('没有此类商品的精度')
            self.log.logger.error('没有此类商品的精度')
            raise ValueError
        if prod_code[0:-2] == "HSI":
            order_options = 1
            valid_type = 3
        params = {
            'prodCode': prod_code,
            'buySell': side,
            'qty': quantity,
            'orderOptions': order_options,
            'validType': valid_type,
            'orderType': order_type,
            'status': status,
            'userId': self.account,
            'decInPrice': dec_in_price,
        }
        if order_type == 0:
            params['price'] = price
        try:
            ret = requests.post(self.__rest_root + '/addOrder/{}'.format(self.account), json=params, timeout=5).json()
            return self.__dispose_info(ret)
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def cancel_all(self):
        """
        撤销所有订单
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + '/deleteAllOrder/{}'.format(self.account), timeout=5).json()
            # print(ret)
            self.log.logger.info(ret)
            return self.__dispose_info(ret)
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def cancel_order(self, order_id, prod_code, cl_order_id=''):
        """
        撤单
        :param order_id: 订单号
        :param prod_code: 商品种类
        :param cl_order_id: 客户id
        :return:
        """
        try:
            ret = requests.get(
                self.__rest_root + "/deleteOrder/{}/{}/{}/{}".format(self.account, order_id, prod_code, cl_order_id),
                timeout=5).json()
            return self.__dispose_info(ret)
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def check_position(self, prod_code):
        """
        查询持仓
        :param prod_code: 商品编码
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + "/pos/{}/{}".format(self.account, prod_code), timeout=5).json()
            msg = self.__dispose_info(ret)
            if chr(msg['longShort']) == 'B':
                msg['q'] = msg['qty'] + msg['longQty'] - msg['shortQty']
            elif chr(msg['longShort']) == 'S':
                msg['q'] = -msg['qty'] + msg['longQty'] - msg['shortQty']
            return msg
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def check_all_position(self):
        """
        查询全部持仓
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + '/allPos/{}'.format(self.account), timeout=5).json()
            msg = self.__dispose_info(ret)
            if msg is not 'error' and type(msg) is list:
                for i in msg:
                    if chr(i['longShort']) == 'B':
                        i['q'] = i['qty'] + i['longQty'] - i['shortQty']
                    elif chr(i['longShort']) == 'S':
                        i['q'] = -i['qty'] + i['longQty'] - i['shortQty']
                    self.pos[i['prodCode']] = {"q": i["q"]}
                status_list = list()
                for symbol in self.pos.keys():
                    for B_S in self.pos[symbol].keys():
                        status_list.append(self.pos[symbol][B_S])
                if len(set(status_list)) == 1 and list(set(status_list))[0] == 0:
                    self.pos_status = 0
                else:
                    self.pos_status = 1
                return self.pos
            else:
                return self.pos
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def subscription(self, prod_code, subscribe='price', mode=1):
        """
        订阅或取消订阅
        :param subscribe: price ticker quoteRequest
        :param prod_code: 商品编号
        :param mode: 0取消订阅 1订阅市场数据
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + "/{}/{}/{}/{}".format(subscribe, self.account, prod_code, mode),
                               timeout=5).json()
            msg = self.__dispose_info(ret)
            if msg == '订阅成功':
                # print(msg)
                self.log.logger.info(msg)
            else:
                # print(ret)
                self.log.logger.info(msg)
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def get_depth(self, prod_code):
        """
        查询市场价格深度
        :param prod_code: 商品编码
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + "/price/{}/{}".format(self.account, prod_code), timeout=5).json()
            msg = self.__dispose_info(ret)
            # print(ret)
            # print(msg)
            depth_dic = dict()
            depth_dic['bid'] = [b_price for b_price in msg['bid'] if b_price > 0]
            if not depth_dic['bid']:
                self.subscription(prod_code)
                return self.get_depth(prod_code)
            depth_dic['bidQty'] = [bidqty for bidqty in msg['bidQty'] if bidqty > 0]
            depth_dic['ask'] = [a_price for a_price in msg['ask'] if a_price > 0]
            depth_dic['askQty'] = [askqty for askqty in msg['askQty'] if askqty > 0 or 0.0]
            depth_dic['timestamp'] = msg['timestamp']
            return depth_dic
        except Exception as e:
            # print(e)
            self.log.logger.error(e)
            return False

    def write_data_for_file(self, prod_code):
        count = 1
        while True:
            try:
                ret = requests.get(self.__rest_root + "/price/{}/{}".format(self.account, prod_code), timeout=5).json()
                # print(ret)
                if ret['data']['timestamp'] == '0':
                    self.subscription(prod_code)
                    continue
                price = ret['data']['last'][0]
                quantity = ret['data']['lastQty'][0]
                timestamp = ret['data']['timestamp']
                date = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                cur_path = os.getcwd() + os.path.sep + 'data'
                file_name = date.strftime(
                    '%Y-%m-%d') + '_' + prod_code + '.csv'
                if price == 0 and quantity == 0:
                    time.sleep(1)
                    continue
                if os.path.exists(cur_path):
                    if not os.path.exists(cur_path + os.path.sep + prod_code):
                        os.mkdir(cur_path + os.path.sep + prod_code)
                else:
                    os.makedirs(cur_path + os.path.sep + prod_code)
                # data_new = [[prod_code, price, quantity, date]]
                data_new = '{}, {}, {}, {}\n'.format(prod_code, price, quantity, str(date))
                if count == 1:
                    data_old = data_new
                else:
                    if data_old == data_new:
                        # self.log.logger.info('appear same data, data_old={}, data_new={}'.format(data_old, data_new))
                        # 睡一秒再继续进行
                        time.sleep(1)
                        count += 1
                        continue
                    else:
                        data_old = data_new
                # print(curPath + os.path.sep + prodCode + os.path.sep + fileName)
                try:
                    with open(cur_path + os.path.sep + prod_code + os.path.sep + file_name, 'r') as f:
                        f.read()
                    with open(cur_path + os.path.sep + prod_code + os.path.sep + file_name, 'a+') as f:
                        f.write(data_new)
                    self.log.logger.info('save a data data_new=%s'%data_new)
                    # csv.reader(open(cur_path + os.path.sep + prod_code + os.path.sep + file_name, encoding='utf-8'))
                    # save_data = pd.DataFrame(data_new)
                    # save_data.to_csv(cur_path + os.path.sep + prod_code + os.path.sep + file_name, header=False,
                    #                  index=False, mode='a+',
                    #                  encoding='utf-8')
                except:
                    headers = "Type, Price, quantity, date\n"
                    data = headers + data_new
                    with open(cur_path + os.path.sep + prod_code + os.path.sep + file_name, 'w') as f:
                        f.write(data)
                    # save_data = pd.DataFrame(data_new)
                    # csv_headers = ['Type', 'Price', 'quantity', 'date']
                    # save_data.to_csv(cur_path + os.path.sep + prod_code + os.path.sep + file_name, header=csv_headers,
                    #                  index=False,
                    #                  mode='a+', encoding='utf-8')
                # 存储数据
            except Exception as e:
                # print(e)
                self.log.logger.error(e)
                # print(prod_code + '存储失败')
                self.log.logger.error(prod_code + '存储失败')
                break
            time.sleep(1)
            count += 1
        return False

    def get_data(self, prod_code):
        self.log.logger.info('开始抓取数据')
        th = threading.Thread(target=self.write_data_for_file, args=(prod_code,))
        th.start()

    # @staticmethod
    def get_kline(self, prod_code):
        date = datetime.datetime.now()
        cur_path = os.getcwd() + os.path.sep + 'data' + os.path.sep + prod_code + os.path.sep + date.strftime(
            '%Y-%m-%d') + '_' + prod_code + '.csv'
        if not os.path.exists(cur_path):
            # print(prod_code + '找不到当天的数据，')
            self.log.logger.warning(prod_code + '找不到当天的数据，')
            return False
        else:
            df = pd.read_csv(cur_path)
            start_time = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute)
            index_list = []
            count = 0
            for i in df['date']:
                if (start_time + datetime.timedelta(minutes=1)) > datetime.datetime.strptime(i,
                                                                                             '%Y-%m-%d %H:%M:%S') >= start_time:
                    index_list.append(count)
                    count += 1
                else:
                    count += 1
            if index_list:
                kline_data = df[min(index_list):max(index_list) + 1]
                # print(kline_data)
                kline = [kline_data['Price'][min(index_list)], max(kline_data['Price']), min(kline_data['Price']),
                         kline_data['Price'][max(index_list)], sum(kline_data['quantity']),
                         start_time.strftime('%Y-%m-%d %H:%M:%S')]
                return kline
            else:
                # print(start_time.strftime('%Y-%m-%d %H:%M:%S') + '没有抓到这一分钟的数据')
                self.log.logger.warning('没有抓到这一分钟的数据')
                return False
