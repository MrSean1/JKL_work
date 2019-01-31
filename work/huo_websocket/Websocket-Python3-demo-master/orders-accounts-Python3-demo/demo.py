import json
import zlib
import time
import websocket
import base64
import hmac
import hashlib
import glob
import configparser
from urllib import parse
from datetime import datetime

# 获取变量
__iniFilePath = glob.glob("params.ini")
cfg = configparser.ConfigParser()
cfg.read(__iniFilePath, encoding='utf-8')
accessKey = cfg.get('ws', 'accessKey')
secretKey = cfg.get('ws', 'secretKey')

protocol = cfg.get('ws', 'protocol')
_host = cfg.get('ws', '_host')
path = cfg.get('ws', 'path')

url = protocol + _host + path


class Message:
    # ---------------鉴权------------------

    def _auth(self, auth):
        authenticaton_data = auth[1]
        _accessKeySecret = auth[0]
        authenticaton_data['Signature'] = _sign(authenticaton_data, _accessKeySecret)
        print(authenticaton_data)
        return json.dumps(authenticaton_data)  # 鉴权一次中止操作

    # 订阅多个，padding
    def sub_padding(self, ws, message, data=None, totalcount=None):
        ws_result = str(zlib.decompressobj(31).decompress(message), encoding="utf-8")
        # js_result = json.loads(ws_result)
        #
        # ss = (int(round(time.time() * 1000)) - js_result['ts'])
        print('接收服务器数据为 ：%s' % ws_result)
        # if ss > 200:
        #     print('延迟 %d' % (ss))
        if totalcount < 1:
            for k in data:
                print('向服务器发送订阅 :%s' % k)
                ws.send(json.dumps(k))
        ping_id = json.loads(ws_result).get('ts')
        if 'ping' in ws_result:
            pong_data = '{"op":"pong","ts": %s}' % ping_id
            ws.send(pong_data)
            print(get_now_time())
            # print('%d' % (ss))
            print('向服务器发送pong :%s' % pong_data)

    def req(self, ws, message, data, totalcount):
        ws_result = str(zlib.decompressobj(31).decompress(message), encoding="utf-8")
        print('服务器响应数据%s' % ws_result)
        print(time.time())
        if totalcount < 1:
            print('向服务器发送数据1%s' % data)
            ws.send(json.dumps(data))
        ping_id = json.loads(ws_result).get('ts')
        if 'ping' in ws_result:
            pong_data = '{"op":"pong","ts": %s}' % ping_id
            ws.send(pong_data)
            print('向服务器发送pong :%s' % pong_data)


# websocket
class websockClient():

    def __init__(self):
        self.req_ws = None
        self.instance_id = ''
        self.count = 0
        self.unsubcount = 0
        self.totalcount = 0
        self.func = None
        # self.data_NK_HS-YM=None
        self._auth = None

    # 接收消息
    def on_message(self, ws, message):
        self.req_ws = ws
        MSG = Message()
        if self.func:
            hasattr(self, self.func)
            func = getattr(MSG, self.func)
            func(ws, message, data=self.data, totalcount=self.totalcount)
            self.totalcount += 1

    # 发生错误
    def on_error(self, ws, error):
        print(ws.on_error.__dict__)

    # 连接断开
    def on_close(self, ws):
        print("### closed ###")

    # 发送数据
    def send_data(self):
        _auth = Message()._auth(self._auth)
        return _auth

    # 建立连接
    def on_open(self, ws):
        def run(*args):
            ws.send(self.send_data())
            time.sleep(1)

        run()

    def start_websocket(self, func, data, authdata):
        self.func = func
        self.data = data
        self._auth = authdata
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(url,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

    def get_ws(self):
        return self.req_ws


# 签名
def _sign(param=None, _accessKeySecret=None):
    # 签名:
    if param is None:
        params = {}
    params = {}
    params['SignatureMethod'] = param.get('SignatureMethod') if type(param.get('SignatureMethod')) == type(
        'a') else '' if param.get('SignatureMethod') else ''
    params['SignatureVersion'] = param.get('SignatureVersion') if type(param.get('SignatureVersion')) == type(
        'a') else '' if param.get('SignatureVersion') else ''
    params['AccessKeyId'] = param.get('AccessKeyId') if type(param.get('AccessKeyId')) == type(
        'a') else '' if param.get('AccessKeyId') else ''
    params['Timestamp'] = param.get('Timestamp') if type(param.get('Timestamp')) == type('a') else '' if param.get(
        'Timestamp') else ''
    print(params)
    # 排序:
    keys = sorted(params.keys())
    # 加入&
    qs = '&'.join(['%s=%s' % (key, _encode(params[key])) for key in keys])
    # 请求方法，域名，路径，参数 后加入`\n`
    payload = '%s\n%s\n%s\n%s' % ('GET', _host, path, qs)
    dig = hmac.new(_accessKeySecret, msg=payload.encode('utf-8'), digestmod=hashlib.sha256).digest()

    return base64.b64encode(dig).decode()


def _utc():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')


def _encode(s):
    # return urllib.pathname2url(s)
    return parse.quote(s, safe='')


# 获取当前时间
def get_now_time():
    timestamp = int(time.time())
    time_local = time.localtime(timestamp)
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return now_time


authdata = [
    secretKey.encode('utf-8'),
    {
        "op": "auth",
        "AccessKeyId": accessKey,
        "SignatureMethod": "HmacSHA256",
        "SignatureVersion": "2",
        "Timestamp": _utc()
    }
]

# 订阅参数
datasymbols = [
    {
        'op': 'sub',
        'topic': 'market.ethusdt.depth.step0',
        'cid': '40sdfkajs'
    },
    {
        'op': 'sub',
        'topic': 'market.ethusdt.kline.1min',
        'cid': '40sdfkajs',
    },
    # {"req": "market.ethusdt.kline.1min", "id": "id10", "from": 1513391453, "to": 1513392453},
    # {"sub": "market.ethusdt.trade.detail", "id": "id10"}
]

# 订阅或取消订阅
websockClient().start_websocket(func='sub_padding', data=datasymbols, authdata=authdata)

#
# #查询参数
datareq = [
    {
        "op": "req",
        "topic": "accounts.list",
        "cid": 'sfdsfsfdsf'
    },
    {
        "op": "req",
        "topic": "orders.detail",
        'cid': '40sdfkajs',
        "order-id": '1543924'
    },
    {
        "op": "req",
        "topic": "orders.list",
        "cid": '32sdfsawa',
        "account-id": 18580,  # zhantong601@163.com
        "symbol": 'ethusdt',
        "types": "",
        "start-date": "",
        "end-date": "",
        "states": "submitted,filled,partial-canceled,partial-filled,canceled",
        "from": "1543875",
        "direct": "next",
        "size": '200'
    }
]

# 发送req请求
# websockClient().start_websocket(func='req', data_NK_HS-YM=datareq[2], authdata=authdata)
# websockClient().start_websocket(func='req', data_NK_HS-YM=datareq[1], authdata=authdata)
# websockClient().start_websocket(func='req', data_NK_HS-YM=datareq[0], authdata=authdata)
# websockClient().start_websocket(func='req', data_NK_HS-YM=datareq, authdata=authdata)
