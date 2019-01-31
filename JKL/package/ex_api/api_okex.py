from urllib import parse
import pycurl
import hashlib
import hmac
import json
import io
import certifi


class api_okex():
    def __init__(self, key):
        self.api_key = key[0]
        self.bsecret = key[1].encode('utf-8')
        self.account_root = 'https://www.okb.com/'
        self.headers = ['Content-Type: application/x-www-form-urlencoded']

    def __sym(self, symbol):
        return symbol[0].lower() + '_' + symbol[1].lower()

    def sort_params(self, params):
        p = dict(sorted(params.items(), key=lambda item: item[0]))
        return p

    def __sign(self, message):
        return hashlib.md5(message.encode()).hexdigest().upper()
        # return hmac.new(self.bsecret, message.encode('ascii'), digestmod=hashlib.md5).hexdigest().upper()

    def __api_call(self, url, type, params=json.dumps({})):
        curl = pycurl.Curl()
        iofunc = io.BytesIO()
        curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
        curl.setopt(pycurl.CAINFO, certifi.where())
        curl.setopt(pycurl.HTTPHEADER, self.headers)
        if type == 'POST':
            curl.setopt(pycurl.CUSTOMREQUEST, 'POST')
            curl.setopt(pycurl.POSTFIELDS, params)
            print(params)
        elif type == 'GET':
            curl.setopt(pycurl.CUSTOMREQUEST, 'GET')
        elif type == 'DELETE':
            curl.setopt(pycurl.CUSTOMREQUEST, 'DELETE')
        curl.setopt(pycurl.TIMEOUT, 30)
        curl.setopt(pycurl.USERAGENT,
                    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36')
        print(url)
        curl.setopt(pycurl.URL, url)
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

    def get_depth(self, symbol, size=10):
        symbol = self.__sym(symbol)
        method = 'api/v1/depth.do?symbol=' + symbol + '&size=' + str(size)
        url = self.account_root + method
        ret = self.__api_call(url, 'GET')
        print(ret)
        return ret

    # 获取账户信息
    def get_account(self):
        method = 'api/v1/userinfo.do'
        url = self.account_root + method
        params = {
            'api_key': self.api_key,
        }
        params = self.sort_params(params)
        params['secret_key'] = self.bsecret
        params = parse.urlencode(params)
        params_dict = {'api_key': self.api_key, 'sign': self.__sign(params)}
        params_dict = parse.urlencode(params_dict)
        ret = self.__api_call(url, 'POST', params_dict)
        return ret["info"]["funds"]

    # 下单
    def order(self, symbol, type, amount, price=''):
        method = 'api/v1/trade.do'
        params = {
            'api_key': self.api_key,
            'symbol': self.__sym(symbol),
            'type': type,
            'amount': amount,
        }
        if price:
            params['price'] = price
        url = self.account_root + method
        params = self.sort_params(params)
        params['secret_key'] = self.bsecret
        params = parse.urlencode(params)
        params_dict = {
            'api_key': self.api_key,
            'symbol': self.__sym(symbol),
            'type': type,
            'amount': amount,
            'sign': self.__sign(params),
        }
        if price:
            params_dict['price'] = price
        params_dict = parse.urlencode(params_dict)
        ret = self.__api_call(url, 'POST', params_dict)
        if ret['error_code']:
            return ret
        elif ret['result']:
            return ret

    # 撤销订单
    def cancel(self, orderId, symbol):
        method = 'api/v1/cancel_order.do'
        params = {
            'api_key': self.api_key,
            'symbol': self.__sym(symbol),
            'order_id': orderId,
        }
        url = self.account_root + method
        params = self.sort_params(params)
        params['secret_key'] = self.bsecret
        params = parse.urlencode(params)
        params_dict = {
            'api_key': self.api_key,
            'symbol': self.__sym(symbol),
            'order_id': orderId,
            'sign': self.__sign(params),
        }

        params_dict = parse.urlencode(params_dict)
        ret = self.__api_call(url, 'POST', params_dict)
        return ret

    # 获取订单信息
    def get_query(self, order_id, symbol):
        method = 'api/v1/order_info.do'
        params = {
            'api_key': self.api_key,
            'symbol': self.__sym(symbol),
            'order_id': order_id,
        }
        url = self.account_root + method
        params = self.sort_params(params)
        params['secret_key'] = self.bsecret
        params = parse.urlencode(params)
        params_dict = {
            'api_key': self.api_key,
            'symbol': self.__sym(symbol),
            'order_id': order_id,
            'sign': self.__sign(params),
        }
        params_dict = parse.urlencode(params_dict)
        ret = self.__api_call(url, 'POST', params_dict)
        return ret['orders']

    # 获得所有订单
    def get_my_depth(self, symbol, status=0, current_page=1, page_length=200):
        method = 'api/v1/order_history.do'
        params = {
            'api_key': self.api_key,
            'symbol': self.__sym(symbol),
            'status': status,
            'current_page': current_page,
            'page_length': page_length,
        }
        url = self.account_root + method
        params = self.sort_params(params)
        params['secret_key'] = self.bsecret
        params = parse.urlencode(params)
        params_dict = {
            'api_key': self.api_key,
            'symbol': self.__sym(symbol),
            'status': status,
            'current_page': current_page,
            'page_length': page_length,
            'sign': self.__sign(params),
        }
        params_dict = parse.urlencode(params_dict)
        ret = self.__api_call(url, 'POST', params_dict)
        return ret
