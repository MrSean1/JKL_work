import requests
from mt4_account import MT4Account

sp_account = p = {
    "userId": "73883259",
    "accNo": "73883259",
    "host": "f1.xyzq.com.hk",
    "appId": "XYZQ",
    "licence": "8871B82FB6233160",
    "password": "qq123456"
}

demo_acc = {
    "account": 9014325,
    "password": "3xsacls",
    "broker": "ADSS-Demo"
}
demo_acc = {
    "account": 9014328,
    "password": "x3lzlup",
    "broker": "ADSS-Demo"
}

acc_1 = {
    "account": 222057151,
    "password": "asm123123.",
    "broker": "ADSS-Live1"
}
acc_2 = {
    "account": 222057267,
    "password": "zl123123.",
    "broker": "ADSS-Live1"
}
acc_3 = {
    "account": 222057730,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
acc_4 = {
    "account": 222057152,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
acc_5 = {
    "account": 222057153,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
acc_6 = {
    "account": 222057270,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
acc_7 = {
    "account": 222057274,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
acc_8 = {
    "account": 222057728,
    "password": "lxl1394042.",
    "broker": "ADSS-Live1"
}
acc_9 = {
    "account": 222057745,
    "password": "zzh123456!",
    "broker": "ADSS-Live1"
}
acc_10 = {
    "account": 222057751,
    "password": "yxt123456!",
    "broker": "ADSS-Live1"
}
acc_11 = {
    "account": 222057800,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
acc_12 = {
    "account": 222057801,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}

acc_13 = {
    "account": 222057797,
    "password": "jzm123456.",
    "broker": "ADSS-Live1"
}
acc_FX_13 = {
    "account": 635443,
    "password": "UTy3Hec3",
    "broker": "FxPro.com-Real06"
}
acc_IFC_13 = {
    "account": 59466,
    "password": "zJ97LjT",
    "broker": "IFCMarkets-Real"
}


# mt4_url = 'http://47.75.194.25:8989/addAccount'
# mt4_url = 'http://47.75.195.6:8989/addAccount'
mt4_url = 'http://47.244.37.23:8989/addAccount'
sp_url = 'http://47.75.194.25:8081/addUser'

response = requests.post(mt4_url, json=demo_acc)
requests.post(mt4_url, json=demo_acc).json()
requests.post(sp_url, json=sp_account).json()
