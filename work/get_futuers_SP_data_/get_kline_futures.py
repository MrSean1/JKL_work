# *_*coding:utf-8 *_*
import datetime
import os

from Log import Logger

log = Logger('./log/get_kline_futures.log')


class GetKline:
    def __init__(self, prod_code, time_kind='1m'):
        self.prod_code = prod_code
        if time_kind in ['1m', '5m', '1h']:
            self.time_kind = time_kind
        else:
            log.logger.error('时间类型输入错误')

    def get_data_for_file(self):
        date = datetime.datetime.now()
        cur_path = os.getcwd() + os.path.sep + 'data' + os.path.sep + self.prod_code + os.path.sep + date.strftime(
            '%Y-%m-%d') + '_' + self.prod_code + '.csv'
        if not os.path.exists(cur_path):
            log.logger.warning(self.prod_code + '找不到当天的数据，')
            return False
        else:
            with open(cur_path, 'r')as f:
                msg = f.read()


def get_kline(prod_code):
    date = datetime.datetime.now()
    cur_path = os.getcwd() + os.path.sep + 'data' + os.path.sep + prod_code + os.path.sep + date.strftime(
        '%Y-%m-%d') + '_' + prod_code + '.csv'
    if not os.path.exists(cur_path):
        # print(prod_code + '找不到当天的数据，')
        log.logger.warning(prod_code + '找不到当天的数据，')
        return False
    else:
        with open(cur_path, 'r')as f:
            msg = f.read()
        start_time = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute)
        price_list = list()
        volume = 0
        for data_list in msg.split('\n'):
            for second_data in data_list.split(','):
                if (start_time + datetime.timedelta(minutes=1)) > datetime.datetime.strptime(second_data[3],
                                                                                             '%Y-%m-%d %H:%M:%S') >= start_time:
                    price_list.append(second_data[1])
                    volume += second_data[2]
        if price_list:
            kline = [price_list[0], max(price_list), min(price_list), price_list[-1], volume,
                     start_time.strftime('%Y-%m-%d %H:%M:%S')]
            return kline
        else:
            log.logger.warning('没有抓到这一分钟的数据')
            return False

    # df = pd.read_csv(cur_path)
        # start_time = datetime.datetime(date.year, date.month, date.day, date.hour, date.minute)
        # index_list = []
        # count = 0
        # for i in df['date']:
        #     if (start_time + datetime.timedelta(minutes=1)) > datetime.datetime.strptime(i,
        #                                                                                  '%Y-%m-%d %H:%M:%S') >= start_time:
        #         index_list.append(count)
        #         count += 1
        #     else:
        #         count += 1
        # if index_list:
        #     kline_data = df[min(index_list):max(index_list) + 1]
        #     # print(kline_data)
        #     kline = [kline_data['Price'][min(index_list)], max(kline_data['Price']), min(kline_data['Price']),
        #              kline_data['Price'][max(index_list)], sum(kline_data['quantity']),
        #              start_time.strftime('%Y-%m-%d %H:%M:%S')]
        #     return kline
        # else:
        #     # print(start_time.strftime('%Y-%m-%d %H:%M:%S') + '没有抓到这一分钟的数据')
        #     log.logger.warning('没有抓到这一分钟的数据')
        #     return False
