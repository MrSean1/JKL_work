# *_*coding:utf-8 *_*
import time
import random
import pycurl
import hmac
import hashlib
import io
import certifi
import json
import pandas as pd

class get_data():

    def __api_call(self, url, headers, type, params=json.dumps({})):
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
        curl.setopt(pycurl.TIMEOUT, 30)
        print(url)
        curl.setopt(pycurl.URL, url)
        # curl.getinfo(pycurl.HTTP_CODE)
        print("Http Code:\t%s" % curl.getinfo(curl.HTTP_CODE))
        try:
            curl.perform()
            ret = iofunc.getvalue().decode('utf-8')

        except Exception as e:
            print(e)
            return False
        print(ret)
        try:
            ret = json.loads(ret)
        except Exception as e:
            print(e)
            return False
        return ret

    def get_data(self):
        start_number = 0
        end_number = 1

        # params = {
        #     'start': start_number,
        #     'end': end_number,
        # }
        headers = ["Content-Type: application/json",
                   "Cookie: __cfduid=d429592a42efd4a565797f65c7440e51c1542091056; quanto_referrer=None; quanto_landing=%2Fhome; _ga=GA1.2.1098452085.1542091064; quanto_device=f4ca45eee0e550e19d93d0a3d59407fa; seen_data_modal=true; quanto_session_id=session_5bee53e78b7c76003e8925c9; _gid=GA1.2.1910204725.1542345703; community_home=%2Fposts; research_logout_url=ZzA4bkRxcjh6dFZ0R29SUTFUM0RLdz09LS1TZ0RabDAza2xJWllpYTVZMEZ3bW1BPT0%3D--1a89319843459794167ff4f8ce3224e65e267ce2; first_session=%7B%22visits%22%3A59%2C%22start%22%3A1542091064134%2C%22last_visit%22%3A1542357455139%2C%22url%22%3A%22https%3A%2F%2Fwww.quantopian.com%2F%22%2C%22path%22%3A%22%2F%22%2C%22referrer%22%3A%22%22%2C%22referrer_info%22%3A%7B%22host%22%3A%22www.quantopian.com%22%2C%22path%22%3A%22%2F%22%2C%22protocol%22%3A%22https%3A%22%2C%22port%22%3A80%2C%22search%22%3A%22%22%2C%22query%22%3A%7B%7D%7D%2C%22search%22%3A%7B%22engine%22%3Anull%2C%22query%22%3Anull%7D%2C%22prev_visit%22%3A1542357443274%2C%22time_since_last_visit%22%3A11865%2C%22version%22%3A0.4%7D; mp_75873953cd404bcc1da88a55ff51e3b4_mixpanel=%7B%22distinct_id%22%3A%20%221670bca4636511-00d3a3cf5912ad-3961430f-1fa400-1670bca46371237%22%2C%22%24device_id%22%3A%20%221670bca4636511-00d3a3cf5912ad-3961430f-1fa400-1670bca46371237%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22__mps%22%3A%20%7B%7D%2C%22__mpso%22%3A%20%7B%7D%2C%22__mpus%22%3A%20%7B%7D%2C%22__mpa%22%3A%20%7B%7D%2C%22__mpu%22%3A%20%7B%7D%2C%22__mpap%22%3A%20%5B%5D%2C%22__alias%22%3A%20%225bea71614aada0004752ed6b%22%2C%22%24email%22%3A%20%22wht190421%40163.com%22%2C%22user_id%22%3A%20%225bea71614aada0004752ed6b%22%2C%22%24user_id%22%3A%20%225bea71614aada0004752ed6b%22%7D; quanto_ide_main_splitter=340px; mp_mixpanel__c=41; _qf_session_v2=aWxNYzNLS1BsTnc1OEtrV2RENzFPSGpyRExTcURDV3dRRU1sNm9HYXdVTm5FSUpwb3VrYlRXYW0xaUJuMFdxdmdJdWcrWEhTQnVMNnpKN1R2N0t2RElpc09rVEJqVUFoR0svK3F1bVEvazRQQXhjMTZ1OCtaMUgzYVp4NlBNOG41TVVLUW9sa2dTa1hCcTRvclQ0ek1qYXNnRHFMNk0yR0ptYUxtZTNJdUZGaE5jR2JiR2V0ZCtIc0h1a2trL0VVa2NjWW5Vdm9XZHlreG1qVmJJSHNzaDQxYVM1U0l1WTljMDkzV1FISkNZQUp3U2hFQzRSVkJ6aHF5SlFiT1JsSDl4ZExTYWoyZUpYK1hoSVRWSlc2Y1Q5TTQ5SDh0SHc4Y0pJVC8waW4rSHhsa3VycGxDOVMwRldLWmJiV3c1UEk2V3BrSE1tVzVORzJMcysyM2xGc0ZBNjh2ZXpCb0Vjbi9ZWTFjWDlSOTAxL3k5Z2Ywa0tnZ0NvbE1xeW9BbWQxUFI4YnQrMnhLbi9WWmxrMmFYbEhGbDdENE9BOGJUR3FZYUM0ZTN5ZmpTODZzd3Fac0YvQmRlRXFaS1lqaXRMbHRBVlRHM1crZ05OakhHdFZIWVNWOTFSNVgya0VoQUwyT25mUHExRTV4S0dndXdneGRwR1c3RnZMZlBQUytYbkNKeC84emJhVno3R3kweHg5RG5jYlE0bmVzWWRMazY3bTFEeWxOa09aTVR4cU1tUzIzY0pLNjNkaTN5bktHdk50WkFyRGZoOFBiZll3STRzdUhFTmNOdz09LS1tTTZCQzNnSy9GZC9tb1VtYW1kd3lRPT0%3D--02f4de9af6fa85e60e377da2d371bb4f08a1593e"
                   "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
                   ]
        # ret = self.__api_call(url, headers, 'GET')
        # print(ret)
        while True:
            fileName = 'YM.cvs'
            number = 1
            start_number = end_number
            end_number += 499
            url = 'https://www.quantopian.com/backtests/log_entries?backtest_id=5bee81de7e85014a39e34675&start=%s&end=%s' % (
                start_number, end_number)
            ret = self.__api_call(url, headers, 'GET')
            self.write_data(ret, fileName, number)
            number += 1
            if start_number >= ret['data_NK_HS-YM']['max_avail']:
                break
        print('写完了')

    def get_token(self):
        url = 'https://www.quantopian.com/users/sign_in'
        headers = ["Content-Type: application/json",
                   "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
                   "Accept-Language: zh-CN,zh;q=0.9",
                   "Accept-Encoding: gzip, deflate, br"
                   ]
        params = {
            'email': 'wht190421@163.com',
            'password': 'WANG190421',
            'remember_me': '0'
        }
        params = json.dumps(params)
        ret = self.__api_call(url, headers, 'POST', params)
        print(ret)
        return ret

    def write_data(self, ret, fileName, number):
        data = []
        for i in ret['data_NK_HS-YM']['logs']:
            message = i['m'].split('\n')
            for i in message:
                # colnum = [j for j in i[0].split(' ') if j != '']
                value = [j for j in i[1].split(' ') if j != '']
                print(value)
                value[1] = value[1].split('+')[0]
                data.append(value)
        data_f = pd.DataFrame(data)
        try:
            if number == 1:
                csv_headers = ['data_NK_HS-YM', 'time', 'close', 'high', 'low', 'open', 'volume']
                data_f.to_csv(fileName, header=csv_headers, index=False, mode='a+', encoding='utf-8')
            else:
                data_f.to_csv(fileName, header=False, index=False, mode='a', encoding='utf-8')

        except UnicodeEncodeError:
            print("编码错误, 该数据无法写到文件中, 直接忽略该数据")
        print('写完一个')

# user%5Bemail%5D=wht190421%40163.com&user%5Bpassword%5D=WANG190421&user%5Bremember_me%5D=0
# user%5Bemail%5D=wht190421%40163.com&user%5Bpassword%5D=WANG190421&user%5Bremember_me%5D=0
