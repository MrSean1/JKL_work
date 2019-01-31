import urllib.request
import re
import http.cookiejar
import time

ck = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(ck)
opener = urllib.request.build_opener(handler)
url = 'https://www.quantopian.com/users/sign_in?'
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
}
form_data = {
    'email': 'wht190421@163.com',
    'password': 'WANG190421',
    'remember_me': '0'
}
form_data = urllib.parse.urlencode(form_data).encode('utf8')
request = urllib.request.Request(url=url, headers=headers)
post_response = opener.open(request, data=form_data)
print(post_response)

start = 0
end = 10
data_url = 'https://www.quantopian.com/backtests/log_entries?backtest_id=5bf27c9941778c41d0e90e0c&start=%s&end=%s' % (
start, end)
data_request = urllib.request.Request(url=data_url, headers=headers)
data = opener.open(data_request)
print(data)