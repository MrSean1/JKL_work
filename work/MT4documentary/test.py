# *_*coding:utf-8 *_*
import threading
import time

while True:
    res_close = close_together()
    for i in range(len(mt4_acc)):
        if res_open[0][i] != "false":
            if type(res_close[0][i]) == type({}) \
                    and str(res_open[0][i]) in res_close[0][i].keys() \
                    and res_close[0][i][str(res_open[0][i])] is True:
                res_open[0][i] = "false"
    break_flag = True
    for i in range(len(mt4_acc)):
        if res_open[0][i] != "false":
            break_flag = False
    if break_flag is True:
        break


def close_together():
    th_mt4 = [MyThread(mt4_acc[i].close_all_position, args=()) for i in range(len(mt4_acc))]
    [th.start() for th in th_mt4]
    [th.join() for th in th_mt4]
    return [[th.get_result() for th in th_mt4]]


import threading
import time


class a:
    def __init__(self, c):
        self.c = c
        self.signal = False
        self.start_signal = False
        self.d = 0

    def b(self, d):
        if self.signal:
            # print ('执行a')
            pass
        else:
            self.d = d + 1
            # print ('执行并修改a, self.d = %s' % self.d)
            self.signal = True
            self.start_signal = True

    def g(self):
        if self.start_signal:
            self.d -= 1
            # print ('执行并修改g self.d = %s' % self.d)
            self.start_signal = False
            self.signal = False
        else:
            # print ('执行g')
            pass

a = a(1)


def refresh():
    i = 0
    while i < 1000:
        a.b(2)
        i += 1
        time.sleep(0.1)


def fallow():
    j = 0
    while j < 10000:
        a.g()
        j += 1
        time.sleep(0.01)


th_1 = threading.Thread(target=refresh, args=())
th_2 = threading.Thread(target=fallow, args=())
th_1.start()
th_2.start()
th_1.join()
th_2.join()
# time.sleep(1)
print ("结果%s" % a.d)