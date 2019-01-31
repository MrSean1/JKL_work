from ex_api.api import base_api
import pycurl
import hashlib
import hmac
import urllib
import base64
import time
import json


class api_bithumb(base_api):
    def __sym(self, symbol):
        return symbol[0].upper()

    def __sign(self, message):
        signature = hmac.new(self.bsecret, message.encode('utf-8'), hashlib.sha512).hexdigest().encode('utf-8')
        return base64.b64encode(signature).decode('utf-8')

    def __api_call(self, method, xtype, params):
        curl, iofunc = self.initcurl(xtype)
        base_endpoint = 'https://api.bithumb.com'
        message = self.sort_params(params)
        m_f = base_endpoint + method + '?' + message
        if xtype == 1:
            endpoint_item_array = {
                "endpoint": method
            }
            uri_array = dict(endpoint_item_array, **params)
            str_data = urllib.parse.urlencode(uri_array)
            nonce = str(int(time.time() * 1000))
            message = method + chr(0) + str_data + chr(0) + nonce
            signature = self.__sign(message)
            curl.setopt(pycurl.POST, 1)
            curl.setopt(pycurl.POSTFIELDS, str_data)
            curl.setopt(curl.HTTPHEADER,
                        ['Api-Key: ' + self.api_key, 'Api-Sign: ' + signature, 'Api-Nonce: ' + nonce])
        curl.setopt(pycurl.URL, base_endpoint + method)
        try:
            curl.perform()
        except Exception as e:
            print(e)
            print('Error: curl.perform')
        ret_message = iofunc.getvalue().decode('utf-8')
        # print(ret_message)
        curl.close()
        iofunc.close()
        try:
            ret = json.loads(ret_message)
        except Exception as e:
            print(e)
            print('Error: json.loads')
            return ret_message
        else:
            return ret

    def get_depth(self, symbol, size=5):
        method = '/public/orderbook/' + self.__sym(symbol)
        params = {
            'count': size
        }
        ret = self.__api_call(method, 0, params)
        list1 = ret['data']['bids']
        list2 = ret['data']['asks']
        dict = {}
        list = []
        list3 = []
        list4 = []
        list5 = []
        for i in list1:
            list.append([i['quantity'], i['price']])
        for j in list2:
            list3.append([j['quantity'], j['price']])
        for ii in list3:
            ii.reverse()
            list4.append(ii)
        for jj in list:
            jj.reverse()
            list5.append(jj)
        dict['asks'] = list4
        dict['bids'] = list5
        return dict

    def order(self, symbol, side, quantity, price):
        if side == 'buy':
            side = 'bid'
        elif side == 'sell':
            side = 'ask'
        method = '/trade/place'
        params = {
            'apiKey': self.api_key,
            'secretKey': self.bsecret.decode('utf-8'),
            'order_currency': self.__sym(symbol),
            'payment_currency': 'KRW',
            'units': str(quantity),
            'price': str(int(price)),
            'type': side,
        }
        ret = self.__api_call(method, 1, params)
        ret = ret['order_id']
        return ret

    def get_account(self, symbol=['ALL']):
        method = "/info/balance"
        params = {
            'apiKey': self.api_key,
            'secretKey': self.bsecret.decode('utf-8'),
            "currency": self.__sym(symbol)
        }
        ret = self.__api_call(method, 1, params)
        return ret

        # 获取用户信息
        # def get_my_depth(self,symbol,side='',price='',units=''):
        #     method = '/trade/place'
        #     params = {
        #         'apiKey': self.api_key,
        #         'secretKey': self.bsecret.decode('utf-8'),
        #         'order_currency':self.__sym(symbol),
        #         'Payment_currency':str('KRW'),
        #     }
        #     if side:
        #         params['type']=str(side)
        #     if price:
        #         params["price"] = int(price)
        #     if units:
        #         params['units'] = float(units)
        #
        #     ret = self.__api_call(method, 1, params)
        #     return ret
        #
        # 用户信息
        # def get_my(self,orderId='',side='',quantity='',symbol='',):
        #     method = "/info/orders"
        #     params ={
        #         'apiKey': self.api_key,
        #         'secretKey': self.bsecret.decode('utf-8'),
        #         'after':1417160401000,
        #          }
        #     if orderId:
        #         params['order_id'] = str(orderId)
        #     if side:
        #         params['type'] = str(side)
        #     if quantity:
        #         params['count'] = int(quantity)
        #     if symbol:
        #         params['currency'] = self.__sym(symbol)
        #     ret = self.__api_call(method, 1, params)
        #     return ret
        #
        #

    #     撤销订单
    def cancel(self, side='', orderId='', symbol=''):
        method = "/trade/cancel"
        params = {
            'apiKey': self.api_key,
            'secretKey': self.bsecret.decode('utf-8'),
            'order_id': str(orderId)
        }
        if side:
            params['type'] = str(side)
        if symbol:
            params['currency'] = str(self.__sym(symbol))
        ret = self.__api_call(method, 1, params)
        return ret


        # if __name__ == '__main__':
        #     key = ['8eb883df5770835599a0584ff6fcb3a8',
        #            '15c1ca9a729ee9203a20c522d27bad21']
        #     api = api_bithumb(key)
        #     symbol = ['LTC','KRW']
        # api.get_depth(symbol)
        # api.get_account()
        # api.order(symbol,'sell',0.01,200000)
        # api.get_my_depth(symbol,'asks',price=200000,units=0.1)
        # api.get_cancel(orderId=1521459878922046,symbol=symbol,side='asks')
        # api.get_my()

    # 查询交易数量
    def get_data(self, currency=''):
        if currency:
            method = '/public/ticker'
        else:
            method = '/public/ticker/{' + str(currency) + '}'
        ret = self.__api_call(method, 0, params='')
        return ret
