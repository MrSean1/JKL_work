from email.mime.text import MIMEText
import os
import smtplib
import time
from ex_api.exchange import Exchange, MyThread
from accounts_bxx import account_info
import json
import sys

ex_name = sys.argv[1]
sym = sys.argv[2]
sym_base = sys.argv[3]
symbol = [sym, sym_base]

symbol = [sym, sym_base]
USD_CNY = 6.3
USDT_CNY = 6.6

bxx_key = account_info[ex_name][symbol[1]][symbol[0]]
ex_bxx = [Exchange('bxx', key) for key in bxx_key]

user = 'pkusimon@qq.com'
pwd = 'zvgtfnzjvlkmbdig'
to_xl = '568327240@qq.com'
# to_customer = '568327240@qq.com'
to_customer = '940820195@qq.com'
# to_customer = 'colapu@qq.com'
# to_customer = 'pfs1033@163.com'
if sym == 'DVC':
    to_customer = '468415432@qq.com'
smtp_server = 'smtp.qq.com'


def send_email_xl(message):
    try:
        message['From'] = user
        message['To'] = to_xl
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(1)
        server.login(user, pwd)
        server.sendmail(user, to_xl, message.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print("Falied,%s" % e)


def send_email_customer(message):
    try:
        message['From'] = user
        message['To'] = to_customer
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(1)
        server.login(user, pwd)
        server.sendmail(user, to_customer, message.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print("Falied,%s" % e)


def get_all_balance():
    th_b = []
    for ex in ex_bxx:
        th_b.append(MyThread(ex.api.get_account, args=()))
    [th.start() for th in th_b]
    [th.join() for th in th_b]
    ac_list = [th.get_result() for th in th_b]
    sum_sym = 0
    sum_sym_base = 0
    for acl in ac_list:
        for dic in acl:
            if dic['coinName'] == sym:
                sum_sym += dic['carryingAmount']
            elif dic['coinName'] == sym_base:
                sum_sym_base += dic['carryingAmount']
    return sum_sym, sum_sym_base


old_sym_balance, old_sym_base_balance = get_all_balance()
old_balance = {
    sym: old_sym_balance,
    sym_base: old_sym_base_balance
}


def check_balance_bxx():
    tex = ''
    sym_balance, sym_base_balance = get_all_balance()
    tex += 'Current total balance of ' + sym + ' is ' + str(sym_balance) + '\n'
    tex += 'Current total balance of ' + sym_base + ' is ' + str(sym_base_balance) + '\n'
    tex += 'Difference to last report is\n'
    tex += sym + ': ' + str(sym_balance - old_balance[sym]) + '\n'
    tex += sym_base + ': ' + str(sym_base_balance - old_balance[sym_base])
    old_balance[sym] = sym_balance
    old_balance[sym_base] = sym_base_balance
    print(tex)
    msg = MIMEText(tex)
    msg['Subject'] = 'Account Report of ' + sym + '_' + sym_base
    send_email_xl(msg)
    send_email_customer(msg)
    # send_email_test(msg)
    with open('./balance_' + sym + '_' + sym_base + '.txt', 'a') as f:
        f.writelines(time.asctime())
        f.writelines(tex)
        f.writelines('\n')


check_balance_bxx()
while True:
    if int(time.strftime('%M')) in [0]:
        check_balance_bxx()
    time.sleep(59)
