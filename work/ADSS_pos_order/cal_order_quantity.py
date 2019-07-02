import logging
import random

import math

from mt4_config import *


# 根据下单量   随机调整需要下多少个订单
class CalOrderQty:
    def __init__(self, account):
        self.account = account
        self.logger = logging.getLogger("CalOrderQty " + str(account))

    def order_qty(self, m_order_info):
        # if m_order_info['balance'] and m_order_info['marginrequired']:
        # 账户余额以及查询市场报价接口通的话， 采用仓位变化计算下单， 否则采用之前的比例下单方式，并且需要保留几位小数
        if '.' in str(m_order_info['lotstep']):
            accuracy = len(str(m_order_info['lotstep']).split('.')[1])
            f_order_volume = round(round(
                m_order_info['balance'] / (m_order_info['marginrequired'] + m_order_info['spead']) * m_order_info[
                    'total_warehouse_position'] * 0.95, accuracy) - m_order_info['lotstep'], accuracy)
        else:
            accuracy_length = len(str(m_order_info['lotstep']))
            if accuracy_length > 1:
                f_order_volume = m_order_info['balance'] / (
                    m_order_info['marginrequired'] + m_order_info['spead']) * m_order_info['total_warehouse_position']
                f_order_volume = f_order_volume // int(math.pow(10, accuracy_length - 1)) * int(
                    math.pow(10, accuracy_length - 1))
            else:
                f_order_volume = int(
                    m_order_info['balance'] / (m_order_info['marginrequired'] + m_order_info['spead']) * m_order_info[
                        'total_warehouse_position'])
        if m_order_info['minlot']:
            pass
        else:
            m_order_info['minlot'] = 1
        f_order_volume = max(m_order_info['minlot'], f_order_volume)
        print('计算出来的总下单手数为：{}'.format(f_order_volume))
        f_order_count = f_order_volume // m_order_info['maxlot']
        # volume.sort()
        ret = [{'symbol': m_order_info['symbol'], 'volume': m_order_info['maxlot'],
                'order_type': m_order_info['order_type']} for vol in range(f_order_count)]
        f_order_col_last = f_order_volume % m_order_info['maxlot']
        if f_order_volume:
            ret.append(
                {'symbol': m_order_info['symbol'], 'volume': f_order_col_last, 'order_type': m_order_info['order_type']})
        return ret
