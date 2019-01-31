from ex_api.api import base_api
import pycurl
import hmac
import hashlib
import json
import base64
import io
import certifi
import urllib
from urllib import parse
import time


class api_coinegg(base_api):
    def __init__(self, key):
        self.api_key = key[0]
        self.secret_key = key[1]
        self.region = 'usc'

    def __sym(self, symbol):
        return symbol[0].lower(), symbol[1].lower()

    def __sign(self, message_c):
        signature = hmac.new(hashlib.md5(self.secret_key.encode('ascii')).hexdigest().encode(),
                             message_c.encode('ascii'),
                             digestmod=hashlib.sha256).hexdigest()
        return signature

    def __api_call(self, method, xtype, params='', reg=True):
        headers = ['Content-Type: multipart/form-data_NK_HS-YM']
        base_endpoint = 'https://api.coinegg.com'
        curl, iofunc = self.initcurl(xtype)
        curl.setopt(pycurl.USERAGENT,
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
        if xtype == 0:
            if reg is True:
                url = base_endpoint + method + '/region/' + self.region + '?' + self.sort_params(params)
            else:
                url = base_endpoint + method + '?' + self.sort_params(params)
        if xtype == 1:
            if reg is True:
                url = base_endpoint + method + '/region/' + self.region
            else:
                url = base_endpoint + method
            curl.setopt(pycurl.HTTPHEADER, headers)
            params['signature'] = self.__sign(urllib.parse.urlencode(params))
            post_data = []
            for ke in params.keys():
                post_data.append((ke, str(params[ke])))
            # print(post_data)
            curl.setopt(pycurl.HTTPPOST, post_data)
        curl.setopt(pycurl.URL, url)
        # print(url)
        # print(params)
        try:
            curl.perform()
        except Exception as e:
            print(e)
            print('Error: curl.perform')
            return False
        ret_message = iofunc.getvalue().decode('utf-8')
        # print(ret_message)
        curl.close()
        iofunc.close()
        try:
            ret = json.loads(ret_message)
        except Exception as e:
            print(e)
            print('Error: json.loads')
            return False
        else:
            return ret

    def get_depth(self, symbol):
        method = '/api/v1/depth'
        symbol, self.region = self.__sym(symbol)
        params = {
            'coin': symbol
        }
        ret = self.__api_call(method, 0, params)
        return ret

    def get_account(self):
        method = '/api/v1/balance/'
        params = {
            'key': self.api_key,
            'nonce': int(time.time() * 1000)
        }
        ret = self.__api_call(method, 1, params, reg=False)
        return ret

    def cancel(self, orderid):
        method = '/api/v1/trade_cancel'
        params = {
            'key': self.api_key,
            'nonce': int(time.time() * 1000)
        }


# key = ['3eedg-k6efr-1i75v-fbzvc-ndwfj-9frxu-mz91c',
#        'WOHa4-kaJAm-z{LxX-(3a.D-U7^z1-Y3$15-rWS//']
#
# api = api_coinegg(key)
# api.get_account()
# api.get_depth(['HART', 'USC'])

# curl https://api.coinegg.com/api/v1/balance?key=3eedg-k6efr-1i75v-fbzvc-ndwfj-9frxu-mz91c&nonce=1524036285798&signature=d2ea471f4f45e11761e22f1e9495e0cc949309524b20d2edd6c0f316e1cd4873

# post_data = [('key', 'ed6pr-vs9h3-8zsq8-17nck-nk56q-s5vth-m7vtv'),
#              ('signature', '4ca6a4deee4cbf95890542f4d91715833f8bda17de830fd72ed91ef7b6648f65'),
#              ('nonce', '1524131069837')]
# url_post = 'https://api.coinegg.com/api/v1/balance/'
# crl = pycurl.Curl()
# crl.setopt(pycurl.URL, url_post)
# crl.setopt(pycurl.CUSTOMREQUEST, 'POST')
# crl.setopt(pycurl.HTTPPOST, post_data)
# strUserAgent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36"
# crl.setopt(pycurl.USERAGENT, strUserAgent)
# strHeader = ['Content-Type: multipart/form-data_NK_HS-YM']
# crl.setopt(pycurl.HTTPHEADER, strHeader)
#
# iofunc = io.BytesIO()
# crl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
