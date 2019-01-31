from urllib import parse
import pycurl
import hashlib
import hmac
import json
import io
import certifi
import requests
import time


class api_bitmex():
    def __init__(self, key):
        self.api_key = key[0]
        self.bsecret = key[1].encode()
        self.base_root = 'https://www.bitmex.com/api/v1'
        self.r = requests.Session()
        self.r.headers['api-key'] = self.api_key
        self.r.headers['content-type'] = 'application/json'

    def __sym(self, symbol):
        return symbol.upper()

    def __sign(self, type, path, nonce, data):
        msg = type + '/api/v1' + path + str(nonce) + str(data)
        return hmac.new(self.bsecret, msg.encode(), digestmod=hashlib.sha256).hexdigest()

    def __refresh_header(self, type, path, data):
        expires = int(round(time.time()) + 3600)
        self.r.headers['api-expires'] = str(expires)
        self.r.headers['api-signature'] = self.__sign(type, path, expires, data)

    def api_get(self, method):
        self.__refresh_header('GET', method, '')
        res = self.r.get(self.base_root + method)
        return res.json()

    def api_post(self, method, data):
        self.__refresh_header('POST', method, data)
        res = self.r.post(self.base_root + method, json=data)
        return res.json()
