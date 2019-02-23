# *_*coding:utf-8 *_*
import time

from config import *
import wmi
import os
from send_email import Email

CommandLine = CommandLine
Caption = Caption

sys_process = wmi.WMI()


def main():
    process_list = []
    for process in sys_process.Win32_Process():
        process_list.append([process.CommandLine, process.Caption])
    if [CommandLine, Caption] in process_list:
        log.logger.info('进程正在运行')
    else:
        log.logger.error('process get_data_futures deth')
        log.logger.info('正在准备重启')
        restart_process = 'start /b python ' + restart_process_path
        try:
            os.system(restart_process)
            log.logger.info('已经重启')
            Email(em_user, pwd, address, smtp_server).send_email(message='sp数据抓取进程已经重启，请查看是否出错', title='sp数据抓取重启')
        except Exception as e:
            log.logger.error('重启失败' + str(e))
            Email(em_user, pwd, address, smtp_server).send_email(message='sp数据抓取进程重启失败，请查看哪里出错', title='sp数据抓取重启失败')


if __name__ == '__main__':
    while True:
        main()
        time.sleep(30)
