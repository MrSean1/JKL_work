# *_*coding:utf-8 *_*
import os
import time
from datetime import datetime

from send_email.send_email import Email

em_user = '295861809@qq.com'
pwd = 'agagwzladccqbhce'
address = '295861809@qq.com'
smtp_server = 'smtp.qq.com'

process_count_old = [i.split('-u')[1].split('\n')[0] for i in os.popen('ps -f -C python').readlines()[1:]]

while True:
    process_count_new = [i.split('-u')[1].split('\n')[0] for i in os.popen('ps -f -C python').readlines()[1:]]
    if len(process_count_new) < len(process_count_old):
        deth_process = [i for i in process_count_old if i not in process_count_new]
        deth_process = str(deth_process)
        message = '{}个进程意外关闭，当前进程数量为{}，意外关闭的进程为{}'.format(
        len(process_count_old) - len(process_count_new), len(process_count_new), deth_process)
        title = '旧服进程数量警告'
        Email(em_user, pwd, address, smtp_server).send_email(message, title)
    now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' '
    print(now_time + '当前进程数量为：')
    print(len(process_count_new))
    process_count_old = process_count_new
    time.sleep(60)