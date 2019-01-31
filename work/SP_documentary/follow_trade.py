# 处理rest接口访问
import requests
# 判断交易时间
import datetime
# 进行可能的相关数据分析
# import numpy as np
# import pandas as pd
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

product_dict = ["YMH9", "HSIZ8","HSIF9", "SSIH9"]


# 主账户类
# 需要从主账户获取各种信号
class MainAccount(Account):
    def __init__(self, account):
        Account.__init__(self, account)
        self.latest_trade_time = datetime.datetime.now()

    def check_update(self):
        new_l = self.get_trade_order()
        if new_l == "系统没有成交单":
            new_l = []
        if len(new_l) == 0:
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
        old_pos = dict(self.pos)
        self.check_all_position()
        d_pos = dict()
        pos = dict()
        for prod in product_dict:
            if prod in old_pos.keys():
                old_q = old_pos[prod]["q"]
            else:
                old_q = 0
            if prod in self.pos.keys():
                new_q = self.pos[prod]["q"]
            else:
                new_q = 0
            if new_q - old_q != 0:
                d_pos[prod] = new_q - old_q
                pos[prod] = new_q
                dep = self.get_depth(prod)
                m_price[prod] = (dep["bid"][0] + dep["ask"][0]) / 2
        self.logger.warning(
            "mean price: " + str(m_price) + " position difference: " + str(d_pos) + "position " + str(pos))
        return m_price, d_pos, pos


# 主账户影子账户类
# 之后可能需要
class ShadowAccount(Account):
    def __init__(self, account):
        Account.__init__(self, account)


# 跟单账户类
# 需要跟随主账户进行下单
class FollowAccount(Account):
    def __init__(self, account):
        Account.__init__(self, account)
        self.pos_obj = {}
        for prod in product_dict:
            self.pos_obj[prod] = {
                "q": 0,
                "price": 0,
                "win": 0,
                "lose": 0
            }
        self.pos = {}
        for prod in product_dict:
            self.pos[prod] = {
                "q": 0
            }
        self.check_all_position()
        self.margin_dict = {
            "HSIZ8": 110000,
            "HSIF9": 110000,
            "YMH9": 45000,
            "SSIZ8": 45000
        }

    # 将pos_obj与主账户的仓位状况同步
    def refresh_object_naive(self, ret):
        # self.get_account()
        # self.check_all_position()
        m_price = ret[0]
        d_pos = ret[1]
        pos = ret[2]
        pos_obj = dict()
        for prod in m_price.keys():
            pos_obj[prod] = dict()
            pos_obj[prod]["q"] = int(pos[prod] * 1.5)
            if pos[prod] > 0:
                pos_obj[prod]["price"] = m_price[prod] + 5
                pos_obj[prod]["win"] = 100000
                pos_obj[prod]["lose"] = m_price[prod] - 200
            elif pos[prod] < 0:
                pos_obj[prod]["price"] = m_price[prod] - 5
                pos_obj[prod]["win"] = 0
                pos_obj[prod]["lose"] = m_price[prod] + 200
            else:
                pos_obj[prod]["price"] = m_price[prod]
                pos_obj[prod]["win"] = 0
                pos_obj[prod]["lose"] = 0
            self.pos_obj[prod] = dict(pos_obj[prod])
            self.logger.warning("refresh obj: " + str(pos_obj[prod]))

    def follow_object(self):
        self.check_all_position()
        self.logger.info("position checked")
        for prod in product_dict:
            # 判断是否存在仓位差
            if prod in self.pos.keys():
                pos_cur = self.pos[prod]['q']
            else:
                pos_cur = 0
            pos_diff = self.pos_obj[prod]['q'] - pos_cur
            self.logger.info(str(prod) + " diff: " + str(pos_diff))
            # 若未到达目标仓位，则判断价格是否合适；若是，则跟单
            if pos_diff != 0:
                if pos_diff > 0:
                    side = 'buy'
                else:
                    side = 'sell'
                # 判断价格是否合适
                depth = self.get_depth(prod)
                fp = False
                if side == 'buy':
                    if depth['ask'][0] <= self.pos_obj[prod]['price']:
                        fp = True
                        tp = depth['ask'][-1]
                else:
                    if depth['bid'][0] >= self.pos_obj[prod]['price']:
                        fp = True
                        tp = depth['bid'][-1]
                if fp is True:
                    # 下单
                    tq = min(depth["askQty"][0], depth["bidQty"][0], abs(pos_diff))
                    # 市价
                    # self.add_order(6, prod, side, tq)
                    # 限价
                    self.add_order(0, prod, side, tq, tp)
                    self.logger.warning(
                        "Open: " + str(side) + " " + str(tq) + " " + str(prod) + " at better price than " + str(
                            self.pos_obj[prod]['price']))
                    self.cancel_all()
                    time.sleep(0.5)
            # 计算新的平仓条件
            # 判断是否满足平仓条件；若是，则按照价格平一单，并将目标仓位绝对值减小一，目标价格置成最小或最大
            # self.check_all_position()
            if prod in self.pos.keys() and self.pos[prod]['q'] != 0:
                self.check_all_position()
                depth = self.get_depth(prod)
                mean_price = 1 / 2 * (depth['bid'][0] + depth['ask'][0])
                dec_flag = False
                if self.pos[prod]['q'] > 0:
                    if mean_price >= self.pos_obj[prod]['win'] or mean_price <= self.pos_obj[prod]['lose']:
                        dec_flag = True
                        if self.pos_obj[prod]["q"] > self.pos[prod]['q'] - 1:
                            self.pos_obj[prod]['q'] = self.pos[prod]['q'] - 1
                            self.pos_obj[prod]['price'] = mean_price * 0.9
                        tq = min(depth["askQty"][0], depth["bidQty"][0], self.pos[prod]["q"])
                        # self.add_order(6, prod, 'sell', 1)
                        self.add_order(0, prod, 'sell', 1, depth['bid'][-1])
                        self.logger.warning(
                            "Close: " + "sell" + " " + str(tq) + " " + str(
                                prod) + " at better price than " + str(mean_price))
                        self.cancel_all()
                elif self.pos[prod]['q'] < 0:
                    if mean_price <= self.pos_obj[prod]['win'] or mean_price >= self.pos_obj[prod]['lose']:
                        dec_flag = True
                        if self.pos_obj[prod]["q"] < self.pos[prod]['q'] + 1:
                            self.pos_obj[prod]['q'] = self.pos[prod]['q'] + 1
                            self.pos_obj[prod]['price'] = mean_price * 1.1
                        tq = min(depth["askQty"][0], depth["bidQty"][0], -self.pos[prod]["q"])
                        # self.add_order(6, prod, 'buy', 1)
                        self.add_order(0, prod, 'buy', 1, depth['ask'][-1])
                        self.logger.warning(
                            "Close: " + "buy " + " " + str(tq) + " " + str(
                                prod) + " at better price than " + str(mean_price))
                        self.cancel_all()


# main_acc = MainAccount('DEMO201812036')
# follow_acc = FollowAccount('DEMO201812037')  # 之后可能是一个跟单账户组，现在只做一个

main_acc = MainAccount('73883259')
follow_acc = FollowAccount('73883669')  # 之后可能是一个跟单账户组，现在只做一个


def refresh():
    while True:
        try:
            ret = main_acc.check_update()
            if ret:
                follow_acc.refresh_object_naive(ret)
            else:
                time.sleep(0.1)
        except Exception as e:
            print(e)
            main_acc.login()
            follow_acc.login()


def follow():
    while True:
        try:
            follow_acc.follow_object()
        except Exception as e:
            print(e)
            follow_acc.login()


main_acc.check_all_position()
follow_acc.check_all_position()
# follow_acc.pos_obj["YMZ8"] = {"q": 12, "price": 24202, "win": 100000, "lose": 24000}

th_refresh = Thread(target=refresh, args=())
th_follow = Thread(target=follow, args=())

th_refresh.start()
th_follow.start()

# follow_acc1.pos_obj["SSIH9"] = {
#     "q": -15,
#     "price": 21792.5,
#     "win": 0,
#     "lose": 21992.5
# }
#
# follow_acc1.add_order(0, "SSIH9", "buy", 1, )
#
# follow_acc1.add_order(0, "YMZ8", "buy", 1, 24600)
#
# follow_acc1.add_order(0, "HSIZ8", "buy", 1, 24600)
#
#
# def test():
#     while True:
#         # follow_acc1.follow_object()
#         main_acc1.check_update()
#         # main_acc.check_update()
#
#
# th_test = Thread(target=test, args=())
# th_test.start()
#
# th_test1 = Thread(target=test, args=())
# th_test1.start()
#
# th_test2 = Thread(target=test, args=())
# th_test2.start()
logger.setLevel(logging.INFO)
logger.setLevel(logging.WARNING)

# step 1: 检查主账户
# 检查主账户的订单是否有更新
# 不管任何情况，根据实际情况更新类中的信息（持仓/余额/保证金）
# DEBUG：通过接口查询这些信息，进行对比，理应是一样的
# 判断跟单账户（组）的同步状态，由此分四种情况
# 若无更新且跟单账户已同步，进入下一循环
# 若无更新且跟单账户未同步，进入step 2
# 若有更新且跟单账户已同步，进入step 3
# 若有更新且跟单账户未同步，分多种情况，进入step 100

# step 2: 检查跟单账户
# 检查跟单账户订单的成交情况，若已全部成交，则将同步状态置为0，否则继续为1，也可能出现部分成交的状况
# 不管任何情况，根据实际情况更新类中的信息（持仓/余额/保证金）
# DEBUG：通过接口查询这些信息，进行对比，理应是一样的

# step 3: 尝试与主账户同步
# step 3.1: 若
# 根据主账户的更新情况，方向和价格是确定的
# 计算跟单账户应该下的量
# 跟单账户下单
# 不管任何情况，根据实际情况更新类中的信息（持仓/余额/保证金）
# DEBUG：通过接口查询这些信息，进行对比，理应是一样的

# 检查主账户更新的订单
# 若有更新，则更新子账户的目标仓位
# 检查子账户是否与目标仓位同步
# 若未同步，则试图同步
# 若已同步，检查是否达到平仓条件
# 若已达到，则开始快速平仓
