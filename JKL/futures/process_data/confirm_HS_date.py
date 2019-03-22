# *_*coding:utf-8 *_*
import datetime
import time
# 获取农历日历的接口
# requests.get('https://www.sojson.com/open/api/lunar/json.shtml?date=2016-2-3')
from selenium import webdriver


# 香港理念公假日展示页面
def get_HongKong_holiday(year):
    driver = webdriver.Chrome(
        executable_path="D:/work/register_fxh/chromedriver.exe"
        # executable_path="I:/D盘/work/register_fxh/chromedriver.exe"
        # chrome_options=webdriver.ChromeOptions()
    )
    driver.get('http://www.gov.hk/sc/about/abouthk/holiday/{}.htm'.format(year))
    time.sleep(2)
    holiday_name_time = driver.find_element_by_xpath('//table/tbody').text
    festival_and_date = []
    for holiday in holiday_name_time.split(' '):
        if holiday:
            festival_and_date += holiday.split('\n')
    count = 1
    festival_dic = dict()
    with open('HS_holiday.txt', 'r',) as f:
        festival_dic_for_year = f.read()
    if festival_dic_for_year:
        festival_dic_for_year = eval(festival_dic_for_year)
    else:
        festival_dic_for_year = dict()
    for i in festival_and_date[2:]:
        if count % 3 == 1:
            festival = i
        elif count % 3 == 2:
            date = datetime.datetime.strptime(str(year) + '年' + i, '%Y年%m月%d日')
            date = date.strftime('%Y/%m/%d')
        elif count % 3 == 0:
            festival_dic[date] = festival
        count += 1
    festival_dic_for_year[year] = festival_dic
    with open('HS_holiday.txt', 'w',) as f:
        f.write(str(festival_dic_for_year))
    print('数据已经写进日期文件中')


class ConfirmHSDate:
    def __init__(self, date):
        self.date = date

    def judge_date_in_trade_time(self):
        before_date = datetime.datetime.strptime(self.date.split(' ')[0], '%Y/%m/%d') - datetime.timedelta(days=1)
        the_date = datetime.datetime.strptime(self.date.split(' ')[0], '%Y/%m/%d')
        t_b_time = self.trade_time(before_date)
        t_t_time = self.trade_time(the_date)
        # # 原本输入的时间
        date = datetime.datetime.strptime(self.date, '%Y/%m/%d %H:%M:%S')
        if t_b_time:
            if len(t_b_time) == 3:
                start_night_trade_time = datetime.datetime.strptime(t_b_time[2][0], '%Y/%m/%d %H:%M:%S')
                end_night_trade_time = datetime.datetime.strptime(t_b_time[2][1], '%Y/%m/%d %H:%M:%S')
            else:
                start_night_trade_time = ''
                end_night_trade_time = ''
            start_morning_trade_time = datetime.datetime.strptime(t_b_time[0][0], '%Y/%m/%d %H:%M:%S')
            end_morning_trade_time = datetime.datetime.strptime(t_b_time[0][1], '%Y/%m/%d %H:%M:%S')
            start_afternoon_trade_time = datetime.datetime.strptime(t_b_time[1][0], '%Y/%m/%d %H:%M:%S')
            end_afternoon_trade_time = datetime.datetime.strptime(t_b_time[1][1], '%Y/%m/%d %H:%M:%S')
            if start_morning_trade_time <= date <= end_morning_trade_time:
                return t_b_time
            elif start_afternoon_trade_time <= date <= end_afternoon_trade_time:
                return t_b_time
            elif start_night_trade_time != '' and start_night_trade_time <= date <= end_night_trade_time:
                return t_b_time
            else:
                if t_t_time:
                    if len(t_t_time) == 3:
                        start_night_trade_time = datetime.datetime.strptime(t_t_time[2][0], '%Y/%m/%d %H:%M:%S')
                        end_night_trade_time = datetime.datetime.strptime(t_t_time[2][1], '%Y/%m/%d %H:%M:%S')
                    else:
                        start_night_trade_time = ''
                        end_night_trade_time = ''
                    start_morning_trade_time = datetime.datetime.strptime(t_t_time[0][0], '%Y/%m/%d %H:%M:%S')
                    end_morning_trade_time = datetime.datetime.strptime(t_t_time[0][1], '%Y/%m/%d %H:%M:%S')
                    start_afternoon_trade_time = datetime.datetime.strptime(t_t_time[1][0], '%Y/%m/%d %H:%M:%S')
                    end_afternoon_trade_time = datetime.datetime.strptime(t_t_time[1][1], '%Y/%m/%d %H:%M:%S')
                    # start_night_trade_time = datetime.datetime.strptime(t_t_time[2][0], '%Y/%m/%d %H:%M:%S')
                    # end_night_trade_time = datetime.datetime.strptime(t_t_time[2][1], '%Y/%m/%d %H:%M:%S')
                    if start_morning_trade_time <= date <= end_morning_trade_time:
                        return t_t_time
                    elif start_afternoon_trade_time <= date <= end_afternoon_trade_time:
                        return t_t_time
                    elif start_night_trade_time != '' and start_night_trade_time <= date <= end_night_trade_time:
                        return t_t_time
                    else:
                        return False
                else:
                    return False
        elif t_t_time:
            if len(t_t_time) == 3:
                start_night_trade_time = datetime.datetime.strptime(t_t_time[2][0], '%Y/%m/%d %H:%M:%S')
                end_night_trade_time = datetime.datetime.strptime(t_t_time[2][1], '%Y/%m/%d %H:%M:%S')
            else:
                start_night_trade_time = ''
                end_night_trade_time = ''
            start_morning_trade_time = datetime.datetime.strptime(t_t_time[0][0], '%Y/%m/%d %H:%M:%S')
            end_morning_trade_time = datetime.datetime.strptime(t_t_time[0][1], '%Y/%m/%d %H:%M:%S')
            start_afternoon_trade_time = datetime.datetime.strptime(t_t_time[1][0], '%Y/%m/%d %H:%M:%S')
            end_afternoon_trade_time = datetime.datetime.strptime(t_t_time[1][1], '%Y/%m/%d %H:%M:%S')
            # start_night_trade_time = datetime.datetime.strptime(t_t_time[2][0], '%Y/%m/%d %H:%M:%S')
            # end_night_trade_time = datetime.datetime.strptime(t_t_time[2][1], '%Y/%m/%d %H:%M:%S')
            if start_morning_trade_time <= date <= end_morning_trade_time:
                return t_t_time
            elif start_afternoon_trade_time <= date <= end_afternoon_trade_time:
                return t_t_time
            elif start_night_trade_time != '' and start_night_trade_time <= date <= end_night_trade_time:
                return t_t_time
            else:
                if t_b_time:
                    if len(t_b_time) == 3:
                        start_night_trade_time = datetime.datetime.strptime(t_b_time[2][0], '%Y/%m/%d %H:%M:%S')
                        end_night_trade_time = datetime.datetime.strptime(t_b_time[2][1], '%Y/%m/%d %H:%M:%S')
                    else:
                        start_night_trade_time = ''
                        end_night_trade_time = ''
                    start_morning_trade_time = datetime.datetime.strptime(t_b_time[0][0], '%Y/%m/%d %H:%M:%S')
                    end_morning_trade_time = datetime.datetime.strptime(t_b_time[0][1], '%Y/%m/%d %H:%M:%S')
                    start_afternoon_trade_time = datetime.datetime.strptime(t_b_time[1][0], '%Y/%m/%d %H:%M:%S')
                    end_afternoon_trade_time = datetime.datetime.strptime(t_b_time[1][1], '%Y/%m/%d %H:%M:%S')
                    # start_night_trade_time = datetime.datetime.strptime(t_b_time[2][0], '%Y/%m/%d %H:%M:%S')
                    # end_night_trade_time = datetime.datetime.strptime(t_b_time[2][1], '%Y/%m/%d %H:%M:%S')
                    if start_morning_trade_time <= date <= end_morning_trade_time:
                        return t_b_time
                    elif start_afternoon_trade_time <= date <= end_afternoon_trade_time:
                        return t_b_time
                    elif start_night_trade_time != '' and start_night_trade_time <= date <= end_night_trade_time:
                        return t_b_time
                    else:
                        return False
                else:
                    return False
        else:
            return False

    def trade_time(self, date):
        # 判断是否在休息日
        ret = self.__rest_day(date)
        # 如在工作日
        '''
            16/1/4之前： 9:16-12:00 13:01-16:15 17:16-23:45
            16/7/25当天 往后： 9:16-12:00 13:01-16:30 17:16-23:45
            17/11/6当天 往后： 9:16-12:00 13:01-16:30 17:16-1:00
        '''
        if ret:
            start_morning_trade_time = date.strftime('%Y/%m/%d') + ' ' + '09:16:00'
            end_morning_trade_time = date.strftime('%Y/%m/%d') + ' ' + '12:00:00'
            start_afternoon_trade_time = date.strftime('%Y/%m/%d') + ' ' + '13:01:00'
            start_night_trade_time = date.strftime('%Y/%m/%d') + ' ' + '17:16:00'
            # if data.year == 2016:
            if date < datetime.datetime.strptime('2013/5/10', '%Y/%m/%d'):
                end_afternoon_trade_time = date.strftime('%Y/%m/%d') + ' ' + '16:15:00'
                end_night_trade_time = ''
            elif date < datetime.datetime.strptime('2014/11/3', '%Y/%m/%d'):
                end_afternoon_trade_time = date.strftime('%Y/%m/%d') + ' ' + '16:15:00'
                end_night_trade_time = date.strftime('%Y/%m/%d') + ' ' + '23:00:00'
            elif date < datetime.datetime.strptime('2016/7/25', '%Y/%m/%d'):
                end_afternoon_trade_time = date.strftime('%Y/%m/%d') + ' ' + '16:15:00'
                end_night_trade_time = date.strftime('%Y/%m/%d') + ' ' + '23:45:00'
            elif date < datetime.datetime.strptime('2017/11/6', '%Y/%m/%d'):
                end_afternoon_trade_time = date.strftime('%Y/%m/%d') + ' ' + '16:30:00'
                end_night_trade_time = date.strftime('%Y/%m/%d') + ' ' + '23:45:00'
            else:
                end_afternoon_trade_time = date.strftime('%Y/%m/%d') + ' ' + '16:30:00'
                night_date = date + datetime.timedelta(days=1)
                end_night_trade_time = night_date.strftime('%Y/%m/%d') + ' ' + '01:00:00'
            if end_night_trade_time:
                return [[start_morning_trade_time, end_morning_trade_time],
                        [start_afternoon_trade_time, end_afternoon_trade_time],
                        [start_night_trade_time, end_night_trade_time]]
            else:
                return [[start_morning_trade_time, end_morning_trade_time],
                        [start_afternoon_trade_time, end_afternoon_trade_time]]
        else:
            return ret

    def __rest_day(self, date):
        """
        判断是否在休息日
        :return: 是休息日 False 不是休息日 True
        """
        # 计算元旦放假时间
        week = date.weekday()
        if week == 5 or week == 6:
            return False
        else:
            while True:
                holiday_dic = self.__read_holiday_for_dic()
                if date.year in holiday_dic.keys():
                    for i in holiday_dic[date.year].keys():
                        if date == datetime.datetime.strptime(i, '%Y/%m/%d'):
                            return False
                        else:
                            return True
                else:
                    get_HongKong_holiday(date.year)

    @staticmethod
    def __read_holiday_for_dic():
        with open('HS_holiday.txt', 'r') as f:
            holiday = f.read()
        holiday_dic = eval(holiday)
        return holiday_dic


a = ConfirmHSDate('2019/2/28 07:02:00')
a.judge_date_in_trade_time()
