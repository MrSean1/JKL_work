import logging
import random

from mt4_config import *


# 根据下单量   随机调整需要下多少个订单
class CalOrderQty:
    def __init__(self, account):
        self.account = account
        self.logger = logging.getLogger("CalOrderQty " + str(account))

    def order_qty(self, m_order_info):
        f_order_volume = int(pos[self.account] * m_order_info['volume'])
        # add_order_count = random.randint(f_order_volume // 5, 8)
        # f_order_volume = 2
        if max(1, f_order_volume) <= 2:
            # add_order_count = 1
            # m_order_info['volume'] = max(1, f_order_volume)
            print('m_order_info:' + str(m_order_info))
            return [{'symbol': m_order_info['symbol'], 'volume': max(1, f_order_volume),
                     'order_type': m_order_info['order_type']}]
        elif f_order_volume <= 5:
            add_order_count = random.randint(1, 2)
        elif f_order_volume <= 10:
            add_order_count = random.randint(2, 4)
        elif f_order_volume <= 20:
            add_order_count = random.randint(4, 7)
        else:
            add_order_count = random.randint(4, 8)
        # add_order_count = random.randint(min(max(1, f_order_volume // 5), 6), 8)
        volume = list()
        print(add_order_count)
        fixed_proportion = add_order_count
        while add_order_count:
            if f_order_volume - sum(volume) == 0:
                break
            else:
                # volume1 = random.randint(1, f_order_volume - sum(volume))
                volume1 = random.randint(max(1, int((f_order_volume / fixed_proportion) * 0.5)),
                                         max(1, int((f_order_volume / fixed_proportion) * 1.5)))
                volume.append(volume1)
                if sum(volume) > f_order_volume:
                    volume.pop(-1)
                    volume.append(f_order_volume - sum(volume))
                    break
                elif sum(volume) == f_order_volume:
                    break
                if add_order_count == 1 and sum(volume) > f_order_volume:
                    volume.pop(-1)
                    volume.append(f_order_volume - sum(volume))
                    break
                # elif add_order_count == 1 and f_order_volume - sum(volume) <= int(
                #         (f_order_volume / add_order_count) * 0.5):
                #     volume.append(f_order_volume - sum(volume))
                elif add_order_count == 1 and sum(volume) < f_order_volume:
                    volume.pop(-1)
                    volume.append(f_order_volume - sum(volume))
            add_order_count -= 1
        # self.logger.info('副账户：{}，拆分的订单为：{}, 副账户需要下单总量：{}'.format(self.account, volume, f_order_volume))
        volume.sort()
        ret = [{'symbol': m_order_info['symbol'], 'volume': vol, 'order_type': m_order_info['order_type']} for vol in
               volume]
        return ret
