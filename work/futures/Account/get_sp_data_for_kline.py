# *_*coding:utf-8 *_*
import csv
import datetime
import os
from threading import Thread

import requests
import pandas as pd
from Account.sp_account import Account


class GetDataForKline(Account):

    def get_data(self, prod_code):
        try:
            ret = requests.get(self.__rest_root + "/price/{}/{}".format(self.account, prod_code), timeout=15).json()
            price = ret['last'][0]
            quantity = ret['lastQty'][0]
            time = ret['timestamp']
            date = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            file_name = './data/' + prod_code + '/' + date.strftime('%Y/%m/%d') + '_' + prod_code + '.csv'
            if not os.path.exists('./data/' + prod_code):
                os.mkdir('./data/' + prod_code)
            data = [[prod_code, price, quantity, date]]
            try:
                csv.reader(open(file_name, encoding='utf-8'))
                save_data = pd.DataFrame(data)
                save_data.to_csv(file_name, header=False, index=False, mode='a+', encoding='utf-8')
            except Exception as e:
                save_data = pd.DataFrame(data)
                csv_headers = ['Type', 'Price', 'quantity', 'date']
                save_data.to_csv(file_name, header=csv_headers, index=False, mode='a+', encoding='utf-8')
            # 存储数据
        except Exception as e:
            print(e)
            print('存储失败')

    def get_data_f(self, prod_code):
        Thread(self.get_data(prod_code)).start()
        Thread.join()
