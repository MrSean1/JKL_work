# *_*coding:utf-8 *_*

import datetime


class Confirm_YM_Date():
    def __init__(self, date):
        # self.date = datetime.datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        self.date = date

    def judge_date_in_trade_time(self):
        before_date = datetime.datetime.strptime(self.date.split(' ')[0], '%Y/%m/%d') - datetime.timedelta(days=1)
        the_date = datetime.datetime.strptime(self.date.split(' ')[0], '%Y/%m/%d')
        t_b_time = self.trade_time(before_date)
        t_t_time = self.trade_time(the_date)
        # 原本输入的时间
        date = datetime.datetime.strptime(self.date, '%Y/%m/%d %H:%M:%S')
        if t_b_time:
            start_befor_trade_time = datetime.datetime.strptime(t_b_time[0], '%Y/%m/%d %H:%M:%S')
            end_befor_trade_time = datetime.datetime.strptime(t_b_time[1], '%Y/%m/%d %H:%M:%S')
            if start_befor_trade_time <= date <= end_befor_trade_time:
                return t_b_time
            elif t_t_time:
                start_the_trade_time = datetime.datetime.strptime(t_t_time[0], '%Y/%m/%d %H:%M:%S')
                end_the_trade_time = datetime.datetime.strptime(t_t_time[1], '%Y/%m/%d %H:%M:%S')
                if start_the_trade_time <= date <= end_the_trade_time:
                    return t_t_time
                else:
                    return False  # 不在交易日
            else:
                return False  # 不再交易日
        elif t_t_time:
            start_the_trade_time = datetime.datetime.strptime(t_t_time[0], '%Y/%m/%d %H:%M:%S')
            end_the_trade_time = datetime.datetime.strptime(t_t_time[1], '%Y/%m/%d %H:%M:%S')
            if start_the_trade_time <= date <= end_the_trade_time:
                return t_t_time
            else:
                return False  # 不在交易日
        else:
            return False  # 该日期均不再两天的交易时间里面

    def __judge_St_WT(self, date):
        '''
        :return: 判断冬夏令时
        '''
        end = int(date.strftime("%W"))
        begin = int(datetime.datetime(date.year, date.month, 1).strftime("%W"))
        which_weeks = end - begin + 1
        # # 判断洲周几0-6  周一到周日
        # week = self.date.weekday()
        if date.month == 3 and which_weeks > 2:
            return '夏令时'
        elif date.month == 11 and which_weeks <= 1:
            return '夏令时'
        elif 3 < date.month < 11:
            return '夏令时'
        else:
            return '冬令时'

    def trade_time(self, date):
        '''
        :param date: 带有年月日得 datetime时间
        :return: 该日得交易时间
        '''
        # 判断冬夏令时
        ret = self.__judge_St_WT(date)
        # 判断该日是否为休息日
        ret_week = self.__rest_day(date)

        if ret_week is True:
            # 特殊交易时间
            s_day = self.__special_date(date)
            if ret == '夏令时':
                tr_time = date.strftime('%Y/%m/%d')
                start_time = tr_time + ' ' + '06:01:00'
                if s_day == 0:
                    e_time = date + datetime.timedelta(days=1)
                    if date < datetime.datetime(2013, 7, 23):
                        end_time = e_time.strftime('%Y/%m/%d') + ' ' + '04:15:00'
                    elif date < datetime.datetime(2015, 8, 12):
                        end_time = e_time.strftime('%Y/%m/%d') + ' ' + '05:15:00'
                    else:
                        end_time = e_time.strftime('%Y/%m/%d') + ' ' + '05:00:00'
                    return start_time, end_time
                else:
                    if s_day == 1:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '01:00:00'
                    elif s_day == 2:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '02:00:00'
                    elif s_day == 0.5:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '00:30:00'
                    elif s_day == -0.5:
                        # end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S')
                        end_time = tr_time + ' ' + '23:30:00'
                    elif s_day == 1.25:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '01:15:00'
                    elif s_day == 2.25:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '02:15:00'
                    return start_time, end_time
            elif ret == '冬令时':
                tr_time = date.strftime('%Y/%m/%d')
                start_time = tr_time + ' ' + '07:01:00'
                if s_day == 0:
                    e_time = date + datetime.timedelta(days=1)
                    if date < datetime.datetime(2013, 7, 23):
                        end_time = e_time.strftime('%Y/%m/%d') + ' ' + '05:15:00'
                    elif date < datetime.datetime(2015, 8, 12):
                        end_time = e_time.strftime('%Y/%m/%d') + ' ' + '06:15:00'
                    else:
                        end_time = e_time.strftime('%Y/%m/%d') + ' ' + '06:00:00'
                    return start_time, end_time
                    # end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                    #     hours=23, minutes=-1)
                    # end_time = end_time.strftime('%Y/%m/%d %H:%M:%S')
                    # return start_time, end_time
                else:
                    if s_day == 1:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '01:00:00'
                    elif s_day == 2:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '02:00:00'
                    elif s_day == 0.5:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '00:30:00'
                    elif s_day == -0.5:
                        # end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S')
                        end_time = tr_time + ' ' + '23:30:00'
                    elif s_day == 1.25:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '01:15:00'
                    elif s_day == 2.25:
                        end_time = datetime.datetime.strptime(start_time, '%Y/%m/%d %H:%M:%S') + datetime.timedelta(
                            days=1)
                        end_time = end_time.strftime('%Y/%m/%d') + ' ' + '02:15:00'
                    return start_time, end_time
        else:
            return ret_week
            # return '今天是休息日'

    #
    # def judge_weekend(self):
    #     '''
    #     :return: True 是交易日 False 不是交易日
    #     '''
    #     ret = self.date.weekday()
    #     if ret == 5 or ret == 6:
    #         return True
    #     else:
    #         return False

    def __special_date(self, date):
        '''
        元旦不交易
        小马丁·路德·金的生日： 一月份第三个周一
        总统日： 二月的第三个星期一
        烈士纪念日: 五月的最后一个周一
        独立日： 7/4 交易到凌晨一点
        劳动节： 九月的第一个周一
        感恩节： 十一月第四个周四
        感恩节后一天: 交易到两点一刻
        :return: 0 正常交易时间 1 交易到凌晨一点 2 交易到凌晨两点 2.25 交易到凌晨2:15 0.5 交易到0:30 -0.5交易到当日23:30
        '''
        if date.month == 1:
            first_day_of_month_week = datetime.datetime(date.year, 1, 1).weekday()
            if first_day_of_month_week != 0:
                Madi_day = 14 + 7 - int(first_day_of_month_week) + 1
                Madi_day = datetime.datetime(date.year, 1, Madi_day)
            else:
                Madi_day = datetime.datetime(date.year, 1, 15)
            if date.date() == Madi_day.date():
                if date.year < 2015:
                    return 0.5
                else:
                    return 2
            else:
                return 0
        if date.month == 2:
            first_day_of_month_week = datetime.datetime(date.year, 2, 1).weekday()
            if first_day_of_month_week != 0:
                Washington_day = 14 + 7 - int(first_day_of_month_week) + 1
                Washington_day = datetime.datetime(date.year, 2, Washington_day)
            else:
                Washington_day = datetime.datetime(date.year, 2, 15)
            if date.date() == Washington_day.date():
                if date.year < 2015:
                    return 0.5
                else:
                    return 2
            else:
                return 0
        if date.month == 5:
            week = datetime.datetime(date.year, date.month, 31)
            if week.weekday() == 0:
                if date.date() == week.date():
                    if date.year < 2014:
                        return -0.5
                    else:
                        return 1
                else:
                    return 0
            else:
                Martyrs_day = week - datetime.timedelta(hours=(week.weekday() * 24))
                if Martyrs_day.date() == date.date():
                    # return '交易日交易到凌晨一点'
                    if date.year < 2014:
                        return -0.5
                    else:
                        return 1
                else:
                    return 0
        elif date.month == 7:
            if date.day == 3:
                # if date.year < 2017:
                if datetime.datetime(date.year, 7, 4).weekday() == 5:
                    return 1
                else:
                    return 1.25
            elif date.day == 4:
                if date.year < 2014:
                    return -0.5
                else:
                    return 1
            else:
                return 0
        elif date.month == 9:
            week = datetime.datetime(date.year, date.month, 1)
            if week.weekday() == 0:
                if date.date() == week.date():
                    if date.year < 2014:
                        return -0.5
                    else:
                        return 1
                else:
                    return 0
            else:
                Labor_Day = week + datetime.timedelta(hours=((6 - week.weekday() + 1) * 24))
                if Labor_Day.date() == date.date():
                    if date.year < 2014:
                        return -0.5
                    else:
                        return 1
                else:
                    return 0
        elif date.month == 11:
            first_day_of_month = datetime.datetime(date.year, 11, 1).weekday()
            if first_day_of_month < 3:
                first_thursday = 1 + 3 - int(first_day_of_month)
                thanksgiving_day = datetime.datetime(date.year, 11, first_thursday + 21)
            elif first_day_of_month > 3:
                first_thursday = 7 - (int(first_day_of_month) - 3) + 1
                thanksgiving_day = datetime.datetime(date.year, 11, first_thursday + 21)
            else:
                # first_day_of_month == 3:
                thanksgiving_day = datetime.datetime(date.year, 11, 22)
            if date.date() == thanksgiving_day.date():
                if date.year < 2014:
                    return 0.5
                else:
                    return 2
            elif date.date() == (thanksgiving_day + datetime.timedelta(days=1)).date():
                return 2.25
            else:
                return 0
        elif date.month == 12:
            if date.day == 24:
                return 2.25
            else:
                return 0
        else:
            return 0

    def __rest_day(self, date):
        '''
        判断是否在元旦休息日 及 判断是否在圣诞节 及周末
        :return: 是休息日 False 不是休息日 True
        '''
        # 计算出元旦是周几并得出放假时间
        rest_day = []
        New_year_day = datetime.datetime(date.year, 1, 1)
        Christmas_day = datetime.datetime(date.year, 12, 25)
        if New_year_day.weekday() == 5:
            rest_day.append(New_year_day - datetime.timedelta(days=1))
        elif New_year_day.weekday() == 6:
            rest_day.append(New_year_day + datetime.timedelta(days=1))
        else:
            rest_day.append(New_year_day)
        if Christmas_day.weekday() == 5:
            rest_day.append(Christmas_day - datetime.timedelta(days=1))
        elif Christmas_day.weekday() == 6:
            rest_day.append(Christmas_day + datetime.timedelta(days=1))
        else:
            rest_day.append(Christmas_day)
        if date in rest_day:
            return False
        # 周末放假
        elif date.weekday() == 5 or date.weekday() == 6:
            return False
        else:
            return True


# a = Confirm_YM_Date('2012/01/12 05:15:00')
# a.judge_date_in_trade_time()
