#!/usr/bin/python
# *_*coding:utf-8 *_*
import threading
import time
import pandas as pd

# from MT4.mt4_account import MT4Account
from Account.mt4_account import MT4Account
from Account.sp_account import Account


def test(account_MT4, account_SP):
    MT4 = MT4Account(account_MT4)
    SP = Account(account_SP)
    i = 1
    result = list()
    while i < 101:
        time_start = time.time()
        depth_1 = SP.get_depth('YMH9')
        if depth_1 == 'false':
            print(account_SP + 'MT4_add_order')
        sp_get_depth_1 = time.time() - time_start
        ret1 = MT4.get_depth('EURUSD')
        MT4_get_depth_1 = time.time() - time_start - sp_get_depth_1
        if ret1 == 'error':
            print(account_MT4 + 'MT4_get_depth')
            i += 1
            continue
        else:
            order_id = MT4.add_order('EURUSD', 0.01, 'OP_SELL')
            MT4_add_order = time.time() - time_start - sp_get_depth_1 - MT4_get_depth_1
            print(order_id)
            if order_id == 'error':
                print(account_MT4 + 'MT4_add_order')
                i += 1
                continue
            else:
                depth = SP.get_depth('YMH9')
                if depth == 'false':
                    print(account_SP + 'MT4_add_order')
                sp_get_depth_2 = time.time() - time_start - sp_get_depth_1 - MT4_get_depth_1 - MT4_add_order
                MT4_depth = MT4.get_depth('EURUSD')
                if MT4_depth == 'error':
                    print(account_MT4 + 'MT4_get_depth')
                MT4_get_depth_2 = time.time() - time_start - sp_get_depth_1 - MT4_get_depth_1 - MT4_add_order - sp_get_depth_2
                ret = MT4.close_position(order_id, 0.01, 0)  # 平仓
                MT4_close_positiion = time.time() - time_start - sp_get_depth_1 - MT4_get_depth_1 - MT4_add_order - sp_get_depth_2 - MT4_get_depth_2
                print(ret)
                if ret == 'error':
                    print(account_MT4 + 'MT4_close_position')
            time_end = time.time()
            time_difference = time_end - time_start
            # data_NK_HS-YM = [account, i, time_difference]
            data = [account_SP, account_MT4, sp_get_depth_1, MT4_get_depth_1, MT4_add_order, sp_get_depth_2,
                    MT4_get_depth_2, MT4_close_positiion, time_difference]
            result.append(data)
            i += 1
            break
    df = pd.DataFrame(result)
    # cvs_headers = [''sp_get_depth_1', 'MT4_get_depth_1', 'MT4_add_order', 'sp_get_depth_2', 'MT4_get_depth_2',
    #                'MT4_close_positiion', 'time_all']
    df.to_csv('abc.cvs', header=False, index=False, mode='a+', encoding='utf-8')
    print('写完了')


if __name__ == '__main__':
    account_MT4 = ["30266262", "30278465", "30275963", "30275964", "30275965"]

    th = [threading.Thread(target=test, args=(i, 'DEMO201901267A')) for i in account_MT4]
    [t.start() for t in th]
