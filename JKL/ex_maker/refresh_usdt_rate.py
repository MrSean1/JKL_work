import pycurl
import io
import certifi
import time
import urllib
import urllib.parse
import json

while True:
    print(time.asctime())
    curl = pycurl.Curl()
    iofunc = io.BytesIO()
    curl.setopt(pycurl.WRITEFUNCTION, iofunc.write)
    curl.setopt(pycurl.CAINFO, certifi.where())
    curl.setopt(pycurl.TIMEOUT, 15)
    curl.setopt(pycurl.CUSTOMREQUEST, 'GET')
    curl.setopt(pycurl.HTTPHEADER, ["Content-Type: application/json"])
    curl.setopt(pycurl.USERAGENT,
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
                + "/39.0.2171.71 Safari/537.36")
    # curl.setopt(pycurl.URL,
    #             'https://otc-api.huobipro.com/v1/otc/trade/list/public?' +
    #             'coinId=2&currency=1&tradeType=1&currentPage=1&payWay=&country=&merchant=1&online=1&range=0')
    curl.setopt(pycurl.URL, "https://otc-api.huobi.com/v1/data/trade-market?"
                + "country=37&currency=1&payMethod=0&currPage=1&coinId=2&tradeType=sell&blockType=general&online=1")
    curl.perform()
    a = json.loads(iofunc.getvalue().decode())
    curl.close()
    iofunc.close()
    USDT_rate = str(a['data'][2]['price'])
    if 6 < float(USDT_rate) < 7.5:
        print('USDT rate is ', USDT_rate)
        with open('./USDT_rate.txt', 'w') as f:
            f.write(USDT_rate)
    else:
        print('api may exist errors')
    time.sleep(1800)
