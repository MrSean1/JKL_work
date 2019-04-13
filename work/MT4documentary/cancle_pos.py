from mt4_account import MT4Account
from Mythread import MyThread

account = [
    "222057800",
    '222057801',
    '222057270',
    '222057153',
    '222057151',
    '222057274',
    '222057730',
    '222057152',
    '222057751',
    '222057745',
    '222057728',
    '222057267',
    '222057797'
]

acc = [MT4Account(acc) for acc in account]
cl_th = [MyThread(i.close_all_position, args=()) for i in acc]
[th.start() for th in cl_th]
[th.join() for th in cl_th]
[th.get_result() for th in cl_th]
