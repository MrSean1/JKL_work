import base64
import datetime
import hashlib
import hmac
import json
import urllib
import urllib.parse
import urllib.request
import pycurl
import io
import certifi


class api_hadax:
    def __init__(self, key):
        # 此处填写APIKEY
        self.ACCESS_KEY = key[0]
        self.SECRET_KEY = key[1]
        # API 请求地址
        self.MARKET_URL = "https://api.hadax.com"
        self.TRADE_URL = "https://api.hadax.com"
        self.acc_id = ''

    def http_get_request(self, url, params, add_to_headers=None):
        postdata = urllib.parse.urlencode(params)
        ret_url = url + '?' + postdata
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.TIMEOUT, 15)
        curl.setopt(pycurl.CUSTOMREQUEST, 'GET')
        curl.setopt(pycurl.URL, ret_url)
        curl.setopt(pycurl.USERAGENT,
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
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

    def http_post_request(self, url, params, add_to_headers=None):
        ret_url = url
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.TIMEOUT, 15)
        curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
        curl.setopt(pycurl.URL, ret_url)
        curl.setopt(pycurl.POSTFIELDS, json.dumps(params))
        curl.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
        curl.setopt(pycurl.USERAGENT,
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
        # print(ret_url)
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

    def api_key_get(self, params, request_path):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': self.ACCESS_KEY,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_url = self.TRADE_URL
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params['Signature'] = self.createSign(params, method, host_name, request_path)

        url = host_url + request_path
        return self.http_get_request(url, params)

    def api_key_post(self, params, request_path):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': self.ACCESS_KEY,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}
        host_url = self.TRADE_URL
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = self.createSign(params_to_sign, method, host_name, request_path)
        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        return self.http_post_request(url, params)

    def createSign(self, pParams, method, host_url, request_path):
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = self.SECRET_KEY.encode(encoding='UTF8')
        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

    # 获取KLine
    def get_volume(self, symbol):
        # :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 1day, 1mon, 1week, 1year }

        symbol = (symbol[0] + symbol[1]).lower()
        params = {'symbol': symbol,
                  'period': str('5min'),
                  'size': str(1)}

        url = self.MARKET_URL + '/market/history/kline'
        ret = self.http_get_request(url, params)
        ret = ret['data_NK_HS-YM'][0]['amount']
        return ret

    # 获取marketdepth
    def get_depth(self, symbol):
        symbol = (symbol[0] + symbol[1]).lower()
        params = {'symbol': symbol,
                  'type': str('step0')}
        url = self.MARKET_URL + '/market/depth'
        response = self.http_get_request(url, params)
        ret = response['tick']
        return ret

    # 获取 Market Detail 24小时成交量数据
    def get_detail(self, symbol):
        symbol = (symbol[0] + symbol[1]).lower()
        params = {'symbol': symbol}
        url = self.MARKET_URL + '/market/detail'
        return self.http_get_request(url, params)

    # 查询用户所有资产ID
    def get_accounts(self):
        path = "/v1/account/accounts"
        params = {}
        ret = self.api_key_get(params, path)
        return ret['data_NK_HS-YM'][0]['id']

    # 获取当前账户资产
    def get_account(self, acct_id=None):
        if not self.acc_id:
            self.acc_id = self.get_accounts()
        if not acct_id:
            acct_id = self.acc_id
        url = "/v1/account/accounts/{0}/balance".format(acct_id)
        params = {"account-id": acct_id}
        ret = self.api_key_get(params, url)
        ret = ret['data_NK_HS-YM']['list']
        return ret

    # 下单
    # 创建并执行订单
    def order(self, symbol, side, quantity, price=''):
        """
        :param source: 如果使用借贷资产交易，请在下单接口,请求参数source中填写'margin-api'
        :param _type: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        """
        symbol = (symbol[0] + symbol[1]).lower()
        if not self.acc_id:
            self.acc_id = self.get_accounts()
        try:
            acct_id = self.acc_id
        except BaseException as e:
            print('get acct_id error.%s' % e)
        params = {"account-id": acct_id,
                  "amount": quantity,
                  "symbol": symbol,
                  "type": str(side + '-limit'),
                  }
        if price:
            params["price"] = price
        url = '/v1/order/orders/place'
        ret = self.api_key_post(params, url)
        ret = ret['data_NK_HS-YM']
        return ret

    # 撤销订单
    def cancel(self, orderId):
        params = {}
        url = "/v1/order/orders/{0}/submitcancel".format(orderId)
        ret = self.api_key_post(params, url)
        return ret

    # 查询某个订单
    def order_info(self, orderId):
        params = {}
        url = "/v1/order/orders/{0}".format(orderId)
        return self.api_key_get(params, url)

    # 查询某个订单的成交明细
    def order_matchresults(self, orderId):
        params = {}
        url = "/v1/order/orders/{0}/matchresults".format(orderId)
        return self.api_key_get(params, url)

    # 查询当前成交、历史成交
    def get_my_depth(self, symbol, types='', start_date='', end_date='', _from='', direct='', size=''):
        # :param types: 可选值 {buy-market：市价买, sell-market：市价卖, buy-limit：限价买, sell-limit：限价卖}
        # :param direct: 可选值{prev 向前，next 向后}
        symbol = (symbol[0] + symbol[1]).lower()
        params = {'symbol': symbol}
        if types:
            params[types] = types
        if start_date:
            params['start-date'] = start_date
        if end_date:
            params['end-date'] = end_date
        if _from:
            params['from'] = _from
        if direct:
            params['direct'] = direct
        if size:
            params['size'] = size
        url = '/v1/order/matchresults'
        ret = self.api_key_get(params, url)
        return ret
