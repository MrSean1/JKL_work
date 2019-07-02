# coding:utf-8
import logging

from cal_order_quantity import CalOrderQty
from mt4_account import MT4Account
from send_email import Email

em_user = '295861809@qq.com'
pwd = 'qxkrwbmoxosdbhfi'
address = ['295861809@qq.com', ]
smtp_server = 'smtp.qq.com'


class MT4AccountAddOrder(MT4Account):
    def __init__(self, account, ip,):
        MT4Account.__init__(account, ip)
        self.account = account
        self.email = Email(em_user=em_user, pwd=pwd, address=address, smtp_server=smtp_server)
        self.logger = logging.getLogger('MT4AccountAddOrder ' + str(account))
        self.calorderqty = CalOrderQty(account)


    def add_adss_order(self, order_type, symbol, position):
        if order_type == 'buy':
            order_type = 'OP_BUY'
        elif order_type == 'sell':
            order_type = 'OP_SELL'
        try:
            acc_info = self.get_account()
            if acc_info:
                balance = acc_info['balance']
            else:
                # 采用初始余额进行计算
                '''
                
                '''
                pass
        except Exception as e:
            self.logger.error('账户： ' + str(self.account) + ' ' + str(e))
        try:
            symbol_market = self.get_depth(self.symbol)
            if symbol_market:
                '''
                'minlot': msg['MINLOT'],    # 最小交易量
                'maxlot': msg['MAXLOT'],    # 最大交易量
                'lotstep': msg['LOTSTEP'],  # 交易步长
                'marginrequired': msg['MARGINREQUIRED'],    # 每手保证金
                'spead': msg['SPREAD'], # 产品的点差
                'time': msg['TIME'], # 获取数据的当前时间
                '''
                spead = symbol_market['spead']  #点差
                minlot = symbol_market['minlot']    #最小交易量
                maxlot = symbol_market['maxlot']    #最大交易量
                lotstep = symbol_market['lotstep']   #交易步长
                marginrequired = symbol_market['marginrequired']    # 每手保证金
            else:
                # 访问不到数据  采用另外一种东西获取
                pass
        except Exception as e:
            self.logger.error('账户： ' + str(self.account) + ' ' + str(e))
        # 将获取到的数据传递给分单方法，计算要下的订单
        cal_order_info = dict()
        cal_order_info['balance'] = balance
        cal_order_info['marginrequired'] = marginrequired
        cal_order_info['spead'] = spead
        cal_order_info['minlot'] = minlot
        cal_order_info['maxlot'] = maxlot
        cal_order_info['lotstep'] = lotstep
        cal_order_info['total_warehouse_position'] = position
        cal_order_info['symbol'] = symbol
        cal_order_info['order_type'] = order_type
        order_info_list = self.calorderqty.order_qty(cal_order_info)
        while order_info_list:
            order_info = order_info_list.pop(0)
            order_id = self.add_order(order_info['symbol'], order_info['volume'])
            if type(order_id) is int:
                self.logger.info('账户：{} 下单成功，id:{} 订单信息：{}'.format(self.account, order_id, order_info))
            else:
                msg = '账户：{} 下单失败，下单信息是：{} 返回值是：{}'.format(self.account, order_info, order_id)
                title = 'MT4 跟单问题'
                self.logger.error(msg)
                self.email.send_email(message=msg, title=title)


    def close_pos(self, cancel):
        # 直接调用一键平仓
        try:
            if cancel == 'cancel':
                close_pos_ret = self.close_all_position()
                for ret in close_pos_ret:
                    if list(ret.valuse())[0]:
                        continue
                    else:
                        msg = '账户：{}， 订单没有被平掉， 订单号是：{}'.format(self.account, list(ret.valuse())[0])
                        title = 'MT4 跟单问题'
                        self.logger.error(msg)
                        self.email.send_email(message=msg, title=title)
            else:
                self.logger.error('账户：{}， 参数传递不对， 传递的参数为：{}'.format(self.account, cancel))
        except Exception as e:
            self.logger.error('账户：{}， 平常接口出现问题，错误信息是：{}'.format(self.account, str(e)))
            # 此时出现问题则立刻调用狼哥平常接口，或者手动平仓