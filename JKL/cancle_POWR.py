# *_*coding:utf-8 *_*
import sys
import os
import time

from ex_api.exchange import Exchange, MyThread
start_time = time.time()
account_info = dict()
account_info['TTEX'] = {
    'BTC': {
        'POWR': [],
    },
}
for i in range(5000, 7000):
    account_info['TTEX']['BTC']['POWR'].append(['TTEX', str(12012340001 + i), '1234Rty77899x']),
symbol = ['POWR', "BTC"]
bxx_key = account_info["TTEX"]["BTC"]['POWR']
ex_bxx = [Exchange('bxx', key) for key in bxx_key]
th_cancel_all = []
for i in range(len(ex_bxx), 0, -1):
    th_cancel_all.append(MyThread(ex_bxx[i - 1].cancel_all_bxx, args=(symbol,)))
    # ex_bxx[i - 1].cancel_all_bxx(symbol)
[th.start() for th in th_cancel_all]
[th.join() for th in th_cancel_all]
end_time = time.time()
print('&&&&&&&&&&&&&&&&&&&&&&')
print('共用%s' % (end_time-start_time))
