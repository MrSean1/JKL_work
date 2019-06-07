import requests

# account = [30266263, 30266262, 30268]

# sp

p = {
    "userId": "1001524404",
    "accNo": "1001524404",
    "host": "14.136.212.168",
    "appId": "QVSR",
    "licence": "IH83N1IC37G445KZ3",
    "password": "628883"
}
ret = requests.post("http://47.75.194.25:8081/addUser", json=p)
c = 'B0291F296F77054360BE016AABF6DF17'

# 福汇测试账户
dic = {
    "account": 96109442,
    "password": "qwe12345",
    "broker": "FXCM-USDReal04"
}
# 俄罗斯账户 13250
dic = {
    "account": 1500044308,
    "password": "mhww28",
    "broker": "ICMarkets-Live15"
}
# 罗总账户 13454.82
dic = {
    "account": 1100039838,
    "password": "Ww302010",
    "broker": "ICMarkets-Live11"
}
# 刘志强 12470.36
dic = {
    "account": 1100034678,
    "password": "Ww302010",
    "broker": "ICMarkets-Live11"
}
# 成桂燕 16969.86
dic = {
    "account": 1100035190,
    "password": "Ww302010",
    "broker": "ICMarkets-Live11"
}
# 百利好测试账户
dic = {
    "account": 65892105,
    "password": "cbb788",
    "broker": "PlotioFX-Live"
}
# 百利好延迟账户 3008.48
dic = {
    "account": 65653090,
    "password": "dgf467",
    "broker": "PlotioFX-Live"
}
# IC延迟账户 13571.3
dic = {
    "account": 1100035201,
    "password": "Ww302010",
    "broker": "ICMarkets-Live11"
}
# divisa无延迟账户
dic = {
    "account": 1060062,
    "password": "2kqkYqM",
    "broker": "EquitiUS-Live"
}

# 罗总大额账户
dic = {
    "account": 727318,
    "password": "luoweijia",
    "broker": "ICMarkets-Live06"
}
dic = {
    "account": 727384,
    "password": "luoweijia",
    "broker": "ICMarkets-Live06"
}
# 0404账户
dic = {
    "account": 936204,
    "password": "654321",
    "broker": "ICMarkets-Live08"
}
# 欧福

a = requests.post("http://47.75.194.25:8989/addAccount", json=dic)

# ADSS
ip = '35.177.25.61'
a
ip = '35.178.11.110'
dic = {
    "account": 222057267,
    "password": "zl123123.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057274,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057751,
    "password": "yxt123456!",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057730,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057728,
    "password": "lxl1394042.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057873,
    "password": "jzm199737.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057937,
    "password": "zzh123456!",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057875,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057942,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057943,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057982,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222057985,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
ip = '35.178.11.110'
dic = {
    "account": 222058034,
    "password": "jzm199737.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222058031,
    "password": "jzm199737.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222058035,
    "password": "jzm199737.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222058041,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
ip = '35.177.25.61'
dic = {
    "account": 222058036,
    "password": "jzm199737.",
    "broker": "ADSS-Live1"
}
dic = {
    "account": 222058100,
    "password": "Anna123456.",
    "broker": "ADSS-Live1"
}

# IFCMarkets-Real

dic = {
    "account": 59466,
    "password": "gJRavS1R@M",
    "broker": "IFCMarkets-Real"
}
dic = {
    "account": 59575,
    "password": "C@p@DNCFQ2",
    "broker": "IFCMarkets-Real"
}
dic = {
    "account": 59670,
    "password": "!1pMwc@v3r",
    "broker": "IFCMarkets-Real"
}

# SimpleFX-LiveUK

dic = {
    "account": 233815,
    "password": "yy186186bb",
    "broker": "SimpleFX-LiveUK"
}
dic = {
    "account": 233873,
    "password": "aa186186bb",
    "broker": "SimpleFX-LiveUK"
}
dic = {
    "account": 233877,
    "password": "zy123456",
    "broker": "SimpleFX-LiveUK"
}
ip = '35.177.25.61'
dic = {
    "account": 232841,
    "password": "QBZ79856",
    "broker": "SimpleFX-LiveUK"
}
ip = '35.178.11.110'
dic = {
    "account": 232989,
    "password": "ZJ38138",
    "broker": "SimpleFX-LiveUK"
}
dic = {
    "account": 232911,
    "password": "WLS84572",
    "broker": "SimpleFX-LiveUK"
}
dic = {
    "account": 233862,
    "password": "luoweijia1",
    "broker": "SimpleFX-LiveUK"
}
dic = {
    "account": 233875,
    "password": "gh123456",
    "broker": "SimpleFX-LiveUK"
}
dic = {
    "account": 233878,
    "password": "xx186186hh",
    "broker": "SimpleFX-LiveUK"
}
dic = {
    "account": 234116,
    "password": "Yxt123456",
    "broker": "SimpleFX-LiveUK"
}
dic = {
    "account": 234123,
    "password": "fjj123456",
    "broker": "SimpleFX-LiveUK"
}

# ThinkForexAU-Live

dic = {
    "account": 9767134,
    "password": "8eAZOPCQ",
    "broker": "ThinkForexAU-Live"
}
dic = {
    "account": 9767126,
    "password": "1TSYSlgW",
    "broker": "ThinkForexAU-Live"
}
dic = {
    "account": 9767128,
    "password": "0FYykEaf",
    "broker": "ThinkForexAU-Live"
}
dic = {
    "account": 9764782,
    "password": "qq010203",
    "broker": "ThinkForexAU-Live"
}
dic = {
    "account": 9765714,
    "password": "qq010203",
    "broker": "ThinkForexAU-Live"
}

# IC 自己

dic = {
    "account": 942532,
    "password": "bxst15",
    "broker": "ICMarkets-Live08"
}
dic = {
    "account": 1100036191,
    "password": "pvri58",
    "broker": "ICMarkets-Live11"
}
dic = {
    "account": 1100033670,
    "password": "Ww302010",
    "broker": "ICMarkets-Live11"
}
dic = {
    "account": 937316,
    "password": "nspt50",
    "broker": "ICMarkets-Live08"
}
dic = {
    "account": 937323,
    "password": "jicj62",
    "broker": "ICMarkets-Live08"
}

# AVA
dic = {
    "account": 80031475,
    "password": "ZJchongqing123",
    "broker": "Ava-Real 5"
}

# XTRINT-Live
dic = {
    "account": 155974,
    "password": "Aa123456",
    "broker": "XTRINT-Live"
}

# demo
dic = {
    "account": 9017158,
    "password": "do2yrol",
    "broker": "ADSS-Demo"
}
dic = {
    "account": 9017159,
    "password": "pui1kqi",
    "broker": "ADSS-Demo"
}
dic = {
    "account": 9017161,
    "password": "1pewkfh",
    "broker": "ADSS-Demo"
}
dic = {
    "account": 9019080,
    "password": "xdmy1og",
    "broker": "ADSS-Demo"
}
dic = {
    "account": 9020129,
    "password": "1jrjftg",
    "broker": "ADSS-Demo"
}
dic = {
    "account": 9020130,
    "password": "uev1lxp",
    "broker": "ADSS-Demo"
}
dic = {
    "account": 9020131,
    "password": "v8qxmez",
    "broker": "ADSS-Demo"
}

# IC MT5

dic = {
    "account": 5088218,
    "password": "eWzGquB9",
    "broker": "ICMarkets-MT5"
}
dic = {
    "account": 5087518,
    "password": "yHqNPdih",
    "broker": "ICMarkets-MT5"
}
dic = {
    "account": 5087542,
    "password": "YpKMvX2a",
    "broker": "ICMarkets-MT5"
}
dic = {
    "account": 5087122,
    "password": "h9Mzm1DQ",
    "broker": "ICMarkets-MT5"
}
dic = {
    "account": 5089416,
    "password": "pyPNJh1W",
    "broker": "ICMarkets-MT5"
}

# IC demo
dic = {
    "account": 50093009,
    "password": "cAxaP1pG",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50093013,
    "password": "HZK2MwBn",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50093012,
    "password": "Ljc6YMw6",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50095716,
    "password": "DPyVsxba",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50095717,
    "password": "Y6zkq92u",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50095718,
    "password": "7h26pBdi",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50095719,
    "password": "LtbMLCcE",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50095720,
    "password": "bg9Rs9Qy",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50095721,
    "password": "XI9bwJxF",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50095722,
    "password": "YkTCk7ZM",
    "broker": "5*207.246.127.101:1950"
}
dic = {
    "account": 50095723,
    "password": "tRdjBNmC",
    "broker": "5*207.246.127.101:1950"
}

import time

a = ['VRTX',
     'TLRY',
     'ADP',
     'CME',
     'MAR',
     'DISH',
     'ADI',
     'AMGN',
     'TMUS',
     'FOX',
     'CSX',
     'PEP',
     'TXN',
     'CTSH',
     'PYPL',
     'EA',
     'MDLZ',
     'GILD',
     'WBA',
     'SBUX',
     'CELG',
     'FOXA',
     'AMAT',
     'CRON', ]
t = list()
for i in range(5):
    for j in a:
        t1 = time.time()
        info = dict()
        info['operation'] = 'stock'
        info['opera'] = j
        ret = requests.post("http://47.75.151.240:8009/share/buy_shares/", data=info).json()
        if ret['msg'] == '写入文件成功':
            print('写入成功')
        else:
            print('失败了')
        while True:
            ret2 = requests.post("http://47.75.151.240:8009/share/check_info/", data=info).json()
            if ret2['msg'] == '信息存在':
                continue
            else:
                print(ret2)
                break
        t2 = time.time()
        t3 = t2 - t1
        print(t3)
        t.append(t3)

# 挂单方式
info = {'method': 'buy', 'operation': 'CHFJPY', 'number': '100', 'price': '160.55', }
requests.post("http://47.75.151.240:8009/share/buy_shares/", data=info).json()
# 查询是否挂完
info = {'method': 'buy', 'operation': 'ADP.NAS', 'number': '100', 'price': '160.55', }
requests.post("http://47.75.151.240:8009/share/check_info/", data=info).json()
# 撤销挂单
info = {"share": "CME", "param": "182"}
requests.post("http://47.75.151.240:8009/share/buy_shares/", data=info).json()
# 查询是否挂完
info = {"share": "CME", "param": "182"}
requests.post("http://47.75.151.240:8009/share/check_info/", data=info).json()

import requests
import time

t1 = time.time()
info = {'method': 'sell', 'operation': 'BTCUSD', 'number': '100', 'price': '8100'}
result = requests.post("http://47.75.151.240:8009/share/buy_shares/", data=info).json()
print(result)
while True:
    ret = requests.post("http://47.75.151.240:8009/share/check_info/", data=info).json()
    if ret['msg'] == '文件不存在':
        print(ret)
        break
    else:
        continue
t2 = time.time()
print(t2 - t1)

import requests
import time

t1 = time.time()
info = {"share": "cancle", 'param': '123354'}
result = requests.post("http://47.75.151.240:8009/share/buy_shares/", data=info).json()
print(result)
while True:
    ret = requests.post("http://47.75.151.240:8009/share/check_info/", data=info).json()
    if ret['msg'] == '文件不存在':
        print(ret)
        break
    else:
        continue
t2 = time.time()
print(t2 - t1)
