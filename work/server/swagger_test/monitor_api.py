import time
import sys
from datetime import datetime
from threading import Thread

from account_api.Login_Controller import login_controller
from account_api.User_Market_Controller import user_market_controller
from account_api.User_Controller import user_controller
from account_api.User_Bank_Controller import user_bank_controller
from market_api.fifth_four_functions import fifth_four_functions
from market_api.fourth_four_functions import fourth_four_functions
from market_api.second_four_functions import second_four_functions
from market_api.third_four_functions import third_four_functions
from market_api.first_four_functions import first_four_functions

# '568327240@qq.com'
from send_email.write_email import WriteEmail


class MyThread(Thread):
    def __init__(self, func, args=(), lag=0):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.lag = lag

    def run(self):
        time.sleep(self.lag)
        count = 0
        while count < 10:
            try:
                self.result = self.func(*self.args)
                if self.result is not False:
                    break
                else:
                    raise ValueError
            except Exception:

                time.sleep(1)
                count += 1
                continue

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


em_user = '295861809@qq.com'
pwd = 'agagwzladccqbhce'
address = ['295861809@qq.com', 'shadow_zhulin@163.com']
smtp_server = 'smtp.qq.com'


class Monitor_api():
    def __init__(self, website):
        self.website = website

    def check_api(self):
        t = []
        for i in self.website:
            t.append(MyThread(login_controller(i).access_token()))
            t.append(MyThread(login_controller(i).login()))
            t.append(MyThread(login_controller(i).refreshToken()))
            t.append(MyThread(login_controller(i).history()))
            t.append(MyThread(user_bank_controller(i).cards()))
            t.append(MyThread(user_bank_controller(i).bank()))
            t.append(MyThread(user_bank_controller(i).bind()))
            t.append(MyThread(user_controller(i).apikey()))
            t.append(MyThread(user_controller(i).getApikey()))
            t.append(MyThread(user_controller(i).user_account()))
            t.append(MyThread(user_controller(i).authUser()))
            t.append(MyThread(user_controller(i).checkEmail()))
            t.append(MyThread(user_controller(i).checkTel()))
            t.append(MyThread(user_controller(i).checkUname()))
            t.append(MyThread(user_controller(i).cancel()))
            t.append(MyThread(user_controller(i).generate()))
            t.append(MyThread(user_controller(i).verify()))
            t.append(MyThread(user_controller(i).userinfo()))
            t.append(MyThread(user_controller(i).invitation()))
            t.append(MyThread(user_controller(i).language()))
            t.append(MyThread(user_controller(i).register()))
            t.append(MyThread(user_controller(i).setPassword()))
            t.append(MyThread(user_controller(i).setPayPassword()))
            t.append(MyThread(user_controller(i).updateEmail()))
            t.append(MyThread(user_controller(i).updateLoginPassword()))
            t.append(MyThread(user_controller(i).updatePayPassword()))
            t.append(MyThread(user_controller(i).userBase()))
            t.append(MyThread(user_market_controller(i).addFavorite()))
            t.append(MyThread(user_market_controller(i).deleteFavorite()))
            # t.append(MyThread(fifth_four_functions(i).addWorkIssue()))
            t.append(MyThread(fifth_four_functions(i).getWorkIssue()))
            # if i[0] not in ['DAPP', 'GT210', 'COINX']:
            #     t.append(MyThread(fifth_four_functions(i).getpool()))
            #     t.append(MyThread(fifth_four_functions(i).setpool()))
            #     t.append(MyThread(fifth_four_functions(i).pool_data()))
            t.append(MyThread(fifth_four_functions(i).reward_info()))
            t.append(MyThread(fifth_four_functions(i).reward_unfreeze()))
            t.append(MyThread(first_four_functions(i).accounts()))
            t.append(MyThread(first_four_functions(i).allCoin()))
            t.append(MyThread(first_four_functions(i).baseCoin()))
            t.append(MyThread(first_four_functions(i).wallet()))
            t.append(MyThread(first_four_functions(i).recharge()))
            t.append(MyThread(first_four_functions(i).recharge_record()))
            t.append(MyThread(first_four_functions(i).withdraw()))
            t.append(MyThread(first_four_functions(i).user_record()))
            t.append(MyThread(fourth_four_functions(i).trading_area()))
            t.append(MyThread(fourth_four_functions(i).trading_area_list()))
            t.append(MyThread(fourth_four_functions(i).preupload()))
            t.append(MyThread(fourth_four_functions(i).upload_callback()))
            t.append(MyThread(fourth_four_functions(i).user_account()))
            t.append(MyThread(fourth_four_functions(i).wallet_address()))
            t.append(MyThread(fourth_four_functions(i).deleteAddress()))
            t.append(MyThread(fourth_four_functions(i).getCoinAddress()))
            t.append(MyThread(second_four_functions(i).banner()))
            t.append(MyThread(second_four_functions(i).documents()))
            t.append(MyThread(second_four_functions(i).notice1()))
            t.append(MyThread(second_four_functions(i).notice2()))
            t.append(MyThread(second_four_functions(i).dealOrder()))
            t.append(MyThread(second_four_functions(i).entrustOrder()))
            t.append(MyThread(second_four_functions(i).otc_account()))
            t.append(MyThread(second_four_functions(i).buy()))
            t.append(MyThread(second_four_functions(i).buy_record()))
            t.append(MyThread(second_four_functions(i).sell()))
            t.append(MyThread(second_four_functions(i).sell_record()))
            t.append(MyThread(third_four_functions(i).sendTo()))
            t.append(MyThread(third_four_functions(i).trade_market()))
            t.append(MyThread(third_four_functions(i).home_market()))
            t.append(MyThread(third_four_functions(i).market_depth()))
            t.append(MyThread(third_four_functions(i).favorite()))
            t.append(MyThread(third_four_functions(i).getBySymbol()))
            t.append(MyThread(third_four_functions(i).kline()))
            t.append(MyThread(third_four_functions(i).realtime_ticker()))
            t.append(MyThread(third_four_functions(i).new_trades()))
            t.append(MyThread(third_four_functions(i).orderid_to_entrust()))
            t.append(MyThread(third_four_functions(i).unfinish_orderid_to_entrust()))
            t.append(MyThread(third_four_functions(i).history_orderid_to_entrust()))
        [th.start() for th in t]
        [th.join() for th in t]

    def send_all_email(self, count):
        email = WriteEmail('', '', filename='./email_msg/warn_api.txt')
        email.send(count, em_user, pwd, address, smtp_server, 'api接口')
        email.del_email()


# ['HBANK', '13120362121', 'WANG190421'],
website = [
            ['COINX', '123456', 'WANG190421'],
            ['BXX', '123456', 'WANG190421'],
            ['TTEX', '123456', 'WANG190421'],
            # ['COINFLY', '13120362121', 'WANG190421'],
            # ['DAPP', '123456', 'WANG190421'],
            # ['GT210', '123456', 'WANG190421'],
            ]
# monitor_list = ['login_controller', 'user_bank_controller', 'user_market_controller',
#                 'fifth_four_functions',
#                 'fourth_four_functions', 'third_four_functions', 'second_four_functions',
#                 'fifth_four_functions']


m = Monitor_api(website)
flag_30m = 0
count = 0
while True:
    m.check_api()
    if flag_30m % 1 == 0:
        m.send_all_email(count)
    count = (count + 1) % 2
    time.sleep(1800)
    flag_30m += 1
