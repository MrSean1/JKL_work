import sys
import os
from ex_api.exchange import Exchange, MyThread
from accounts_bxx import account_info

ex_name = sys.argv[1]
print(ex_name)

process = os.popen('ps -f -C python').read().split('\n')[1:-1]
a = [i.split()[1] for i in process if ex_name in i and 'kill' not in i]
print(a)

# kill all process of exchange
for pid in a:
    try:
        os.popen('kill ' + str(pid))
    except Exception as e:
        print(e)

# cancel all orders of exchange
for sym_base in account_info[ex_name].keys():
    for sym in account_info[ex_name][sym_base].keys():
        symbol = [sym, sym_base]
        bxx_key = account_info[ex_name][sym_base][sym]
        ex_bxx = [Exchange('bxx', key) for key in bxx_key]
        th_cancel_all = []
        for i in range(len(ex_bxx), 0, -1):
            th_cancel_all.append(MyThread(ex_bxx[i - 1].cancel_all_bxx, args=(symbol,)))
            # ex_bxx[i - 1].cancel_all_bxx(symbol)
        [th.start() for th in th_cancel_all]
        [th.join() for th in th_cancel_all]
