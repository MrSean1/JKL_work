# *_*coding:utf-8 *_*
import calendar
import threading
import time
import datetime

from sp_account import Account
from send_email import Email
from config import *

sp_account = Account(account)


def run(prod_code):
    time.sleep(5)
    while True:
        ret = sp_account.write_data_for_file(prod_code)
        if ret is False:
            time.sleep(1)
            msg = sp_account.login()
            if msg is False:
                # 发邮件提醒
                email_msg = '登陆失败，请检测是程序出错还是服务出错\n，' + str(msg)
                email_title = 'SP数据抓取问题'
                try:
                    Email(em_user=em_user, pwd=pwd, address=address, smtp_server=smtp_server).send_email(
                        message=email_msg,
                        title=email_title)
                except Exception as e:
                    log.logger.error(e)
                break
            else:
                time.sleep(2)
                sp_account.subscription(prod_code)
                continue


def main():
    """
    采用多线程对sp期货数据进行抓取
    :return:
    """
    # 时间是否在双休  最后一天为结算日   前一天为交割日   交割日前三天   需要更换到下一批期货上
    today_time = datetime.datetime.now()
    end_time_trade = judge_datetime_replace(today_time)
    if today_time - end_time_trade > datetime.timedelta(days=1):
        # 进入下一个月的期货
        product_list[1] = 'HSI' + mouth_mark[today_time.month + 1] + str(datetime.datetime.now().year % 10)
    thread = [threading.Thread(target=run, args=(product,)) for product in product_list]
    [th.start() for th in thread]
    [th.join() for th in thread]


def judge_datetime_replace(date):
    """
    :param date: 当天日期
    :return: 最后的交易日
    """
    total_day = calendar.monthrange(date.year, date.month)[1]
    last_day_month = datetime.datetime.strptime('{}-{}-{}'.format(date.year, date.month, total_day), '%Y-%m-%d')
    if 5 > last_day_month.weekday() >= 2:
        last_trade_day = last_day_month - datetime.timedelta(days=2)
        return last_trade_day
    elif 7 > last_day_month.weekday() >= 5:
        last_trade_day = last_day_month - datetime.timedelta(days=(last_day_month.weekday() - 2))
        return last_trade_day
    else:
        last_trade_day = last_day_month - datetime.timedelta(days=(1 + last_day_month.weekday()))
        return last_trade_day


if __name__ == '__main__':
    main()
