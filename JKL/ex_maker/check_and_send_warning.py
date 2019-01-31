from email.mime.text import MIMEText
import os
import smtplib
import time

# from ex_api.exchange import Exchange
# from trade_pair_coinfig import account_info
# import json

# binance_key = ['YDEaP2pwwNnTgxnVvTykElck9tTL3ODt5pYZGZWANPPCqIoRAK02Ma003susa9nZ',
#                'LFhd1YzD9Hby4SVlXFqL0sxhXg3I30tjJsjCH8u90KGkIClp9PMLs1Ockr4dGQDd']
#
# huobi_key = ['23d16220-7b1883cc-dc468afc-6865d',
#              'fe31646f-78407147-ec119bc8-cbdab']
#
# coinw_key = ['a048a77f-b61e-49c5-b459-3ad171242959', 'ZTMF18573EILZLUIBB4RARLDOM3YCFOAYPXZ']
#
# ex_bin = Exchange('binance', binance_key)
#
# ex_huobi = Exchange('huobi', huobi_key)
#
# ex_cw = Exchange('coinw', coinw_key)
#
# symbol_bin = ['BTC', 'ETH', 'LTC', 'QTUM', 'USDT']
# symbol_huobi = ['DASH', 'EOS', 'HSR', 'USDT']
# symbol_cw = ['Doge', 'hpy', 'CNYT']
# symbol_usd = ['BTC', 'ETH', 'LTC', 'QTUM', 'DASH', 'EOS', 'HPY', 'DOGE', 'HPS', 'HSR', 'CNXX', 'XMX', 'DVC']
# symbol_btc = ['LTC', 'ETH', 'QTUM', 'EOS', 'DASH', 'HPS', 'CNXX', 'TRX', 'XMX', 'ZIL', 'AE', 'CTXC', 'BNB', 'HT', 'NAS']

user = 'pkusimon@qq.com'
pwd = 'zvgtfnzjvlkmbdig'
to_xl = '568327240@qq.com'
to_yl = '124397321@qq.com'
to_ht = '295861809@qq.com'
to_test = '1207866702@qq.com'
smtp_server = 'smtp.qq.com'


# ex_bin.refresh_account()
# balance_bin = {sym: float(ex_bin.account_info[sym]['avaid_balance']) for sym in symbol_bin}
#
# ex_huobi.refresh_account()
# balance_huobi = {}
# for sym in symbol_huobi:
#     for dic in ex_huobi.account_info:
#         if dic['currency'] == sym.lower() and dic['type'] == 'trade':
#             balance_huobi[sym] = float(dic['balance'])
#             break
#
# ex_cw.refresh_account()
# balance_cw = {sym: float(ex_cw.account_info[sym]['avaid_balance']) for sym in symbol_cw}



def send_email(message, to):
    try:
        message['From'] = user
        message['To'] = to
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(1)
        server.login(user, pwd)
        server.sendmail(user, to, message.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print("Falied,%s" % e)


# balance_coinx = {
#     'USD': {},
#     'BTC': {}
# }
#
#
# def get_symbol_balance_coinx(symbol):
#     coinx_key = account_info[symbol[1]][symbol[0]]
#     ex_cx = [Exchange('bixin', key) for key in coinx_key]
#     for ex in ex_cx:
#         ex.refresh_account()
#     balance = dict()
#     balance[symbol[1]] = sum([float(ex.account_info[symbol[1]]['balance']) for ex in ex_cx])
#     balance[symbol[0]] = sum([float(ex.account_info[symbol[0]]['balance']) for ex in ex_cx])
#     return balance
#
#
# def check_balance_coinx():
#     tex = ''
#     for sym in symbol_usd:
#         try:
#             temp_balance_symbol = get_symbol_balance_coinx([sym, 'USD'])
#             diff = ''
#             if sym not in balance_coinx['USD'].keys():
#                 balance_coinx['USD'][sym] = temp_balance_symbol.copy()
#             else:
#                 if temp_balance_symbol[sym] - float(balance_coinx['USD'][sym][sym]) != 0:
#                     diff += 'difference: ' + sym + ' ' + str(
#                         float(temp_balance_symbol[sym]) - float(balance_coinx['USD'][sym][sym]))
#                     diff += '  USD ' + str(
#                         float(temp_balance_symbol['USD']) - float(balance_coinx['USD'][sym]['USD']))
#                     tex += sym + '_USD\n' + sym + ':' + str(temp_balance_symbol[sym]) + '\nUSD:' + \
#                            str(temp_balance_symbol['USD']) + '\n' + diff + '\n\n'
#                 balance_coinx['USD'][sym][sym] = temp_balance_symbol[sym]
#                 balance_coinx['USD'][sym]['USD'] = temp_balance_symbol['USD']
#             coinx_key = account_info['USD'][sym]
#             ex_cx = [Exchange('bixin', key) for key in coinx_key]
#             a = [len(ex.api.get_my_depth([sym, 'USD'])) for ex in ex_cx]
#             if max(a) > 80:
#                 msg0 = MIMEText(sym + ' USD 账号可能无法撤单')
#                 msg0['Subject'] = '可能无法撤单'
#                 send_email_xl(msg0)
#                 send_email_yl(msg0)
#         except Exception as e:
#             print(e)
#     for sym in symbol_btc:
#         try:
#             temp_balance_symbol = get_symbol_balance_coinx([sym, 'BTC'])
#             diff = ''
#             if sym not in balance_coinx['BTC'].keys():
#                 balance_coinx['BTC'][sym] = temp_balance_symbol.copy()
#             else:
#                 if temp_balance_symbol[sym] - float(balance_coinx['BTC'][sym][sym]) != 0:
#                     diff += 'difference: ' + sym + ' ' + str(
#                         float(temp_balance_symbol[sym]) - float(balance_coinx['BTC'][sym][sym]))
#                     diff += '  BTC ' + str(
#                         float(temp_balance_symbol['BTC']) - float(balance_coinx['BTC'][sym]['BTC']))
#                     tex += sym + '_BTC\n' + sym + ':' + str(temp_balance_symbol[sym]) + '\nBTC:' + \
#                            str(temp_balance_symbol['BTC']) + '\n' + diff + '\n\n'
#                 balance_coinx['BTC'][sym][sym] = temp_balance_symbol[sym]
#                 balance_coinx['BTC'][sym]['BTC'] = temp_balance_symbol['BTC']
#             a = [len(ex.api.get_my_depth([sym, 'BTC'])) for ex in ex_cx]
#             if max(a) > 80:
#                 msg0 = MIMEText(sym + ' BTC 账号可能无法撤单')
#                 msg0['Subject'] = '可能无法撤单'
#                 send_email_xl(msg0)
#                 send_email_yl(msg0)
#         except Exception as e:
#             print(e)
#     print(tex)
#     msg = MIMEText(tex)
#     msg['Subject'] = '每小时账户报告'
#     send_email_xl(msg)
#     send_email_yl(msg)
#     # send_email_test(msg)
#     with open('./balance.txt', 'a') as f:
#         f.writelines(time.asctime())
#         f.writelines(json.dumps(balance_coinx))
#         f.writelines('\n')
#
#
# def check_balance_binance():
#     balance_bin_new = dict(balance_bin)
#     try:
#         ex_bin.refresh_account()
#         if ex_bin.account_info is False:
#             raise ValueError
#     except Exception:
#         print('binance account api error')
#     else:
#         balance_bin_new = {sym: float(ex_bin.account_info[sym]['avaid_balance']) for sym in symbol_bin}
#         if balance_bin_new['BTC'] < 0.1 and balance_bin_new['BTC'] != balance_bin['BTC']:
#             msg = MIMEText('BTC当前余额为' + str(balance_bin_new['BTC']))
#             msg['Subject'] = '币安余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#         elif balance_bin_new['LTC'] < 4 and balance_bin_new['LTC'] != balance_bin['LTC']:
#             msg = MIMEText('LTC当前余额为' + str(balance_bin_new['LTC']))
#             msg['Subject'] = '币安余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#         elif balance_bin_new['ETH'] < 2 and balance_bin_new['ETH'] != balance_bin['ETH']:
#             msg = MIMEText('ETH当前余额为' + str(balance_bin_new['ETH']))
#             msg['Subject'] = '币安余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#         elif balance_bin_new['QTUM'] < 10 and balance_bin_new['QTUM'] != balance_bin['QTUM']:
#             msg = MIMEText('QTUM当前余额为' + str(balance_bin_new['QTUM']))
#             msg['Subject'] = '币安余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#         elif balance_bin_new['USDT'] < 1000 and balance_bin_new['USDT'] != balance_bin['USDT']:
#             msg = MIMEText('USDT当前余额为' + str(balance_bin_new['USDT']))
#             msg['Subject'] = '币安余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#     return balance_bin_new
#
#
# def check_balance_huobi():
#     balance_huobi_new = dict(balance_huobi)
#     try:
#         ex_huobi.refresh_account()
#         if ex_huobi.account_info is False:
#             raise ValueError
#     except Exception:
#         print('huobi account api error')
#     else:
#         balance_huobi_new = {}
#         for sym in symbol_huobi:
#             for dic in ex_huobi.account_info:
#                 if dic['currency'] == sym.lower() and dic['type'] == 'trade':
#                     balance_huobi_new[sym] = float(dic['balance'])
#                     break
#         if balance_huobi_new['EOS'] < 20 and balance_huobi_new['EOS'] != balance_huobi['EOS']:
#             msg = MIMEText('EOS当前余额为' + str(balance_huobi_new['EOS']))
#             msg['Subject'] = '火币余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#         elif balance_huobi_new['DASH'] < 2 and balance_huobi_new['DASH'] != balance_huobi['DASH']:
#             msg = MIMEText('DASH当前余额为' + str(balance_huobi_new['DASH']))
#             msg['Subject'] = '火币余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#         elif balance_huobi_new['USDT'] < 500 and balance_huobi_new['USDT'] != balance_huobi['USDT']:
#             msg = MIMEText('USDT当前余额为' + str(balance_huobi_new['USDT']))
#             msg['Subject'] = '火币余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#     return balance_huobi_new
#
#
# def check_balance_coinw():
#     balance_cw_new = dict(balance_cw)
#     try:
#         ex_cw.refresh_account()
#         if ex_cw.account_info is False:
#             raise ValueError
#     except Exception:
#         print('coinw account api error')
#     else:
#         balance_cw_new = {sym: float(ex_cw.account_info[sym]['avaid_balance']) for sym in symbol_cw}
#         if balance_cw_new['Doge'] < 20000 and balance_cw_new['Doge'] != balance_cw['Doge']:
#             msg = MIMEText('DOGE当前余额为' + str(balance_cw_new['Doge']))
#             msg['Subject'] = 'coinw余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#         elif balance_cw_new['hpy'] < 10000 and balance_cw_new['hpy'] != balance_cw['hpy']:
#             msg = MIMEText('hpy当前余额为' + str(balance_cw_new['hpy']))
#             msg['Subject'] = 'coinw余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#         elif balance_cw_new['CNYT'] < 2000 and balance_cw_new['CNYT'] != balance_cw['CNYT']:
#             msg = MIMEText('CNYT当前余额为' + str(balance_cw_new['CNYT']))
#             msg['Subject'] = 'coinw余额警告'
#             send_email_xl(msg)
#             send_email_yl(msg)
#     return balance_cw_new


process = os.popen('ps -f -C python').read().split('\n')[1:-1]
process_short = [pr.split(' -u ')[1] for pr in process]
number_process = len(process_short)
report_balance_flag = False
# check_balance_coinx()

while True:
    # if int(time.strftime('%M')) in [0]:
    #     check_balance_coinx()
    a = os.popen('ps -f -C python').read().split('\n')[1:-1]
    b = [pr.split(' -u ')[1] for pr in a]
    print(time.asctime())
    print(len(b))
    if len(set(process_short).difference(set(b))) != 0:
        msg = MIMEText('有' + str(number_process - len(b)) + '个进程被意外关闭，当前为' + str(len(b)) + '个\n被关闭的进程为'
                       + str(set(process_short).difference(set(b))) + '\n')
        msg['Subject'] = '进程数量警告'
        send_email(msg, to_xl)
        send_email(msg, to_ht)
    number_process = len(b)
    process_short = list(b)
    # balance_bin = check_balance_binance()
    # balance_cw = check_balance_coinw()
    # balance_huobi = check_balance_huobi()
    time.sleep(55)
