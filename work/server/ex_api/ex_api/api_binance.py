from ex_api.api import base_api
import pycurl
import hashlib
import hmac
import json


class api_binance(base_api):
    def __sym(self, symbol):
        return symbol[0] + symbol[1]

    def __sign(self, message):
        return hmac.new(self.bsecret, message.encode('ascii'), digestmod=hashlib.sha256).hexdigest()

    def __api_call(self, method, xtype, params='', params_c=''):
        curl, iofunc = self.initcurl(xtype)
        curl.setopt(pycurl.HTTPHEADER, ['X-MBX-APIKEY: ' + self.api_key])
        base_endpoint = 'https://api.binance.com'
        if params == '':
            if params_c != '':
                m_c = self.sort_params(params_c)
                signature = self.__sign(m_c)
                m_f = base_endpoint + method + '?' + m_c + '&signature=' + signature
            else:
                m_f = base_endpoint + method
        else:
            m = self.sort_params(params)
            if params_c == '':
                m_f = base_endpoint + method + '?' + m
            else:
                m_c = self.sort_params(params_c)
                signature = self.__sign(m_c)
                m_f = base_endpoint + method + '?' + m + '&' + m_c + '&signature=' + signature
        curl.setopt(pycurl.URL, m_f)
        print(m_f)
        try:
            curl.perform()
        except Exception as e:
            print(e)
            print('Error: curl.perform')
            return False
        ret_message = iofunc.getvalue().decode('utf-8')
        print(ret_message)
        curl.close()
        iofunc.close()
        try:
            ret = json.loads(ret_message)
        except Exception as e:
            print(e)
            print('Error: json.loads')
            # print(ret_message)
            return False
        else:
            return ret

    def get_depth(self, symbol, size=5):
        method = '/api/v1/depth'
        params = {
            'symbol': self.__sym(symbol),
            'limit': str(size)
        }
        depth = self.__api_call(method, 0, params=params)
        # ask_1 = eval(depth['asks'][0][0])
        # bid_1 = eval(depth['bids'][0][0])
        # return [ask_1, bid_1]
        dict = {}
        bids = depth['bids']
        asks = depth['asks']
        dict['asks'] = asks
        dict['bids'] = bids
        return dict

    def get_timestamp(self):
        method = '/api/v1/time'
        time = self.__api_call(method, 0)['serverTime']
        return str(time)

    def get_account(self):
        method = '/api/v3/account'
        params_c = {
            'timestamp': self.get_timestamp()
        }
        ret = self.__api_call(method, 0, params_c=params_c)
        ret = ret['balances']
        ret = list(ret)
        dict = {}
        for i in ret:
            dict[i['asset']] = {}
            dict[i['asset']]["ac_type"] = i['asset']
            dict[i['asset']]["avaid_balance"] = i['free']
            dict[i['asset']]['freeze_balance'] = i['locked']
        return dict

    def order(self, symbol, side, quantity, price='', type='LIMIT', timeInForce='GTC'):
        method = '/api/v3/order'
        params_c = {
            'symbol': self.__sym(symbol),
            'side': side,
            'quantity': str(quantity),
            'type': type,
            'timeInForce': timeInForce,
            'timestamp': self.get_timestamp()
        }
        if 'price':
            params_c['price'] = str(price)
        ret = self.__api_call(method, 1, params_c=params_c)
        ret = ret['orderId']
        return ret

    # 查询所有订单
    def get_my_depth(self):
        method = "/api/v3/openOrders"
        params_c = {
            'timestamp': self.get_timestamp()
        }
        ret = self.__api_call(method, 0, params_c=params_c)
        return ret

    #     撤销订单
    def cancel(self, orderId, symbol):
        method = "/api/v3/order"
        params_c = {
            'symbol': self.__sym(symbol),
            'orderId': str(orderId),
            'timestamp': self.get_timestamp()
        }
        ret = self.__api_call(method, 2, params_c=params_c)
        return ret

    # 查询交易数量
    def get_volume(self, symbol, interval, size='1'):
        method = '/api/v1/klines'
        params = {
            'symbol': self.__sym(symbol),
            'interval': interval,
            'limit': str(size),
        }
        ret = self.__api_call(method, 0, params=params)
        list_vol = []
        for list in ret:
            vo = list[5]
            list_vol.append(vo)
        return list_vol

    def get_query_info(self, order_id, symbol):
        method = '/api/v3/order'
        params = {
            'symbol': self.__sym(symbol),
            'orderId': str(order_id),
            'timestamp': self.get_timestamp()
        }
        ret = self.__api_call(method, 0, params_c=params)
        return ret
