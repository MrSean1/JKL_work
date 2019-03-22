# *_*coding:utf-8 *_*
import time
from threading import Thread


class MyThread(Thread):
    def __init__(self, func, args=(), lag=0):
        super(MyThread, self).__init__()
        self.func = func
        self.args = args
        self.lag = lag

    def run(self):
        time.sleep(self.lag)
        while True:
            try:
                self.result = self.func(*self.args)
                if self.result is not False:
                    break
                else:
                    raise ValueError
            except Exception:
                time.sleep(1)
                continue

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None
