# 处理rest接口访问
import requests
# 判断交易时间
import datetime
# 进行可能的相关数据分析
import numpy as np
import pandas as pd
import time
from threading import Thread

from Account import Account

import logging


# p = {
#     "userId": "73883669",
#     "accNo": "73883669",
#     "host": "f1.xyzq.com.hk",
#     "appId": "XYZQ",
#     "licence": "8871B82FB6233160",
#     "password": "qq010203"
# }
# ret=requests.post("http://bxx.pub/addUser",json=p)


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


logger = setup_logger()
logger.setLevel(logging.INFO)

# prodcut_dict = ["YMZ8", "HSIZ8", "SSIH9"]
prodcut_dict = ["YMZ8", "HSIZ8", "SSIH9", 'HOK9']


# 主账户类
# 需要从主账户获取各种信号
class MainAccount(Account):
    def __init__(self, account):
        Account.__init__(self, account)
        self.latest_trade_time = datetime.datetime.now()

    def check_update(self):
        new_l = self.get_trade_order()
        if len(new_l) == 0 or new_l == '系统没有成交单':
            self.logger.info("no order today")
            return False
        for dic in new_l:
            dic["tradeTime"] = datetime.datetime.strptime(dic["tradeTime"], "%Y-%m-%d %H:%M:%S")
        lt = new_l[-1]["tradeTime"]
        self.logger.info("latest trade time is " + str(datetime.datetime.strftime(lt, "%Y-%m-%d %H:%M:%S")))
        l = [dic for dic in new_l if dic["tradeTime"] > self.latest_trade_time]
        if len(l) == 0:
            return False
        self.latest_trade_time = lt
        self.logger.warning("new trade orders coming")
        m_price = dict()
        d_pos = dict()
        pos = dict()
        old_pos = dict(self.pos)
        dec_dic = {'HO': 4, 'HSI': 0, 'SSI': 0, 'YM': 0}
        for prod in prodcut_dict:
            count = 0
            price = 0
            if len(set([i['buySell'] for i in l if prod == i['prodCode']])) < 2:
                for order in l:
                    if prod == order['prodCode']:
                        count += 1
                        if order['buySell'] == 'buy':
                            try:
                                d_pos[prod] += order['qty']
                            except KeyError:
                                d_pos[prod] = 0
                                d_pos[prod] += order['qty']
                            try:
                                pos[prod] += order['qty']
                                self.pos[prod]['q'] += order['qty']
                            except KeyError:
                                pos[prod] = old_pos[prod]['q']
                                pos[prod] += order['qty']
                                self.pos[prod]['q'] += order['qty']
                        elif order['buySell'] == 'sell':
                            try:
                                d_pos[prod] -= order['qty']
                            except KeyError:
                                d_pos[prod] = 0
                                d_pos[prod] -= order['qty']
                            try:
                                pos[prod] -= order['qty']
                                self.pos[prod]['q'] -= order['qty']
                            except KeyError:
                                pos[prod] = old_pos[prod]['q']
                                pos[prod] -= order['qty']
                                self.pos[prod]['q'] -= order['qty']
                        price += order['price']
                if count is 0 and price is not 0:
                    if dec_dic[prod[0:-2]] == 0:
                        m_price[prod] = int(round(price/1, dec_dic[prod[0:-2]]))
                    else:
                        m_price[prod] = round(price / 1, dec_dic[prod[0:-2]])
                elif count is not 0:
                    if dec_dic[prod[0:-2]] == 0:
                        m_price[prod] = int(round(price/count, dec_dic[prod[0:-2]]))
                    else:
                        m_price[prod] = round(price / count, dec_dic[prod[0:-2]])
            else:
                self.logger.warning('orders to buy and sell in same products')
                self.check_all_position()
        if not m_price and not d_pos and not pos:
            return False
        self.logger.warning(
            "mean price: " + str(m_price) + " position difference: " + str(d_pos) + "position " + str(pos))
        return m_price, d_pos, pos

main_acc = MainAccount('DEMO201812036')

# # 主账户影子账户类
# # 之后可能需要
# class ShadowAccount(Account):
#     def __init__(self):
#         Account.__init__()
#
#
# # 跟单账户类
# # 需要跟随主账户进行下单
# class FollowAccount:
#     def __init__(self):
#         Account.__init__()
#         # 记录账户
#         self.sync_status = 0  # 是否与主账户同步
#
#
# main_acc = MainAccount()
# follow_acc = FollowAccount()  # 之后可能是一个跟单账户组，现在只做一个
#
# while True:
#     # step 1: 检查主账户
#     # 检查主账户的订单是否有更新
#     # 不管任何情况，根据实际情况更新类中的信息（持仓/余额/保证金）
#     # DEBUG：通过接口查询这些信息，进行对比，理应是一样的
#     # 判断跟单账户（组）的同步状态，由此分四种情况
#     # 若无更新且跟单账户已同步，进入下一循环
#     # 若无更新且跟单账户未同步，进入step 2
#     # 若有更新且跟单账户已同步，进入step 3
#     # 若有更新且跟单账户未同步，分多种情况，进入step 100
#
#     # step 2: 检查跟单账户
#     # 检查跟单账户订单的成交情况，若已全部成交，则将同步状态置为0，否则继续为1，也可能出现部分成交的状况
#     # 不管任何情况，根据实际情况更新类中的信息（持仓/余额/保证金）
#     # DEBUG：通过接口查询这些信息，进行对比，理应是一样的
#
#     # step 3: 跟单用户下单
#     # 根据主账户的更新情况，方向和价格是确定的
#     # 计算跟单账户应该下的量
#     # 跟单账户下单
#     # 不管任何情况，根据实际情况更新类中的信息（持仓/余额/保证金）
#     # DEBUG：通过接口查询这些信息，进行对比，理应是一样的
#     pass
