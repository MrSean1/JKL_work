import datetime
import logging
import time

import requests

from Mythread import MyThread


# from send_click_signal import setup_logger
def setup_logger():
    # Prints logger info to terminal
    logging.basicConfig(
        level=logging.INFO,
        filename="./log/mt4_{}.log".format(datetime.datetime.now().date()),
        format='%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s',
        filemode='a',
    )
    # logging.FileHandler(filename="./log/mt4_logs.log", encoding='utf-8')
    logger = logging.getLogger()
    # logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    sh = logging.StreamHandler()  # 往屏幕上输出
    # 屏幕输出格式
    sh.setFormatter("%(asctime)s - %(name)s[line:%(lineno)d] - %(levelname)s: %(message)s")
    logger.addHandler(ch)
    return logger


logger = setup_logger()

foreign_exchange = [
    'EURUSD',
    'USDRUB',
    'XPTUSD',
    'XPDUSD',
    'XAUUSD',
    'XAGUSD',
    'EURAUD',
    'USDCHF',
    'GBPUSD',
    'USDJPY',
    'AUDUSD',
    'USDCAD',
    'EURJPY',
    'EURGBP',
    'GBPCHF',
    'GBPJPY',
    'EURCHF',
    'NZDUSD',
    'EURCAD',
    'AUDCHF',
    'GBPAUD',
    'GBPCAD',
    'AUDNZD',
    'AUDCAD',
    'AUDJPY',
    'NZDCAD',
    'SEKJPY',
    'GBPNZD',
    'USDSGD',
    'NZDCHF',
    'SGDJPY',
    'TRYJPY',
    'ZARJPY',
    'HKDJPY',
    'CHFJPY',
    'EURNZD',
    'CADCHF',
    'CADJPY',
    'NZDJPY',
    'EURNOK',
    'NOKSEK',
    'EURSEK',
    'EURHUF',
    'GBPSEK',
    'EURTRY',
    'EURCZK',
    'EURPLN',
    'CHFNOK',
    'USDTRY',
    'USDNOK',
    'USDSEK',
    'USDHKD',
    'USDHUF',
    'USDMXN',
    'USDCZK',
    'USDPLN',
    'USDCNH',
    'USDDKK',
    'USDZAR',
]

ip_list = ['47.244.38.60',
           '47.52.173.108',
           '47.75.69.184',
           '47.244.37.23',
           '47.75.169.118',
           '47.52.244.28', ]


def send_add(volume, ip, stock, s_type):
    pos = {
        '47.244.38.60': 1,
        '47.52.173.108': 2,
        '47.244.37.23': 3,
        '47.75.169.118': 4,
        '47.52.244.28': 1,
    }
    order_info = dict()
    order_info['number'] = int(volume * pos[ip])
    order_info['direction'] = s_type
    order_info['share'] = stock
    req = requests.session()
    # 文件写进去
    try:
        ret = req.post('http://{}:8009/share/buy_shares/'.format(ip), data=order_info).json()
        logger.info('ip:{}, 下单信号写入情况：{}'.format(ip, ret))
    except Exception as e:
        logger.error("ip:{}, 写下单信号接口错误，错误信息：{}".format(ip, e))
    # 检查文件什么时间完成
    try:
        ret1 = req.post('http://{}:8009/share/check_info/'.format(ip), data=order_info).json()
        logger.info('ip:{}, 下单信号检查情况：{}'.format(ip, ret1))
        if ret1['msg'] == '信息不存在':
            logger.info('ip: {} 此次下单操作完成'.format(ip))
            req.close()
            return True
        else:
            logger.error('ip：{} 此次下单操作完成不正常请查看日志'.format(ip))
            req.close()
            return False
    except Exception as e:
        req.close()
        logger.error("ip:{}, 检查下单信好接口错误，错误信息：{}".format(ip, e))
        return False


def cancle_signal(ip):
    calcle = {
        'direction': 'cancle'
    }
    req = requests.session()
    try:
        ret = req.post('http://{}:8009/share/buy_shares/'.format(ip), data=calcle).json()
        logger.info('ip:{}, 平仓信号写入情况：{}'.format(ip, ret))
    except Exception as e:
        logger.error("ip:{}, 平仓单信号接口错误，错误信息：{}".format(ip, e))
    # 检查文件什么时间完成
    try:
        ret1 = req.post('http://{}:8009/share/check_info/'.format(ip), data=calcle).json()
        logger.info('ip:{}, 平仓信号检查情况：{}'.format(ip, ret1))
        if ret1['msg'] == '信息不存在':
            logger.info('ip: {} 此次平仓操作完成'.format(ip))
            req.close()
            return True
        else:
            logger.error('ip：{} 此次平仓操作完成不正常请查看日志'.format(ip))
            req.close()
            return False
    except Exception as e:
        req.close()
        logger.error("ip:{}, 检查平仓信好接口错误，错误信息：{}".format(ip, e))
        return False


def start(volume, ip):
    while True:
        for stock in foreign_exchange:
            for k in range(2):
                if k == 0:
                    s_type = 'sell'
                else:
                    s_type = 'buy'
                for i in range(5):
                    a = send_add(volume, ip, stock, s_type)
                    logger.info('第{}次，发送下单信号完成情况结果：{}'.format(str(i + 1), str(a)))
                for i in range(2):
                    b = cancle_signal(ip)
                    logger.info('第{}次，发送平仓信号完成情况结果：{}'.format(str(i + 1), str(b)))
                time.sleep(2)


test_th = [MyThread(start, args=(1, ip,)) for ip in ip_list]
[th.start() for th in test_th]
[th.join() for th in test_th]
