# *_*coding:utf-8 *_*
import datetime


class MainAccount(Account):
    def __init__(self, account):
        Account.__init__(self, account)
        self.latest_trade_time = datetime.datetime.now()

    def check_update(self):
        new_l = self.get_trade_order()
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
        for prod in prodcut_dict:
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