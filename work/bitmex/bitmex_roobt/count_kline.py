import datetime


class count_kline():
    def __init__(self, type, last_time, trade_data, last_price):
        self.type = type
        if self.type == '1m':
            self._time = 60
        elif self.type == '5m':
            self._time = 300
        elif self.type == '1h':
            self._time = 3600

        self.trade_data = trade_data
        self.last_time = last_time
        self.new_kline = []
        self.last_price = last_price

    def count(self):
        '''
            将websocket的数据统计成K线
            一分钟K线数据由websocket交易数据统计出来
            一小时K线数据和5分钟K线数据由一分钟K线统计出来
        :return: 一组最新的K线数据
        '''
        self.last_time = self.strtime_to_timedatetime(self.last_time) + datetime.timedelta(0, self._time)
        if self.type == '1h' or self.type == '5m':
            self.__count_1h()
        else:
            while True:
                # print(self.type + '开始获得新的列表')
                base_kline = [[dic['timestamp'], dic['price'], dic['size']] for dic in
                              self.trade_data if
                              datetime.timedelta(
                                  0, 0) <= self.last_time - self.strtime_to_timedatetime(
                                  dic['timestamp']) < datetime.timedelta(0, self._time)]

                with open('abc.txt', 'a') as f:
                    f.write(str(base_kline))
                    f.write('\n')
                try:
                    self.make_kline(base_kline, self.last_time)
                except Exception as e:
                    # print(e)
                    pass
                self.last_time += datetime.timedelta(0, self._time)
                if self.last_time - self.strtime_to_timedatetime(self.trade_data[-1]['timestamp']) > datetime.timedelta(
                        0, self._time) and base_kline == []:
                    # print(self.type + '最后一次循环')
                    break
        # print('循环完毕')
        # print('\n')
        return self.new_kline

    def __count_1h(self):
        '''
        :return: 一小时K线数据的统计
        '''
        while True:
            # print(self.type + '开始获得新的列表')
            base_kline = [list for list in self.trade_data if datetime.timedelta(
                0, 0) <= self.last_time - self.strtime_to_timedatetime(list[0]) < datetime.timedelta(0, self._time)]
            # print(self.type + '等待刷新到K线中的数据' + str(base_kline))
            try:
                self.make_1h_kline(base_kline, self.last_time)
            except Exception as e:
                # print(e)
                pass
            self.last_time += datetime.timedelta(0, self._time)
            if self.last_time - self.strtime_to_timedatetime(self.trade_data[-1][0]) > datetime.timedelta(
                    0, self._time) and base_kline == []:
                # print(self.type + '最后一次循环')
                break

    def make_1h_kline(self, base_kline, kline_time):
        '''
        :param base_kline: 一分钟K线数据
        :param kline_time: 完整的K线数据时间
        :return: 最新统计出来的K线数据
        '''
        price_high = [lis[2] for lis in base_kline]
        price_high.sort()
        price_low = [lis[3] for lis in base_kline]
        price_low.sort()
        if self.new_kline:
            self.last_price = self.new_kline[-1][-2]
        kline = [self.timedatetime_to_strtime(kline_time), self.last_price, price_high[-1], price_low[0],
                 base_kline[-1][4],
                 sum([lis[-1] for lis in base_kline])]
        self.new_kline.append(kline)

    def strtime_to_timedatetime(self, time_str):
        '''
        :param time_str: bitmex的K线时间
        :return: datetime类型时间
        '''
        time_str = time_str.replace('T', ' ')
        time_str = time_str.replace('Z', '')
        timestamp = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
        return timestamp

    def timedatetime_to_strtime(self, time_datetime):
        '''
        :param time_datetime: datetime 类型kxian时间
        :return: K线 时间字符串
        '''
        time_datetime = datetime.datetime.replace(time_datetime, second=0, microsecond=0)
        time_str = datetime.datetime.strftime(time_datetime, '%Y-%m-%d %H:%M:%S.%f', )
        time_str = time_str.replace(' ', 'T')[0:-3] + 'Z'
        return time_str

    def make_kline(self, base_kline, kline_time):
        '''
        :param base_kline:  由websocket的交易数据整理出的K线数据
        :param kline_time:  K线开始的时间
        :return:
        '''
        if self.new_kline:
            self.last_price = self.new_kline[-1][-2]
        price = [list[1] for list in base_kline]
        price.sort()
        kline = [self.timedatetime_to_strtime(kline_time), self.last_price, price[-1], price[0], base_kline[-1][1],
                 sum([list[2] for list in base_kline])]
        self.new_kline.append(kline)
