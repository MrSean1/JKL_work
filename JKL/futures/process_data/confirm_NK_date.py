# *_*coding:utf-8 *_*
import datetime


class Confirm_HK_Date():
    def __init__(self, date):
        # self.date = datetime.datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        self.date = date

    def judge_date_in_trade_time(self):
        before_date = datetime.datetime.strptime(self.date.split(' ')[0], '%Y/%m/%d') - datetime.timedelta(days=1)
        the_date = datetime.datetime.strptime(self.date.split(' ')[0], '%Y/%m/%d')
        t_b_time = self.trade_time(before_date)
        t_t_time = self.trade_time(the_date)
        date = datetime.datetime.strptime(self.date, '%Y/%m/%d %H:%M:%S')
        if t_b_time:
            morning_start_trade_time = datetime.datetime.strptime(t_b_time[0][0], '%Y/%m/%d %H:%M:%S')
            morning_end_trade_time = datetime.datetime.strptime(t_b_time[0][1], '%Y/%m/%d %H:%M:%S')
            afternoon_start_trade_time = datetime.datetime.strptime(t_b_time[1][0], '%Y/%m/%d %H:%M:%S')
            afternoon_end_trade_time = datetime.datetime.strptime(t_b_time[1][1], '%Y/%m/%d %H:%M:%S')
            if morning_start_trade_time <= date <= morning_end_trade_time:
                return t_b_time
            elif afternoon_start_trade_time <= date <= afternoon_end_trade_time:
                return t_b_time
            else:
                if t_t_time:
                    morning_start_trade_time = datetime.datetime.strptime(t_t_time[0][0], '%Y/%m/%d %H:%M:%S')
                    morning_end_trade_time = datetime.datetime.strptime(t_t_time[0][1], '%Y/%m/%d %H:%M:%S')
                    afternoon_start_trade_time = datetime.datetime.strptime(t_t_time[1][0], '%Y/%m/%d %H:%M:%S')
                    afternoon_end_trade_time = datetime.datetime.strptime(t_t_time[1][1], '%Y/%m/%d %H:%M:%S')
                    if morning_start_trade_time <= date <= morning_end_trade_time:
                        return t_t_time
                    elif afternoon_start_trade_time <= date <= afternoon_end_trade_time:
                        return t_t_time
                    else:
                        return False
                else:
                    return False
        elif t_t_time:
            morning_start_trade_time = datetime.datetime.strptime(t_t_time[0][0], '%Y/%m/%d %H:%M:%S')
            morning_end_trade_time = datetime.datetime.strptime(t_t_time[0][1], '%Y/%m/%d %H:%M:%S')
            afternoon_start_trade_time = datetime.datetime.strptime(t_t_time[1][0], '%Y/%m/%d %H:%M:%S')
            afternoon_end_trade_time = datetime.datetime.strptime(t_t_time[1][1], '%Y/%m/%d %H:%M:%S')
            if morning_start_trade_time <= date <= morning_end_trade_time:
                return t_t_time
            elif afternoon_start_trade_time <= date <= afternoon_end_trade_time:
                return t_t_time
            else:
                if t_b_time:
                    morning_start_trade_time = datetime.datetime.strptime(t_b_time[0], '%Y/%m/%d %H:%M:%S')
                    morning_end_trade_time = datetime.datetime.strptime(t_b_time[1], '%Y/%m/%d %H:%M:%S')
                    afternoon_start_trade_time = datetime.datetime.strptime(t_b_time[2], '%Y/%m/%d %H:%M:%S')
                    afternoon_end_trade_time = datetime.datetime.strptime(t_b_time[3], '%Y/%m/%d %H:%M:%S')
                    if morning_start_trade_time <= date <= morning_end_trade_time:
                        return t_b_time
                    elif afternoon_start_trade_time <= date <= afternoon_end_trade_time:
                        return t_b_time
                    else:
                        return False
                else:
                    return False
        else:
            return False

    def trade_time(self, date):
        '''
        :param date: 带有年月日得 datetime时间
        :return: 该日得交易时间
        '''
        ret = self.__rest_day(date)
        if ret:
            if date <= datetime.datetime.strptime('2013/7/30', '%Y/%m/%d'):
                morning_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '07:46:00'
                morning_end_trade_time = date.strftime('%Y/%m/%d') + ' ' + '14:25:00'
                afternoon_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '15:16:00'
                afternoon_end_trade_time = (date + datetime.timedelta(days=1)).strftime('%Y/%m/%d') + ' ' + '02:00:00'
            elif date <= datetime.datetime.strptime('2016/7/10', '%Y/%m/%d'):
                morning_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '07:46:00'
                morning_end_trade_time = date.strftime('%Y/%m/%d') + ' ' + '14:30:00'
                afternoon_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '15:16:00'
                afternoon_end_trade_time = (date + datetime.timedelta(days=1)).strftime('%Y/%m/%d') + ' ' + '02:00:00'
            elif date <= datetime.datetime.strptime('2016/11/10', '%Y/%m/%d'):
                morning_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '07:31:00'
                morning_end_trade_time = date.strftime('%Y/%m/%d') + ' ' + '14:30:00'
                afternoon_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '15:16:00'
                afternoon_end_trade_time = (date + datetime.timedelta(days=1)).strftime('%Y/%m/%d') + ' ' + '02:00:00'
            elif date <= datetime.datetime.strptime('2016/11/13', '%Y/%m/%d'):
                morning_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '07:31:00'
                morning_end_trade_time = date.strftime('%Y/%m/%d') + ' ' + '14:25:00'
                afternoon_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '15:16:00'
                afternoon_end_trade_time = (date + datetime.timedelta(days=1)).strftime('%Y/%m/%d') + ' ' + '02:00:00'
            elif date <= datetime.datetime.strptime('2018/06/07', '%Y/%m/%d'):
                morning_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '07:31:00'
                morning_end_trade_time = date.strftime('%Y/%m/%d') + ' ' + '14:25:00'
                afternoon_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '15:01:00'
                afternoon_end_trade_time = (date + datetime.timedelta(days=1)).strftime('%Y/%m/%d') + ' ' + '04:45:00'
            # elif date > datetime.datetime.strptime('2018/06/07', '%Y/%m/%d'):
            else:
                morning_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '07:31:00'
                morning_end_trade_time = date.strftime('%Y/%m/%d') + ' ' + '14:25:00'
                afternoon_start_trade_time = date.strftime('%Y/%m/%d') + ' ' + '14:56:00'
                afternoon_end_trade_time = (date + datetime.timedelta(days=1)).strftime('%Y/%m/%d') + ' ' + '04:45:00'
            return [[morning_start_trade_time, morning_end_trade_time],
                    [afternoon_start_trade_time, afternoon_end_trade_time]]
        else:
            return ret

    def __rest_day(self, date):
        '''
        判断是否在元旦休息日
        :return: 是休息日 False 不是休息日 True
        '''
        # 判断是不是在双休
        if date.weekday() == 5 or date.weekday() == 6:
            return False
        else:
            return True


sd = Confirm_HK_Date('2012/1/4 07:46:00')
sd.judge_date_in_trade_time()
