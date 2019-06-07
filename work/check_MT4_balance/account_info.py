import os
import datetime
import logging
import pandas as pd
import json
import xlwt
from mt4_account import MT4Account
import smtplib


def setup_logger():
    # Prints logger info to terminaing.basicConfig(
    #     level=logging.INFO,
    #     filename="./log/mt4_{}.log".format(datetime.datetime.now().date()),
    #     format="%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s",
    #     filemode='a',
    #     # encoding='utf-8',
    # )
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    fh = logging.FileHandler(filename="./log/gdbank_{}.log".format(datetime.datetime.now().date()), encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    # ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    # create formatter
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    # sh = logging.StreamHandler()  # 往屏幕上输出
    # 屏幕输出格式
    # sh.setFormatter("%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    # logger.addHandler(sh)
    # sh.setFormatter("%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    return logger


def get_balance_info():
    rmb_data = []
    usd_data = ["ADSS-Live1", "IFCMarkets-Real", "ThinkForexAU-Live", "Ava-Real5", "XTRINT-Live"]
    btb_data = ["SimpleFX-LiveUK"]
    f = xlwt.Workbook(encoding='ascii')
    sheet = f.add_sheet('sheet')
    time = datetime.datetime.now().date()
    csv_data = pd.read_csv('account.csv')
    sheet.write(0, 0, label='平台')
    sheet.write(0, 1, label='账户')
    sheet.write(0, 2, label='人民币')
    sheet.write(0, 3, label='美元')
    sheet.write(0, 4, label='比特币')
    for i in range(0, len(csv_data)):
        account = str(csv_data.iloc[i]["account"])
        ipv4 = str(csv_data.iloc[i]["ip_ipv4"])
        broker = str(csv_data.iloc[i]["broker"])
        try:
            mt4_status = MT4Account(account, ipv4).get_account()
            if mt4_status:
                mt4 = MT4Account(account, ipv4)
                balance = mt4.balance
            else:
                balance = 'False'
        except Exception as e:
            logger.error(e)
        sheet.write(i + 1, 0, broker)
        sheet.write(i + 1, 1, account)
        if broker in rmb_data:
            sheet.write(i + 1, 2, balance)
        elif broker in usd_data:
            sheet.write(i + 1, 3, balance)
        elif broker in btb_data:
            sheet.write(i + 1, 4, balance)
    f.save('./余额/%s资金余额统计.xls' % (time))


if __name__ == '__main__':
    logger = setup_logger()
    get_balance_info()

