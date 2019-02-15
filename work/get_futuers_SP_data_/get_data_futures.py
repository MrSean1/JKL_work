# *_*coding:utf-8 *_*
import threading
import time

from sp_account import Account

product_list = ["YMH9", "HSIZ8", "HSIF9", "SSIH9"]


def run(prod_code):
    sp_account = Account('73883669')
    time.sleep(5)
    while True:
        ret = sp_account.write_data_for_file(prod_code)
        if ret is False:
            msg = sp_account.login()
            if msg is False:
                # 发邮件提醒
                break
            else:
                continue


def main():
    thread = [threading.Thread(target=run, args=(product,)) for product in product_list]
    [th.start() for th in thread]
    [th.join() for th in thread]


if __name__ == '__main__':
    main()
