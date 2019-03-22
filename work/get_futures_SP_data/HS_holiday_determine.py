# *_*coding:utf-8 *_*
# 香港理念公假日展示页面
import datetime
import time
# 获取农历日历的接口
# requests.get('https://www.sojson.com/open/api/lunar/json.shtml?date=2016-2-3')
from selenium import webdriver


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
    with open('HS_holiday.txt', 'r', ) as f:
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
    with open('HS_holiday.txt', 'w', ) as f:
        f.write(str(festival_dic_for_year))
    print('数据已经写进日期文件中')


def rest_day(date):
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
            # 判断是否在文件中的休息日里面
            holiday_dic = read_holiday_for_dic()
            if date.year in holiday_dic.keys():
                for i in holiday_dic[date.year].keys():
                    if date == datetime.datetime.strptime(i, '%Y/%m/%d'):
                        return False
                    else:
                        return True
            else:
                # 若当年日期不再文件中  则重新抓取当年休息日
                get_HongKong_holiday(date.year)


def read_holiday_for_dic():
    with open('HS_holiday.txt', 'r') as f:
        holiday = f.read()
    holiday_dic = eval(holiday)
    return holiday_dic
