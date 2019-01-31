import json

import websocket
import _thread as thread
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send(json.dumps({"op": 'subscribe', "args": ['orderBook10:XBTUSD']}))
    result = ws.recv()
    print(result)
    time.sleep(10)
    ws.close()


def ws_bitmex(base_url, command, args=None):
    ws = websocket.WebSocketApp(base_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    # send_command(command, args)


# def send_command(ws, command, args=None):
#     if args is None:
#         args = []

    # thread.start_new_thread(send_command, ())


# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("wss://www.bitmex.com/realtime",
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)
#     ws.on_open = on_open
    # ws.run_forever(ping_interval=60, ping_timeout=5)

if __name__ == "__main__":
    ws_bitmex(base_url="wss://www.bitmex.com/realtime", command='subscribe', args=['orderBook10:XBTUSD'])