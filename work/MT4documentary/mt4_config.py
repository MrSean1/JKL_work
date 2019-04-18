# *_*coding:utf-8 *_*
all_account = {'main_account': "9014442",
               'fallow_account': ["9014435", "9014492"],
               }

account_level = dict()

# , "9013778", "9014123", '9014124', '9014125', '9014127'

# pos = dict()
pos = {
    '9014435': 0.10019084106045713,
    '9014492': 0.19745577969502645
    # '9013777': 1.9208740318845979,
    # '9013778': 1.2170707689032019,
    # '9014123': 1.6634285258031032,
    # '9014124': 166.4285258031032,
    # '9014125': 33.26857051606206,
    # '9014127': 166.3428525803103
}
# for f_acc in all_account['fallow_account']:
#     pos[f_acc] = account_level[f_acc]

em_user = '295861809@qq.com'
pwd = 'qxkrwbmoxosdbhfi'
address = ['295861809@qq.com', ]
smtp_server = 'smtp.qq.com'

# get_depth  完成返回值
# a = {'msg': 'success', 'code': 1,
#      'data': {'LOW': 1.12808, 'HIGH': 1.13223, 'TIME': '2019-04-17T03:34:11.000+0000', 'BID': 1.13103, 'ASK': 1.13119,
#               'POINT': 1e-05, 'DIGITS': 5.0, 'SPREAD': 16.0, 'STOPLEVEL': 10.0, 'LOTSIZE': 100000.0, 'TICKVALUE': 1.0,
#               'TICKSIZE': 1e-05, 'SWAPLONG': -2.38, 'SWAPSHORT': 0.72, 'STARTING': 0.0, 'EXPIRATION': 0.0,
#               'TRADEALLOWED': 1.0, 'MINLOT': 0.01, 'LOTSTEP': 0.01, 'MAXLOT': 1000.0, 'SWAPTYPE': 0.0,
#               'PROFITCALCMODE': 0.0, 'MARGINCALCMODE': 0.0, 'MARGININIT': 0.0, 'MARGINMAINTENANCE': 0.0,
#               'MARGINHEDGED': 0.0, 'MARGINREQUIRED': 226.24, 'FREEZELEVEL': 5.0}}
# b = {'msg': 'success', 'code': 1,
#      'data': {'LOW': 70.665, 'HIGH': 72.005, 'TIME': '2019-04-16T11:59:59.000+0000', 'BID': 71.555, 'ASK': 71.655,
#               'POINT': 0.001, 'DIGITS': 3.0, 'SPREAD': 100.0, 'STOPLEVEL': 20.0, 'LOTSIZE': 1.0, 'TICKVALUE': 0.001,
#               'TICKSIZE': 1e-05, 'SWAPLONG': 0.0, 'SWAPSHORT': 0.0, 'STARTING': 0.0, 'EXPIRATION': 0.0,
#               'TRADEALLOWED': 0.0, 'MINLOT': 1.0, 'LOTSTEP': 0.01, 'MAXLOT': 1000.0, 'SWAPTYPE': 0.0,
#               'PROFITCALCMODE': 2.0, 'MARGINCALCMODE': 3.0, 'MARGININIT': 0.0, 'MARGINMAINTENANCE': 0.0,
#               'MARGINHEDGED': 0.0, 'MARGINREQUIRED': 358.28, 'FREEZELEVEL': 10.0}}
