# *_*coding:utf-8 *_*
import time

from sp_account import Account

product_list = ["YMH9", "HSIZ8", "HSIF9", "SSIH9"]


def main():
    sp_account = Account('73883669')
    time.sleep(5)
    for product in product_list:
        sp_account.get_data(product)


if __name__ == '__main__':
    main()
