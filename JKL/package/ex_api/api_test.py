from ex_api.exchange import Exchange, MyThread
import time
import random
import sys
import pycurl
import io
import certifi
import json
import hashlib
import base64
import pandas as pd


def tempcurl(url, headers, params, type):
    curl = pycurl.Curl()
    iofunc = io.BytesIO()
    curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
    curl.setopt(pycurl.CAINFO, certifi.where())
    curl.setopt(pycurl.HTTPHEADER, headers)
    if type == 'POST':
        curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
        curl.setopt(pycurl.POSTFIELDS, params)
    elif type == 'GET':
        curl.setopt(pycurl.CUSTOMREQUEST, 'GET')
    elif type == 'DELETE':
        curl.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
    # curl.setopt(pycurl.TIMEOUT, 15)
    # print(url)
    curl.setopt(pycurl.URL, url)
    curl.perform()
    ret = iofunc.getvalue().decode('utf-8')
    print(ret)
    ret = json.loads(ret)
    print(ret)
    return ret


url = 'http://api.bxx.com/api/data/login.jhtml?userCode=15000000001&password=bxx001&mastKey=2cb8aabb1ea2c2728afa8c9b3c675f27'
url = 'http://47.75.159.37:80/checkAccount'
header = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
          'Connection': 'keep-alive',
          'X-Requested-With': 'XMLHttpRequest'}
data = {'userCode': '15000000001', 'password': 'bxx001', 'mastKey': '2cb8aabb1ea2c2728afa8c9b3c675f27'}
tempcurl(url, header, json.dumps(data), 'POST')
import requests
a=requests.post(url,headers=header,data=data)
#
#
# # order
# def order(account_id, symbol, side, quantity, price):
#     access_token = all_token[account_id]
#     headers = ["Content-Type: application/json", "Authorization: " + access_token]
#     url = 'http://47.52.147.151:8080/v2/s/trade/order/entrusts'
#     params = {
#         "price": price,
#         "symbol": symbol,
#         "type": 1,
#         "volume": quantity,
#     }
#     if side == 'sell':
#         params['type'] = 2
#     params = json.dumps(params)
#     ret = tempcurl(url, headers, params, 'POST')
#     return ret
#
#
# # order_list
# def get_my_depth(account_id, symbol, page=1, size=100):
#     access_token = all_token[account_id]
#     headers = ["Content-Type: application/json", "Authorization: " + access_token]
#     url = 'http://47.52.147.151:8080/v2/s/trade/order/entrusts/' + symbol + '/' + str(page) + '/' + str(size)
#     params = {
#     }
#     params = json.dumps(params)
#     tempcurl(url, headers, params, 'GET')
#     ret = tempcurl(url, headers, params, 'GET')
#     return ret['data']['records']
#
#
# # cancel
# def cancel(account_id, order_id):
#     access_token = all_token[account_id]
#     headers = ["Content-Type: application/json", "Authorization: " + access_token]
#     url = 'http://47.52.147.151:8080/v2/s/trade/order/entrusts/' + str(order_id)
#     params = {
#     }
#     params = json.dumps(params)
#     ret = tempcurl(url, headers, params, 'DELETE')
#     return ret
#
#
# def cancel_all():
#     thp_cancel = []
#     thp_my_depth = []
#     for i in range(len(all_token)):
#         thp_my_depth.append(MyThread(get_my_depth, args=(i, 'BTCUSDT')))
#     st = time.time()
#     [th.start() for th in thp_my_depth]
#     [th.join() for th in thp_my_depth]
#     print(time.time() - st)
#     account_order = [th.get_result() for th in thp_my_depth]
#     for i in range(len(all_token)):
#         orders = account_order[i]
#         for o in orders:
#             oid = o['orderId']
#             thp_cancel.append(MyThread(cancel, args=(i, oid)))
#     st = time.time()
#     [th.start() for th in thp_cancel]
#     [th.join() for th in thp_cancel]
#     print(time.time() - st)
#
#
# # login
# def get_token(access_key, secret):
#     url = 'http://47.52.147.151:8080/v2/u/cgi-bin/token?access_key=' + access_key + '&secret=' + secret
#     headers = ["Content-Type: application/json"]
#     params = {}
#     params = json.dumps(params)
#     ret = tempcurl(url, headers, params, 'GET')
#     return ret['data']['access_token']
#
#
# # all_token = []
# # data = pd.read_table('test_account.txt')
# # access_key_id = list(data['access_key_id'])
# # secret_key = list(data['access_key_secret'])
# # thp_token = []
# # for i in range(len(secret_key)):
# #     thp_token.append(MyThread(get_token, args=(access_key_id[i], secret_key[i],)))
# # tim = time.time()
# # [th.start() for th in thp_token]
# # [th.join() for th in thp_token]
# # print(time.time() - tim)
# # all_token = [th.get_result() for th in thp_token]
#
# data = pd.read_table('tokens.txt', header=None)
# all_token = list(data.iloc[:, 0])
# while True:
#     # thp_order_buy = []
#     # for i in range(500):
#     #     thp_order_buy.append(MyThread(order, args=(i, 'BTCUSDT', 'buy', 1, 7000)))
#     thp_order_sell = []
#     for i in range(1000, 1500):
#         thp_order_sell.append(MyThread(order, args=(i, 'BTCUSDT', 'sell', 1, 7000)))
#     st = time.time()
#     # [th.start() for th in thp_order_buy]
#     [th.start() for th in thp_order_sell]
#     # [th.join() for th in thp_order_buy]
#     [th.join() for th in thp_order_sell]
#     # time.sleep(1)
#     print(time.time() - st)
#
import asyncio
import aiohttp
import pandas as pd
import json
import time

data = pd.read_table('tokens.txt', header=None)
all_token = list(data.iloc[:, 0])


# async session = aiohttp.ClientSession()

# headers = {
#     "Content-Type": "application/json",
#     "Authorization": all_token[0]
# }
# url = 'http://47.52.147.151:8080/v2/s/trade/order/entrusts'
# params = {
#     "price": 7000,
#     "symbol": 'BTCUSDT',
#     "type": 1,
#     "volume": 1,
# }


async def order(session, account_id, side):
    params = {
        "price": 1,
        "symbol": 'BTCUSDT',
        "type": 1,
        "volume": 1,
    }
    if side == 'sell':
        params['type'] = 2
    url = 'http://47.52.147.151:8080/v2/s/trade/order/entrusts'
    headers = {
        "Content-Type": "application/json",
        "Authorization": all_token[account_id]
    }
    async with session.post(url, data=json.dumps(params), headers=headers) as resp:
        print(await resp.json())


async def get_account(session, account_id):
    url = 'http://47.52.147.151:8080/v2/s/account/accounts'
    headers = {
        "Content-Type": "application/json",
        "Authorization": all_token[account_id]
    }
    async with session.get(url, headers=headers) as resp:
        print(await resp.json())
        return await resp.json()


async def main_test():
    st = time.time()
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(2000):
            tasks.append(asyncio.ensure_future(order(session, i, 'sell')))
        for i in range(2000, 4000):
            tasks.append(asyncio.ensure_future(order(session, i, 'buy')))
        await asyncio.wait(tasks)
        print(time.time() - st)


async def main_accounts():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(4000):
            tasks.append(asyncio.ensure_future(get_account(session, i)))
        await asyncio.wait(tasks)
        return [task.result()['data']['assertList'][0:2] for task in tasks]


while True:
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_test())
# loop1.close()

loop = asyncio.get_event_loop()
res = loop.run_until_complete(main_accounts())

btc_amount = [re[1]['carryingAmount'] for re in res]

for ex in ex_bxx:
    ex.api.get_account()[0]