
import http.client

import json

# 服务地址
host = "intapi.253.com"
# 端口号
port = 80
# 版本号
version = "v1.1"
# 查账户信息的URI
# balance_get_uri = "/balance/json"

# 智能匹配模版短信接口的URI
sms_send_uri = "/send/json"

# 创蓝账号
account = "I3636721"

# 创蓝密码
password = "vEjVYZ5F9T9720"


def send_sms(text, phone):
    """
    能用接口发短信
    """
    params = {
        'account': account,
        'password': password,
        'msg': text,
        'mobile': phone,
        'report': 'false'
    }
    params = json.dumps(params)
    headers = {
        "Content-type": "application/json"
    }
    conn = http.client.HTTPConnection(host, port=port, timeout=30)
    conn.request("POST", sms_send_uri, params, headers)
    response = conn.getresponse()
    response_str = response.read()
    conn.close()
    print(response_str)
    return response_str

