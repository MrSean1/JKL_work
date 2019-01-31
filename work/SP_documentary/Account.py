# *_*coding:utf-8 *_*
import json
import logging
import requests

# account = 'DEMO201812037'
prodcut_dict = [ "YMH9", "HSIZ8","HSIF9", "SSIH9"]


class Account:
    def __init__(self, account):
        self.account = account
        self.balance = 0  # 总余额
        self.margin = 0  # 已使用保证金
        self.maintain_margin = 0  # 维持保证金
        self.buy_power = 0  # 购买力 约等于余额减去保证金
        self.pos = {}  # 当前仓位
        self.order_status = 0  # 无挂单/有挂单
        self.pos_status = 0  # 有仓位/无仓位
        # self.__rest_root = 'http://bxx.pub'
        self.__rest_root = "http://localhost:8081"
        self.login()
        # self.check_all_position()
        self.get_account()
        self.get_orders()
        self.logger = logging.getLogger(__name__)
        # for prod in prodcut_dict:
        #     self.get_depth(prod)

    # 用requests实现各种api方法
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
            print(ret)
            return 'error'

    def login(self):
        try:
            ret = requests.get(self.__rest_root + "/login/{}".format(self.account), timeout=15).json()
            print(self.__dispose_info(ret))
        except Exception as e:
            print(e)

    def logout(self):
        try:
            ret = requests.get(self.__rest_root + '/logout/{}'.format(self.account), timeout=15).json()
            print(self.__dispose_info(ret))
        except Exception as e:
            print(e)

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
            ret = requests.get(self.__rest_root + "/accInfo/{}".format(self.account), timeout=15).json()
            msg = self.__dispose_info(ret)
            print(msg)
            if msg is not 'error':
                self.balance = msg['nav']
                self.margin = msg['iMargin']
                self.buy_power = msg['buyingPower']
                self.maintain_margin = msg['mmargin']  # 维持保证金
        except Exception as e:
            print(e)

    def get_orders(self):
        """
        查询未成交订单
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + '/getOrders/{}'.format(self.account), timeout=15).json()
            msg = self.__dispose_info(ret)
            if msg is not 'error' and type(msg) is list:
                order_list = [i for i in msg if i['status'] == 1]
                if order_list:
                    self.order_status = 1
                return order_list
            else:
                print(ret)
        except Exception as e:
            print(e)
            return 'false'

    def get_trade_order(self):
        """
        查询已成交订单
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + '/getTradeOrders/{}'.format(self.account), timeout=15).json()
            if ret == "系统没有成交单":
                ret = []
            return self.__dispose_info(ret)
        except Exception as e:
            print(e)
            return 'false'

    def get_order(self, order_id):
        """
        根据订单id查询
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + "/getOrder/{}/{}".format(self.account, order_id), timeout=10).json()
            return self.__dispose_info(ret)
        except Exception as e:
            print(e)
            return 'false'

    def add_order(self, orderType, prodCode, side, quantity, price=0, orderOptions=0, ValidType=0,
                  status=1):
        """
        下单
        :param orderType:0 限价 6市价
        :param prodCode: 商品编码
        :param side: 买卖类型
        :param quantity: 量
        :param price: 价格
        :param orderOptions: 默认0  有时1
        :param validType: 0当天有效 3直到有效期
        :param status: 1为有效单 2为无效单
        :return:
        """
        dec_dic = {'HO': 4, 'HSI': 0, 'SSI': 0, 'YM': 0}
        if prodCode[0:-2] in dec_dic.keys():
            decInPrice = dec_dic[prodCode[0:-2]]
        else:
            print('没有此类商品的精度')
            raise ValueError
        if prodCode[0:-2] == "HSI":
            orderOptions = 1
            ValidType = 3
        parmes = {
            'prodCode': prodCode,
            'buySell': side,
            'qty': quantity,
            'orderOptions': orderOptions,
            'validType': ValidType,
            'orderType': orderType,
            'status': status,
            'userId': self.account,
            'decInPrice': decInPrice,
        }
        if orderType == 0:
            parmes['price'] = price
        try:
            ret = requests.post(self.__rest_root + '/addOrder/{}'.format(self.account), json=parmes, timeout=15).json()
            return self.__dispose_info(ret)
        except Exception as e:
            print(e)
            return 'false'

    def cancel_all(self):
        """
        撤销所有订单
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + '/deleteAllOrder/{}'.format(self.account), timeout=15).json()
            print(ret)
            return self.__dispose_info(ret)
        except Exception as e:
            print(e)
            return 'false'

    def cancel_order(self, orderId, prodCode, clOrderId=''):
        """
        撤单
        :param orderId: 订单号
        :param prodCode: 商品种类
        :param clOrderId: 客户id
        :return:
        """
        try:
            ret = requests.get(
                self.__rest_root + "/deleteOrder/{}/{}/{}/{}".format(self.account, orderId, prodCode, clOrderId),
                timeout=15).json()
            return self.__dispose_info(ret)
        except Exception as e:
            print(e)
            return 'false'

    def check_position(self, prodCode):
        """
        查询持仓
        :param prodCode: 商品编码
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + "/pos/{}/{}".format(self.account, prodCode), timeout=15).json()
            msg = self.__dispose_info(ret)
            if chr(msg['longShort']) == 'B':
                msg['q'] = msg['qty'] + msg['longQty'] - msg['shortQty']
            elif chr(msg['longShort']) == 'S':
                msg['q'] = -msg['qty'] + msg['longQty'] - msg['shortQty']
            return msg
        except Exception as e:
            print(e)
            return 'false'

    def check_all_position(self):
        """
        查询全部持仓
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + '/allPos/{}'.format(self.account), timeout=15).json()
            msg = self.__dispose_info(ret)
            if msg is not 'error' and type(msg) is list:
                for i in msg:
                    if chr(i['longShort']) == 'B':
                        i['q'] = i['qty'] + i['longQty'] - i['shortQty']
                    elif chr(i['longShort']) == 'S':
                        i['q'] = -i['qty'] + i['longQty'] - i['shortQty']
                    self.pos[i['prodCode']] = {"q": i["q"]}
                if self.pos:
                    self.pos_status = 1  # 有仓位/无仓位
                return self.pos
            else:
                return self.pos
                # print(ret)
        except Exception as e:
            print(e)
            return 'false'

    def subscription(self, prodCode, subscribe='price', mode=1):
        """
        订阅或取消订阅
        :param subscribe: price ticker quoteRequest
        :param prodCode: 商品编号
        :param mode: 0取消订阅 1订阅市场数据
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + "/{}/{}/{}/{}".format(subscribe, self.account, prodCode, mode),
                               timeout=15).json()
            msg = self.__dispose_info(ret)
            if msg == '订阅成功':
                print(msg)
            else:
                print(ret)
        except Exception as e:
            print(e)
            return 'false'

    def get_depth(self, prodCode):
        """
        查询市场价格深度
        :param prodCode: 商品编码
        :return:
        """
        try:
            ret = requests.get(self.__rest_root + "/price/{}/{}".format(self.account, prodCode), timeout=15).json()
            msg = self.__dispose_info(ret)
            # print(msg)
            depth_dic = {}
            depth_dic['bid'] = [b_price for b_price in msg['bid'] if b_price > 0]
            if not depth_dic['bid']:
                self.subscription(prodCode)
                return self.get_depth(prodCode)
            depth_dic['bidQty'] = [bidqty for bidqty in msg['bidQty'] if bidqty > 0]
            depth_dic['ask'] = [a_price for a_price in msg['ask'] if a_price > 0]
            depth_dic['askQty'] = [askqty for askqty in msg['askQty'] if askqty > 0 or 0.0]
            depth_dic['timestamp'] = msg['timestamp']
            return depth_dic
        except Exception as e:
            print(e)
            return 'false'
