import time, hmac, hashlib

import websocket
import threading
import traceback
from time import sleep
import json
import urllib.parse


class ws_bitmex:
    # Don't grow a table larger than this amount. Helps cap memory usage.
    MAX_TABLE_LEN = 200

    def __init__(self, endpoint, symbol, api_key=None, api_secret=None):
        self.endpoint = endpoint
        self.symbol = symbol

        if api_key is not None and api_secret is None:
            raise ValueError('api_secret is required if api_key is provided')
        if api_key is None and api_secret is not None:
            raise ValueError('api_key is required if api_secret is provided')

        self.api_key = api_key
        self.api_secret = api_secret

        self.data = {}
        self.keys = {}
        self.count = 0
        self.exited = False

        wsURL = self.__get_url()
        print("Connecting to url: %s" % wsURL)
        # 建立连接
        self.__connect(wsURL, symbol)

        if api_key:
            self.__wait_for_account()

    # 退出长连接
    def exit(self):
        '''Call this to exit - will close websocket.'''
        self.exited = True
        self.ws.close()

    # 查看市场深度
    def market_depth(self):
        try:
            return self.data['orderBook10']
        except Exception:
            return []

    def __connect(self, wsURL, symbol):
        self.ws = websocket.WebSocketApp(wsURL,
                                         on_message=self.__on_message,
                                         on_close=self.__on_close,
                                         on_open=self.__on_open,
                                         on_error=self.__on_error,
                                         )
        self.wst = threading.Thread(target=lambda: self.ws.run_forever(ping_interval=10))
        # 线程保护
        self.wst.daemon = True
        self.wst.start()
        print("Started thread")

        conn_timeout = 5
        while not self.ws.sock or not self.ws.sock.connected and conn_timeout:
            sleep(1)
            conn_timeout -= 1
        if not conn_timeout:
            print("无法连接到bitmex.")
            self.exit()
            raise websocket.WebSocketTimeoutException('Couldn\'t connect to WS! Exiting.')

    def __get_url(self):
        symbolSubs = ["orderBook10", ]
        subscriptions = [sub + ':' + self.symbol for sub in symbolSubs]
        urlParts = list(urllib.parse.urlparse(self.endpoint))
        urlParts[0] = urlParts[0].replace('http', 'ws')
        urlParts[2] = "/realtime?subscribe={}".format(','.join(subscriptions))
        return urllib.parse.urlunparse(urlParts)

    def __get_auth(self):
        '''Return auth headers. Will use API Keys if present in settings.'''
        if self.api_key:
            nonce = int(round(time.time() * 1000))
            return [
                "api-nonce: " + str(nonce),
                "api-signature: " + self._sign(self.api_secret, 'GET', '/realtime', nonce, ''),
                "api-key:" + self.api_key
            ]
        else:
            print("没有验证信息")
            return []

    def _sign(self, secret, verb, url, nonce, data):
        """Generate a request signature compatible with BitMEX."""
        parsedURL = urllib.parse.urlparse(url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + '?' + parsedURL.query

        message = (verb + path + str(nonce) + data).encode('utf-8')

        signature = hmac.new(secret.encode('utf-8'), message, digestmod=hashlib.sha256).hexdigest()
        return signature

    def __wait_for_account(self):
        '''On subscribe, this data will come down. Wait for it.'''
        while not {'orderBook10'} <= set(self.data):
            sleep(0.1)

    def send_command(self, command, args=None):
        '''Send a raw command.'''
        if args is None:
            args = []
        self.ws.send(json.dumps({"op": command, "args": args}))

    def __on_message(self, ws, message):
        '''Handler for parsing WS messages.'''
        message = json.loads(message)

        table = message['table'] if 'table' in message else None
        action = message['action'] if 'action' in message else None
        try:
            if 'subscribe' in message:
                print("订阅是 %s." % message['subscribe'])
            elif action:
                if table not in self.data:
                    self.data[table] = []
                # 存放原始数据
                if action == 'partial':
                    print("%s: partial %s" % (table, message['data']))
                    self.data[table] += message['data']
                    self.keys[table] = message['keys']

                elif action == 'update':
                    # 更新数据
                    for updateData in message['data']:
                        item = findItemByKeys(self.keys[table], self.data[table], updateData)
                        # 检查是否有更新的数据
                        if not item:
                            return
                        item.update(updateData)
                else:
                    raise Exception("Unknown action: %s" % action)
        except:
            print(traceback.format_exc())

    def __on_error(self, ws, error):
        '''Called on fatal websocket errors. We exit on these.'''
        if not self.exited:
            print("Error : %s" % error)
            raise websocket.WebSocketException(error)

    def __on_open(self, ws):
        '''Called when the WS opens.'''
        print("websocket start")

    def __on_close(self, ws):
        '''Called on websocket close.'''
        print('Websocket Closed')


# 判断前后两次的值并实现更新
def findItemByKeys(keys, table, matchData):
    for item in table:
        matched = True
        for key in keys:
            if item[key] != matchData[key]:
                matched = False
        if matched:
            return item


if __name__ == "__main__":
    ws = ws_bitmex(endpoint="wss://www.bitmex.com/realtime", symbol="XBTUSD", )
    while (ws.ws.sock.connected):
        market_depth = ws.market_depth()
        print(market_depth)
        sleep(10)
